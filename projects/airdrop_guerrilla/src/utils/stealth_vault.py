import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path

class StealthVault:
    """
    He thong luu tru bao mat cach ly (Stealth Vault).
    Dung de ma hoa va bao ve Private Keys/Mnemonic cho Airdrop Bot.
    """
    
    def __init__(self, vault_path: str = None):
        if vault_path is None:
            # Luu vao vung data cua project
            self.vault_dir = Path(__file__).resolve().parent.parent.parent / "data" / "vault"
        else:
            self.vault_dir = Path(vault_path)
            
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.key_file = self.vault_dir / ".vault_key"
        self.cipher_suite = self._load_or_create_key()

    def _load_or_create_key(self):
        """Khoi tao hoac nạp key ma hoa tu Master Key he thong."""
        master_key = os.getenv("WALLET_MASTER_KEY", "default-fallback-key-for-dev")
        salt = b'stealth-isolation-salt' # Trong thực tế nên random và lưu lại
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
        return Fernet(key)

    def encrypt_and_store(self, alias: str, secret_data: str):
        """Ma hoa va luu tru du lieu."""
        encrypted_data = self.cipher_suite.encrypt(secret_data.encode())
        file_path = self.vault_dir / f"{alias}.vault"
        with open(file_path, "wb") as f:
            f.write(encrypted_data)
        return file_path

    def decrypt_and_retrieve(self, alias: str) -> str:
        """Giai ma va lay du lieu."""
        file_path = self.vault_dir / f"{alias}.vault"
        if not file_path.exists():
            return None
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        return self.cipher_suite.decrypt(encrypted_data).decode()

if __name__ == "__main__":
    # Test Vault
    vault = StealthVault()
    # vault.encrypt_and_store("test_wallet", "this is a private key")
    # print(vault.decrypt_and_retrieve("test_wallet"))
