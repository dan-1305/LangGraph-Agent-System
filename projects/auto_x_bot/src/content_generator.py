import sys
from pathlib import Path

# Thêm base_dir để import các module cốt lõi
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.factory.config import create_fallback_chain

class ContentGenerator:
    def __init__(self):
        # Dùng model xịn để viết văn sáng tạo
        self.llm = create_fallback_chain(
            model_list=["gemini-2.5-pro", "gemini-2.5-flash"], 
            temperature=0.8
        )

    def generate_crypto_tweet(self, news_items: list) -> str:
        """
        Dựa vào danh sách tin tức, suy nghĩ ra 1 dòng Tweet duy nhất cực kỳ viral,
        chuẩn phong cách Crypto Twitter (có emoji, hashtags #Crypto #Bitcoin).
        Không dài quá 280 ký tự.
        """
        news_str = "\n".join(news_items)
        prompt = f"""Bạn là một chuyên gia tạo Content trên mạng xã hội X (Twitter) trong mảng Tiền mã hóa (Crypto).
Dưới đây là một số tin tức mới nhất vừa thu thập được từ CoinTelegraph:
{news_str}

Nhiệm vụ của bạn:
- Hãy chọn 1-2 tin tức ĐÁNG CHÚ Ý NHẤT trong danh sách trên.
- Viết MỘT (01) bài Tweet ngắn gọn, súc tích, mang tính chất "giật gân", "shill" hoặc phân tích góc nhìn sâu sắc để câu tương tác (Like, Repost).
- Độ dài TUYỆT ĐỐI không vượt quá 280 ký tự.
- Bắt buộc có Emoji phù hợp và hashtags (ví dụ #Crypto #BTC #ETH).
- Văn phong: Cá tính, sắc bén, mang phong cách Crypto Twitter. Ngôn ngữ Tiếng Việt.

CHỈ TRẢ VỀ NỘI DUNG TWEET, KHÔNG CẦN GIẢI THÍCH THÊM."""

        try:
            response = self.llm.invoke(prompt)
            tweet = response.content.strip()
            # Bỏ ngoặc kép nếu LLM tự sinh ra
            if tweet.startswith('"') and tweet.endswith('"'):
                tweet = tweet[1:-1]
            return tweet
        except Exception as e:
            print(f"❌ Lỗi sinh Tweet: {e}")
            return "Hôm nay thị trường #Crypto biến động quá! AE đã chuẩn bị tâm lý chưa? 🚀 #Bitcoin #Trading"
