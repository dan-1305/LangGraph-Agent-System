import os
import shutil
from pathlib import Path

class MultiAccountManager:
    """
    Quan ly da tai khoan (Multi-Account) cho Airdrop Sentinel.
    Ho tro quan ly doc lap cac Chrome Profiles va Wallet Secrets.
    """
    def __init__(self, base_profile_dir: str = None):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        if base_profile_dir:
            self.base_profile_dir = Path(base_profile_dir)
        else:
            self.base_profile_dir = self.root_dir / "data" / "profiles"
            
        self.base_profile_dir.mkdir(parents=True, exist_ok=True)

    def get_account_profile_path(self, account_id: str) -> str:
        """Lay duong dan thu muc profile cho mot account cu the."""
        profile_path = self.base_profile_dir / f"acc_{account_id}"
        profile_path.mkdir(parents=True, exist_ok=True)
        return str(profile_path)

    def list_accounts(self) -> list:
        """Liet ke danh sach cac account hien co."""
        return [d.name.replace("acc_", "") for d in self.base_profile_dir.iterdir() if d.is_dir() and d.name.startswith("acc_")]

    def delete_account(self, account_id: str):
        """Xoa mot account va du lieu profile di kem."""
        profile_path = self.base_profile_dir / f"acc_{account_id}"
        if profile_path.exists():
            shutil.rmtree(profile_path)
            print(f"🗑️ Da xoa account: {account_id}")

if __name__ == "__main__":
    manager = MultiAccountManager()
    path = manager.get_account_profile_path("001")
    print(f"Test profile path: {path}")
    print(f"All accounts: {manager.list_accounts()}")
