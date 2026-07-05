import pytest
import pandas as pd
import numpy as np
import time
from projects.ai_trading_agent.src.validation_gate import validation_gate

def test_slippage_guard_rejects_high_volatility():
    """
    Test Case: Verify Slippage Guard rejects a proposal when market price deviates by 1.5%.
    """
    # 1. Tạo dữ liệu giả lập (Mock Data) 7 ngày
    data = {
        'close': [60000, 60100, 60200, 60300, 60400, 60500, 61000],
        'high': [61000] * 7,
        'low': [59000] * 7
    }
    df = pd.DataFrame(data)
    
    # Giả sử giá phân tích cuối cùng là 61000 (df.iloc[-1])
    # Nhưng giá thị trường thực tế vọt lên 62000 (Trượt ~1.6%)
    market_price = 62000 
    
    proposal = {
        "allocation": {"BTC": 0.5, "USDT": 0.5},
        "reasoning": "Test buy signal"
    }

    # 2. Thực thi Validation Gate và đo lường thời gian
    start_time = time.time()
    result = validation_gate.validate_proposal(df, proposal, market_price=market_price)
    latency = time.time() - start_time

    # 3. Kiểm chứng (Assertions)
    assert result["status"] == "REJECT", "Gate should reject high slippage"
    assert "Slippage Guard" in result["reason"], "Reason should mention Slippage Guard"
    assert latency < 1.0, f"Latency too high: {latency:.2f}s"
    
    print(f"\n[Test] Slippage Guard Test PASSED. Latency: {latency:.4f}s")

def test_trend_filter_rejects_downtrend():
    """
    Test Case: Verify Trend Filter rejects a buy proposal during a downtrend (Price < SMA 50).
    """
    # Tạo trend giảm (Giá liên tục dưới SMA 50)
    prices = [65000] * 50 + [60000] * 7 # SMA 50 sẽ cao hơn 60000
    df = pd.DataFrame({'close': prices})
    
    proposal = {
        "allocation": {"BTC": 0.8, "USDT": 0.2}
    }
    
    result = validation_gate.validate_proposal(df, proposal)
    
    assert result["status"] == "REJECT"
    assert "nằm dưới SMA 50" in result["reason"]
    print("[Test] Trend Filter Test PASSED.")
