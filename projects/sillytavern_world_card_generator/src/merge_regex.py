import json
from pathlib import Path

# Dùng absolute path
BASE_DIR = Path(__file__).resolve().parent
preset_dir = BASE_DIR / "data" / "templates" / "preset"

# Đường dẫn các file
dreammini_preset_path = preset_dir / "【Dreammini】3.92-Ultra-0907-Decal-PNTT.json"
dreammini_regex_path = preset_dir / "regex_dreammini.json"
output_path = preset_dir / "【Dreammini】3.92-Ultra-Merged-Test.json"

try:
    # 1. Đọc file Preset
    with open(dreammini_preset_path, "r", encoding="utf-8") as f:
        preset_data = json.load(f)
        
    # 2. Đọc file Regex rời
    with open(dreammini_regex_path, "r", encoding="utf-8") as f:
        regex_data = json.load(f)
        
    # 3. Lấy danh sách các rule (trong bản export regex rời, regex_scripts nằm trong key 'rules')
    regex_rules = regex_data.get("rules", [])
    
    # 4. Gộp vào Preset
    if "extensions" not in preset_data:
        preset_data["extensions"] = {}
        
    preset_data["extensions"]["regex_scripts"] = regex_rules
    
    # 5. Lưu ra file test mới
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(preset_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Gộp thành công! Đã chèn {len(regex_rules)} đoạn regex vào file Preset.")
    print(f"📂 File lưu tại: {output_path}")

except Exception as e:
    print(f"❌ Lỗi khi gộp file: {e}")
