import sys
import os
import datetime
from pathlib import Path

# Add project root to sys.path to resolve imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from jarvis_core.vision_parser import parse_schedule_image
from jarvis_core.google_services import get_creds, create_calendar_event

def get_next_weekday(day_name):
    """
    Hàm tính toán ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất.
    Ví dụ: 'Thứ 2' -> trả về YYYY-MM-DD của thứ 2 tuần này/tuần tới.
    """
    days = {
        'thứ 2': 0, 'monday': 0,
        'thứ 3': 1, 'tuesday': 1,
        'thứ 4': 2, 'wednesday': 2,
        'thứ 5': 3, 'thursday': 3,
        'thứ 6': 4, 'friday': 4,
        'thứ 7': 5, 'saturday': 5,
        'chủ nhật': 6, 'sunday': 6, 'cn': 6
    }
    
    day_name_lower = day_name.lower().strip()
    target_day = None
    for k, v in days.items():
        if k in day_name_lower:
            target_day = v
            break
            
    if target_day is None:
        return datetime.date.today().isoformat()
        
    today = datetime.date.today()
    days_ahead = target_day - today.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return (today + datetime.timedelta(days_ahead)).isoformat()

def test_pipeline(image_path: str):
    if not os.path.exists(image_path):
        print(f"❌ Không tìm thấy ảnh tại: {image_path}")
        return
        
    print(f"🔍 Bắt đầu đọc ảnh: {image_path}")
    events_json = parse_schedule_image(image_path)
    
    if not events_json:
        print("❌ Không trích xuất được sự kiện nào từ ảnh.")
        return
        
    print(f"✅ Đã trích xuất {len(events_json)} sự kiện:")
    
    creds = get_creds()
    if not creds:
        print("❌ Không lấy được Credentials Google Calendar. Hủy đồng bộ.")
        return
        
    for ev in events_json:
        print(f" - {ev.get('summary')} | {ev.get('date')} {ev.get('start_time')}-{ev.get('end_time')}")
        
        # Xử lý ngày tháng
        raw_date = ev.get('date', '')
        # Nếu không phải format YYYY-MM-DD
        if len(raw_date) != 10 or "-" not in raw_date:
            date_iso = get_next_weekday(raw_date)
        else:
            date_iso = raw_date
            
        start_time_iso = f"{date_iso}T{ev.get('start_time', '00:00')}:00"
        end_time_iso = f"{date_iso}T{ev.get('end_time', '01:00')}:00"
        
        create_calendar_event(
            creds=creds,
            summary=ev.get('summary', 'Sự kiện không tên'),
            start_time_iso=start_time_iso,
            end_time_iso=end_time_iso,
            description=ev.get('description', 'Tạo tự động từ ảnh lịch'),
            location=ev.get('location', '')
        )
    print("✅ Hoàn tất đồng bộ Lịch!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python test_vision_calendar.py <đường_dẫn_ảnh>")
    else:
        test_pipeline(sys.argv[1])
