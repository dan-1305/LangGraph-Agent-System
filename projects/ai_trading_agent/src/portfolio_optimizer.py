import sqlite3
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import sys
import os
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    import projects.ai_trading_agent.src.config as Config_Module
    Config = Config_Module.Config
except ImportError:
    class Config:
        DB_PATH = Path("projects/ai_trading_agent/data/trading_market.db")

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

def calculate_risk_parity_weights(returns):
    """
    Tính toán tỷ trọng theo phương pháp Risk Parity (Cân bằng rủi ro).
    Mục tiêu: Đóng góp rủi ro của mỗi tài sản vào danh mục là bằng nhau.
    """
    vols = returns.std() * np.sqrt(365)
    inv_vols = 1.0 / vols
    weights = inv_vols / np.sum(inv_vols)
    return weights

def optimize_portfolio(tickers=["BTC-USD", "ETH-USD", "SOL-USD"], days=30, method="risk_parity"):
    """
    Thực hiện tối ưu hóa danh mục. Hỗ trợ MPT (Sharpe) và Risk Parity.
    """
    print(f"🧮 Đang tối ưu hóa Danh mục ({method}) cho {days} ngày qua...")
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
    initial_guess = num_assets * [1. / num_assets,]
    
    # Chạy tối ưu hóa
    try:
        optimal_weights = initial_guess
        
        if method == "mpt":
            constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bounds = tuple((0.0, 1.0) for asset in range(num_assets))
            result = minimize(negative_sharpe_ratio, initial_guess, args=(returns,),
                              method='SLSQP', bounds=bounds, constraints=constraints)
            if not result.success:
                print("⚠️ MPT không hội tụ, chuyển sang Risk Parity.")
                method = "risk_parity"
            else:
                optimal_weights = result.x

        if method == "risk_parity":
            optimal_weights = calculate_risk_parity_weights(returns).values

        # Gắn tỷ trọng vào tên coin
        allocation = {}
        for i, col in enumerate(returns.columns):
            coin = col.split('-')[0]
            allocation[coin] = round(float(optimal_weights[i]), 4)
            
        p_ret, p_std = calculate_portfolio_performance(optimal_weights, returns)
        sharpe = (p_ret) / p_std if p_std > 0 else 0
        
        print(f"✅ Tối ưu ({method}) hoàn tất! Sharpe Ratio: {sharpe:.2f}")
        return {
            "allocation": allocation,
            "expected_return": p_ret,
            "expected_volatility": p_std,
            "sharpe_ratio": sharpe,
            "method": method
        }
    except Exception as e:
        print(f"⚠️ Lỗi trong quá trình tối ưu hóa: {e}")
        return None

if __name__ == "__main__":
    result = optimize_portfolio()
    if result:
        print("\nTỷ trọng tối ưu đề xuất:")
        for coin, weight in result["allocation"].items():
            print(f"  - {coin}: {weight*100:.1f}%")
