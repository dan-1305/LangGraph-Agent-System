import pandas as pd
import numpy as np
import ta

class TechnicalEngine:
    """
    Động Cơ Giao Dịch (The Technical Engine) dựa trên Steven B. Achelis.
    Sử dụng TA-Lib / ta để xác định tín hiệu Mua/Bán.
    """
    def __init__(self):
        pass

    def analyze_trend(self, df: pd.DataFrame) -> dict:
        """
        Phân tích biểu đồ giá (df cần có cột 'close', 'high', 'low', 'volume')
        Trả về các tín hiệu kỹ thuật cốt lõi.
        """
        if df.empty or len(df) < 50:
            return {"signal": "HOLD", "reason": "Not enough data"}

        # Đảm bảo index là datetime và sắp xếp tăng dần
        df = df.copy()

        # 1. Moving Averages (Xác định Xu Hướng)
        df['sma_50'] = ta.trend.sma_indicator(df['close'], window=50)
        df['sma_200'] = ta.trend.sma_indicator(df['close'], window=200)

        # 2. RSI
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)

        # 3. Bollinger Bands
        bb = ta.volatility.BollingerBands(close=df['close'], window=20, window_dev=2)
        df['bb_lower'] = bb.bollinger_lband()
        df['bb_upper'] = bb.bollinger_hband()

        # 4. MACD
        macd = ta.trend.MACD(close=df['close'])
        df['macd_line'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()

        # Lấy dữ liệu nến mới nhất
        current = df.iloc[-1]
        prev = df.iloc[-2]

        signal = "HOLD"
        reasons = []

        # --- LUẬT MUA (BUY RULES) ---
        # Điều kiện 1: RSI Quá bán
        if current['rsi'] < 30:
            reasons.append(f"RSI Oversold ({current['rsi']:.2f} < 30)")

        # Điều kiện 2: Chạm dải dưới BB và MACD cắt lên
        if current['close'] <= current['bb_lower'] * 1.02: # Sai số 2%
            if prev['macd_line'] < prev['macd_signal'] and current['macd_line'] > current['macd_signal']:
                reasons.append("Price at Lower BB + MACD Bullish Cross")

        # Xác nhận xu hướng dài hạn (Golden Cross)
        if current['sma_50'] > current['sma_200']:
            reasons.append("Long-term Bullish Trend (SMA50 > SMA200)")

        if reasons and current['rsi'] < 40: # Cần rsi < 40 để an toàn mua
            signal = "BUY"

        # --- LUẬT BÁN (SELL RULES) ---
        sell_reasons = []
        if current['rsi'] > 70:
            sell_reasons.append(f"RSI Overbought ({current['rsi']:.2f} > 70)")
            
        if current['close'] >= current['bb_upper'] * 0.98:
            if prev['macd_line'] > prev['macd_signal'] and current['macd_line'] < current['macd_signal']:
                sell_reasons.append("Price at Upper BB + MACD Bearish Cross")

        if sell_reasons:
            signal = "SELL"
            reasons = sell_reasons

        return {
            "signal": signal,
            "reasons": reasons,
            "current_price": current['close'],
            "rsi": current['rsi'],
            "macd": current['macd_line']
        }
