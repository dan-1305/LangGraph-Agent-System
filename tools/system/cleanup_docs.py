import os
import sys
import shutil
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

def cleanup_docs():
    root_dir = Path(__file__).resolve().parent.parent.parent
    
    print("🧹 BẮT ĐẦU DỌN DẸP TÀI LIỆU...")
    
    # 1. Xử lý trùng lặp ARCHITECTURE
    old_arch = root_dir / "ARCHITECTURE.md"
    new_arch = root_dir / "context" / "ARCHITECTURE.md"
    
    if old_arch.exists() and new_arch.exists():
        print(f"[-] Thay thế {old_arch.name} bằng redirect link.")
        with open(old_arch, "w", encoding="utf-8") as f:
            f.write("# 🏗️ System Architecture\n\n")
            f.write("> **NOTICE:** This document has been moved and updated to V2.\n")
            f.write("> Please refer to the new core architecture document at: `context/ARCHITECTURE.md`\n")

    # 2. Xóa các file rác/trùng lặp hoàn toàn
    files_to_remove = [
        root_dir / "docs" / "FLAGSHIP_EXECUTIVE_SUMMARY.md", # Trùng 100% với context/
    ]
    
    for f in files_to_remove:
        if f.exists():
            print(f"[-] Đang xóa file trùng lặp: {f.relative_to(root_dir)}")
            f.unlink()
            
    print("✅ Hoàn tất dọn dẹp sơ bộ. Vui lòng kiểm tra lại cấu trúc.")

if __name__ == "__main__":
    cleanup_docs()