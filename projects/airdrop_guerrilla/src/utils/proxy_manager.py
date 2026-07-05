import random
from pathlib import Path
import json

class ProxyManager:
    """
    Quan ly danh sach Proxy cho quan doan Clone.
    Ho tro gan co dinh IP cho tung Account de tranh bi detect.
    """
    def __init__(self, proxy_list_path: str = None):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        if proxy_list_path:
            self.proxy_file = Path(proxy_list_path)
        else:
            self.proxy_file = self.root_dir / "data" / "proxies.json"
            
        self.proxies = self._load_proxies()

    def _load_proxies(self):
        """Nap danh sach proxy tu file."""
        if not self.proxy_file.exists():
            # Tao file rong neu chua co
            self.proxy_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.proxy_file, "w") as f:
                json.dump([], f)
            return []
        
        with open(self.proxy_file, "r") as f:
            return json.load(f)

    def get_proxy_for_account(self, account_id: str) -> str:
        """
        Lay proxy gan cho account. 
        Su dung thuat toan hashing account_id de luon lay dung 1 proxy cho 1 acc.
        """
        if not self.proxies:
            return None
            
        # Tinh index dua tren hash cua account_id
        idx = hash(account_id) % len(self.proxies)
        return self.proxies[idx]

    def add_proxy(self, proxy_str: str):
        """Them proxy moi vao danh sach (Format: http://user:pass@host:port)."""
        if proxy_str not in self.proxies:
            self.proxies.append(proxy_str)
            with open(self.proxy_file, "w") as f:
                json.dump(self.proxies, f, indent=4)
            print(f"✅ Da them proxy moi: {proxy_str}")

if __name__ == "__main__":
    pm = ProxyManager()
    # pm.add_proxy("http://proxyuser:proxypass@1.2.3.4:8080")
    print(f"Proxy for acc 001: {pm.get_proxy_for_account('001')}")
