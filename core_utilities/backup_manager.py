import os
import shutil
import time
import zipfile
import logging
from datetime import datetime
from pathlib import Path
from core_utilities.notification_gateway import send_alert
from logging.handlers import RotatingFileHandler

base_dir = Path(__file__).resolve().parent.parent

# Thiết lập log cho Backup Manager
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "backup.log")
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[handler, logging.StreamHandler()])

def get_storage_dir() -> Path:
    """Lấy thư mục data lưu trữ hiện tại (ưu tiên ổ D nếu có trong biến môi trường)"""
    from dotenv import load_dotenv
    load_dotenv(base_dir / ".env")
    storage_dir = os.getenv("STORAGE_DIR")
    if storage_dir:
        return Path(storage_dir)
    return base_dir / "data"

def backup_databases():
    """Nén tất cả các file .db (SQLite) thành file zip để backup."""
    logging.info("Bắt đầu quá trình Backup dữ liệu định kỳ...")
    
    storage_dir = get_storage_dir()
    backup_dir = storage_dir / "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"db_backup_{timestamp}.zip"
    backup_path = backup_dir / backup_filename
    
    db_files = []
    # Quét tìm các file .db và .sqlite3
    for ext in ["*.db", "*.sqlite3"]:
        db_files.extend(list(storage_dir.rglob(ext)))
        
    # Thêm file .env vào danh sách backup
    env_file = base_dir / ".env"
    if env_file.exists():
        db_files.append(env_file)
        
    if not db_files:
        logging.warning("Không tìm thấy file Database nào để backup.")
        return
        
    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for db_file in db_files:
                if "backups" not in str(db_file): # Bỏ qua thư mục backup
                    # Xử lý riêng cho file .env nằm ngoài storage_dir
                    if db_file.name == ".env":
                        arcname = "system_config.env"
                    else:
                        # Giữ nguyên cấu trúc thư mục tương đối
                        arcname = db_file.relative_to(storage_dir)
                    zipf.write(db_file, arcname)
                    logging.info(f"  + Đã nén: {arcname}")
                    
        file_size_mb = os.path.getsize(backup_path) / (1024 * 1024)
        msg = f"✅ Backup Database thành công!\n- Tên file: {backup_filename}\n- Kích thước: {file_size_mb:.2f} MB\n- Tổng số file: {len(db_files)}"
        logging.info(msg.replace("\n", " "))
        send_alert(msg, level="INFO", component="BACKUP_MANAGER")
        
        # Cleanup: Giữ lại 7 file backup gần nhất
        clean_old_backups(backup_dir, prefix="db_backup_*.zip", keep_last=7)
        
    except Exception as e:
        err_msg = f"❌ Lỗi nghiêm trọng khi backup Database: {e}"
        logging.error(err_msg)
        send_alert(err_msg, level="ERROR", component="BACKUP_MANAGER")

def backup_full_workspace():
    """Nén Zip toàn bộ thư mục workspace ngoại trừ các thư mục ảo/không cần thiết."""
    logging.info("Bắt đầu quá trình Backup Full Workspace...")
    
    storage_dir = get_storage_dir()
    backup_dir = storage_dir / "workspace_backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"workspace_backup_{timestamp}.zip"
    backup_path = backup_dir / backup_filename
    
    ignore_dirs = {'.venv', 'venv', '__pycache__', '.git', 'node_modules', str(storage_dir.name)}
    
    try:
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(base_dir):
                # Loại bỏ thư mục bị ignore
                dirs[:] = [d for d in dirs if d not in ignore_dirs and "backup" not in d]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    # Giữ cấu trúc thư mục tương đối
                    arcname = os.path.relpath(file_path, base_dir)
                    zipf.write(file_path, arcname)
                    
        file_size_mb = os.path.getsize(backup_path) / (1024 * 1024)
        msg = f"✅ Backup Workspace thành công!\n- Tên file: {backup_filename}\n- Kích thước: {file_size_mb:.2f} MB\n- Nơi lưu: {backup_dir}"
        logging.info(msg.replace("\n", " "))
        send_alert(msg, level="INFO", component="BACKUP_MANAGER")
        
        # Cleanup: Giữ lại 3 bản full backup gần nhất
        clean_old_backups(backup_dir, prefix="workspace_backup_*.zip", keep_last=3)
        
    except Exception as e:
        err_msg = f"❌ Lỗi nghiêm trọng khi backup Full Workspace: {e}"
        logging.error(err_msg)
        send_alert(err_msg, level="ERROR", component="BACKUP_MANAGER")

def clean_old_backups(backup_dir: Path, prefix: str = "db_backup_*.zip", keep_last: int = 7):
    """Giữ lại `keep_last` file backup mới nhất và xóa các file cũ hơn."""
    backups = sorted(list(backup_dir.glob(prefix)), key=os.path.getmtime, reverse=True)
    if len(backups) > keep_last:
        for old_backup in backups[keep_last:]:
            try:
                os.remove(old_backup)
                logging.info(f"Đã xóa file backup cũ: {old_backup.name}")
            except Exception as e:
                logging.error(f"Lỗi khi xóa file backup {old_backup.name}: {e}")

def backup_loop():
    """Chạy vòng lặp ngầm (cronjob) backup định kỳ mỗi 24 tiếng."""
    while True:
        backup_databases()
        # Chờ 24 tiếng
        time.sleep(24 * 3600)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--now":
            backup_databases()
        elif sys.argv[1] == "--full":
            backup_full_workspace()
    else:
        backup_loop()
