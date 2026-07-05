import os
import sys
import shutil
from pathlib import Path

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def root_cleanup():
    root_dir = Path(__file__).resolve().parent.parent.parent
    
    print("🧹 BẮT ĐẦU DỌN DẸP THƯ MỤC GỐC...")
    
    # 1. Tạo thư mục docs/guides
    guides_dir = root_dir / "docs" / "guides"
    os.makedirs(guides_dir, exist_ok=True)
    
    # 2. Di chuyển tài liệu Markdown lẻ ở Root
    docs_to_move = [
        "AI_ONBOARDING_GUIDE.md",
        "CAREER_STRATEGY.md",
        "CONTEXT_SUMMARY.md",
        "INSTRUCTIONS.md",
        "MASTER_GUIDE.md"
    ]
    
    for doc in docs_to_move:
        src = root_dir / doc
        dst = guides_dir / doc
        if src.exists():
            print(f"[-] Di chuyển {doc} -> docs/guides/")
            shutil.move(src, dst)
            
    # 3. Xóa các file/thư mục rác hoàn toàn
    trash_items = [
        "langgraph_agent_system.egg-info", # Build thừa của python/pip cũ
        "setup.py"                         # Đã chuyển sang uv workspace
    ]
    
    for item in trash_items:
        path = root_dir / item
        if path.exists():
            print(f"[-] Xóa file/thư mục thừa: {item}")
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
            except Exception as e:
                print(f"  [!] Lỗi khi xóa {item}: {e}")
                
    # ml_output.txt đang bị lock, ta có thể bỏ qua nó hoặc xoá nội dung thay vì xoá file
    ml_output = root_dir / "ml_output.txt"
    if ml_output.exists():
        try:
            open(ml_output, 'w').close()
            print("[-] Đã làm trống file đang bị lock: ml_output.txt")
        except Exception as e:
            print(f"  [!] Lỗi khi làm trống ml_output.txt: {e}")
                
    # 4. Gom Data Output
    data_archive_dir = root_dir / "docs" / "archive_data"
    os.makedirs(data_archive_dir, exist_ok=True)
    
    data_dirs = [
        "analysis_user",
        "images_output",
        "input",
        "output"
    ]
    
    for d in data_dirs:
        src = root_dir / d
        dst = data_archive_dir / d
        if src.exists():
            print(f"[-] Lưu trữ thư mục data {d} -> docs/archive_data/")
            shutil.move(src, dst)
            
    print("✅ Hoàn tất dọn dẹp thư mục gốc.")

if __name__ == "__main__":
    root_cleanup()