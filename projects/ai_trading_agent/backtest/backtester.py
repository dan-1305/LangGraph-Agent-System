import sys
import pandas as pd
from pathlib import Path
import warnings
import sqlite3
import numpy as np
import time

# Bỏ qua cảnh báo Pydantic
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')

# Thêm src vào path
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))
src_dir = base_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))
    
root_dir = base_dir.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from langgraph_agent import MultiAgentTradingSystem

def run_multi_asset_backtest(initial_capital=10000.0, max_days=14, trading_fee=0.001):
    """
    Backtest chiến lược Multi-Agent (Portfolio Allocation) so với Benchmark (HODL BTC).
    """
    print(f"🚀 BẮT ĐẦU BACKTEST MULTI-ASSET ({max_days} ngày | Vốn: ${initial_capital:,})")
    
    db_path = base_dir.parent.parent / "data" / "trading_market.db"
    if not db_path.exists():
        print("❌ Không tìm thấy database.")
        return
        
    conn = sqlite3.connect(db_path)
    
    # Load data
    tickers = ["BTC", "ETH", "SOL"]
    dfs = {}
    for t in tickers:
        table_name = f"{t}_USD"
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name} ORDER BY Date", conn)
            df['Date'] = pd.to_datetime(df['Date'])
            dfs[t] = df.set_index('Date')
        except Exception as e:
            print(f"Lỗi load {t}: {e}")
    conn.close()
    
    if not dfs:
        return
        
    # Lấy common dates
    common_dates = dfs["BTC"].index
    for t in tickers[1:]:
        common_dates = common_dates.intersection(dfs[t].index)
        
    common_dates = common_dates.sort_values()
    
    # Cắt lấy max_days cuối cùng (có trừ đi window 5 ngày để lấy data)
    window_size = 5
    if len(common_dates) > max_days + window_size:
        test_dates = common_dates[-(max_days):]
    else:
        test_dates = common_dates[window_size:]
        
    print(f"📅 Giai đoạn test: {test_dates[0].strftime('%Y-%m-%d')} đến {test_dates[-1].strftime('%Y-%m-%d')}")
    
    agent = MultiAgentTradingSystem()
    
    # Portfolio AI Strategy
    portfolio = {"USDT": initial_capital, "BTC": 0.0, "ETH": 0.0, "SOL": 0.0}
    ai_history = []
    
    # Portfolio HODL Benchmark (100% BTC từ ngày đầu)
    start_btc_price = dfs["BTC"].loc[test_dates[0]]['Close']
    hodl_btc_amount = (initial_capital * (1 - trading_fee)) / start_btc_price
    hodl_history = []
    
    for i, current_date in enumerate(test_dates):
        print(f"\n--- Ngày {current_date.strftime('%Y-%m-%d')} ---")
        
        # 1. Tính giá trị danh mục hiện tại (trước khi rebalance)
        current_prices = {t: dfs[t].loc[current_date]['Close'] for t in tickers}
        current_total_value = portfolio["USDT"]
        for t in tickers:
            current_total_value += portfolio[t] * current_prices[t]
            
        # Tính Benchmark Value
        benchmark_value = hodl_btc_amount * current_prices["BTC"]
        hodl_history.append(benchmark_value)
        
        print(f"💰 AI Portfolio: ${current_total_value:,.2f} | HODL BTC: ${benchmark_value:,.2f}")
        
        # 2. Tạo context cho AI
        idx_in_common = common_dates.get_loc(current_date)
        hist_dates = common_dates[idx_in_common - window_size + 1 : idx_in_common + 1]
        
        multi_asset_data_str = ""
        fundamental_str = "--- BASIC FUNDAMENTALS ---\n"
        for t in tickers:
            recent_df = dfs[t].loc[hist_dates]
            multi_asset_data_str += f"\n--- {t}-USD ---\n"
            multi_asset_data_str += recent_df[['Close', 'Volume', 'SMA_20', 'RSI_14']].to_string() + "\n"
            
            # Giả lập Fundamental đơn giản
            curr_p = recent_df['Close'].iloc[-1]
            max_p = dfs[t].loc[:current_date]['Close'].max()
            dd = (max_p - curr_p) / max_p * 100
            fundamental_str += f"{t}: Giá ${curr_p:.2f} | Đỉnh cao nhất ${max_p:.2f} | Mức giảm: -{dd:.2f}%\n"

        # 3. AI ra quyết định (Thêm delay để tránh Rate Limit)
        print("🧠 Đang gọi AI Agent...")
        try:
            decision = agent.analyze_and_trade(
                multi_asset_data_str, 
                portfolio, 
                news_list=["Thị trường biến động lịch sử"], 
                fundamental_data=fundamental_str
            )
            time.sleep(3) # Tránh Rate Limit Gemini
        except Exception as e:
            print(f"⚠️ Lỗi AI, tự động Hold: {e}")
            decision = {"allocation": {}}
            
        allocation = decision.get("allocation", {})
        if not allocation:
            print("⚪ HOLD (Giữ nguyên danh mục)")
            ai_history.append(current_total_value)
            continue
            
        # SMART SIZING (Giả lập đơn giản) & REBALANCING TRIGGER (15%)
        # Tính tỷ trọng hiện tại
        current_weights = {"USDT": portfolio["USDT"] / current_total_value if current_total_value > 0 else 0}
        for t in tickers:
            current_weights[t] = (portfolio[t] * current_prices[t]) / current_total_value if current_total_value > 0 else 0
            
        target_weights = allocation.copy()
        
        # Kiểm tra độ lệch
        max_dev = 0
        for k in target_weights.keys():
            dev = abs(target_weights[k] - current_weights.get(k, 0))
            if dev > max_dev: max_dev = dev
            
        if max_dev < 0.15:
            print(f"⚖️ BỎ QUA REBALANCE (Độ lệch cực đại {max_dev*100:.1f}% < 15%)")
            ai_history.append(current_total_value)
            continue
            
        # THỰC THI REBALANCE
        print(f"🔄 THỰC THI REBALANCE (Độ lệch {max_dev*100:.1f}%)")
        new_portfolio = {"USDT": 0.0, "BTC": 0.0, "ETH": 0.0, "SOL": 0.0}
        new_total_value = current_total_value
        
        for coin, w in target_weights.items():
            target_usd = current_total_value * w
            if coin == "USDT":
                new_portfolio["USDT"] = target_usd
            else:
                amount = target_usd / current_prices[coin]
                # Trừ phí giao dịch giả định cho phần chênh lệch mua bán
                diff_usd = abs(target_usd - (current_weights.get(coin, 0) * current_total_value))
                fee = diff_usd * trading_fee
                new_total_value -= fee
                new_portfolio[coin] = amount
                print(f"  - {coin}: {w*100:.1f}% (~${target_usd:.2f})")
                
        portfolio = new_portfolio
        ai_history.append(new_total_value)

    # ==== TỔNG KẾT BÁO CÁO ====
    final_ai = ai_history[-1]
    final_hodl = hodl_history[-1]
    
    ai_roi = (final_ai - initial_capital) / initial_capital * 100
    hodl_roi = (final_hodl - initial_capital) / initial_capital * 100
    alpha = ai_roi - hodl_roi
    
    # Tính Sharpe
    ai_returns = pd.Series(ai_history).pct_change().dropna()
    hodl_returns = pd.Series(hodl_history).pct_change().dropna()
    
    ai_sharpe = (ai_returns.mean() / ai_returns.std()) * np.sqrt(365) if ai_returns.std() > 0 else 0
    hodl_sharpe = (hodl_returns.mean() / hodl_returns.std()) * np.sqrt(365) if hodl_returns.std() > 0 else 0
    
    # Tính Max Drawdown
    ai_cum = (1 + ai_returns).cumprod()
    ai_dd = (ai_cum - ai_cum.cummax()) / ai_cum.cummax()
    ai_max_dd = ai_dd.min() * 100 if not ai_dd.empty else 0
    
    hodl_cum = (1 + hodl_returns).cumprod()
    hodl_dd = (hodl_cum - hodl_cum.cummax()) / hodl_cum.cummax()
    hodl_max_dd = hodl_dd.min() * 100 if not hodl_dd.empty else 0

    print("\n=========================================")
    print("🏆 KẾT QUẢ SO SÁNH (AI STRATEGY vs HODL BTC)")
    print("=========================================")
    print("Chỉ số             | AI Portfolio    | HODL BTC")
    print("-------------------|-----------------|---------")
    print(f"Vốn cuối cùng      | ${final_ai:,.2f}      | ${final_hodl:,.2f}")
    print(f"Tỷ suất lợi nhuận  | {ai_roi:+.2f}%          | {hodl_roi:+.2f}%")
    print(f"Sharpe Ratio       | {ai_sharpe:.2f}            | {hodl_sharpe:.2f}")
    print(f"Max Drawdown       | {ai_max_dd:.2f}%          | {hodl_max_dd:.2f}%")
    print("=========================================")
    if alpha > 0:
        print(f"🎉 CHIẾN THẮNG! Hệ thống AI tạo ra Alpha = {alpha:+.2f}% so với việc chỉ giữ BTC.")
    else:
        print(f"⚠️ THẤT BẠI! Hệ thống AI hoạt động kém hơn việc HODL BTC ({alpha:+.2f}%). Cần tinh chỉnh Prompt.")
        
    return {
        "ai_roi": ai_roi,
        "hodl_roi": hodl_roi,
        "alpha": alpha,
        "ai_sharpe": ai_sharpe,
        "ai_max_dd": ai_max_dd
    }

if __name__ == "__main__":
    run_multi_asset_backtest(max_days=10)
