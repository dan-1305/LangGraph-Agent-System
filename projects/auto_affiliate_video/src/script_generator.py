import sys
from dotenv import load_dotenv
from pathlib import Path

# Load biến môi trường và đảm bảo src của project chính vào sys.path
# __file__ -> .../projects/auto_affiliate_video/src/script_generator.py
# main_project_root sẽ là thư mục gốc của toàn bộ project (LangGraph_Agent_System)
main_project_root = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(main_project_root / ".env")
main_src_path = main_project_root / "src"
if str(main_src_path) not in sys.path:
    sys.path.insert(0, str(main_src_path))

# Bây giờ có thể import từ src của project chính
from src.base_agent import BaseAgent

class ScriptGenerator(BaseAgent):
    def __init__(self):
        super().__init__(model_name="label:tier-1", temperature=0.7)

    def _ai_handler(self, state: dict) -> dict:
        return state

    def _logic_handler(self, state: dict) -> dict:
        return state

    def generate_short_video_script(self, product_name: str, key_features: str) -> str:
        """
        Dùng OpenAI/Gemini để viết kịch bản video ngắn (dưới 60s) cho TikTok/Shorts.
        Áp dụng quy tắc Hook của sách Zero to Hero và Sức mạnh Ngôn từ.
        """
        print(f"✍️ Đang viết kịch bản AI cho sản phẩm: {product_name}...")
        
        system_prompt = """Bạn là một chuyên gia sáng tạo nội dung video ngắn (TikTok, YouTube Shorts, Reels) chuyên nghiệp và trung thực.
Luật viết kịch bản:
1. Độ dài tối đa: 130-150 từ (để đọc vừa vẹn trong 60 giây).
2. Bắt đầu bằng một câu mở đầu thu hút sự chú ý của người xem một cách tự nhiên.
3. KHÔNG chào hỏi rườm rà. Đi thẳng vào vấn đề.
4. Nêu 2-3 tính năng hoặc lợi ích chính của sản phẩm một cách khách quan.
5. Kết thúc bằng một lời mời tìm hiểu thêm hoặc mua hàng lịch sự, ví dụ: 'Bấm vào link bên dưới để tham khảo nhé!'.
6. Trả về DUY NHẤT nội dung lời thoại (Text), không bao gồm mô tả cảnh quay hay hành động."""

        user_prompt = f"""
Sản phẩm: {product_name}
Tính năng/Điểm nổi bật: {key_features}
Hãy viết kịch bản lời thoại ngay bây giờ.
"""

        try:
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            script = self._call_llm_with_retry(full_prompt)
            return script.strip()
        except Exception as e:
            print(f"❌ [Circuit Breaker] Fallback kích hoạt do lỗi API: {e}")
            return f"Bạn có biết {product_name} đang là sản phẩm hot nhất hiện nay không? Với {key_features}, đây là chân ái của bạn. Mua ngay ở link bên dưới nhé!"

if __name__ == "__main__":
    generator = ScriptGenerator()
    script = generator.generate_short_video_script(
        product_name="Bàn phím cơ không dây Xinmeng",
        key_features="Gõ cực êm, pin dùng 1 tháng, có đèn LED RGB, giá sinh viên"
    )
    print("\n--- KỊCH BẢN AI TẠO ---")
    print(script)
    print("-------------------------")
