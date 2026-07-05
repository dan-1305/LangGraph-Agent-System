import json
import re
from pathlib import Path
import ast
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def fix_missing_base_agent(reports_path="reports/compliance_violations.json"):
    reports_file = Path(reports_path)
    if not reports_file.exists():
        print(f"Error: {reports_path} not found.")
        return

    with open(reports_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    violations = data.get("violations", [])
    
    # Group by file
    file_map = {}
    for v in violations:
        if v.get("type") == "MISSING_BASE_AGENT":
            fpath = v.get("file")
            cls_name = v.get("class")
            if fpath and cls_name:
                if fpath not in file_map:
                    file_map[fpath] = []
                file_map[fpath].append(cls_name)

    fixed_count = 0
    for fpath, classes in file_map.items():
        file_path = Path(fpath)
        if not file_path.exists():
            print(f"File not found: {fpath}")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        changed = False
        
        # Thêm import nếu chưa có
        if "from src.base_agent import BaseAgent" not in content and "import BaseAgent" not in content:
            # Tìm vị trí an toàn để chèn import
            lines = content.split('\n')
            insert_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('import ') or line.startswith('from '):
                    insert_idx = i
                    break
            lines.insert(insert_idx, "from src.base_agent import BaseAgent")
            content = '\n'.join(lines)
            changed = True

        for cls_name in classes:
            # Tìm định nghĩa class
            # Trường hợp 1: class Name:
            pattern1 = rf"class\s+{cls_name}\s*:"
            if re.search(pattern1, content):
                content = re.sub(pattern1, f"class {cls_name}(BaseAgent):", content)
                changed = True
                fixed_count += 1
                continue
                
            # Trường hợp 2: class Name(Parent):
            pattern2 = rf"class\s+{cls_name}\s*\(([^)]+)\):"
            match2 = re.search(pattern2, content)
            if match2:
                parents = match2.group(1)
                # Nếu chưa kế thừa BaseAgent
                if "BaseAgent" not in parents:
                    content = re.sub(pattern2, f"class {cls_name}(BaseAgent, {parents}):", content)
                    changed = True
                    fixed_count += 1

        if changed:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Fixed {len(classes)} classes in {fpath}")

    print(f"\n🎉 Hoàn tất Auto-Fix. Đã sửa {fixed_count} lỗi MISSING_BASE_AGENT.")

if __name__ == "__main__":
    fix_missing_base_agent()
