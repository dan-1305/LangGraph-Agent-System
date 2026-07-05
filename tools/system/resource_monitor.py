import sys
import io
import psutil
import os
import json

# Fix Unicode for Windows
if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer') and 'pytest' not in sys.modules:
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from pathlib import Path
from datetime import datetime

def get_system_stats():
    """Thu thập thông tin tài nguyên phần cứng."""
    stats = {}
    
    # Kiểm tra RAM
    mem = psutil.virtual_memory()
    stats['ram'] = {
        'total_gb': round(mem.total / (1024**3), 2),
        'available_gb': round(mem.available / (1024**3), 2),
        'percent_used': mem.percent
    }
    
    # Kiểm tra Ổ đĩa D: (LangGraphStorage)
    storage_path = "D:\\"
    if os.path.exists(storage_path):
        usage = psutil.disk_usage(storage_path)
        stats['storage_d'] = {
            'total_gb': round(usage.total / (1024**3), 2),
            'free_gb': round(usage.free / (1024**3), 2),
            'percent_used': usage.percent
        }
    else:
        # Fallback to C: if D: not exists
        usage = psutil.disk_usage("C:\\")
        stats['storage_c'] = {
            'total_gb': round(usage.total / (1024**3), 2),
            'free_gb': round(usage.free / (1024**3), 2),
            'percent_used': usage.percent
        }
        
    return stats

def update_global_state():
    """Cập nhật tài nguyên vào GLOBAL_STATE.md."""
    stats = get_system_stats()
    base_dir = Path(__file__).resolve().parent.parent.parent
    state_file = base_dir / "context" / "GLOBAL_STATE.md"
    
    if not state_file.exists():
        print("Error: GLOBAL_STATE.md not found.")
        return

    with open(state_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Tìm vị trí để chèn hoặc cập nhật
    new_lines = []
    hardware_section_exists = False
    
    for line in lines:
        if "## 🔋 HARDWARE awareness" in line:
            hardware_section_exists = True
            break
            
    if hardware_section_exists:
        # Xóa section cũ để ghi mới
        skip = False
        for line in lines:
            if "## 🔋 HARDWARE awareness" in line:
                skip = True
                new_lines.append(line)
                new_lines.append(f"- **RAM:** {stats['ram']['available_gb']}GB available ({stats['ram']['percent_used']}% used)\n")
                storage = stats.get('storage_d') or stats.get('storage_c')
                drive = "D:" if stats.get('storage_d') else "C:"
                new_lines.append(f"- **Storage ({drive}):** {storage['free_gb']}GB free ({storage['percent_used']}% used)\n")
                new_lines.append(f"- **Last Scan:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            elif skip and line.startswith("##"):
                skip = False
                new_lines.append(line)
            elif not skip:
                new_lines.append(line)
    else:
        # Chèn vào trước phần Trust Registry
        for line in lines:
            if "## 🛡️ Trust Registry" in line:
                new_lines.append("## 🔋 HARDWARE awareness\n")
                new_lines.append(f"- **RAM:** {stats['ram']['available_gb']}GB available ({stats['ram']['percent_used']}% used)\n")
                storage = stats.get('storage_d') or stats.get('storage_c')
                drive = "D:" if stats.get('storage_d') else "C:"
                new_lines.append(f"- **Storage ({drive}):** {storage['free_gb']}GB free ({storage['percent_used']}% used)\n")
                new_lines.append(f"- **Last Scan:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            new_lines.append(line)

    with open(state_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("✅ GLOBAL_STATE.md updated with hardware stats.")

if __name__ == "__main__":
    update_global_state()
