import os
import ast
import json
import time
import functools
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from typing import List, Dict, Any
from collections import defaultdict

def get_target_directories() -> List[Path]:
    root = Path(__file__).resolve().parent.parent.parent
    return [
        root / "src",
        root / "core",
        root / "core_utilities",
        root / "projects"
    ]

def scan_python_files(directories: List[Path]) -> List[Path]:
    py_files = []
    for d in directories:
        if d.exists():
            for filepath in d.rglob("*.py"):
                # Bỏ qua các thư mục không cần thiết
                if ".venv" in filepath.parts or "__pycache__" in filepath.parts or "temp_workspace" in filepath.parts:
                    continue
                py_files.append(filepath)
    return py_files

def parse_file(filepath: Path) -> List[Dict[str, Any]]:
    functions = []
    try:
        content = filepath.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(filepath))
    except Exception as e:
        print(f"Lỗi parse {filepath}: {e}")
        return functions

    # Tìm các hàm cấp cao nhất (module level)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            functions.append({
                "type": "function",
                "name": node.name,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "args": [arg.arg for arg in node.args.args],
                "docstring": ast.get_docstring(node) or "",
                "file": str(filepath.relative_to(filepath.parents[3] if len(filepath.parts) > 3 else filepath.parent)),
                "line": node.lineno
            })
        elif isinstance(node, ast.ClassDef):
            for class_node in ast.iter_child_nodes(node):
                if isinstance(class_node, ast.FunctionDef) or isinstance(class_node, ast.AsyncFunctionDef):
                    functions.append({
                        "type": "method",
                        "class": node.name,
                        "name": class_node.name,
                        "is_async": isinstance(class_node, ast.AsyncFunctionDef),
                        "args": [arg.arg for arg in class_node.args.args],
                        "docstring": ast.get_docstring(class_node) or "",
                        "file": str(filepath.relative_to(filepath.parents[3] if len(filepath.parts) > 3 else filepath.parent)),
                        "line": class_node.lineno
                    })
    return functions

def generate_registry(functions: List[Dict[str, Any]], root_dir: Path):
    registry_path = root_dir / "docs" / "GLOBAL_FUNCTION_REGISTRY.md"
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Group by file
    grouped = defaultdict(list)
    for f in functions:
        grouped[f["file"]].append(f)
        
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write("# 📚 GLOBAL FUNCTION REGISTRY\n\n")
        f.write("> **Bách khoa toàn thư API Nội bộ.** Tự động tạo bởi `global_function_auditor.py`.\n\n")
        f.write(f"Tổng số hàm/phương thức: **{len(functions)}**\n\n")
        
        # Danh sách trùng lặp
        name_counts = defaultdict(list)
        for func in functions:
            name_counts[func["name"]].append(func["file"])
        
        duplicates = {k: v for k, v in name_counts.items() if len(v) > 1 and not k.startswith("__")}
        
        if duplicates:
            f.write("## ⚠️ CÁC HÀM CÓ THỂ BỊ TRÙNG LẶP (DUPLICATES)\n")
            f.write("Cần xem xét gộp chung hoặc refactor:\n")
            for name, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)[:20]:
                f.write(f"- `{name}` xuất hiện trong {len(files)} files: {', '.join(set(files))}\n")
            f.write("\n---\n\n")
            
        for filepath, funcs in sorted(grouped.items()):
            f.write(f"## 📁 `{filepath}`\n")
            for func in sorted(funcs, key=lambda x: x["name"]):
                type_prefix = f"**{func['class']}**." if func.get("class") else ""
                async_prefix = "async " if func.get("is_async") else ""
                f.write(f"### ⚡ `{async_prefix}{type_prefix}{func['name']}({', '.join(func['args'])})`\n")
                if func['docstring']:
                    doc = func['docstring'].replace('\n', ' ')
                    if len(doc) > 150: doc = doc[:150] + "..."
                    f.write(f"- *Mô tả:* {doc}\n")
                f.write(f"- *Dòng:* {func['line']}\n\n")

    print(f"✅ Đã tạo GLOBAL_FUNCTION_REGISTRY.md tại {registry_path}")
    return duplicates

# --- PERFORMANCE PROFILING ---
def performance_profiler(func):
    """
    Decorator dùng để đo thời gian, mem (giả lập) của 1 hàm bất kỳ.
    Sử dụng: @performance_profiler
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        # Tracing memory requires tracemalloc, keeping simple here
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = (end_time - start_time) * 1000  # ms
        
        log_msg = f"[PROFILER] {func.__name__} took {elapsed:.2f} ms"
        print(log_msg)
        
        # Ghi log ra file
        log_file = Path(__file__).resolve().parent.parent.parent / "reports" / "FUNCTION_PERFORMANCE_AUDIT.md"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"- `{func.__name__}`: **{elapsed:.2f} ms**\n")
            
        return result
    return wrapper

def main():
    root = Path(__file__).resolve().parent.parent.parent
    dirs = get_target_directories()
    files = scan_python_files(dirs)
    
    print(f"🔍 Đang quét {len(files)} file Python...")
    all_functions = []
    for f in files:
        funcs = parse_file(f)
        all_functions.extend(funcs)
        
    print(f"📊 Tìm thấy tổng cộng {len(all_functions)} hàm/phương thức.")
    duplicates = generate_registry(all_functions, root)
    
    # Tạo report cơ bản
    report_path = root / "reports" / "FUNCTION_PERFORMANCE_AUDIT.md"
    if not report_path.exists():
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# ⏱️ FUNCTION PERFORMANCE AUDIT\n\n")
            f.write("Báo cáo đo đạc hiệu năng của các hàm cốt lõi.\n\n")
    
if __name__ == "__main__":
    main()
