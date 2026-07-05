import os
import sys
from pathlib import Path

# Fix for windows encoding
if sys.stdout.encoding != 'utf-8':
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def analyze_directory(root_dir: Path) -> dict:
    """Quét thư mục gốc và trả về cấu trúc các sub-projects."""
    projects_dir = root_dir / "projects"
    projects = []
    
    if projects_dir.exists():
        for item in projects_dir.iterdir():
            if item.is_dir() and not item.name.startswith(('_', '.')):
                projects.append(item.name)
    
    return {
        "total_projects": len(projects),
        "projects_list": projects
    }

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    print_header("📚 ON-DEMAND DOCS SYNC - TỰ ĐỘNG ĐỒNG BỘ TÀI LIỆU")
    print(f"Root path: {root_dir}")
    
    # 1. Quét dự án
    print("\n[1] Đang quét cấu trúc thư mục...")
    dir_info = analyze_directory(root_dir)
    print(f"Phát hiện {dir_info['total_projects']} sub-projects:")
    for proj in dir_info['projects_list']:
        print(f"  - {proj}")
        
    # 2. Kiểm tra các file tài liệu cốt lõi
    print("\n[2] Kiểm tra trạng thái tài liệu...")
    docs_to_check = [
        "context/ROADMAP.md",
        "context/ARCHITECTURE.md",
        "context/JARVIS_CHRONICLES.md",
        "README.md"
    ]
    
    missing_docs = []
    for doc in docs_to_check:
        doc_path = root_dir / doc
        if doc_path.exists():
            print(f"  [OK] Đã tìm thấy {doc} ({doc_path.stat().st_size} bytes)")
        else:
            print(f"  [MISSING] Không tìm thấy {doc}")
            missing_docs.append(doc)
            
    # 3. Đưa ra đề xuất (Simulation)
    print("\n[3] Đề xuất cập nhật (Mô phỏng LLM Analysis)...")
    if "tools/system/sync_docs.py" not in open(root_dir / "context/ROADMAP.md", encoding="utf-8").read():
        print("  [CẢNH BÁO] ROADMAP.md có thể chưa cập nhật tiến độ công cụ sync_docs.py!")
    else:
        print("  [OK] ROADMAP.md đã ghi nhận tiến độ sync_docs.py.")
        
    print("\n💡 HƯỚNG DẪN:")
    print("Đây là công cụ GCLI hỗ trợ Dev tự động đánh giá Documentation Debt.")
    print("Trong các bản cập nhật tới, công cụ này sẽ tích hợp BaseAgent (LLM) để:")
    print("  1. Đọc git diff của các commit gần nhất.")
    print("  2. Tự động sinh file JSON chứa bản thảo markdown cần thay đổi.")
    print("  3. Yêu cầu Admin xác nhận (Y/n) trước khi ghi đè vào file .md gốc.")

if __name__ == "__main__":
    main()
