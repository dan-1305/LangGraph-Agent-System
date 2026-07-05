from core_utilities.http_client import HTTPClient
import sys
import io
import os
import random
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Force stdout to be UTF-8 for Windows console
if hasattr(sys.stdout, 'reconfigure'):
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

# Đảm bảo import được các module trong project
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.automation.wallet_manager import WalletManager
from src.networks.monad import MonadNetwork
from src.networks.soneium import SoneiumNetwork
from src.networks.inco import IncoNetwork

# 1. Khởi tạo môi trường
# Tách Bot: Lấy .env từ thư mục của chính bot (để bán package độc lập)
load_dotenv(base_dir / ".env")
DB_PATH = base_dir / "data" / "airdrop_guerrilla.db"
# Đọc key chung để đồng bộ với wallet_manager (đồng bộ tên biến)
WALLET_MASTER_KEY = os.getenv("WALLET_MASTER_KEY")
TELE_TOKEN = os.getenv("TELE_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message: str):
    """Gửi thông báo qua Telegram"""
    if not TELE_TOKEN or not CHAT_ID:
        print("⚠️ Chưa cấu hình TELE_TOKEN hoặc CHAT_ID, bỏ qua gửi thông báo Telegram.")
        return
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = HTTPClient.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Lỗi khi gửi Telegram: {e}")

def log_transaction_to_db(wallet_address: str, network: str, action: str, tx_hash: str, status: str, error_msg: str = ""):
    """Ghi nhận lịch sử giao dịch vào SQLite Database để phục vụ chấm điểm sau này."""
    # Đảm bảo thư mục tồn tại
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS onchain_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            wallet_address TEXT,
            network_name TEXT,
            action_type TEXT,
            tx_hash TEXT,
            status TEXT,
            error_message TEXT
        )
    ''')
    
    cursor.execute('''
        INSERT INTO onchain_logs (timestamp, wallet_address, network_name, action_type, tx_hash, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), wallet_address, network, action, tx_hash, status, error_msg))
    
    conn.commit()
    conn.close()

def execute_random_action(chain_instance, wallet_address: str, network_name: str):
    """Áp dụng thuật toán xúc xắc 80/20 chống bộ lọc Sybil (Với Jitter Amount)."""
    roll = random.randint(1, 100)
    tx_hash = None
    action_type = ""
    
    try:
        if roll <= 80:
            # 80% Tỷ lệ: Gửi một lượng Native Token (Jitter Amount dựa theo mạng)
            action_type = "Transfer"
            current_balance = chain_instance.get_balance()
            if current_balance <= 0.0001:
                random_amount = current_balance * 0.5  # Nếu quá nghèo thì gửi 50% số dư ít ỏi
            else:
                # Tùy chỉnh mức gửi theo quỹ thực tế đang có
                if network_name == "Monad":
                    # Đang có ~20 MON, gửi ngẫu nhiên 0.1 đến 1.5 MON mỗi lượt
                    random_amount = round(random.uniform(0.1, 1.5), 6)
                elif network_name == "Soneium":
                    # Đang có ~5.2 ETH testnet, gửi ngẫu nhiên 0.05 đến 0.2 ETH mỗi lượt
                    random_amount = round(random.uniform(0.05, 0.2), 6)
                else:
                    # Gửi ngẫu nhiên từ 1% đến 5% số dư cho mạng khác
                    jitter_percent = random.uniform(0.01, 0.05)
                    random_amount = round(current_balance * jitter_percent, 6)
                    
                # Rào lỗi nếu ramdom amount vượt số dư
                if random_amount > current_balance * 0.8:
                    random_amount = current_balance * 0.5
                
            print(f"[{network_name}] Đổ xúc xắc ra {roll}. Chọn hành động GỬI TOKEN ({random_amount} {chain_instance.symbol} - Jitter Amount)...")
            tx_hash = chain_instance.send_native_token(wallet_address, random_amount)
            
        else:
            # 20% Tỷ lệ: Deploy Smart Contract rỗng
            action_type = "Deploy Contract"
            print(f"[{network_name}] Đổ xúc xắc ra {roll}. Chọn hành động DEPLOY DUMMY CONTRACT...")
            tx_hash = chain_instance.deploy_dummy_contract()
            
        if tx_hash:
            print(f"✅ [{network_name}] Thực thi thành công {action_type}. Tx: {tx_hash}")
            log_transaction_to_db(wallet_address, network_name, action_type, tx_hash, "SUCCESS")
        else:
            print(f"❌ [{network_name}] {action_type} thất bại (Giao dịch bị Revert hoặc rớt mạng).")
            log_transaction_to_db(wallet_address, network_name, action_type, "", "FAILED", "Reverted or Timeout")
        
    except Exception as e:
        print(f"❌ [{network_name}] Lỗi thực thi: {e}")
        log_transaction_to_db(wallet_address, network_name, action_type or "Unknown", "", "ERROR", str(e))

def main():
    print("=== Khởi động Stealth Engine Automation (RPC Mode) ===")
    
    db_path = base_dir / "data" / "wallets" / "secure_wallets.json"
    
    # Để WalletManager tự quản lý việc tìm kiếm Key
    wm = WalletManager(str(db_path), None)
    
    if not wm.wallets:
        print("⚠️ Không tìm thấy ví trong Database. Đang nạp từ file .env...")
        env_pk = os.getenv("WALLET_PRIVATE_KEY")
        if env_pk:
            try:
                from eth_account import Account
                # Derive public address from private key
                acct = Account.from_key(env_pk)
                real_address = acct.address
                # Extract auth tokens if present
                tw_token = os.getenv("Auth_Token_X", "")
                dc_token = os.getenv("Auth_Token_Discord", "")
                
                wm.add_wallet(real_address, env_pk, "Imported from .env", tw_token, dc_token)
                print(f"✅ Đã nạp thành công ví chính: {real_address}")
            except Exception as e:
                print(f"❌ Lỗi nạp ví từ .env: {e}")
                return
        else:
            print("❌ Không tìm thấy WALLET_PRIVATE_KEY trong .env. Tiến trình dừng.")
            return

    # Duyệt qua từng ví
    for address, info in wm.wallets.items():
        print("\n" + "="*60)
        print(f"💼 Đang xử lý ví: {info.get('name', 'Unknown')} ({address})")
        print("="*60)
        
        # Giải mã lấy Private Key và cấu hình Proxy
        decrypted = wm.get_decrypted_data(address)
        private_key = decrypted.get('private_key')
        proxy_url = decrypted.get('proxy_url', "")
        
        if not private_key:
            print("❌ Không giải mã được Private Key. Bỏ qua ví này.")
            continue
            
        # Khởi tạo danh sách các mạng mục tiêu (Thêm Try-Except bắt lỗi khởi tạo nếu tất cả RPC chết)
        networks = {}
        try: networks["Monad"] = MonadNetwork(private_key, proxy_url)
        except Exception as e: print(f"⚠️ Không thể khởi tạo Monad: {e}")
            
        try: networks["Soneium"] = SoneiumNetwork(private_key, proxy_url)
        except Exception as e: print(f"⚠️ Không thể khởi tạo Soneium: {e}")
            
        # [2026-06-07] Tạm ẩn mạng Inco vì chưa có Testnet chính thức/Faucet
        # try: networks["Inco"] = IncoNetwork(private_key, proxy_url)
        # except Exception as e: print(f"⚠️ Không thể khởi tạo Inco: {e}")
        
        # Xáo trộn thứ tự cày mạng lưới để tránh hành vi rập khuôn
        network_list = list(networks.items())
        random.shuffle(network_list)
        
        for network_name, chain_instance in network_list:
            try:
                if not getattr(chain_instance, 'w3', None):
                    print(f"\n❌ [SKIP] Mạng {network_name} bỏ qua do lỗi khởi tạo RPC.")
                    continue
                    
                # Check số dư và báo động
                if not chain_instance.check_balance_and_survival():
                    continue

                # Giả lập độ trễ hành vi giống người thật (Random Sleep 3 đến 8 phút)
                sleep_time = random.randint(180, 480)
                print(f"\n⏳ [Stealth Mode] Nghỉ ngẫu nhiên {sleep_time // 60} phút {sleep_time % 60} giây trước khi tương tác mạng {network_name}...")
                
                # Countdown Loop để báo hiệu hệ thống vẫn đang chạy (không bị đơ)
                remaining = sleep_time
                while remaining > 0:
                    mins, secs = divmod(remaining, 60)
                    print(f"   => Đang chờ... Còn lại {mins:02d}:{secs:02d} ", end="\r", flush=True)
                    step = min(10, remaining)  # Cập nhật mỗi 10 giây hoặc ít hơn nếu sắp hết
                    time.sleep(step)
                    remaining -= step
                print("   => Hết thời gian chờ, tiến hành giao dịch!        ")

                # Kích hoạt hành động 80/20
                execute_random_action(chain_instance, address, network_name)
            except Exception as e:
                print(f"\n❌ [ERROR] Lỗi nghiêm trọng trên mạng {network_name}: {e}. Đang nhảy sang mạng tiếp theo...")
                continue
            
        # API Guard: Xóa sạch Private Key khỏi bộ nhớ RAM sau khi xử lý xong ví đó
        del private_key
        
    print("\n🎉 === HOÀN THÀNH PHIÊN CÀY CUỐC ON-CHAIN NGÀY HÔM NAY ===")
    send_telegram_message("✅ <b>Airdrop Guerrilla</b>: Đã hoàn thành phiên cày cuốc On-chain ngày hôm nay!")

if __name__ == "__main__":
    main()
