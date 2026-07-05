import os
import sys
import io
import ast
from pathlib import Path

# Force UTF-8 for Windows Console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_system_map(root_dirs=["src", "projects", "core", "scheduler", "tools"]):
    base_dir = Path(__file__).resolve().parent.parent.parent
    output_lines = [
        "# 🗺️ BẢN ĐỒ HỆ THỐNG VÀ CHỨC NĂNG (SYSTEM MAP - AUTO GENERATED)",
        "\nĐây là Bản đồ định vị toàn bộ cấu trúc dự án. Được tạo tự động thông qua quét AST (Abstract Syntax Tree). Hệ thống RAG dùng file này để định vị vị trí các hàm và chức năng.\n",
        "---"
    ]
    
    for directory in root_dirs:
        dir_path = base_dir / directory
        if not dir_path.exists():
            continue
            
        output_lines.append(f"\n## THƯ MỤC: `{directory}/`")
        
        for root, dirs, files in os.walk(dir_path):
            # Strict Blacklist filtering for RAG mapping
            blacklist_dirs = {
                '.venv', 'venv', 'env', 'node_modules', 
                '__pycache__', '.pytest_cache', '.git', '.vscode', '.idea',
                'dist', 'build', 'langgraph_agent_system.egg-info'
            }
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in blacklist_dirs]
            
            py_files = [f for f in files if f.endswith(".py") and not f.startswith('.')]
            if not py_files:
                continue
                
            rel_root = Path(root).relative_to(base_dir)
            
            for file in py_files:
                file_path = os.path.join(root, file)
                rel_path = f"{rel_root}/{file}".replace("\\", "/")
                
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        
                    parsed_ast = ast.parse(file_content, filename=file)
                    
                    file_docstring = ast.get_docstring(parsed_ast)
                    file_desc = file_docstring.split("\n")[0] if file_docstring else "Không có mô tả."
                    
                    output_lines.append(f"\n### 📄 File: `{rel_path}`")
                    output_lines.append(f"- **Mô tả File:** {file_desc}")
                    
                    functions = []
                    classes = []
                    
                    for node in parsed_ast.body:
                        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                            doc = ast.get_docstring(node)
                            desc = doc.split("\n")[0] if doc else ""
                            functions.append((node.name, desc))
                            
                        elif isinstance(node, ast.ClassDef):
                            doc = ast.get_docstring(node)
                            desc = doc.split("\n")[0] if doc else ""
                            classes.append((node.name, desc))
                            
                            # Quét method trong class
                            for child in node.body:
                                if isinstance(child, ast.FunctionDef) or isinstance(child, ast.AsyncFunctionDef):
                                    m_doc = ast.get_docstring(child)
                                    m_desc = m_doc.split("\n")[0] if m_doc else ""
                                    functions.append((f"{node.name}.{child.name}", m_desc))
                                    
                    if classes:
                        output_lines.append("\n**Các Lớp (Classes):**")
                        for c_name, c_desc in classes:
                            desc_str = f": {c_desc}" if c_desc else ""
                            output_lines.append(f"- `{c_name}`{desc_str}")
                            
                    if functions:
                        output_lines.append("\n**Các Hàm (Functions/Methods):**")
                        for f_name, f_desc in functions:
                            desc_str = f": {f_desc}" if f_desc else ""
                            output_lines.append(f"- `{f_name}()`{desc_str}")
                            
                except Exception as e:
                    output_lines.append(f"\n### 📄 File: `{rel_path}`")
                    output_lines.append(f"- Lỗi phân tích AST: {str(e)}")

    output_path = base_dir / "docs" / "SYSTEM_MAP.md"
    os.makedirs(output_path.parent, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
        
    print(f"✅ Đã tạo thành công {output_path} với {len(output_lines)} dòng!")

if __name__ == "__main__":
    generate_system_map()
