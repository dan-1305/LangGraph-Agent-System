import pandas as pd
import numpy as np
import ta

class TechnicalEngine:
    """
    ⚡ SOVEREIGN HIGH-PERFORMANCE ENGINE ⚡
    Định vị: Strategic Swing Trading Advisor.
    Tiêu chuẩn: Mark Minervini Stage 2 Trend Template.
    Tối ưu: Pandas Vectorization (< 1s execution).
    """
    def __init__(self):
        pass

    def analyze_trend(self, df: pd.DataFrame) -> dict:
        """
        Phân tích theo chuẩn Minervini Stage 2 (Uptrend mạnh).
        Sử dụng Vectorization để đạt hiệu năng tối đa.
        """
        if df.empty or len(df) < 200:
            return {"signal": "WAIT", "reason": "Cần ít nhất 200 nến để xác định Stage 2 (SMA 200)."}

        df = df.copy()
        
        # --- [Phase 1: Vectorized Indicator Calculation] ---
        df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
        df['sma_150'] = ta.trend.sma_indicator(df['close'], window=150)
        df['sma_200'] = ta.trend.sma_indicator(df['close'], window=200)
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        
        # Lấy đỉnh/đáy 52 tuần để tính Margin of Safety
        high_52w = df['high'].rolling(window=252, min_periods=1).max()
        low_52w = df['low'].rolling(window=252, min_periods=1).min()
        
        # --- [Phase 2: Minervini Trend Template Validation] ---
        # 1. Giá hiện tại nằm trên SMA 150 và SMA 200
        cond1 = (df['close'] > df['sma_150']) & (df['close'] > df['sma_200'])
        # 2. SMA 150 nằm trên SMA 200
        cond2 = df['sma_150'] > df['sma_200']
        # 3. SMA 200 đang hướng lên (ít nhất trong 1 tháng/20 phiên)
        df['sma_200_prev'] = df['sma_200'].shift(20)
        cond3 = df['sma_200'] > df['sma_200_prev']
        # 4. SMA 50 nằm trên SMA 150 và SMA 200
        cond4 = (df['sma_50'] > df['sma_150']) & (df['sma_50'] > df['sma_200'])
        # 5. Giá hiện tại cao hơn đáy 52 tuần ít nhất 25% (Hàng dẫn dắt)
        cond5 = df['close'] >= (low_52w * 1.25)
        # 6. Giá hiện tại nằm trong vùng 25% của đỉnh 52 tuần (Đang tích lũy đỉnh)
        cond6 = df['close'] >= (high_52w * 0.75)

        # Hợp nhất tất cả điều kiện để xác định Stage 2
        df['is_stage_2'] = cond1 & cond2 & cond3 & cond4 & cond5 & cond6

        # --- [Phase 3: Decision Extraction] ---
        current = df.iloc[-1]
        
        signal = "HOLD"
        reasons = []
        
        if current['is_stage_2']:
            signal = "WATCHLIST/BUY"
            reasons.append("Confirm Stage 2 Uptrend (Minervini Template)")
            if current['rsi'] < 65: # Chờ nhịp nghỉ để vào hàng
                reasons.append("RSI is Healthy for Entry (< 65)")
        else:
            # Check rủi ro sụp đổ (Stage 4)
            if current['close'] < current['sma_200']:
                signal = "AVOID/SELL"
                reasons.append("Risk of Stage 4 Downtrend (Price < SMA 200)")

        return {
            "signal": signal,
            "reasons": reasons,
            "metrics": {
                "price": current['close'],
                "sma_50": current['sma_50'],
                "sma_200": current['sma_200'],
                "rsi": current['rsi'],
                "dist_from_low_52w": f"{((current['close']/current.name)-1)*100:.2f}%" if hasattr(current, 'name') and isinstance(current.name, (int, float)) else "N/A"
            },
            "philosophy": "Swing Trading / Strategic Advisor"
        }

# Singleton instance
engine = TechnicalEngine()
