import os
import json
import hashlib
import getpass
from pathlib import Path
from cryptography.fernet import Fernet

class WalletManager:
    """
    Trình quản lý Ví tự động (Wallet Manager).
    Chịu trách nhiệm mã hóa/giải mã Private Key an toàn và quản lý User-Agent chống Sybil.
    """
    def __init__(self, db_path: str, master_key: bytes = None):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        import base64
        # Nếu chưa cung cấp Master Key, cố đọc từ biến môi trường
        from dotenv import load_dotenv, set_key
        load_dotenv()
        if master_key is None:
            key_str = os.getenv("WALLET_MASTER_KEY")
            if not key_str:
                print("[WARNING] Chua tim thay WALLET_MASTER_KEY trong bien moi truong. He thong se tu dong tao moi...")
                key_str = Fernet.generate_key().decode('utf-8')
                # Tự động ghi vào file .env ở thư mục gốc
                env_path = Path(__file__).resolve().parent.parent.parent.parent.parent / ".env"
                if env_path.exists():
                    try:
                        set_key(str(env_path), "WALLET_MASTER_KEY", key_str)
                        print(f"[SUCCESS] Da tu dong luu WALLET_MASTER_KEY vao file .env!")
                    except Exception as e:
                        print(f"[ERROR] Khong the ghi vao file .env: {e}")
                else:
                    print(f"[ERROR] Khong tim thay file .env tai {env_path}")
            master_key_bytes = key_str.encode('utf-8')
        else:
            master_key_bytes = master_key
            
        try:
            self.cipher = Fernet(master_key_bytes)
        except ValueError:
            # Fallback: băm key để đạt 32 bytes chuẩn Fernet
            digest = hashlib.sha256(master_key_bytes).digest()
            fernet_key = base64.urlsafe_b64encode(digest)
            self.cipher = Fernet(fernet_key)
            
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

    def add_wallet(self, address: str, private_key: str, name: str = "Default", twitter_token: str = "", discord_token: str = "", proxy_url: str = "") -> None:
        """
        Thêm một ví mới, mã hóa Private Key, X auth_token, Discord token và gán User-Agent tĩnh.
        Hỗ trợ gắn thêm Proxy để Route IP riêng lẻ.
        """
        if address in self.wallets:
            print(f"[WARNING] Vi {address} da ton tai trong he thong!")
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
            "proxy_url": proxy_url,
            "status": "Active"
        }
        self._save_db()
        print(f"[SUCCESS] Da them vi {name} ({address[:6]}...{address[-4:]}) an toan!")

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
            "user_agent": wallet.get("user_agent", ""),
            "proxy_url": wallet.get("proxy_url", "")
        }

if __name__ == "__main__":
    # Test thử chức năng mã hóa và quản lý ví
    base_dir = Path(__file__).resolve().parent.parent.parent
    db_file = base_dir / "data" / "wallets" / "secure_wallets.json"
    
    # Xoá db cũ nếu có để test sạch
    if db_file.exists():
        os.remove(db_file)
    
    # Truyền None để WalletManager tự đọc key từ .env,
    # qua đó đảm bảo DB được mã hóa bằng đúng key mà full_auto_cli.py sẽ dùng để giải mã.
    wm = WalletManager(str(db_file), None)
    
    # Thêm ví giả lập
    fake_address = "0x71C7656EC7ab88b098defB751B7401B5f6d8976F"
    fake_pk = "0x0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
    
    print("\n--- TEST WALLET MANAGER ---")
    wm.add_wallet(fake_address, fake_pk, "Main Farm Wallet", "fake_auth_token_twitter", "fake_discord_token_xyz")
    
    # Lấy thông tin chống Sybil
    wallet_info = wm.wallets[fake_address]
    print("\nThong tin Database (Da ma hoa):")
    print(f"- Encrypted PK: {wallet_info['encrypted_private_key'][:30]}... (Bao mat 100%)")
    print(f"- Static User-Agent: {wallet_info['user_agent']}")
    
    # Giải mã
    decrypted_data = wm.get_decrypted_data(fake_address)
    print(f"\nGiai ma thanh cong: PK co khop voi goc khong? -> {decrypted_data['private_key'] == fake_pk}")
