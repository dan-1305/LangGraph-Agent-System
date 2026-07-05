import os
import glob
from pathlib import Path
import sys

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def fix_sys_stdout_buffer(root_dir="."):
    """
    Quét và sửa lỗi `sys.stdout = io.TextIOWrapper(...)` gây lỗi buffer detached cho Pytest.
    Dùng string replace thay vì regex.
    """
    root_path = Path(root_dir)
    py_files = root_path.rglob("*.py")
    
    fixed_count = 0
    
    target_1 = "sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')"
    target_2 = 'sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")'
    target_3 = "sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')"
    target_4 = 'sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")'
    
    safe_1 = "if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules: sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')"
    safe_3 = "if hasattr(sys.stderr, 'buffer') and 'pytest' not in sys.modules: sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')"
    
    # Sửa mấy cái đã sửa nửa vời:
    target_bad_1 = "if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:\n    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:"
    target_bad_2 = "if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:\n    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')"
    
    for fpath in py_files:
        if 'site-packages' in fpath.parts or '.venv' in fpath.parts:
            continue
            
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
            
        original_content = content
        
        # Sửa file nửa vời về gốc
        if target_bad_1 in content:
            content = content.replace(target_bad_1, "if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:")
            
        # Nếu chưa an toàn thì thay thế
        if target_1 in content and "if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:" not in content:
            content = content.replace(target_1, safe_1)
        if target_2 in content and "if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:" not in content:
            content = content.replace(target_2, safe_1)
            
        if target_3 in content and "if hasattr(sys.stderr, 'buffer') and 'pytest' not in sys.modules:" not in content:
            content = content.replace(target_3, safe_3)
        if target_4 in content and "if hasattr(sys.stderr, 'buffer') and 'pytest' not in sys.modules:" not in content:
            content = content.replace(target_4, safe_3)
            
        if content != original_content:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_count += 1
            print(f"🔧 Fixed Pytest Buffer issue in: {fpath}")
            
    print(f"\n✅ Đã hoàn tất sửa lỗi Pytest Buffer trên {fixed_count} files.")

if __name__ == "__main__":
    fix_sys_stdout_buffer()
