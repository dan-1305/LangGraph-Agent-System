import json
import os
import base64
import sys
from pathlib import Path
from dotenv import load_dotenv

# Đảm bảo có thể import được thư viện core của dự án
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.base_agent import BaseAgent
from core_utilities.image_utils import encode_image

class VisionParserAgent(BaseAgent):
    """
    [ROLE: AI Prompt Engineer / QA Tester]
    Agent chuyên trách bóc tách dữ liệu từ hình ảnh thời khóa biểu.
    Kế thừa BaseAgent để hưởng quyền lợi: Key Rotation, Retry, và Logging chuẩn Monorepo.
    """
    def __init__(self):
        # Sử dụng label:tier-1 để tận dụng hỏa lực mạnh cho Vision OCR (thường dùng model xịn)
        super().__init__(name="VisionParser", role="Grid OCR Expert", agent_label="tier-1", temperature=0.0)

    def _ai_handler(self, *args, **kwargs):
        """Bắt buộc triển khai từ BaseAgent - Không dùng trong luồng này."""
        pass

    def _logic_handler(self, *args, **kwargs):
        """Bắt buộc triển khai từ BaseAgent - Không dùng trong luồng này."""
        pass

    def parse_schedule_image(self, image_path: str):
        """
        Sử dụng BaseAgent để gọi LLM Vision (qua Local Proxy) xử lý ảnh lịch.
        """
        if not os.path.exists(image_path):
            print(f"❌ Lỗi: Không tìm thấy file ảnh tại {image_path}")
            return []

        base64_image = encode_image(image_path)

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
        - Trả về ĐÚNG MỘT MẢNG JSON, KHÔNG CÓ BẤT KỲ VĂN BẢN NÀO KHÁC.
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

        # Chuyển đổi payload sang format nội bộ hỗ trợ Vision
        messages = [
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
        ]

        try:
            # Gọi LLM qua cơ chế bọc thép (Retry, Key Rotation)
            # Dùng _call_llm_with_retry để tự động xử lý lỗi 429/500
            response_text = self._call_llm_with_retry(messages, is_json=True)
            
            if isinstance(response_text, str):
                # Clean markdown nếu LLM trả về string có chứa block code
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                    response_text = response_text.split("```")[1].split("```")[0]
                
                events = json.loads(response_text.strip())
            else:
                events = response_text
                
            return events
        except Exception as e:
            print(f"❌ [VisionParserAgent] Lỗi nghiêm trọng: {e}")
            return []

# Duy trì khả năng tương thích với code cũ đang gọi hàm thô
def parse_schedule_image(image_path: str):
    """Wrapper function để không làm vỡ các module đang import hàm này."""
    agent = VisionParserAgent()
    return agent.parse_schedule_image(image_path)

if __name__ == "__main__":
    # Test nhanh (cần có file ảnh thực tế)
    test_img = "test_schedule.jpg"
    if os.path.exists(test_img):
        print(f"Testing VisionParser with {test_img}...")
        results = parse_schedule_image(test_img)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print("Bỏ qua test vì không tìm thấy test_schedule.jpg")
