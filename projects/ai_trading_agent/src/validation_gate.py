import pandas as pd
import numpy as np

class ValidationGate:
    """
    🛡️ SOVEREIGN VALIDATION GATE (Tier 1 Protection)
    Nhiệm vụ: Chặn đứng các lệnh 'Rác phẩm' bằng Mini-backtest 7 ngày.
    Hiệu năng: Pandas Vectorization (< 1s).
    Tính năng: Slippage Guard (< 0.5%) tích hợp.
    """
    def __init__(self):
        # Ngưỡng giá hợp lý (Sanity Bounds) để chặn dữ liệu rác/thao túng
        self.price_bounds = {
            "BTC": (15000, 250000),
            "ETH": (800, 15000),
            "SOL": (10, 1000)
        }

    def check_data_integrity(self, ticker: str, current_price: float) -> bool:
        """
        [VULN-003] Kiểm tra tính toàn vẹn của dữ liệu (Sanity Check).
        Ngăn chặn ChaosMonkey tiêm giá ảo vào Database.
        """
        base_ticker = ticker.split("-")[0]
        if base_ticker in self.price_bounds:
            low, high = self.price_bounds[base_ticker]
            if not (low <= current_price <= high):
                print(f"⚠️ [INTEGRITY ALERT] Phát hiện giá bất thường cho {ticker}: {current_price}. Ngưỡng cho phép: {low}-{high}")
                return False
        return True

    def validate_proposal(self, df: pd.DataFrame, proposal: dict, market_price: float = None) -> dict:
        """
        Kiểm tra đề xuất lệnh dựa trên dữ liệu 7 ngày và Slippage Guard.
        """
        if df.empty or len(df) < 7:
            return {"status": "REJECT", "reason": "Không đủ dữ liệu 7 ngày để validate."}

        # --- [1. Trend Filter] ---
        # Sử dụng Vectorization để tính SMA nhanh
        df['sma_50'] = df['close'].rolling(window=50, min_periods=1).mean()
        
        last_7_days = df.tail(7)
        avg_close = last_7_days['close'].mean()
        avg_sma = last_7_days['sma_50'].mean()
        
        is_uptrend = avg_close > avg_sma
        
        # --- [2. Slippage Guard (< 0.5%)] ---
        analysis_price = df.iloc[-1]['close']
        slippage = 0.0
        if market_price:
            slippage = abs(market_price - analysis_price) / analysis_price
        
        # --- [3. Decision Logic] ---
        allocation = proposal.get("allocation", {})
        has_buy = any(v > 0 for k, v in allocation.items() if k != "USDT")
        
        if has_buy:
            if not is_uptrend:
                return {
                    "status": "REJECT",
                    "reason": f"Phát hiện rủi ro: Giá trung bình 7 ngày ({avg_close:.2f}) nằm dưới SMA 50 ({avg_sma:.2f}). Lệnh mua bị từ chối để bảo vệ vốn.",
                    "metrics": {"avg_7d": avg_close, "sma_50": avg_sma}
                }
            
            if slippage > 0.005: # 0.5%
                return {
                    "status": "REJECT",
                    "reason": f"HỦY LỆNH (Slippage Guard): Độ trượt giá quá cao ({slippage*100:.2f}% > 0.5%). Thị trường biến động quá nhanh hoặc hệ thống lag.",
                    "metrics": {"slippage": slippage, "analysis_price": analysis_price, "market_price": market_price}
                }
            
        return {
            "status": "PASS",
            "reason": "Đề xuất vượt qua bài kiểm tra Mini-backtest 7 ngày và Slippage Guard.",
            "metrics": {"avg_7d": avg_close, "slippage": slippage}
        }

validation_gate = ValidationGate()
