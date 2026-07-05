import csv
import sys
import os

# Cấu hình encoding cho terminal trên Windows để chống lỗi in tiếng Việt
if sys.stdout.encoding.lower() != 'utf-8':
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding.lower() != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

def convert_data_to_csv(data_file_path: str, output_csv: str):
    """
    Chuyển đổi file locate.data (file CSV ẩn của Godot) thành định dạng chuẩn key,en,vi,ja
    """
    print(f"Bắt đầu chuyển đổi file: {data_file_path}")
    
    if not os.path.exists(data_file_path):
        print(f"Lỗi: Không tìm thấy file {data_file_path}")
        return
        
    converted_count = 0
    rows_to_write = []
    
    # Header chuẩn
    rows_to_write.append(['key', 'en', 'vi', 'ja'])
    
    # Đọc file locate.data, nó thực chất là file CSV với cột: keys, ja
    with open(data_file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None) # Lấy dòng đầu tiên (keys, ja)
        
        for row in reader:
            if not row or len(row) < 2:
                continue
                
            key = row[0]
            ja_text = row[1]
            
            # Lưu theo chuẩn: key, en(trống), vi(trống), ja
            rows_to_write.append([key, "", "", ja_text])
            converted_count += 1
            
    print(f"Đã đọc và chuyển đổi {converted_count} dòng hội thoại.")
    print(f"Đang ghi ra file CSV: {output_csv}")
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_write)
        
    print(f"Hoàn tất! File đã sẵn sàng tại: {output_csv}")

if __name__ == "__main__":
    DATA_FILE = r"SAYONARA_NO_CHECKLIST\locate.data"
    OUTPUT_CSV = r"tools\story_translations.csv"
    
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    convert_data_to_csv(DATA_FILE, OUTPUT_CSV)
