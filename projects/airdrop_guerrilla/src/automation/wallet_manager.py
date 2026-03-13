import os
import json
import hashlib
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
from fake_useragent import UserAgent

class WalletManager:
    """
    Trình quản lý Ví tự động (Wallet Manager).
    Chịu trách nhiệm mã hóa/giải mã Private Key an toàn và quản lý User-Agent chống Sybil.
    """
    def __init__(self, db_path: str, master_key: bytes = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Nếu chưa cung cấp Master Key, cố đọc từ biến môi trường
        if master_key is None:
            key_str = os.getenv("WALLET_MASTER_KEY")
            if not key_str:
                print("⚠️ CẢNH BÁO: Chưa tìm thấy WALLET_MASTER_KEY trong biến môi trường.")
                choice = input("Bạn muốn (1) Nhập Key có sẵn, hay (2) Tự động sinh Key mới? [1/2]: ").strip()
                if choice == '1':
                    key_str = getpass.getpass("🔑 Nhập WALLET_MASTER_KEY (ký tự sẽ được ẩn): ").strip()
                else:
                    key_str = Fernet.generate_key().decode('utf-8')
                    print(f"🔑 Đã sinh WALLET_MASTER_KEY mới. Hãy copy và lưu vào file .env ngay:\n{key_str}")
            self.cipher = Fernet(key_str.encode('utf-8'))
        else:
            self.cipher = Fernet(master_key)
            
        self.wallets = self._load_db()

    def _load_db(self) -> dict:
        """Tải dữ liệu ví từ file JSON."""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_db(self) -> None:
        """Lưu trữ dữ liệu ví xuống file JSON."""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.wallets, f, indent=4)

    def generate_static_user_agent(self, address: str) -> str:
        """
        Sinh ra một User-Agent CỐ ĐỊNH dựa trên địa chỉ ví (Chống Sybil).
        """
        # Băm địa chỉ ví để tạo random seed cố định
        seed = int(hashlib.md5(address.encode('utf-8')).hexdigest(), 16) % (10**8)
        import random
        random.seed(seed)
        
        # Sử dụng danh sách cứng để đảm bảo tính ổn định cao nhất qua thời gian
        ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        assigned_ua = random.choice(ua_list)
        # Reset seed về hiện tại
        random.seed()
        return assigned_ua

    def add_wallet(self, address: str, private_key: str, name: str = "Default", twitter_token: str = "", discord_token: str = "") -> None:
        """
        Thêm một ví mới, mã hóa Private Key, X auth_token, Discord token và gán User-Agent tĩnh.
        """
        if address in self.wallets:
            print(f"⚠️ Ví {address} đã tồn tại trong hệ thống!")
            return
            
        encrypted_pk = self.cipher.encrypt(private_key.encode('utf-8')).decode('utf-8')
        encrypted_tw = self.cipher.encrypt(twitter_token.encode('utf-8')).decode('utf-8') if twitter_token else ""
        encrypted_dc = self.cipher.encrypt(discord_token.encode('utf-8')).decode('utf-8') if discord_token else ""
        
        user_agent = self.generate_static_user_agent(address)
        
        self.wallets[address] = {
            "name": name,
            "encrypted_private_key": encrypted_pk,
            "encrypted_twitter_token": encrypted_tw,
            "encrypted_discord_token": encrypted_dc,
            "user_agent": user_agent,
            "status": "Active"
        }
        self._save_db()
        print(f"✅ Đã thêm ví {name} ({address[:6]}...{address[-4:]}) an toàn!")

    def get_decrypted_data(self, address: str) -> dict:
        """
        Lấy và giải mã Private Key và các Token mxh.
        """
        if address not in self.wallets:
            raise ValueError("Ví không tồn tại!")
            
        wallet = self.wallets[address]
        pk = self.cipher.decrypt(wallet["encrypted_private_key"].encode('utf-8')).decode('utf-8')
        tw = self.cipher.decrypt(wallet["encrypted_twitter_token"].encode('utf-8')).decode('utf-8') if wallet.get("encrypted_twitter_token") else ""
        dc = self.cipher.decrypt(wallet["encrypted_discord_token"].encode('utf-8')).decode('utf-8') if wallet.get("encrypted_discord_token") else ""
        
        return {
            "private_key": pk,
            "twitter_token": tw,
            "discord_token": dc,
            "user_agent": wallet["user_agent"]
        }

if __name__ == "__main__":
    # Test thử chức năng mã hóa và quản lý ví
    base_dir = Path(__file__).resolve().parent.parent.parent
    db_file = base_dir / "data" / "wallets" / "secure_wallets.json"
    
    # Giả lập Master Key (Thực tế phải bỏ vào .env)
    test_master_key = Fernet.generate_key()
    
    wm = WalletManager(str(db_file), test_master_key)
    
    # Thêm ví giả lập
    fake_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    fake_pk = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    
    print("\n--- TEST WALLET MANAGER ---")
    wm.add_wallet(fake_address, fake_pk, "Main Farm Wallet", "fake_auth_token_twitter", "fake_discord_token_xyz")
    
    # Lấy thông tin chống Sybil
    wallet_info = wm.wallets[fake_address]
    print(f"\nThông tin Database (Đã mã hóa):")
    print(f"- Encrypted PK: {wallet_info['encrypted_private_key'][:30]}... (Bảo mật 100%)")
    print(f"- Static User-Agent: {wallet_info['user_agent']}")
    
    # Giải mã
    decrypted_data = wm.get_decrypted_data(fake_address)
    print(f"\nGiải mã thành công: PK có khớp với gốc không? -> {decrypted_data['private_key'] == fake_pk}")
