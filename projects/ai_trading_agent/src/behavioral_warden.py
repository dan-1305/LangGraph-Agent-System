class BehavioralWarden:
    """
    Cầu Dao Tâm Lý (The Behavioral Warden).
    Kiểm soát rủi ro dựa trên tài chính hành vi, chặn đứng các quyết định
    cảm xúc của LLM hoặc sự cố API.
    """
    def __init__(self, stop_loss_pct=0.05, take_profit_pct=0.15, trailing_stop_pct=0.05):
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.trailing_stop_pct = trailing_stop_pct
        
    def evaluate_position(self, entry_price: float, current_price: float, highest_price_since_entry: float) -> dict:
        """
        Đánh giá trạng thái lệnh hiện tại (Long position).
        Trả về 'HOLD' hoặc 'SELL' kèm lý do.
        """
        if entry_price <= 0:
            return {"action": "HOLD", "reason": "No active position"}
            
        pnl_pct = (current_price - entry_price) / entry_price
        
        # Cấm gồng lỗ: Stop-Loss cứng
        if pnl_pct <= -self.stop_loss_pct:
            return {
                "action": "SELL",
                "reason": f"Hard Stop-Loss Triggered ({pnl_pct*100:.2f}% <= -{self.stop_loss_pct*100}%)"
            }
            
        # Cấm chốt lời non: Trailing Stop-Loss
        # Khi giá lên quá Take Profit, nâng stop loss dần
        if highest_price_since_entry > entry_price * (1 + self.take_profit_pct):
            trailing_stop_price = highest_price_since_entry * (1 - self.trailing_stop_pct)
            if current_price <= trailing_stop_price:
                return {
                    "action": "SELL",
                    "reason": f"Trailing Stop-Loss Triggered at ${current_price:.2f} (Peak was ${highest_price_since_entry:.2f})"
                }
                
        return {"action": "HOLD", "reason": f"Position healthy. PnL: {pnl_pct*100:.2f}%"}

    def check_overtrading(self, consecutive_losses: int) -> bool:
        """
        Khóa tài khoản nếu thua lỗ 3 lệnh liên tiếp.
        """
        if consecutive_losses >= 3:
            return False # Stop trading
        return True
