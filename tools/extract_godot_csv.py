import os
import re
import csv
import hashlib
import sys

# Cấu hình encoding cho terminal trên Windows để chống lỗi in tiếng Việt
if sys.stdout.encoding.lower() != 'utf-8':
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

def generate_smart_key(raw_str: str) -> str:
    """Tạo key thông minh từ nội dung: T_<hash_6_char>_<5_từ_đầu>"""
    hash_val = hashlib.md5(raw_str.encode('utf-8')).hexdigest()[:6].upper()
    # Lấy tối đa 5 từ đầu (đối với tiếng Anh/Việt) hoặc 10 ký tự đầu (đối với tiếng Nhật)
    clean_str = re.sub(r'[^\w\s]', '', raw_str) # Xóa ký tự đặc biệt
    words = clean_str.split()
    
    if len(words) > 1: # Chữ có dấu cách (Anh, Việt)
        snippet = "_".join(words[:5])
    else: # Chữ dính liền (Nhật, Trung)
        snippet = clean_str[:10]
        
    return f"T_{hash_val}_{snippet}"

def is_garbage_string(raw_str: str) -> bool:
    """Kiểm tra xem chuỗi có phải là rác không."""
    raw_str = raw_str.strip()
    if len(raw_str) <= 1:
        return True
        
    # 1. Loại trừ các chuỗi path, resource, hoặc định dạng hệ thống
    if re.search(r'res://|user://|uid://|\.png|\.ogg|\.wav|\.tscn|\.gd|\.tres|\.import', raw_str):
        return True
        
    # 2. Loại trừ Node Paths (có chứa dấu gạch chéo /, ví dụ: GUILIST/Menu/ClickOpen)
    # Nhưng cẩn thận không chặn nhầm câu có URL (nếu có, dù URL thường dùng res:// đã bị chặn ở trên)
    if re.search(r'^[A-Za-z0-9_]+/[A-Za-z0-9_/]+$', raw_str):
        return True
        
    # 3. Loại trừ Method Calls (những chuỗi có () ở cuối, ví dụ: _showKeyOff(), changeWindowMode())
    if raw_str.endswith('()'):
        return True
        
    # 4. Loại trừ chuỗi Properties/Node references (bắt đầu bằng _ hoặc chứa dấu hai chấm :, ví dụ: Attention:modulate)
    if raw_str.startswith('_') or re.search(r'[A-Za-z0-9_]+:[a-z_]+', raw_str):
        return True

    # 5. Loại trừ các chuỗi định dạng thuần túy (như %s %s %s) nếu đứng đơn độc không có chữ
    if re.fullmatch(r'^[%s\s\W]+$', raw_str):
        return True

    # 6. Loại trừ các chuỗi rác kiểu "Node2D", "MarginContainer", snake_case, UPPER_CASE
    if re.fullmatch(r'^[A-Za-z0-9_]+$', raw_str):
        # Nếu toàn chữ không có khoảng trắng hoặc ký tự Nhật, và giống tên biến/Node
        return True
        
    # 7. Loại trừ chuỗi chỉ chứa số, số Full-width, dấu câu, hoặc các kí tự mojibake lặp lại
    if re.fullmatch(r'^[\d０-９\s\Wï¼]+$', raw_str):
        return True
        
    # 8. Chặn cứng các chuỗi rác chuyên biệt của Godot Script
    if raw_str in ["resize() Error", "File is Not Found", "OK (Lock File is Not Found)"]:
        return True
        
    return False

def extract_strings_to_csv(source_dir: str, output_csv: str, reference_csv: str = None):
    print(f"Bắt đầu quét thư mục: {source_dir}")
    
    extracted_data = {} # key: { 'en': '', 'vi': '', 'ja': '' }
    
    # Load reference CSV
    if reference_csv and os.path.exists(reference_csv):
        print(f"Loading reference keys from {reference_csv}")
        # Try multiple encodings for the reference CSV
        ref_encodings = ['utf-8-sig', 'utf-8', 'shift_jis', 'cp1252']
        content_lines = []
        for enc in ref_encodings:
            try:
                with open(reference_csv, 'r', encoding=enc) as f:
                    content_lines = f.readlines()
                break
            except Exception:
                continue
                
        if content_lines:
            reader = csv.DictReader(content_lines)
            for row in reader:
                key = row.get('key', '').strip()
                if key:
                    extracted_data[key] = {
                        'en': row.get('en', ''),
                        'vi': row.get('vi', ''),
                        'ja': row.get('ja', '')
                    }
    
    # Bắt tất cả chuỗi string nằm trong ngoặc kép (Multi-line)
    string_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"', re.DOTALL)
    
    # Bắt các cặp WORD_XXXX = "..." hoặc WORD_XXXX : result = "..."
    # Mở rộng để bắt cả hàm tr() và cả những mảng định nghĩa hội thoại.
    word_mapping_pattern = re.compile(r'(WORD_[A-Z0-9_]+)\s*=\s*tr\("([^"]+)"\)|(WORD_[A-Z0-9_]+)\s*:\s*result\s*=\s*tr\("([^"]+)"\)')
    
    # Bắt các lệnh gán text trực tiếp (phổ biến trong Godot UI và Visual Novel Engine)
    # Ví dụ: text = "Hội thoại" hoặc title = "Tên" hoặc say("Hội thoại")
    dialogue_pattern = re.compile(r'(?:text|title|name|dialogue|say)\s*[=:\(]\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.IGNORECASE)
    
    # Valid Text: CỰC KỲ QUAN TRỌNG -> Ưu tiên bắt BẰNG ĐƯỢC tiếng Nhật (Hiragana/Katakana/Kanji)
    # Hoặc các câu có chứa thẻ BBCode ([color=], [center], [i])
    valid_text_pattern = re.compile(r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF]|\[[a-z=]+\]')
    
    file_count = 0
    string_count = 0
    
    # Mở rộng file quét (bao gồm cả .dialogue, .txt, .cfg nếu Dev tự chế script)
    valid_extensions = ('.gd', '.tscn', '.tres', '.json', '.dialogue', '.txt', '.cfg')
    
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(valid_extensions):
                file_count += 1
                file_path = os.path.join(root, file)
                
                content = ""
                # Auto-detect encoding
                for enc in ['utf-8', 'shift_jis', 'cp932']:
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            content = f.read()
                        break # Đọc thành công thì thoát vòng lặp
                    except UnicodeDecodeError:
                        continue
                
                if not content:
                    continue # Bỏ qua nếu không đọc được file
                
                # Hàm giải mã chuỗi tuỳ theo encoding của python
                def decode_str(s):
                    try:
                        return s.encode('utf-8').decode('unicode_escape')
                    except:
                        return s
                
                # 1. Quét các biến WORD_XXXX
                word_matches = word_mapping_pattern.findall(content)
                for m in word_matches:
                    key_name = next(filter(None, m)) 
                    val_index = m.index(key_name) + 1
                    
                    if val_index < len(m) and m[val_index]:
                        raw_str = decode_str(m[val_index])
                        
                        if is_garbage_string(raw_str):
                            # Xoá chuỗi khỏi content nhưng ko nạp vào DB
                            content = content.replace(m[0], "")
                            continue
                            
                        if key_name not in extracted_data:
                            extracted_data[key_name] = {'en': '', 'vi': '', 'ja': raw_str}
                        else:
                            extracted_data[key_name]['ja'] = raw_str
                            
                        string_count += 1
                        # Xóa đoạn đã match để tránh bị quét lại bởi string_pattern
                        content = content.replace(m[0], "")
                
                # 2. Quét các lệnh gán text đặc thù của Visual Novel (text=, say(), v.v)
                dialogue_matches = dialogue_pattern.findall(content)
                for match in dialogue_matches:
                    raw_str = decode_str(match)
                    if not is_garbage_string(raw_str) and valid_text_pattern.search(raw_str):
                        smart_key = generate_smart_key(raw_str)
                        if smart_key not in extracted_data:
                            extracted_data[smart_key] = {'en': '', 'vi': '', 'ja': raw_str}
                            string_count += 1
                        # Xoá tránh trùng
                        content = content.replace(f'"{match}"', '""')

                # 3. Quét các chuỗi text lỏng lẻo còn lại trong ngoặc kép
                matches = string_pattern.findall(content)
                for match in matches:
                    raw_str = decode_str(match)
                    
                    # Lọc kĩ: Phải có tiếng Nhật HOẶC có BBCode thì mới tin là lời thoại/UI text đáng dịch
                    if not is_garbage_string(raw_str) and valid_text_pattern.search(raw_str):
                        smart_key = generate_smart_key(raw_str)
                        if smart_key not in extracted_data:
                            extracted_data[smart_key] = {'en': '', 'vi': '', 'ja': raw_str}
                            string_count += 1

    print(f"Đã quét {file_count} file, tìm thấy tổng {len(extracted_data)} chuỗi text (unique).")
    print(f"Đang ghi ra file CSV: {output_csv}")
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['key', 'en', 'vi', 'ja'])
        
        # Bỏ đi các key mồ côi (chỉ có key mà ko có text ở 'ja' hoặc 'en' hoặc 'vi')
        clean_count = 0
        for key, data in extracted_data.items():
            ja_text = data.get('ja', '').strip()
            en_text = data.get('en', '').strip()
            vi_text = data.get('vi', '').strip()
            
            # Filter Orphaned Keys: Nếu không tìm thấy bất kì nội dung text nào cho key này, loại nó ra.
            if not ja_text and not en_text and not vi_text:
                continue
                
            writer.writerow([key, en_text, vi_text, ja_text])
            clean_count += 1
            
    print(f"Hoàn tất! Đã xuất {clean_count} dòng dữ liệu sạch ra CSV.")

if __name__ == "__main__":
    SOURCE_DIR = r"D:\Users\Admin\Downloads\kimochi\Game\[Kimochi] [RJ01503291] さよならのチェックリスト\SAYONARA_NO_CHECKLIST"
    OUTPUT_CSV = "tools/extracted_translations.csv"
    REF_CSV = r"C:\Users\Admin\Downloads\New Text Document.csv"
    
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    
    if os.path.exists(SOURCE_DIR):
        extract_strings_to_csv(SOURCE_DIR, OUTPUT_CSV, REF_CSV)
    else:
        print(f"Không tìm thấy thư mục {SOURCE_DIR}")