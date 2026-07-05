import os
import shutil
import argparse
import logging
import zipfile
from datetime import datetime
from pathlib import Path

# --- CONFIGURATION ---
STORAGE_DIR = os.getenv("STORAGE_DIR", r"D:\Users\Admin\Downloads\LangGraphStorage")
QUARANTINE_DIR = Path(STORAGE_DIR) / "monorepo_quarantine"
ARCHIVE_DIR = Path(STORAGE_DIR) / "system_archives"
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"

# Ensure directories exist
QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "system_cleaner.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SystemCleaner")

class TripleFilterCleaner:
    """
    Hệ thống thanh lọc 3 lớp (Triple-Filter Protocol):
    Lớp 1: Di chuyển vào khu cách ly (Quarantine) trên ổ D.
    Lớp 2: Nén lại thành file zip sau thời gian kiểm chứng.
    Lớp 3: Xóa vĩnh viễn (Chỉ khi có lệnh hoặc hết hạn lưu trữ).
    """

    @staticmethod
    def level_1_migrate(file_path: str):
        """Di chuyển file/thư mục vào khu vực cách ly (Quarantine)."""
        src = Path(file_path)
        if not src.exists():
            logger.warning(f"File không tồn tại để migrate: {file_path}")
            return False

        # Giữ nguyên cấu trúc thư mục trong quarantine để dễ restore
        rel_path = src.name
        dest = QUARANTINE_DIR / rel_path
        
        # Nếu trùng tên, thêm timestamp
        if dest.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = QUARANTINE_DIR / f"{src.stem}_{timestamp}{src.suffix}"

        try:
            shutil.move(str(src), str(dest))
            logger.info(f"✅ [LEVEL 1] Đã cách ly: {src} -> {dest}")
            return True
        except Exception as e:
            logger.error(f"❌ [LEVEL 1] Lỗi khi migrate {src}: {e}")
            return False

    @staticmethod
    def level_2_compress(quarantine_age_days: int = 7):
        """Nén các file trong quarantine đã cũ hơn X ngày."""
        # Logic này sẽ được gọi định kỳ bởi scheduler
        today = datetime.now()
        files_to_zip = []
        
        for item in QUARANTINE_DIR.iterdir():
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            age = (today - mtime).days
            if age >= quarantine_age_days:
                files_to_zip.append(item)

        if not files_to_zip:
            return

        zip_name = ARCHIVE_DIR / f"cleanup_archive_{today.strftime('%Y%m%d')}.zip"
        try:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files_to_zip:
                    zipf.write(file, file.name)
                    # Sau khi nén thành công thì xóa file lẻ trong quarantine
                    if file.is_dir():
                        shutil.rmtree(file)
                    else:
                        file.unlink()
            logger.info(f"📦 [LEVEL 2] Đã nén {len(files_to_zip)} file vào: {zip_name}")
        except Exception as e:
            logger.error(f"❌ [LEVEL 2] Lỗi nén: {e}")

    @staticmethod
    def level_3_terminate(archive_age_days: int = 30):
        """Xóa vĩnh viễn các bản nén cũ hơn X ngày."""
        # CHỈ THỰC HIỆN KHI CÓ LỆNH HOẶC CẤU HÌNH CỤ THỂ
        # Hiện tại giữ lại để an toàn tuyệt đối
        pass

def clean_zombie_files(aggressive=False):
    """
    Hàm quyét và dọn dẹp các file rác đã biết.
    Sử dụng LEVEL 1 (Migrate) thay vì xóa.
    """
    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    
    # Danh sách các file/thư mục rác tiềm năng (cần được audit bởi Boss)
    zombie_patterns = [
        "dist",
        "repack_verbose.log",
        "temp_full_file_list.txt",
        "temp_audit_list.txt",
        "*.scn", # Godot scenes rác ở root
        "*.zip", # Các bản nén cũ ở root
        "projects/*/archive", # Thư mục lưu trữ cũ trong các dự án
        "projects/sillytavern_world_card_generator/data/templates/WorldBook/Segg",
        "projects/auto_affiliate_video/data/output/*.mp4",
        "reports/factory_run_new_*.md", # Log chạy cũ
    ]
    
    for pattern in zombie_patterns:
        for item in ROOT_DIR.glob(pattern):
            # Tuyệt đối không chạm vào file core
            if "src/base_agent.py" in str(item) or "monorepo_manifest.json" in str(item):
                continue
            TripleFilterCleaner.level_1_migrate(str(item))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign System Cleaner V2 (Triple-Filter)")
    parser.add_argument("--run", action="store_true", help="Chạy quét và cách ly Level 1")
    parser.add_argument("--compress", action="store_true", help="Nén các file cũ trong Quarantine (Level 2)")
    parser.add_argument("--path", type=str, help="Cách ly thủ công một file/thư mục cụ thể")
    
    args = parser.parse_args()
    
    if args.path:
        TripleFilterCleaner.level_1_migrate(args.path)
    elif args.run:
        clean_zombie_files()
    elif args.compress:
        TripleFilterCleaner.level_2_compress()
    else:
        parser.print_help()
