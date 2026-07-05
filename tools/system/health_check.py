import os
import sys
import psutil
from pathlib import Path
import importlib.util

# Đảm bảo in console tiếng Việt không lỗi trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

class SovereignHealthCheck:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.venv_path = self.root_dir / ".venv"
        self.storage_dir = os.getenv("STORAGE_DIR", "D:/Users/Admin/Downloads/LangGraphStorage")

    def check_venv_lock(self):
        """Kiểm tra xem có tiến trình nào đang chiếm dụng .venv không."""
        print("🔍 Đang kiểm tra Venv Lock...")
        locked_files = []
        # Danh sách các file nhạy cảm thường bị lock trên Windows
        critical_venv_files = list(self.venv_path.glob("**/*.pyd")) + list(self.venv_path.glob("**/*.dll"))
        
        for f in critical_venv_files:
            try:
                # Thử rename chính nó để check lock (cách nhanh nhất trên Windows)
                old_name = str(f)
                new_name = str(f) + ".test"
                os.rename(old_name, new_name)
                os.rename(new_name, old_name)
            except OSError:
                locked_files.append(f.name)
        
        if locked_files:
            print(f"⚠️ CẢNH BÁO: {len(locked_files)} file trong .venv đang bị LOCK.")
            print(f"   Các file bị lock: {', '.join(locked_files[:5])}...")
            return False
        print("✅ .venv sạch, không có lock.")
        return True

    def verify_dependencies(self):
        """Kiểm tra xem các thư viện core có load được không."""
        print("🔍 Đang xác minh Dependencies...")
        core_libs = ["numpy", "pandas", "chromadb", "pydantic"]
        missing_or_broken = []
        
        for lib in core_libs:
            try:
                spec = importlib.util.find_spec(lib)
                if spec is None:
                    missing_or_broken.append(lib)
                else:
                    # Thử import thực tế để check lỗi so sánh version (như vụ numpy)
                    importlib.import_module(lib)
            except Exception as e:
                print(f"❌ Lỗi khi load {lib}: {e}")
                missing_or_broken.append(lib)
        
        if missing_or_broken:
            print(f"⚠️ Dependencies hỏng: {', '.join(missing_or_broken)}")
            return False
        print("✅ Tất cả core dependencies ổn định.")
        return True

    def check_hardware_resources(self):
        """Kiểm tra RAM và Disk."""
        print("🔍 Đang kiểm tra tài nguyên hệ thống...")
        mem = psutil.virtual_memory()
        free_ram_gb = mem.available / (1024**3)
        
        # Check Disk D: (Nơi lưu trữ chính)
        try:
            usage = psutil.disk_usage(self.storage_dir)
            free_disk_gb = usage.free / (1024**3)
        except Exception:
            free_disk_gb = 0
            print(f"⚠️ Không thể truy cập Storage Dir: {self.storage_dir}")

        print(f"   RAM khả dụng: {free_ram_gb:.2f} GB")
        print(f"   Disk D: trống: {free_disk_gb:.2f} GB")

        health_status = True
        if free_ram_gb < 1.0:
            print("❌ RAM quá thấp (< 1GB). Hệ thống có thể crash.")
            health_status = False
        if free_disk_gb < 2.0:
            print("❌ Dung lượng ổ D: quá thấp (< 2GB). Ingest/Backup sẽ thất bại.")
            health_status = False
            
        return health_status

    def run_all_checks(self):
        print("\n=== SOVEREIGN HEALTH INSPECTION ===")
        v_lock = self.check_venv_lock()
        deps = self.verify_dependencies()
        hw = self.check_hardware_resources()
        print("===================================\n")
        
        if not v_lock or not deps or not hw:
            print("🚨 [HỆ THỐNG KHÔNG KHỎE MẠNH] Boss nên chạy 'python tools/system/endtask.py' để dọn dẹp.")
            return False
        
        print("🌟 [TRẠNG THÁI: EXCELLENT] Vương triều sẵn sàng vận hành.")
        return True

if __name__ == "__main__":
    checker = SovereignHealthCheck()
    checker.run_all_checks()
