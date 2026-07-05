import hashlib
import time
import urllib.request
import json
import os

def check_license_validity():
    """
    Core DRM Logic.
    This file should be compiled to .pyd / .so using Cython to prevent reverse engineering.
    """
    license_key = os.getenv("JARVIS_LICENSE_KEY", "DEMO_KEY")
    print("[DRM] Verifying License Key:", license_key[:4] + "...")
    
    # 1. Fake Hardware ID check
    hwid = hashlib.sha256(str(os.getlogin() + "SYSTEM_DISK").encode()).hexdigest()
    
    from datetime import datetime
    
    # 2. Network Check (Simulation)
    # Trong thực tế sẽ gọi lên máy chủ của Founder để verify hwid + license_key
    try:
        # Hardcode expire date cho bản Beta
        expire_date = "2026-07-20"
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        if current_date > expire_date:
            raise SystemExit("🛑 LỖI BẢN QUYỀN: Bản Beta đã hết hạn! Vui lòng truy cập https://discord.gg/your_link để mua bản chính thức.")
            
        # Giả lập gọi server
        if license_key == "DEMO_KEY":
            print(f"[DRM] Public Beta Version. Valid until {expire_date}.")
            return True
        elif len(license_key) == 16:
            print("[DRM] Premium License Verified!")
            return True
        else:
            print("[DRM] INVALID LICENSE.")
            return False
    except Exception as e:
        if isinstance(e, SystemExit):
            raise e
        print(f"[DRM] Connection failed: {e}")
        return False

def init_drm():
    if not check_license_validity():
        raise SystemExit("🛑 LỖI BẢN QUYỀN: Vui lòng mua key bản quyền tại Jarvis System!")
