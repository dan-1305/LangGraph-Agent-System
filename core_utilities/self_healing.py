import psutil
import time
import os
import subprocess
import httpx
import logging
from pathlib import Path
import sys

# [FIX] Import relative/absolute logic de dam bao chay duoc tu moi noi
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from core_utilities.notification_gateway import send_alert
except ImportError:
    # Fallback don gian neu khong import duoc
    def send_alert(msg, **kwargs): print(f"[ALERT] {msg}")

# Setup Logging
log_dir = BASE_DIR / "logs"
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    filename=log_dir / "self_healing.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SelfHealingWatchdog:
    """
    He thong tu phuc hoi (Self-Healing).
    Giam sat va tu dong khoi dong lai cac dich vu cot loi neu bi sap.
    """
    
    def __init__(self):
        self.proxy_url = "http://localhost:8001/health"
        self.proxy_script = "projects/local_proxy_server/main.py"
        self.root_dir = BASE_DIR

    def check_proxy_alive(self) -> bool:
        """Kiem tra xem Local Proxy co dang phan hoi khong."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(self.proxy_url)
                return response.status_code == 200
        except Exception:
            return False

    def repair_python_path(self, env_dict: dict) -> dict:
        """[V2] Tu dong thiet lap PYTHONPATH chuan de fix loi ModuleNotFoundError."""
        root_str = str(self.root_dir)
        if "PYTHONPATH" not in env_dict:
            env_dict["PYTHONPATH"] = root_str
        elif root_str not in env_dict["PYTHONPATH"]:
            env_dict["PYTHONPATH"] = f"{root_str}{os.pathsep}{env_dict['PYTHONPATH']}"
        return env_dict

    def restart_proxy(self):
        """Khoi dong lai Local Proxy Server voi co che tu sua duong dan."""
        logging.warning("🔄 Phat hien Local Proxy chet. Dang tien hanh hoi sinh...")
        send_alert("⚠️ Local Proxy bi sap! Dang tu dong khoi dong lai...", level="WARNING", component="SELF_HEALING")
        
        try:
            # Kill process cu neu con treo o port 8001
            kill_cmd = 'powershell -Command "Stop-Process -Id (Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue).OwningProcess -Force -ErrorAction SilentlyContinue"'
            subprocess.run(kill_cmd, shell=True, capture_output=True)
            
            # Chay script khoi dong voi Dynamic Path Injection
            env = self.repair_python_path(os.environ.copy())
            env["PYTHONIOENCODING"] = "utf-8"
            
            cmd = ["uv", "run", "python", str(self.root_dir / self.proxy_script)]
            if os.name == 'nt': # Windows
                subprocess.Popen(cmd, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:
                subprocess.Popen(cmd, env=env)
            
            logging.info(f"✅ Da hoi sinh Proxy voi PYTHONPATH: {env.get('PYTHONPATH')}")
        except Exception as e:
            logging.error(f"❌ Khong the hoi sinh Proxy: {e}")
            send_alert(f"🔴 KHAN CAP: Tu dong phuc hoi Proxy THAT BAI", level="CRITICAL", component="SELF_HEALING")

    def monitor_loop(self):
        logging.info("🏥 He thong Self-Healing da kich hoat.")
        while True:
            if not self.check_proxy_alive():
                self.restart_proxy()
                # Cho 10s de proxy len han
                time.sleep(10)
            
            time.sleep(30) # Kiem tra moi 30 giay

if __name__ == "__main__":
    healer = SelfHealingWatchdog()
    healer.monitor_loop()
