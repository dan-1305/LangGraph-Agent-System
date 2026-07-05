import os
import sys
import psutil
import subprocess
from pathlib import Path
import time

# Đảm bảo in console tiếng Việt không lỗi trên Windows
if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

# Load env để check override
root_dir = Path(__file__).resolve().parent.parent.parent
from dotenv import load_dotenv
load_dotenv(root_dir / '.env')

def run_command(cmd, description):
    print(f"🔄 Đang thực hiện: {description}...")
    try:
        # Sử dụng sys.executable để đảm bảo dùng đúng python của môi trường hiện tại
        full_cmd = [sys.executable] + cmd if cmd[0].endswith('.py') else cmd
        
        result = subprocess.run(
            full_cmd, 
            cwd=str(root_dir),
            capture_output=True, 
            text=True, 
            encoding='utf-8',
            errors='replace'
        )
        
        if result.returncode == 0:
            print(f"✅ {description} thành công.")
            return True
        else:
            print(f"❌ {description} thất bại.")
            return False
    except Exception as e:
        print(f"💥 Lỗi hệ thống khi chạy {description}: {e}")
        return False

def cleanup_processes():
    """Dọn dẹp các tiến trình python/uv mồ côi để giải phóng venv lock."""
    print("🧹 Đang dọn dẹp tiến trình background...")
    current_pid = os.getpid()
    count = 0
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            if proc.info['name'] in ['python.exe', 'python', 'uv.exe', 'uv']:
                cmd_line = " ".join(proc.cmdline())
                if "main_scheduler.py" in cmd_line:
                    print(f"   🛑 Đang tắt Scheduler: PID {proc.info['pid']}")
                    proc.kill()
                    count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    print(f"✅ Đã dọn dẹp {count} tiến trình.")

def has_changes():
    """Kiểm tra xem có thay đổi quan trọng trong mã nguồn không (Git check)."""
    try:
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return True
        return False
    except Exception:
        return True

def anchoring():
    """
    Sovereign Anchoring System (SAS)
    Nhiệm vụ: Chuẩn hóa quy trình "Chốt sổ" thông minh.
    """
    print("==================================================")
    print("🌟 SOVEREIGN ANCHORING PROTOCOL (SAS) ACTIVATED 🌟")
    print("==================================================")

    # 0. Kiểm tra nhu cầu thực tế
    override = os.getenv("SOVEREIGN_OVERRIDE") == "TRUE"
    sas_disabled = os.getenv("SAS_DISABLED") == "TRUE"
    changed = has_changes()

    if sas_disabled and not override:
        print("⏭️ SAS_DISABLED is TRUE. Bỏ qua quy trình chốt sổ.")
        return

    # 0.5 Dọn dẹp tiến trình
    cleanup_processes()

    # 1. Mapping hệ thống (Luôn chạy để đảm bảo bản đồ chuẩn)
    run_command(["tools/system/auto_mapper.py"], "Cập nhật Bản đồ Hệ thống (SYSTEM_MAP)")

    # 2. Backup & Ingest (Chỉ chạy khi có thay đổi để tiết kiệm tài nguyên)
    if changed or override:
        run_command(["core_utilities/backup_manager.py", "--now"], "Sao lưu Dữ liệu (Auto-Backup)")
        run_command(["tools/system/rag_ingest.py", "--force"], "Nạp Tri thức vào RAG (Ingestion)")
    else:
        print("⚡ Không phát hiện thay đổi mã nguồn. Bỏ qua Backup & Ingest để tiết kiệm tài nguyên.")

    # 3. Nén bối cảnh (Luôn chạy để giữ ACTIVE_THOUGHTS gọn gàng)
    run_command(["tools/system/context_compressor.py"], "Nén bộ nhớ ACTIVE_THOUGHTS")

    print("\n📝 [NHẮC NHỞ QUAN TRỌNG]:")
    print("1. Boss ơi, hãy bảo Cline ghi tóm tắt vào context/ACTIVE_THOUGHTS.md")
    print("2. Đừng quên cập nhật cột mốc vào context/JARVIS_CHRONICLES.md")
    
    print("\n🏁 QUY TRÌNH ANCHORING HOÀN TẤT.")
    print("Vương triều Sovereign đã được bảo toàn. Sẵn sàng đóng phiên.")

if __name__ == "__main__":
    anchoring()
