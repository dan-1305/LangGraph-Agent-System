import sys
import os
import json
import logging
import io
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Path setup for root
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.config import create_fallback_chain

logger = logging.getLogger("TraderHero")

class TraderHero:
    """
    AI Agent đóng vai trò Trader. Nó sẽ nhận dữ liệu môi trường từ Dungeon Master,
    sau đó ra quyết định LONG/SHORT/HOLD.
    Nó cũng có "Nhật ký sinh tồn" (Memory) để học hỏi.
    """
    def __init__(self):
        self.llm = create_fallback_chain(
            model_list=["gemini-2.5-flash", "gemini-2.5-flash-lite"], 
            temperature=0.7  # Để AI sáng tạo và có rủi ro
        )
        self.memory = []  # Ký ức các lượt chơi trước
        
    def make_decision(self, state: dict, current_capital: float) -> dict:
        """Đưa ra quyết định dựa trên tin tức hiện tại và ký ức."""
        
        # Nhắc lại ký ức
        memory_str = "Chưa có ký ức."
        if self.memory:
            memory_str = "\n".join(self.memory[-3:]) # Nhớ 3 bài học gần nhất
            
        prompt = f"""Bạn là một TRADER SINH TỒN trong thế giới Crypto cực kỳ khắc nghiệt.
Vốn hiện tại: ${current_capital:,.2f}
Ngày thứ: {state['day']}

[TIN TỨC THỊ TRƯỜNG TRONG NGÀY]
{state['news']}

[KÝ ỨC CỦA BẠN TỪ NHỮNG NGÀY TRƯỚC]
{memory_str}

Nhiệm vụ: Dựa vào Tin tức và Ký ức, hãy ra quyết định giao dịch cho ngày hôm nay (Đòn bẩy mặc định x2).
1. "action": Chọn một trong 3 hành động: "LONG", "SHORT", "HOLD".
2. "reason": Cung cấp lý do giải thích (như đang độc thoại nội tâm).

TRẢ VỀ ĐÚNG ĐỊNH DẠNG JSON SAU:
{{
    "action": "LONG",
    "reason": "Tin tức quá xấu, tôi nghĩ thị trường sẽ tiếp tục bán tháo."
}}
"""
        try:
            response = self.llm.invoke(prompt)
            content = response.content
            
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "{" in content and "}" in content:
                content = content[content.find("{"):content.rfind("}")+1]
                
            decision = json.loads(content)
            
            if decision["action"] not in ["LONG", "SHORT", "HOLD"]:
                decision["action"] = "HOLD"
                
            return decision
            
        except Exception as e:
            logger.error(f"[TraderHero] Bị rối loạn tâm lý (Lỗi API/Parse): {e}")
            return {
                "action": "HOLD",
                "reason": "Tôi quá hoảng sợ, quyết định đứng ngoài quan sát."
            }
            
    def reflect_and_learn(self, combat_result: dict, news: str):
        """Đúc kết kinh nghiệm sau mỗi trận đấu (ngày)."""
        action = combat_result["action_taken"]
        pnl_pct = combat_result["pnl_pct"]
        
        if combat_result["is_liquidated"]:
            lesson = f"BÀI HỌC MÁU: Ngày có tin '{news}', tôi đã {action} và BỊ CHÁY TÀI KHOẢN! Từ nay phải cẩn thận với tin này."
        elif pnl_pct < -0.1:
            lesson = f"BÀI HỌC: Ngày có tin '{news}', tôi đã {action} và LỖ NẶNG. Hành động này là sai lầm."
        elif pnl_pct > 0.1:
            lesson = f"BÀI HỌC: Ngày có tin '{news}', tôi đã {action} và LỜI ĐẬM. Đây là một chiến thuật tốt."
        else:
            return # Không học gì thêm
            
        self.memory.append(lesson)
        logger.info(f"🧠 [TraderHero đúc kết]: {lesson}")

if __name__ == "__main__":
    from dungeon_master import DungeonMaster
    
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    print("=============================================")
    print("⚔️ TRADING RPG SIMULATOR: SURVIVAL DUNGEON ⚔️")
    print("=============================================\n")
    
    dm = DungeonMaster()
    hero = TraderHero()
    
    capital = 1000.0
    
    for _ in range(5): # Chơi thử 5 ngày
        print(f"\n--- NGÀY {dm.day} ---")
        state = dm.generate_next_turn()
        print(f"📜 Sự kiện: {state['news']}")
        
        decision = hero.make_decision(state, capital)
        print(f"🦸 Trader hành động: {decision['action']}")
        print(f"💭 Nội tâm: {decision['reason']}")
        
        result = dm.resolve_combat(decision["action"], state["hidden_price_impact"], capital)
        capital = result["new_capital"]
        
        print(f"💥 Kết quả: Lợi nhuận {result['pnl_pct']*100:.1f}%. Vốn còn lại: ${capital:,.2f}")
        
        hero.reflect_and_learn(result, state["news"])
        
        if result["is_liquidated"]:
            print("☠️ GAME OVER. TRADER ĐÃ CHÁY TÀI KHOẢN!")
            break
            
        time.sleep(1)
    
    print(f"\n🏆 KẾT THÚC GAME. Vốn cuối cùng: ${capital:,.2f}")