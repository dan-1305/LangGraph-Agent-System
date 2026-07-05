import os
import sys
from pathlib import Path

# Fix for windows encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_docs_report():
    root_dir = Path(__file__).resolve().parent.parent.parent
    report_path = root_dir / "reports" / "DOC_DEBATE_ANALYSIS.md"
    
    # Đảm bảo thư mục tồn tại
    os.makedirs(report_path.parent, exist_ok=True)
    
    # Các thư mục cần quét file md
    target_dirs = [root_dir, root_dir / "docs", root_dir / "context"]
    
    with open(report_path, "w", encoding="utf-8") as out_f:
        out_f.write("# 📑 DOCUMENTATION DEBATE ANALYSIS (AUTO-GENERATED)\n\n")
        out_f.write("*Báo cáo rà soát nhanh các file .md trong hệ thống để tìm file lỗi thời.*\n\n")
        
        for d in target_dirs:
            if not d.exists():
                continue
            
            out_f.write(f"## 📂 Thư mục: `{d.relative_to(root_dir) if d != root_dir else '/'}`\n\n")
            
            for file_path in d.iterdir():
                if file_path.is_file() and file_path.name.endswith(".md"):
                    # Đọc 10 dòng đầu tiên
                    try:
                        with open(file_path, "r", encoding="utf-8") as in_f:
                            lines = [in_f.readline().strip() for _ in range(10)]
                    except Exception as e:
                        lines = [f"Lỗi đọc file: {e}"]
                        
                    snippet = "\n".join(filter(None, lines))
                    
                    out_f.write(f"### 📄 `{file_path.name}`\n")
                    out_f.write(f"- **Kích thước:** {file_path.stat().st_size} bytes\n")
                    out_f.write("- **Snippet 10 dòng đầu:**\n```markdown\n")
                    out_f.write(snippet)
                    out_f.write("\n```\n\n")

if __name__ == "__main__":
    generate_docs_report()
    print("Đã tạo báo cáo tại reports/DOC_DEBATE_ANALYSIS.md")