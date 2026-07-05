import os
import shutil
import urllib.parse
from pathlib import Path

def get_zero_byte_py_files(workspace_dir: Path):
    """Lấy danh sách tất cả các file .py có dung lượng 0 byte trong workspace."""
    zero_byte_files = []
    for dp, dn, fn in os.walk(workspace_dir):
        # Bỏ qua các thư mục không cần thiết
        if '.venv' in dp or '.git' in dp or '__pycache__' in dp:
            continue
        for f in fn:
            if f.endswith('.py'):
                full_path = Path(dp) / f
                if full_path.exists() and os.path.getsize(full_path) == 0:
                    zero_byte_files.append(full_path)
    return zero_byte_files

import sys
import io

if hasattr(sys.stdout, 'buffer'):
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def recover_files():
    appdata = os.environ.get('APPDATA')
    if not appdata:
        print("Không tìm thấy biến môi trường APPDATA")
        return
        
    history_dirs = [
        Path(appdata) / "Code" / "User" / "History",
        Path(appdata) / "Code - Insiders" / "User" / "History"
    ]
    
    target_history_dir = None
    for d in history_dirs:
        if d.exists():
            target_history_dir = d
            break
            
    if not target_history_dir:
        print("Không tìm thấy thư mục History của VS Code")
        return
        
    current_workspace = Path(__file__).resolve().parent
    zero_byte_files = get_zero_byte_py_files(current_workspace)
    
    if not zero_byte_files:
        print("[OK] Tuyệt vời! Không tìm thấy file .py nào bị 0 byte. Hệ thống an toàn.")
        return
        
    print(f"[!] Phát hiện {len(zero_byte_files)} file .py bị xóa trắng (0 byte)!")
    print(f"Đang quét thư mục Local History: {target_history_dir}")
    
    found_files = {} # Dict map từ path đích -> file nguồn backup
    
    # Tạo set các đường dẫn cần khôi phục (chuẩn hóa thành chuỗi unix path)
    target_paths = {str(p).replace('\\', '/') for p in zero_byte_files}
    
    for hash_dir in target_history_dir.iterdir():
        if not hash_dir.is_dir():
            continue
            
        entries_file = hash_dir / "entries.json"
        if not entries_file.exists():
            continue
            
        try:
            import json
            with open(entries_file, "r", encoding="utf-8") as f:
                entries_data = json.load(f)
                
            resource = entries_data.get("resource", "")
            try:
                parsed_resource = urllib.parse.unquote(resource)
            except Exception:
                continue
                
            matched_dest = None
            for p in zero_byte_files:
                # Chuyển đổi p (Path) thành absolute path
                abs_path = str(p.resolve()).replace('\\', '/').lower()
                parsed_res_lower = parsed_resource.lower()
                res_lower = resource.lower()
                if abs_path in parsed_res_lower or abs_path.replace('c:', 'c%3a') in res_lower:
                    matched_dest = p
                    break
            
            if matched_dest:
                entries = entries_data.get("entries", [])
                if not entries:
                    continue
                    
                entries.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
                
                for entry in entries:
                    entry_id = entry.get("id")
                    file_path = hash_dir / entry_id
                    
                    if file_path.exists() and os.path.getsize(file_path) > 0:
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            if len(content.strip()) > 0: 
                                if matched_dest not in found_files:
                                    found_files[matched_dest] = file_path
                                    print(f"[*] Tìm thấy bản backup cho: {matched_dest.relative_to(current_workspace)}")
                                break
                        except Exception:
                            pass
        except Exception as e:
            pass

    print(f"\nTổng cộng khôi phục thành công {len(found_files)} / {len(zero_byte_files)} files.")
    
    for dest_path, src_file in found_files.items():
        try:
            shutil.copy(src_file, dest_path)
            print(f"[+] Đã khôi phục: {dest_path}")
        except Exception as e:
            print(f"[-] Lỗi copy {dest_path}: {e}")

if __name__ == "__main__":
    recover_files()
