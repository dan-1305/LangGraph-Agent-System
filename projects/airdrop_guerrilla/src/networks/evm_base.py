import time
import random
from typing import Optional, List
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account
from web3.exceptions import TimeExhausted
from tenacity import retry, stop_after_attempt, wait_random, retry_if_exception_type

import sys
from pathlib import Path
# Tách bot: Xóa liên kết với Monorepo Root, chỉ dùng thư mục hiện tại của project
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
from src.utils.notifier import TelegramNotifier

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="eth_account")

class EVMBase:
    """
    Lớp nền móng xử lý các tác vụ On-chain cho các mạng Layer 1/Layer 2 EVM.
    Được trang bị cơ chế Survival: RPC Fallback, Telegram Alert và Tenacity Retry.
    """
    def __init__(self, network_name: str, rpc_urls: List[str], chain_id: int, private_key: str, symbol: str, explorer_url: str = "", proxy_url: str = ""):
        self.network_name = network_name
        self.rpc_urls = rpc_urls
        self.chain_id = chain_id
        self.private_key = private_key
        self.symbol = symbol
        self.explorer_url = explorer_url
        self.proxy_url = proxy_url
        self.w3 = None
        self.notifier = TelegramNotifier()
        
        self.account = Account.from_key(private_key)
        self.address = self.account.address

        # Kích hoạt Fallback Connection ngay lập tức
        self.init_fallback_connection()

    def init_fallback_connection(self):
        """Duyệt danh sách RPC, tự động chuyển mạch nếu có node sập."""
        req_kwargs = {'timeout': 10}
        if self.proxy_url:
            req_kwargs['proxies'] = {'http': self.proxy_url, 'https': self.proxy_url}
            
        for url in self.rpc_urls:
            try:
                temp_w3 = Web3(Web3.HTTPProvider(url, request_kwargs=req_kwargs))
                temp_w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
                if temp_w3.is_connected():
                    self.w3 = temp_w3
                    print(f"[{self.network_name}] Kêt nối thành công tới RPC: {url}")
                    return
            except Exception:
                print(f"[{self.network_name}] Node RPC {url} bị lỗi. Đang thử dự phòng...")
        
        # Nếu tất cả đều chết, ném lỗi để luồng tổng catch
        raise ConnectionError(f"[{self.network_name}] Tất cả các cổng RPC trong danh sách đều đã chết!")

    def get_balance(self) -> float:
        """Lấy số dư Native Token của ví."""
        balance_wei = self.w3.eth.get_balance(self.address)
        return float(self.w3.from_wei(balance_wei, 'ether'))

    def get_gas_price(self, wait_for_low_gas: bool = False, max_gwei: float = None) -> int:
        """
        Lấy giá Gas hiện tại. Hỗ trợ Gas-Optimization: Chờ đợi gas thấp.
        """
        current_gas_price = self.w3.eth.gas_price
        current_gwei = self.w3.from_wei(current_gas_price, 'gwei')
        
        if wait_for_low_gas and max_gwei:
            print(f"⛽ [Gas-Check] Current: {current_gwei:.2f} Gwei | Target: < {max_gwei} Gwei")
            while current_gwei > max_gwei:
                print(f"💤 Gas dang cao ({current_gwei:.2f} Gwei). Nghi 5 phut...")
                time.sleep(300)
                current_gas_price = self.w3.eth.gas_price
                current_gwei = self.w3.from_wei(current_gas_price, 'gwei')
            print(f"🚀 Gas da ha nhiet ({current_gwei:.2f} Gwei). Tien hanh giao dich!")

        return int(current_gas_price * 1.1)

    def check_balance_and_survival(self) -> bool:
        """Kiểm tra số dư tối thiểu, bắn Telegram báo động nếu cạn tiền."""
        try:
            balance_eth = self.get_balance()
            if balance_eth < 0.0005:
                msg = f"⚠️ [CẢNH BÁO AIRDROP]\nVí: {self.address[:6]}...{self.address[-4:]}\nMạng: {self.network_name}\nTình trạng: Số dư quá thấp ({balance_eth:.5f} {self.symbol}). Hãy đi Faucet gấp!"
                print(msg)
                self.notifier.send_message(msg)  # Hú user đi Faucet
                return False
            return True
        except Exception as e:
            print(f"[{self.network_name}] Lỗi check số dư: {e}")
            return False

    @retry(
        retry=retry_if_exception_type((TimeExhausted, Exception)), 
        stop=stop_after_attempt(3), 
        wait=wait_random(min=2, max=5),
        reraise=True
    )
    def send_native_token(self, to_address: str, amount_ether: float) -> Optional[str]:
        """
        Gửi Native Token (Ví dụ: ETH -> Soneium, MON -> Monad)
        Mục đích: Cày Transaction Hash (TX) để làm mượt ví.
        Đã bọc Tenacity Retry để tự gửi lại nếu nghẽn mạng.
        """
        nonce = self.w3.eth.get_transaction_count(self.address)
        amount_wei = self.w3.to_wei(amount_ether, 'ether')
        
        tx = {
            'nonce': nonce,
            'to': Web3.to_checksum_address(to_address),
            'value': amount_wei,
            'gas': 21000,
            'gasPrice': self.get_gas_price(),
            'chainId': self.chain_id
        }
        
        # Ký và Gửi
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        print(f"🚀 [{self.network_name}] Đã gửi {amount_ether} {self.symbol}. Đang chờ xác nhận...")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            tx_hex = tx_hash.hex()
            if not tx_hex.startswith("0x"):
                tx_hex = "0x" + tx_hex
            print(f"✅ [{self.network_name}] Transaction hoàn tất! Hash: {tx_hex}")
            if self.explorer_url:
                print(f"🔍 Xem tại: {self.explorer_url}/tx/{tx_hex}")
            return tx_hex
        else:
            print(f"❌ [{self.network_name}] Transaction bị Reverted trên chuỗi!")
            return None

    @retry(
        retry=retry_if_exception_type((TimeExhausted, Exception)), 
        stop=stop_after_attempt(3), 
        wait=wait_random(min=2, max=5),
        reraise=True
    )
    def deploy_dummy_contract(self) -> Optional[str]:
        """
        Triển khai một Smart Contract rỗng (Dummy Contract).
        Bí quyết Airdrop: Các ví có lịch sử Deploy Contract thường được đánh giá là "Dev Wallet".
        """
        # Bytecode tối giản của một Contract rỗng (Solidity tạo ra)
        dummy_bytecode = "0x6080604052348015600f57600080fd5b50603f80601d6000396000f3fe6080604052600080fdfea2646970667358221220a2cb7be345bb382583852037cb9a941ea636b07d578b877ff4d468b374bfcfd164736f6c63430008120033"
        
        nonce = self.w3.eth.get_transaction_count(self.address)
        tx = {
            'nonce': nonce,
            'from': self.address,
            'to': None,  # Báo hiệu tạo contract
            'data': dummy_bytecode,
            'gas': 150000,
            'gasPrice': self.get_gas_price(),
            'chainId': self.chain_id
        }
        
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        tx_hex = tx_hash.hex()
        if not tx_hex.startswith("0x"):
            tx_hex = "0x" + tx_hex
            
        print(f"📜 [{self.network_name}] Đang đẩy Smart Contract lên mạng... Hash: {tx_hex}")
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            contract_address = receipt.contractAddress
            print(f"✅ [{self.network_name}] Deploy Contract thành công! Address: {contract_address}")
            if self.explorer_url:
                print(f"🔍 Xem tại: {self.explorer_url}/address/{contract_address}")
            return contract_address
        else:
            print(f"❌ [{self.network_name}] Deploy Contract bị Reverted!")
            return None

    def random_delay(self, min_sec=10, max_sec=60):
        """
        [UPGRADE] Gaussian Random Delay de lach bo loc Sybil.
        Su dung phan phoi chuan (Gaussian) de tao do tre tu nhien hon.
        """
        mu = (min_sec + max_sec) / 2
        sigma = (max_sec - min_sec) / 6
        delay = max(min_sec, min(max_sec, random.gauss(mu, sigma)))
        
        print(f"💤 [{self.network_name}] Stealth Sleep: {delay:.2f}s...")
        time.sleep(delay)

    def fragment_amount(self, total_amount: float, parts: int = 3) -> List[float]:
        """
        Chia nho so luong token thanh cac phan ngau nhien de lam nhiễu analysis.
        """
        if total_amount <= 0 or parts <= 0: return [total_amount]
        
        weights = [random.uniform(0.5, 1.5) for _ in range(parts)]
        total_weight = sum(weights)
        fragments = [round((w / total_weight) * total_amount, 6) for w in weights]
        
        # Dieu chinh phan cuoi de khop tong (do sai so lam tron)
        fragments[-1] = round(total_amount - sum(fragments[:-1]), 6)
        print(f"🧩 Fragmented {total_amount} into {fragments}")
        return fragments
