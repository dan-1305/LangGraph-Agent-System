import json
import random
import time
import logging

logger = logging.getLogger("DungeonMaster")

class DungeonMaster:
    """
    Hệ thống sinh kịch bản ngẫu nhiên đóng vai trò là "Thị trường" (Môi trường game).
    Sinh ra các sự kiện tin tức, giá cả, và các cú shock (như FUD, Bơm thổi).
    """
    def __init__(self):
        self.day = 1
        
        self.scenarios = [
            {"type": "FUD", "desc": "Tin đồn: SEC chuẩn bị khởi kiện một sàn giao dịch lớn. Dòng tiền tháo chạy mạnh.", "price_impact": -0.15},
            {"type": "HYPE", "desc": "Elon Musk vừa thay avatar thành một con Doge cầm Bitcoin. Dòng tiền cuồng loạn đổ vào.", "price_impact": 0.20},
            {"type": "WHALE_DUMP", "desc": "Whale Alert: 50,000 BTC vừa được đẩy lên Binance. Tường xả đã dựng sẵn.", "price_impact": -0.25},
            {"type": "MACRO_GOOD", "desc": "FED thông báo giảm lãi suất 0.5%. Chứng khoán và Crypto đều xanh mướt.", "price_impact": 0.10},
            {"type": "HACK", "desc": "Sàn giao dịch Top 3 vừa bị hack 500 triệu USD. Tâm lý sợ hãi bao trùm.", "price_impact": -0.30},
            {"type": "NORMAL", "desc": "Thị trường đi ngang, volume giao dịch thấp.", "price_impact": 0.02},
            {"type": "NORMAL", "desc": "Không có tin tức gì đặc biệt. Vài dự án nhỏ ra mắt.", "price_impact": -0.01},
        ]
        
    def generate_next_turn(self) -> dict:
        """Sinh ra dữ liệu cho 1 lượt chơi (1 ngày)."""
        scenario = random.choice(self.scenarios)
        
        state = {
            "day": self.day,
            "news": scenario["desc"],
            "market_trend": "Giảm" if scenario["price_impact"] < 0 else "Tăng",
            "hidden_price_impact": scenario["price_impact"]  # TraderHero sẽ không thấy cái này, chỉ hệ thống tính toán dùng
        }
        
        self.day += 1
        return state

    def resolve_combat(self, action: str, price_impact: float, current_capital: float) -> dict:
        """
        Tính toán PnL dựa trên quyết định của TraderHero và biến động thực tế.
        """
        # Logic tính toán đơn giản (Paper trading mini)
        pnl_pct = 0.0
        
        if action == "LONG":
            pnl_pct = price_impact
        elif action == "SHORT":
            pnl_pct = -price_impact
        else: # HOLD (USDT)
            pnl_pct = 0.0
            
        # Áp dụng đòn bẩy x2 mặc định để game thêm kịch tính
        if action in ["LONG", "SHORT"]:
            pnl_pct *= 2.0 
            
        # Liquidation (Cháy túi)
        is_liquidated = False
        if pnl_pct <= -1.0:
            pnl_pct = -1.0
            is_liquidated = True
            
        pnl_value = current_capital * pnl_pct
        new_capital = current_capital + pnl_value
        
        return {
            "action_taken": action,
            "pnl_pct": pnl_pct,
            "pnl_usd": pnl_value,
            "new_capital": new_capital,
            "is_liquidated": is_liquidated
        }
