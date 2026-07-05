import sqlite3
import pandas as pd
import numpy as np
import time
import config as Config_Module
Config = Config_Module.Config

_PRICE_CACHE = {}
_LAST_CACHE_TIME = 0

def get_cached_prices(coins, days):
    global _PRICE_CACHE, _LAST_CACHE_TIME
    current_time = time.time()
    
    # Check if cache is valid (5 minutes) and contains all requested coins
    missing_coins = [c for c in coins if c not in _PRICE_CACHE]
    
    if current_time - _LAST_CACHE_TIME < 300 and not missing_coins:
        return {c: _PRICE_CACHE[c] for c in coins if c in _PRICE_CACHE}
        
    db_path = Config.DB_PATH
    if not db_path.exists():
        return {}
        
    conn = sqlite3.connect(db_path, timeout=20.0)
    conn.execute('PRAGMA journal_mode=WAL;')
    
    new_prices = {}
    # Chỉ query những coin bị thiếu hoặc nếu cache hết hạn thì query lại toàn bộ
    coins_to_fetch = coins if current_time - _LAST_CACHE_TIME >= 300 else missing_coins
    
    for coin in coins_to_fetch:
        table_name = f"{coin}_USD"
        try:
            query = f"SELECT Date, Close FROM {table_name} ORDER BY Date DESC LIMIT {days + 1}"
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date').set_index('Date')
                new_prices[coin] = df['Close']
        except Exception:
            pass
            
    conn.close()
    
    # Update cache
    _PRICE_CACHE.update(new_prices)
    _LAST_CACHE_TIME = current_time
    
    return {c: _PRICE_CACHE[c] for c in coins if c in _PRICE_CACHE}

def run_mini_backtest(allocation_dict, days=7):
    """
    Chạy mini-backtest trên dữ liệu `days` ngày qua với tỷ trọng `allocation_dict`.
    Trả về Dict chứa:
    - total_return_pct: % lợi nhuận
    - sharpe_ratio: Sharpe Ratio (annualized)
    - max_drawdown_pct: % sụt giảm tối đa
    - is_passed: boolean (True nếu chiến lược đủ an toàn)
    """
    db_path = Config.DB_PATH
    
    if not db_path.exists():
        return {"error": "Không tìm thấy database để backtest", "is_passed": True}
        
    # Gom data giá Close của các coin từ Cache RAM
    coins = [c for c in allocation_dict.keys() if c != "USDT"]
    prices = get_cached_prices(coins, days)
    
    if not prices:
        return {"error": "Không lấy được giá để backtest", "is_passed": True}
        
    price_df = pd.DataFrame(prices)
    
    # Tính daily returns của từng coin
    daily_returns = price_df.pct_change().dropna()
    
    if daily_returns.empty:
        return {"error": "Không đủ data tính return", "is_passed": True}
        
    # Tính daily returns của Portfolio
    portfolio_daily_returns = pd.Series(0.0, index=daily_returns.index)
    
    for coin, weight in allocation_dict.items():
        if coin == "USDT":
            continue
        if coin in daily_returns.columns:
            portfolio_daily_returns += daily_returns[coin] * weight
            
    # Tính các metrics
    total_return = (1 + portfolio_daily_returns).prod() - 1
    total_return_pct = total_return * 100
    
    mean_return = portfolio_daily_returns.mean()
    std_return = portfolio_daily_returns.std()
    
    # Sharpe Ratio giả định risk-free rate = 0 (annualized)
    if std_return > 0:
        sharpe_ratio = (mean_return / std_return) * np.sqrt(365)
    else:
        sharpe_ratio = 0.0
        
    # Tính Max Drawdown
    cumulative_returns = (1 + portfolio_daily_returns).cumprod()
    rolling_max = cumulative_returns.cummax()
    drawdown = (cumulative_returns - rolling_max) / rolling_max
    max_drawdown_pct = drawdown.min() * 100
    
    # Điều kiện Validation Gate
    # Ví dụ: Mức return 7 ngày < -5% hoặc Sharpe < -1.0 thì chặn
    is_passed = True
    if total_return_pct < -5.0 or sharpe_ratio < -1.0:
        is_passed = False
        
    return {
        "total_return_pct": total_return_pct,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown_pct": max_drawdown_pct,
        "is_passed": is_passed
    }

if __name__ == "__main__":
    mock_allocation = {"BTC": 0.4, "ETH": 0.3, "SOL": 0.1, "USDT": 0.2}
    result = run_mini_backtest(mock_allocation)
    print(f"Backtest Result: {result}")
