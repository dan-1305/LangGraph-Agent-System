import os
import ast
from collections import defaultdict

def audit_workspace(root_dir="."):
    blacklist_dirs = {
        '.venv', 'venv', 'env', 'node_modules', 
        '__pycache__', '.pytest_cache', '.ruff_cache', '.git', '.github', '.idea',
        'dist', 'build', 'langgraph_agent_system.egg-info', '_archive_old_files', 'archives'
    }

    misplaced_files = []

    for root, dirs, files in os.walk(root_dir):
        # Apply blacklist
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in blacklist_dirs]
        rel_root = os.path.relpath(root, root_dir)
        
        for file in files:
            if not file.endswith('.py'):
                continue
                
            filepath = os.path.join(root, file)
            rel_filepath = os.path.relpath(filepath, root_dir).replace("\\", "/")
            
            # 1. Test Leakage
            if file.startswith('test_') and not rel_root.startswith('tests'):
                misplaced_files.append({
                    "file": rel_filepath,
                    "target": f"tests/{rel_filepath.replace('src/', '').replace('projects/', '')}",
                    "reason": "Test Leakage: File test đang nằm ngoài thư mục `tests/`."
                })
                continue

            # 2. Domain Leakage in tools/
            if rel_root == "tools" or rel_root == ".":
                # Detect specific keywords in filename
                name_lower = file.lower()
                if "godot" in name_lower or "translation" in name_lower or "translate" in name_lower:
                    misplaced_files.append({
                        "file": rel_filepath,
                        "target": f"projects/godot_translator/{file}",
                        "reason": "Domain Leakage: Script dịch thuật game nên nằm trong project tương ứng, không phải ở root hoặc tools chung."
                    })
                elif "comfy" in name_lower or "image" in name_lower:
                    misplaced_files.append({
                        "file": rel_filepath,
                        "target": f"tools/comfy/{file}",
                        "reason": "Domain Leakage: Script xử lý ảnh/ComfyUI nên phân nhóm vào thư mục con."
                    })
                elif "worldcard" in name_lower:
                    misplaced_files.append({
                        "file": rel_filepath,
                        "target": f"projects/sillytavern_world_card_generator/{file}",
                        "reason": "Domain Leakage: Script tạo WorldCard nên nằm trong project SillyTavern."
                    })
                elif "csv" in name_lower or "pipeline" in name_lower:
                     misplaced_files.append({
                        "file": rel_filepath,
                        "target": f"tools/data_processing/{file}",
                        "reason": "Domain Leakage: Các script convert/xử lý data nên gom vào một thư mục data_processing riêng."
                    })

            # 3. Tier Violation Analysis (Very basic AST check)
            if 'src/factory' in rel_filepath or 'src/base' in rel_filepath:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read())
                        has_infra_imports = False
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    if alias.name in ['requests', 'sqlalchemy', 'psycopg2', 'sqlite3']:
                                        has_infra_imports = True
                            elif isinstance(node, ast.ImportFrom):
                                if node.module in ['requests', 'sqlalchemy', 'psycopg2', 'sqlite3']:
                                    has_infra_imports = True
                        
                        if has_infra_imports and "state.py" in file:
                            misplaced_files.append({
                                "file": rel_filepath,
                                "target": "Tách code gọi DB ra thư mục `src/infra/`",
                                "reason": "Tier Violation: File định nghĩa State/Entities (Tier 1) không được chứa logic gọi Database/Network (Tier 3)."
                            })
                except:
                    pass

    # Generate Report
    report_lines = [
        "# ARCHITECTURE AUDIT REPORT",
        "> Quét tự động cấu trúc thư mục để phát hiện các file vi phạm kiến trúc 4-Tier và Domain-Driven Design.",
        "\n## Danh sách các file đặt sai vị trí (Misplaced Files)\n"
    ]

    if not misplaced_files:
        report_lines.append("🎉 Tuyệt vời! Không phát hiện file nào vi phạm quy tắc.")
    else:
        for idx, item in enumerate(misplaced_files, 1):
            report_lines.append(f"### {idx}. {item['file']}")
            report_lines.append(f"- **Vị trí đề xuất chuyển đến:** `{item['target']}`")
            report_lines.append(f"- **Lý do:** {item['reason']}\n")

    with open("ARCHITECTURE_AUDIT_REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

if __name__ == "__main__":
    audit_workspace()
