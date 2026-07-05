import sqlite3
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import config as Config_Module
Config = Config_Module.Config

def get_historical_prices(tickers, days=30):
    """Lấy dữ liệu giá đóng cửa lịch sử từ DB."""
    db_path = Config.DB_PATH
    
    if not db_path.exists():
        return None
        
    conn = sqlite3.connect(db_path, timeout=20.0)
    conn.execute('PRAGMA journal_mode=WAL;')
    prices = {}
    
    for ticker in tickers:
        table_name = ticker.replace("-", "_")
        try:
            query = f"SELECT Date, Close FROM {table_name} ORDER BY Date DESC LIMIT {days}"
            df = pd.read_sql_query(query, conn)
            if not df.empty:
                df['Date'] = pd.to_datetime(df['Date'])
                df = df.sort_values('Date').set_index('Date')
                prices[ticker] = df['Close']
        except Exception as e:
            print(f"⚠️ Lỗi lấy dữ liệu {ticker}: {e}")
            
    conn.close()
    
    if not prices:
        return None
        
    return pd.DataFrame(prices)

def calculate_portfolio_performance(weights, returns):
    """Tính toán lợi nhuận và rủi ro của danh mục."""
    portfolio_return = np.sum(returns.mean() * weights) * 365
    portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 365, weights)))
    return portfolio_return, portfolio_std_dev

def negative_sharpe_ratio(weights, returns, risk_free_rate=0):
    """Hàm mục tiêu để minimize (tìm Sharpe cao nhất)."""
    p_ret, p_std = calculate_portfolio_performance(weights, returns)
    if p_std == 0:
        return 0
    return -(p_ret - risk_free_rate) / p_std

def optimize_portfolio(tickers=["BTC-USD", "ETH-USD", "SOL-USD"], days=30):
    """
    Thực hiện Mean-Variance Optimization để tìm tỷ trọng tối ưu.
    """
    print(f"🧮 Đang tính toán Tỷ trọng Tối ưu (MPT) cho {days} ngày qua...")
    price_df = get_historical_prices(tickers, days)
    
    if price_df is None or price_df.empty:
        print("❌ Không đủ dữ liệu để tối ưu hóa.")
        return None
        
    # Tính daily returns
    returns = price_df.pct_change().dropna()
    num_assets = len(returns.columns)
    
    if num_assets == 0:
        return None
        
    # Thiết lập tham số cho scipy.optimize
    args = (returns,)
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1}) # Tổng tỷ trọng = 1
    bounds = tuple((0.0, 1.0) for asset in range(num_assets)) # Tỷ trọng từ 0 đến 1
    initial_guess = num_assets * [1. / num_assets,] # Khởi tạo chia đều
    
    # Chạy tối ưu hóa
    try:
        result = minimize(negative_sharpe_ratio, initial_guess, args=args,
                          method='SLSQP', bounds=bounds, constraints=constraints)
                          
        if result.success:
            optimal_weights = result.x
            
            # Gắn tỷ trọng vào tên coin
            allocation = {}
            for i, col in enumerate(returns.columns):
                # Clean name (e.g., BTC-USD -> BTC)
                coin = col.split('-')[0]
                allocation[coin] = round(optimal_weights[i], 4)
                
            p_ret, p_std = calculate_portfolio_performance(optimal_weights, returns)
            sharpe = (p_ret) / p_std if p_std > 0 else 0
            
            print(f"✅ Tối ưu hoàn tất! Sharpe Ratio kỳ vọng: {sharpe:.2f}")
            return {
                "allocation": allocation,
                "expected_return": p_ret,
                "expected_volatility": p_std,
                "sharpe_ratio": sharpe
            }
        else:
            print("⚠️ Tối ưu hóa không hội tụ.")
            return None
    except Exception as e:
        print(f"⚠️ Lỗi trong quá trình tối ưu hóa: {e}")
        return None

if __name__ == "__main__":
    result = optimize_portfolio()
    if result:
        print("\nTỷ trọng tối ưu đề xuất:")
        for coin, weight in result["allocation"].items():
            print(f"  - {coin}: {weight*100:.1f}%")
