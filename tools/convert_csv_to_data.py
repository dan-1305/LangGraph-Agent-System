import csv
import sys
import os

# Cấu hình encoding cho terminal trên Windows để chống lỗi in tiếng Việt
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

def convert_csv_to_data(input_csv: str, output_data: str):
    """
    Chuyển đổi file CSV đã dịch trở lại thành định dạng locate.data gốc.
    """
    print(f"Bắt đầu đọc file CSV: {input_csv}")
    
    if not os.path.exists(input_csv):
        print(f"Lỗi: Không tìm thấy file {input_csv}")
        return
        
    converted_count = 0
    rows_to_write = []
    
    # Header chuẩn của locate.data gốc
    rows_to_write.append(['keys', 'ja'])
    
    with open(input_csv, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            print("File CSV trống!")
            return
            
        try:
            key_index = headers.index('key')
            vi_index = headers.index('vi')
            ja_index = headers.index('ja')
        except ValueError as e:
            print(f"File CSV thiếu cột chuẩn. Lỗi: {e}")
            return
            
        for row in reader:
            if not row:
                continue
                
            # Đảm bảo row đủ độ dài
            while len(row) < len(headers):
                row.append("")
                
            key = row[key_index].strip()
            vi_text = row[vi_index].strip()
            ja_text = row[ja_index].strip()
            
            # Lấy text tiếng Việt, nếu chưa dịch hoặc bị lỗi 500 thì fallback về tiếng Nhật
            final_text = vi_text
            if not vi_text or "Error" in vi_text or "500" in vi_text or "429" in vi_text:
                final_text = ja_text
                
            # Ghi theo chuẩn của file locate.data (cột keys, ja)
            # Thêm dấu ngoặc kép bằng module csv tự động xử lý
            rows_to_write.append([key, final_text])
            converted_count += 1
            
    print(f"Đã đọc và chuẩn bị {converted_count} dòng dữ liệu.")
    
    # Backup file cũ nếu có
    if os.path.exists(output_data):
        backup_path = output_data + ".bak"
        print(f"Đang tạo backup file gốc tại: {backup_path}")
        if os.path.exists(backup_path):
            os.remove(backup_path) # Xoá backup cũ
        os.rename(output_data, backup_path)
    
    print(f"Đang ghi ra file Game Data: {output_data}")
    
    # File data của Godot thường yêu cầu quoting ở tất cả các text (tuỳ thuộc engine csv reader)
    with open(output_data, 'w', encoding='utf-8', newline='') as f:
        # QUOTE_ALL đảm bảo các dòng đều có "..." bao quanh như file gốc
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(rows_to_write)
        
    print(f"Hoàn tất! File đã được nhúng vào: {output_data}")

if __name__ == "__main__":
    INPUT_CSV = "tools/story_translations_translated.csv"
    OUTPUT_DATA = r"SAYONARA_NO_CHECKLIST\locate.data"
    
    convert_csv_to_data(INPUT_CSV, OUTPUT_DATA)
