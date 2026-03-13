import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# Load biến môi trường từ thư mục gốc
base_dir = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(base_dir / ".env")

class ScriptGenerator:
    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("GCLI_BASE_URL"),
            api_key=os.getenv("GCLI_API_KEY")
        )
        self.model = "gemini-2.5-flash"  # Sử dụng gemini-2.5-flash cho viết kịch bản nhanh/rẻ

    def generate_short_video_script(self, product_name: str, key_features: str) -> str:
        """
        Dùng OpenAI/Gemini để viết kịch bản video ngắn (dưới 60s) cho TikTok/Shorts.
        Áp dụng quy tắc Hook của sách Zero to Hero và Sức mạnh Ngôn từ.
        """
        print(f"✍️ Đang viết kịch bản AI cho sản phẩm: {product_name}...")
        
        system_prompt = """Bạn là một chuyên gia sáng tạo nội dung video ngắn (TikTok, YouTube Shorts, Reels) và là một bậc thầy về Affiliate Marketing.
Luật viết kịch bản:
1. Độ dài tối đa: 130-150 từ (để đọc vừa vặn trong 60 giây).
2. BẮT BUỘC bắt đầu bằng một câu 'HOOK' cực mạnh trong 3 giây đầu tiên (đặt câu hỏi sốc, nêu một nỗi đau thực tế của khách hàng).
3. KHÔNG chào hỏi rườm rà. Đi thẳng vào vấn đề.
4. Nêu 2-3 tính năng hoặc lợi ích chính của sản phẩm.
5. Kết thúc BẮT BUỘC bằng một Lời kêu gọi hành động (Call to Action - CTA) ngắn gọn, ví dụ: 'Bấm ngay vào link bên dưới để mua nhé!'.
6. Trả về DUY NHẤT nội dung lời thoại (Text), không bao gồm mô tả cảnh quay hay hành động."""

        user_prompt = f"""
Sản phẩm: {product_name}
Tính năng/Điểm nổi bật: {key_features}
Hãy viết kịch bản lời thoại ngay bây giờ.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7
            )
            script = response.choices[0].message.content.strip()
            return script
        except Exception as e:
            print(f"❌ Lỗi khi gọi AI API: {e}")
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