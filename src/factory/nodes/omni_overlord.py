import sys
import io
import os
import json
import logging
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Path setup for root
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Path setup for AI Trading Agent to reuse scrapers
ai_trading_src = root_dir / "projects" / "ai_trading_agent" / "src"
if str(ai_trading_src) not in sys.path:
    sys.path.insert(0, str(ai_trading_src))

from src.factory.config import create_fallback_chain
from news_scraper import fetch_cointelegraph_news

logger = logging.getLogger("OmniOverlord")

class OmniOverlord:
    def __init__(self):
        # Sử dụng model gemini-3.1-flash-lite (Powerhorse - 500 RPD) qua Local Proxy
        self.llm = create_fallback_chain(
            model_list=["gemini-3.1-flash-lite", "gemini-3.5-flash"], 
            temperature=0.0
        )
        
    def check_market_pulse(self) -> dict:
        """
        Đọc tin tức và phân tích xem có biến cố khẩn cấp (Emergency) không.
        Trả về dictionary chứa các trigger flag.
        """
        try:
            logger.info("[Omni Overlord] Đang cào tin tức thị trường và Whale Alert...")
            news_list = fetch_cointelegraph_news(limit=5)
            news_str = "\n".join([f"- {n}" for n in news_list])
            
            prompt = f"""Bạn là THE OMNISCIENT OVERLORD, hệ thống trí tuệ nhân tạo giám sát toàn cầu.
Dưới đây là các tin tức và báo động mới nhất từ thị trường Crypto:
{news_str}

Nhiệm vụ: Phân tích các tin tức trên và quyết định xem có cần kích hoạt BẤT KỲ trạng thái khẩn cấp nào không.
1. "emergency_trading": Đặt thành true NẾU có tin tức chấn động (Sập giá mạnh, Vụ hack lớn, Bắt giữ CEO, Cảnh báo Whale rút/nạp tiền quy mô cực lớn ảnh hưởng thanh khoản).
2. "guerrilla_airdrop_boost": Đặt thành true NẾU có tin tức về việc phí Gas (Gwei) đang rất rẻ, hoặc Mạng lưới (Network) đang airdrop gấp.
3. "reason": Cung cấp lý do ngắn gọn cho quyết định của bạn (dưới 50 chữ).

TRẢ VỀ ĐÚNG ĐỊNH DẠNG JSON SAU (không có markdown code block):
{{
    "emergency_trading": false,
    "guerrilla_airdrop_boost": false,
    "reason": "Thị trường bình ổn, không có báo động đáng chú ý."
}}
"""
            
            response = self.llm.invoke(prompt)
            content = response.content
            
            # Xử lý parse JSON an toàn
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
                
            decision = json.loads(content)
            return decision
            
        except Exception as e:
            logger.error(f"[Omni Overlord] Lỗi khi phân tích thị trường: {e}")
            return {
                "emergency_trading": False,
                "guerrilla_airdrop_boost": False,
                "reason": f"Lỗi phân tích: {e}"
            }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    overlord = OmniOverlord()
    res = overlord.check_market_pulse()
    print("KẾT QUẢ TỪ OVERLORD:")
    print(json.dumps(res, indent=4, ensure_ascii=False))