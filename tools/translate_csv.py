import csv
import sys
import os
import time

# Cấu hình encoding cho terminal trên Windows để chống lỗi in tiếng Việt
if sys.stdout.encoding.lower() != 'utf-8':
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Thư viện 'deep-translator' chưa được cài đặt. Vui lòng chạy lệnh: uv pip install deep-translator")
    sys.exit(1)

def translate_csv(input_csv: str, output_csv: str):
    """
    Đọc file CSV, dịch cột 'ja' (hoặc 'en') sang 'vi' nếu cột 'vi' đang trống.
    Sử dụng GoogleTranslator để dịch.
    """
    if not os.path.exists(input_csv):
        print(f"Lỗi: Không tìm thấy file {input_csv}")
        return
        
    print(f"Đang đọc file: {input_csv}")
    
    translator = GoogleTranslator(source='auto', target='vi')
    
    translated_count = 0
    
    # Đọc toàn bộ file cũ để resume nếu đang chạy dở
    existing_data = []
    headers = []
    
    # Dùng file output làm input nếu đã có file output (để dịch tiếp)
    source_file = output_csv if os.path.exists(output_csv) else input_csv
    print(f"Dữ liệu nguồn: {source_file}")
    
    with open(source_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            print("File CSV trống!")
            return
            
        try:
            vi_index = headers.index('vi')
            ja_index = headers.index('ja')
            en_index = headers.index('en')
        except ValueError as e:
            print(f"File CSV thiếu cột: {e}")
            return
            
        existing_data = list(reader)

    # Dịch và ghi đè trực tiếp mỗi khi có 5 dòng được dịch để tránh mất dữ liệu khi timeout
    pending_saves = 0
    for idx, row in enumerate(existing_data):
        while len(row) < len(headers):
            row.append("")
            
        vi_text = row[vi_index].strip()
        ja_text = row[ja_index].strip()
        en_text = row[en_index].strip()
        
        # Kiểm tra nếu vi_text trống hoặc chứa lỗi 500/Error/429
        needs_translation = False
        if not vi_text:
            needs_translation = True
        elif "Error" in vi_text or "500" in vi_text or "429" in vi_text:
            print(f"[Retry] Đã phát hiện dòng lỗi: {vi_text[:30]}...")
            needs_translation = True
            
        if needs_translation:
            text_to_translate = ja_text if ja_text else en_text
            if text_to_translate and len(text_to_translate) > 1 and not text_to_translate.startswith("res://"):
                try:
                    print(f"Đang dịch: {text_to_translate[:50]}...")
                    translated_text = translator.translate(text_to_translate)
                    
                    if translated_text:
                        existing_data[idx][vi_index] = translated_text
                        translated_count += 1
                        pending_saves += 1
                    time.sleep(0.5) # Chờ 0.5s chống Rate Limit
                except Exception as e:
                    print(f"Lỗi dịch: {e}. Sẽ thử lại ở lần chạy sau.")
                    # Ghi nhận lỗi vào cell để lần sau đọc lại phát hiện
                    existing_data[idx][vi_index] = f"Error: {e}"
        else:
            # Uncomment dòng dưới nếu muốn in log Skip
            # print(f"[Skip] {ja_text[:20]}...")
            pass
                    
        # Lưu file mỗi 5 dòng được dịch để đề phòng timeout bị văng ngang
        if pending_saves >= 5:
            with open(output_csv, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(existing_data)
            pending_saves = 0
            
    # Lưu đợt cuối
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(existing_data)
        
    print(f"Hoàn tất! Đã dịch mới/sửa lỗi thêm {translated_count} dòng.")

if __name__ == "__main__":
    INPUT_FILE = "tools/story_translations.csv"
    OUTPUT_FILE = "tools/story_translations_translated.csv"
    
    translate_csv(INPUT_FILE, OUTPUT_FILE)
