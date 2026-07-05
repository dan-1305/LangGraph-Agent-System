import streamlit as st
import sys
import os
import datetime
import csv
import io
from pathlib import Path

# Add project root to sys.path to resolve imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from jarvis_core.vision_parser import parse_schedule_image

st.set_page_config(page_title="Jarvis Calendar Importer", page_icon="📅", layout="wide")

def get_next_weekday(day_name):
    """Tính ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất."""
    days = {
        'thứ 2': 0, 'monday': 0, 'thứ 3': 1, 'tuesday': 1, 'thứ 4': 2, 'wednesday': 2,
        'thứ 5': 3, 'thursday': 3, 'thứ 6': 4, 'friday': 4, 'thứ 7': 5, 'saturday': 5,
        'chủ nhật': 6, 'sunday': 6, 'cn': 6
    }
    day_name_lower = day_name.lower().strip()
    target_day = next((v for k, v in days.items() if k in day_name_lower), None)
    
    if target_day is None:
        return datetime.date.today().isoformat()
        
    today = datetime.date.today()
    days_ahead = target_day - today.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return (today + datetime.timedelta(days_ahead)).isoformat()

def generate_google_calendar_csv(events):
    """Tạo nội dung CSV chuẩn Google Calendar."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers chuẩn của Google Calendar
    writer.writerow(['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location', 'Private'])
    
    for ev in events:
        subject = ev.get('summary', 'Sự kiện chưa đặt tên')
        description = ev.get('description', 'Được tạo tự động bởi Jarvis OCR')
        
        # LỌC RÁC: Loại bỏ hoàn toàn các môn học dán mác "Tạm ngưng"
        if "tạm ngưng" in subject.lower() or "tạm ngưng" in description.lower():
            continue
            
        raw_date = ev.get('date', '')
        if len(raw_date) != 10 or "-" not in raw_date:
            date_iso = get_next_weekday(raw_date)
        else:
            date_iso = raw_date
            
        start_date = datetime.datetime.strptime(date_iso, "%Y-%m-%d").strftime("%m/%d/%Y")
        end_date = start_date
        
        start_time = ev.get('start_time', '00:00')
        end_time = ev.get('end_time', '01:00')
        location = ev.get('location', '')
        
        writer.writerow([subject, start_date, start_time, end_date, end_time, 'False', description, location, 'False'])
        
    return output.getvalue()

st.title("📅 Jarvis - Image to Google Calendar")
st.markdown("Kéo thả các ảnh lịch tuần/tháng vào đây. Hệ thống sẽ tự động bóc tách và xuất ra file **CSV** để bạn có thể import trực tiếp vào Google Calendar.")

uploaded_files = st.file_uploader("Chọn hoặc kéo thả ảnh lịch", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if uploaded_files:
    if st.button("🚀 Bắt đầu xử lý AI", type="primary"):
        all_events = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Tạo thư mục temp
        temp_dir = Path("data/temp_ui_images")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        for i, file in enumerate(uploaded_files):
            status_text.text(f"Đang xử lý ảnh {i+1}/{len(uploaded_files)}: {file.name} ...")
            
            # Lưu file tạm để genai.upload_file có thể đọc
            temp_path = temp_dir / file.name
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())
                
            # Phân tích bằng Gemini
            events = parse_schedule_image(str(temp_path))
            if events:
                all_events.extend(events)
                
            # Xóa file tạm
            if temp_path.exists():
                os.remove(temp_path)
                
            progress_bar.progress((i + 1) / len(uploaded_files))
            
        status_text.text("✅ Xử lý hoàn tất!")
        
        if all_events:
            st.success(f"🎉 Đã tìm thấy tổng cộng {len(all_events)} sự kiện từ {len(uploaded_files)} ảnh.")
            st.json(all_events, expanded=False)
            
            # Tạo CSV
            csv_data = generate_google_calendar_csv(all_events)
            
            st.download_button(
                label="📥 Tải file CSV cho Google Calendar",
                data=csv_data.encode('utf-8-sig'), # Dùng utf-8-sig để Google đọc tiếng Việt không bị lỗi font
                file_name=f"jarvis_calendar_{datetime.date.today().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            st.info("💡 Hướng dẫn Import: Mở Google Calendar -> Cài đặt (Bánh răng) -> Nhập & Xuất -> Chọn file CSV vừa tải -> Nhập.")
        else:
            st.error("❌ Không thể tìm thấy hoặc bóc tách sự kiện nào từ các ảnh đã tải lên.")
