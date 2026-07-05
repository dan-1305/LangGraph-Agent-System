import os
import re
import ast
import json
import sys
import io
from pathlib import Path

if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
def extract_env_keys(env_path: Path):
    """Đọc file .env và trả về danh sách các biến được định nghĩa (không chứa giá trị)."""
    keys = []
    if not env_path.exists():
        return keys
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                match = re.match(r'^([A-Za-z_][A-Za-z0-9_]*)=', line)
                if match:
                    keys.append(match.group(1))
    return keys

def scan_file_for_env_usage(file_path: Path, env_keys: list):
    """Dùng AST để quét file Python xem có gọi os.getenv('KEY') hay không."""
    found_keys = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=str(file_path))
            
        for node in ast.walk(tree):
            # Tìm kiếm os.getenv("KEY") hoặc os.environ.get("KEY")
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr in ('getenv', 'get'):
                    if node.args and isinstance(node.args[0], ast.Constant):
                        val = node.args[0].value
                        if val in env_keys:
                            found_keys.add(val)
                elif isinstance(node.func, ast.Name) and node.func.id == 'getenv':
                    if node.args and isinstance(node.args[0], ast.Constant):
                        val = node.args[0].value
                        if val in env_keys:
                            found_keys.add(val)
            # Tìm kiếm os.environ["KEY"]
            elif isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Attribute) and node.value.attr == 'environ':
                    if isinstance(node.slice, ast.Constant):
                        val = node.slice.value
                        if val in env_keys:
                            found_keys.add(val)
    except Exception as e:
        # File không phải là python hợp lệ hoặc không parse được
        pass
    return list(found_keys)

def main():
    root_dir = Path(__file__).resolve().parent.parent.parent
    env_path = root_dir / '.env'
    output_path = root_dir / 'config' / 'api_registry.json'
    
    # Đảm bảo thư mục config tồn tại
    output_path.parent.mkdir(exist_ok=True)
    
    env_keys = extract_env_keys(env_path)
    if not env_keys:
        print("Không tìm thấy keys nào trong .env")
        return
        
    registry = {key: [] for key in env_keys}
    
    print(f"Đang quét {len(env_keys)} keys trong source code...")
    
    # Quét toàn bộ thư mục src và projects
    search_dirs = [root_dir / 'src', root_dir / 'projects']
    
    for s_dir in search_dirs:
        if not s_dir.exists():
            continue
        for py_file in s_dir.rglob('*.py'):
            # Bỏ qua các file trong .venv, node_modules...
            if '.venv' in py_file.parts or 'node_modules' in py_file.parts:
                continue
                
            used_keys = scan_file_for_env_usage(py_file, env_keys)
            for key in used_keys:
                rel_path = py_file.relative_to(root_dir).as_posix()
                if rel_path not in registry[key]:
                    registry[key].append(rel_path)
                    
    # Lọc bỏ các keys không được sử dụng
    registry = {k: v for k, v in registry.items() if v}
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=4, ensure_ascii=False)
        
    print(f"✅ Đã tạo mapping API Keys thành công tại: {output_path.relative_to(root_dir)}")

if __name__ == "__main__":
    main()