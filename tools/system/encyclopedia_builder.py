import os
import sys
import ast
import time
from pathlib import Path

def build_encyclopedia():
    base_dir = Path(__file__).resolve().parent.parent.parent
    encyclopedia_path = base_dir / "docs" / "ERROR_ENCYCLOPEDIA.md"
    
    start_time = time.time()
    
    # 1. Read existing manual content
    manual_content = ""
    marker_start = "<!-- AUTO-GENERATED-SECTION-START -->"
    marker_end = "<!-- AUTO-GENERATED-SECTION-END -->"
    
    if encyclopedia_path.exists():
        with open(encyclopedia_path, "r", encoding="utf-8") as f:
            content = f.read()
            if marker_start in content:
                manual_content = content.split(marker_start)[0].strip()
            else:
                manual_content = content.strip()
    else:
        manual_content = "# 📚 BÁCH KHOA TOÀN THƯ HỆ THỐNG (SYSTEM ENCYCLOPEDIA)\n\nĐây là Knowledge Base lưu trữ toàn bộ Lỗi, Luật lệ (Rules) và Cấu trúc Logic Code của toàn bộ Monorepo.\n"
        
    # 2. Extract .clinerules
    rules_section = ["\n## 📜 PHẦN 2: QUY TẮC DỰ ÁN (.clinerules)"]
    
    # Root rules
    root_rule = base_dir / ".clinerules"
    if root_rule.exists():
        rules_section.append("\n### 📍 ROOT PROJECT (.clinerules)")
        with open(root_rule, "r", encoding="utf-8") as f:
            rules_section.append(f.read().strip())
            
    # Subproject rules
    projects_dir = base_dir / "projects"
    if projects_dir.exists():
        for proj in os.listdir(projects_dir):
            proj_path = projects_dir / proj
            if proj_path.is_dir():
                rule_file = proj_path / ".clinerules"
                if rule_file.exists():
                    rules_section.append(f"\n### 📍 PROJECT: {proj}")
                    with open(rule_file, "r", encoding="utf-8") as f:
                        rules_section.append(f.read().strip())
                        
    # 3. Extract AST (System Map & Code Logic)
    logic_section = ["\n## 🧠 PHẦN 3: BẢN ĐỒ LOGIC VÀ CẤU TRÚC (SYSTEM MAP)"]
    root_dirs = ["src", "projects", "core", "scheduler", "tools"]
    
    for directory in root_dirs:
        dir_path = base_dir / directory
        if not dir_path.exists(): continue
            
        logic_section.append(f"\n### 📂 THƯ MỤC: `{directory}/`")
        
        for root, dirs, files in os.walk(dir_path):
            blacklist = {'.venv', 'venv', 'env', 'node_modules', '__pycache__', '.pytest_cache', '.git'}
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in blacklist]
            
            py_files = [f for f in files if f.endswith(".py") and not f.startswith('.')]
            if not py_files: continue
                
            rel_root = Path(root).relative_to(base_dir)
            
            for file in py_files:
                file_path = os.path.join(root, file)
                rel_path = f"{rel_root}/{file}".replace("\\", "/")
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        
                    parsed_ast = ast.parse(file_content, filename=file)
                    file_doc = ast.get_docstring(parsed_ast)
                    file_desc = file_doc.split("\n")[0] if file_doc else "Không có mô tả."
                    
                    logic_section.append(f"\n#### 📄 `{rel_path}` - {file_desc}")
                    
                    for node in parsed_ast.body:
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            doc = ast.get_docstring(node)
                            desc = doc.split("\n")[0] if doc else ""
                            logic_section.append(f"  - `Hàm` **{node.name}()**: {desc}")
                        elif isinstance(node, ast.ClassDef):
                            doc = ast.get_docstring(node)
                            desc = doc.split("\n")[0] if doc else ""
                            logic_section.append(f"  - `Lớp` **{node.name}**: {desc}")
                            for child in node.body:
                                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                    mdoc = ast.get_docstring(child)
                                    mdesc = mdoc.split("\n")[0] if mdoc else ""
                                    logic_section.append(f"    - `Method` {child.name}(): {mdesc}")
                                    
                except Exception as e:
                    logic_section.append(f"\n#### 📄 `{rel_path}` - [LỖI AST: {e}]")
                    
    # Combine everything
    final_content = manual_content + f"\n\n{marker_start}\n"
    final_content += "> ⚠️ PHẦN DƯỚI ĐÂY ĐƯỢC TẠO TỰ ĐỘNG BỞI `encyclopedia_builder.py`. KHÔNG SỬA THỦ CÔNG!\n"
    final_content += "\n".join(rules_section)
    final_content += "\n" + "\n".join(logic_section)
    final_content += f"\n{marker_end}\n"
    
    with open(encyclopedia_path, "w", encoding="utf-8") as f:
        f.write(final_content)
        
    duration = time.time() - start_time
    try:
        print(f"✅ [Encyclopedia] Đã tự động cập nhật Bách khoa toàn thư trong {duration:.3f}s!")
    except UnicodeEncodeError:
        print(f"[Encyclopedia] Da tu dong cap nhat Bach khoa toan thu trong {duration:.3f}s!")

if __name__ == "__main__":
    build_encyclopedia()
