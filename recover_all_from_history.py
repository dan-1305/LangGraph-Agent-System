import os
import shutil
import urllib.parse
import json
import sys
import io
from pathlib import Path

# Fix encoding issue for Windows console
if hasattr(sys.stdout, 'buffer'):
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def recover_all_files():
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
        
    current_workspace = Path("c:/Users/Admin/Desktop/WorkSpace/Project/LangGraph_Agent_System").resolve()
    print(f"Workspace hiện tại: {current_workspace}")
    print(f"Đang quét thư mục Local History: {target_history_dir}")
    
    found_files = {} # Dict map từ path đích -> (file nguồn backup, timestamp)
    
    # Duyệt qua tất cả các folder hash trong History
    all_hash_dirs = list(target_history_dir.iterdir())
    total_dirs = len(all_hash_dirs)
    print(f"Tìm thấy {total_dirs} thư mục history.")

    for i, hash_dir in enumerate(all_hash_dirs):
        if not hash_dir.is_dir():
            continue
            
        if i % 500 == 0:
            print(f"Đang xử lý: {i}/{total_dirs}...")

        entries_file = hash_dir / "entries.json"
        if not entries_file.exists():
            continue
            
        try:
            with open(entries_file, "r", encoding="utf-8") as f:
                entries_data = json.load(f)
                
            resource = entries_data.get("resource", "")
            if not resource:
                continue
                
            try:
                parsed_resource = urllib.parse.unquote(resource)
                # Xử lý format file:///c%3A/... hoặc file:///C:/...
                if parsed_resource.startswith('file:///'):
                    parsed_resource = parsed_resource[8:]
                elif parsed_resource.startswith('file://'):
                    parsed_resource = parsed_resource[7:]
                
                # Chuẩn hóa path để so sánh
                norm_resource = Path(parsed_resource).resolve()
            except Exception:
                continue
            
            # Chỉ khôi phục các file thuộc workspace hiện tại
            if current_workspace in norm_resource.parents or norm_resource == current_workspace:
                entries = entries_data.get("entries", [])
                if not entries:
                    continue
                
                # Lấy entry mới nhất
                latest_entry = max(entries, key=lambda x: x.get("timestamp", 0))
                entry_id = latest_entry.get("id")
                timestamp = latest_entry.get("timestamp", 0)
                file_src = hash_dir / entry_id
                
                if file_src.exists():
                    # Nếu file này đã có trong found_files, chỉ lấy cái mới hơn
                    if norm_resource not in found_files or timestamp > found_files[norm_resource][1]:
                        found_files[norm_resource] = (file_src, timestamp)
        except Exception:
            continue

    print(f"\nTìm thấy {len(found_files)} file trong History thuộc về Workspace này.")
    
    count = 0
    for dest_path, (src_file, timestamp) in found_files.items():
        try:
            # Đảm bảo thư mục cha tồn tại
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file từ history vào workspace (ghi đè)
            shutil.copy2(src_file, dest_path)
            # print(f"[+] Khôi phục: {dest_path}")
            count += 1
        except Exception as e:
            print(f"[-] Lỗi khôi phục {dest_path}: {e}")

    print(f"\nHOÀN TẤT: Đã khôi phục và ghi đè {count} files từ VS Code History.")

if __name__ == "__main__":
    recover_all_files()
