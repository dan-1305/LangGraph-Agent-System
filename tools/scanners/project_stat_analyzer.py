import os
from collections import defaultdict
from datetime import datetime

def analyze_project(root_dir="."):
    total_dirs = 0
    total_files = 0
    ext_counts = defaultdict(int)
    dir_list = []
    
    # Criticality heuristics rules
    critical_dirs = ['src', 'core', 'core_engine', 'tools', 'projects', 'docs', 'context']
    medium_dirs = ['tests', 'config', 'scheduler', 'reports']
    low_dirs = ['logs', 'archives', '_archive_old_files', 'assets', 'images_output']

    # Strict blacklist for virtual environments and external packages
    blacklist_dirs = {
        '.venv', 'venv', 'env', 'node_modules', 
        '__pycache__', '.pytest_cache', '.git', '.vscode', '.idea',
        'dist', 'build', 'langgraph_agent_system.egg-info'
    }

    for root, dirs, files in os.walk(root_dir):
        # Exclude blacklisted dirs and hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in blacklist_dirs]
        
        rel_path = os.path.relpath(root, root_dir)
        if rel_path != ".":
            total_dirs += 1
            dir_list.append(rel_path)

        for file in files:
            # Skip hidden files
            if file.startswith('.'):
                continue
            
            total_files += 1
            ext = os.path.splitext(file)[1].lower()
            if not ext:
                ext = 'no_extension'
            ext_counts[ext] += 1

    # Sorting extensions by count descending
    sorted_exts = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)

    # Generate Markdown Report
    report_lines = []
    report_lines.append(f"# BÁO CÁO THỐNG KÊ VÀ ĐÁNH GIÁ TRỌNG YẾU DỰ ÁN")
    report_lines.append(f"*(Ngày tạo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})*\n")
    
    report_lines.append(f"## 1. Tổng quan")
    report_lines.append(f"- **Tổng số thư mục (loại trừ .hidden và __pycache__):** {total_dirs}")
    report_lines.append(f"- **Tổng số tệp tin:** {total_files}")
    report_lines.append(f"")
    
    report_lines.append(f"## 2. Thống kê theo loại tệp tin (Đuôi file)")
    report_lines.append(f"| Đuôi file | Số lượng | Tỷ lệ (%) | Mức độ trọng yếu (Ước tính) |")
    report_lines.append(f"| :--- | :--- | :--- | :--- |")
    
    for ext, count in sorted_exts:
        pct = (count / total_files) * 100
        # Criticality logic based on extension
        criticality = "Thấp"
        if ext in ['.py', '.toml', '.lock', '.json']:
            criticality = "🔴 Cao (Core Logic/Config)"
        elif ext in ['.md', '.bat', '.sh', '.yml', '.yaml']:
            criticality = "🟡 Trung bình (Docs/Scripts/Ops)"
        elif ext in ['.txt', '.csv', '.zip', '.bak', '.log', '.db', '.sqlite']:
            criticality = "🟢 Thấp (Data/Logs/Archive)"
            
        report_lines.append(f"| `{ext}` | {count} | {pct:.1f}% | {criticality} |")
    
    report_lines.append(f"\n## 3. Phân tích độ trọng yếu theo cấu trúc thư mục")
    report_lines.append(f"Hệ thống LangGraph_Agent_System là một kiến trúc đa tầng (Polymorphic Agent System). Độ trọng yếu được đánh giá như sau:\n")
    
    report_lines.append(f"### 🔴 TIER 1 & TIER 2: Vùng Trọng Yếu Cao Nhất (Core & Application Logic)")
    report_lines.append(f"Đây là bộ não và bộ xương của hệ thống. Bất kỳ thay đổi nào cũng có thể làm sập toàn bộ các Agent.")
    report_lines.append(f"- `src/` (Đặc biệt là `src/factory/`, `src/base_agent.py`): Khung xương của kiến trúc LangGraph V2. Quản lý trạng thái, node, router.")
    report_lines.append(f"- `projects/`: Chứa các Agent độc lập (AI Trading, Airdrop, Chaos QA). Mỗi folder đại diện cho một Domain cụ thể với Domain Rules riêng.")
    report_lines.append(f"- `core/` & `core_engine/`: Các module tiện ích cốt lõi dùng chung.")
    
    report_lines.append(f"\n### 🟡 TIER 3: Vùng Trọng Yếu Trung Bình (Infrastructure & Tooling)")
    report_lines.append(f"Tầng giao tiếp và công cụ hỗ trợ. Lỗi ở đây thường chỉ ảnh hưởng cục bộ (ví dụ: hỏng một tool quét) chứ không sập core.")
    report_lines.append(f"- `tools/`: Chứa hàng loạt script tự động hóa (scanner, RAG query, auto mapper...).")
    report_lines.append(f"- `docs/` & `context/`: Lưu trữ Bách khoa toàn thư, luật lệ, và bản đồ hệ thống cho RAG.")
    report_lines.append(f"- `scheduler/`: Hệ thống lập lịch chạy tự động.")
    report_lines.append(f"- `tests/`: Bộ Unit test bảo vệ hệ thống.")

    report_lines.append(f"\n### 🟢 TIER 4: Vùng Trọng Yếu Thấp (Ephemeral / Data)")
    report_lines.append(f"Vùng đệm, lưu trữ kết quả, log hoặc rác. Xóa đi hệ thống vẫn khởi động bình thường.")
    report_lines.append(f"- `logs/`, `reports/`: Nhật ký và báo cáo đầu ra.")
    report_lines.append(f"- `archives/`, `_archive_old_files/`: Nơi chứa file cũ, file backup.")
    report_lines.append(f"- Các thư mục sinh data tạm thời như `images_output/`.\n")
    
    report_lines.append(f"---\n*Báo cáo được tự động tạo bởi `tools/scanners/project_stat_analyzer.py`*")

    os.makedirs('reports', exist_ok=True)
    report_path = 'reports/PROJECT_STATISTICS_REPORT.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
        
    print(f"[SUCCESS] Da phan tich {total_files} file trong {total_dirs} thu muc.")
    print(f"Bao cao da duoc luu tai: {report_path}")

if __name__ == "__main__":
    analyze_project()
