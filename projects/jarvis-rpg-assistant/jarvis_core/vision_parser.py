import json
import os
import base64
import requests
from pathlib import Path
from dotenv import load_dotenv

# Lấy KEY từ thư mục root của hệ thống
root_env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=root_env_path)

GCLI_API_KEY = os.getenv("GCLI_API_KEY")
# Parse base URL để đảm bảo trỏ đúng vào endpoint chat completions
GCLI_BASE_URL = os.getenv("GCLI_BASE_URL", "https://api.openai.com/v1")
if "chat/completions" not in GCLI_BASE_URL:
    if GCLI_BASE_URL.endswith("/"):
        GCLI_BASE_URL += "chat/completions"
    else:
        GCLI_BASE_URL += "/chat/completions"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def parse_schedule_image(image_path: str):
    """
    Sử dụng GCLI API Key (chuẩn OpenAI Vision) để đọc ảnh lịch và trả về danh sách event JSON.
    """
    if not GCLI_API_KEY:
        print("❌ Lỗi: Không tìm thấy GCLI_API_KEY trong .env")
        return []

    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GCLI_API_KEY}"
    }

    prompt = """
    Bạn là MỘT CHUYÊN GIA BÓC TÁCH DỮ LIỆU TỪ BẢNG BIỂU (GRID OCR EXPERT).
    Đây là ảnh Thời khóa biểu (Lịch học/Lịch thi). Cấu trúc ảnh là một LƯỚI (GRID).
    
    YÊU CẦU BẮT BUỘC:
    1. Quét theo dạng TỌA ĐỘ: Từ Cột Thứ 2 đến Cột Chủ nhật. Trong mỗi Cột, quét từ dòng Sáng -> Chiều -> Tối.
    2. TÌM TẤT CẢ các ô chứa thông tin môn học. TUYỆT ĐỐI KHÔNG ĐƯỢC BỎ SÓT DÙ CHỈ 1 Ô. Cứ thấy ô nào có nền màu và có chữ (ví dụ: "Tiếng Anh 4", "Học sâu và ứng dụng", "Đồ án tổng hợp...") là BẮT BUỘC phải trích xuất thành 1 sự kiện riêng biệt.
    3. Nếu một môn học xuất hiện nhiều lần ở nhiều ô khác nhau, hãy tạo các sự kiện riêng biệt cho từng ô đó.
    4. Trích xuất chính xác Ngày (Date) trên đầu mỗi cột (ví dụ: 08/06/2026 thì parse thành 2026-06-08). Nếu không có năm, tự mặc định là năm nay.
    5. Giờ bắt đầu và kết thúc phải lấy chính xác (ví dụ: "Giờ: 08:00 - 11:30" -> start_time: "08:00", end_time: "11:30").
    
    Định dạng đầu ra:
    - Trả về ĐÚNG MỘT MẢNG JSON, KHÔNG CÓ BẤT KỲ VĂN BẢN NÀO KHÁC (không kèm ```json).
    - Mỗi object có các trường:
      {
        "summary": "Tên sự kiện/Môn học",
        "date": "YYYY-MM-DD",
        "start_time": "HH:MM",
        "end_time": "HH:MM",
        "location": "Phòng học/Địa điểm (nếu có, ví dụ A.305)",
        "description": "Ghi chú thêm (Tên GV, Mã lớp, Hình thức trực tiếp/trực tuyến...)"
      }
    - Đảm bảo JSON hợp lệ tuyệt đối.
    """

    payload = {
        "model": "gemini-2.5-pro", # Đổi sang Pro để chống OCR sót các bảng biểu phức tạp
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.0
    }

    try:
        response = requests.post(GCLI_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        text = result["choices"][0]["message"]["content"].strip()
        
        # Clean markdown
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        events = json.loads(text.strip())
        return events
    except Exception as e:
        print(f"❌ Lỗi khi đọc ảnh qua GCLI Vision: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Chi tiết: {response.text}")
        return []
