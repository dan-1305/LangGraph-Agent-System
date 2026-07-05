import os
import json
import base64
from PIL import Image
from pathlib import Path

# Dùng absolute path để gọi ở đâu cũng được
# Sửa lỗi: BASE_DIR phải trỏ ra ngoài thư mục 'src'
BASE_DIR = Path(__file__).resolve().parent.parent 
card_dir = BASE_DIR / "card"
output_dir = BASE_DIR / "data" / "world_card"
output_dir.mkdir(parents=True, exist_ok=True)

count = 0
for file in os.listdir(card_dir):
    if not file.lower().endswith('.png'):
        continue
    
    img_path = card_dir / file
    try:
        img = Image.open(img_path)
        img.load()  # Force load to read info
        
        # Dữ liệu thẻ SillyTavern V2 thường nằm trong chunk 'chara' dưới dạng Base64
        chara_data = img.info.get('chara')
        
        if chara_data:
            # Giải mã Base64 sang chuỗi, rồi chuyển thành JSON (Dict)
            decoded = base64.b64decode(chara_data).decode('utf-8')
            json_data = json.loads(decoded)
            
            # Lấy tên nhân vật làm tên file JSON
            char_name = json_data.get('name') or json_data.get('data', {}).get('name') or file.replace('.png', '')
            # Lọc bỏ ký tự đặc biệt trong tên file
            safe_name = "".join([c for c in char_name if c.isalnum() or c in (' ', '-', '_')]).rstrip()
            if not safe_name:
                safe_name = file.replace('.png', '')
                
            out_file = output_dir / f"{safe_name}.json"
            
            # Lưu ra file JSON
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)
            
            # Simplified print statement
            print(f"Extracted: {file} -> {out_file.name}")
            count += 1
        else:
            # Simplified print statement
            print(f"Skipped (no 'chara' metadata): {file}")
            
    except Exception as e:
        # Simplified print statement
        print(f"Error reading {file}: {e}")

# Simplified print statement
print(f"\nCompleted! Successfully extracted {count} character cards to {output_dir}")
