import os
import sys
import subprocess

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

def main():
    """
    Entry point chạy ngầm Streamlit. Dùng để thay thế file .bat cho bản Build.
    """
    app_path = os.path.join(os.path.dirname(__file__), "app.py")
    print("Khởi động hệ thống dịch Godot 1-Click...")
    
    # Chạy streamlit dưới dạng subprocess ngầm
    # Tự động mở trình duyệt ở localhost:8503
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", app_path, "--server.port", "8503"])
    except KeyboardInterrupt:
        print("Đã đóng công cụ dịch.")
    except Exception as e:
        print(f"Lỗi khởi động: {e}")

if __name__ == "__main__":
    main()
