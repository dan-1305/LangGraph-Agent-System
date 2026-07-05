import json
import re
from pathlib import Path
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def fix_forbidden_imports(reports_path="reports/compliance_violations.json"):
    reports_file = Path(reports_path)
    if not reports_file.exists():
        print(f"Error: {reports_path} not found.")
        return

    with open(reports_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    violations = data.get("violations", [])
    
    file_map = set()
    for v in violations:
        if v.get("type") == "FORBIDDEN_IMPORT":
            fpath = v.get("file")
            if fpath:
                file_map.add(fpath)

    fixed_count = 0
    for fpath in file_map:
        file_path = Path(fpath)
        if not file_path.exists():
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False
        
        # Xóa import requests/httpx/urllib
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            if re.match(r'^(import|from)\s+(requests|httpx|urllib(\.request)?)', line.strip()):
                changed = True
                continue
            new_lines.append(line)
            
        content = '\n'.join(new_lines)
        
        if changed:
            # Thêm import HTTPClient
            if "from core_utilities.http_client import HTTPClient" not in content:
                # Find safe spot
                insert_idx = 0
                for i, line in enumerate(new_lines):
                    if line.startswith('import ') or line.startswith('from '):
                        insert_idx = i
                        break
                new_lines.insert(insert_idx, "from core_utilities.http_client import HTTPClient")
                content = '\n'.join(new_lines)

            # Replace calls
            content = re.sub(r'\brequests\.get\(', 'HTTPClient.get(', content)
            content = re.sub(r'\brequests\.post\(', 'HTTPClient.post(', content)
            content = re.sub(r'\bhttpx\.get\(', 'HTTPClient.get(', content)
            content = re.sub(r'\bhttpx\.post\(', 'HTTPClient.post(', content)
            
            # Write back
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            fixed_count += 1
            print(f"✅ Fixed imports in {fpath}")

    print(f"\n🎉 Hoàn tất Auto-Fix Imports. Đã sửa {fixed_count} files.")

if __name__ == "__main__":
    fix_forbidden_imports()
