import os
import sys
import pandas as pd
from pathlib import Path
import warnings

# Bỏ qua cảnh báo Pydantic
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')

from agent import TradingAgent
import numpy as np

# Thêm src vào path để import database
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.append(str(base_dir))

from src.database import SystemDB

import sqlite3

def run_backtest(ticker="BTC-USD", initial_capital=10000, window_size=5, max_days=30, trading_fee=0.001):
    """
    Chạy mô phỏng giao dịch (Backtest) trên dữ liệu lịch sử với tiêu chuẩn chuyên gia:
    - Tính phí giao dịch (Trading Fee)
    - Quản lý rủi ro (Position Sizing, Stop-Loss, Take-Profit)
    - Chỉ số nâng cao (Max Drawdown, Sharpe Ratio, Win Rate)
    """
    print(f"🚀 BẮT ĐẦU BACKTEST {ticker} (Vốn ban đầu: ${initial_capital:,} | Phí giao dịch: {trading_fee*100}%)")
    
    # Đọc dữ liệu từ SQLite
    db_path = base_dir.parent.parent / "data" / "trading_market.db"
    conn = sqlite3.connect(db_path)
    table_name = ticker.replace("-", "_")
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    
    # Chỉ lấy các cột cần thiết và drop NA
    df = df[['Date', 'Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI_14']].dropna().reset_index(drop=True)
    
    # Cắt dữ liệu test
    if len(df) > max_days + window_size:
        df = df.iloc[:max_days + window_size].reset_index(drop=True)
        
    agent = TradingAgent()
    
    capital = initial_capital
    position_size = 0 # Số lượng coin đang giữ
    position_entry_price = 0
    current_stop_loss = 0
    current_take_profit = 0
    trade_history = []
    daily_portfolio_values = []
    
    for i in range(window_size, len(df)):
        current_idx = i
        current_row = df.iloc[current_idx]
        current_date = current_row['Date']
        current_price = current_row['Close']
        
        # Lấy dữ liệu cửa sổ (n ngày gần nhất)
        recent_data = df.iloc[current_idx - window_size : current_idx + 1]
        
        print(f"\n--- Ngày {current_date} | Giá: ${current_price:,.2f} ---")
        
        # Kiểm tra Stop-Loss / Take-Profit trước khi gọi AI
        if position_size > 0:
            if current_price <= current_stop_loss:
                action = "SELL"
                reasoning = "Kích hoạt Stop-Loss bảo toàn vốn."
                print(f"🧠 AI Quyết định: {action}")
                print(f"💡 Lý do: {reasoning}")
                
                sell_value = position_size * current_price
                fee = sell_value * trading_fee
                capital += (sell_value - fee)
                profit = (sell_value - fee) - (position_size * position_entry_price)
                profit_pct = (profit / (position_size * position_entry_price)) * 100
                print(f"🔴 THỰC THI: BÁN (STOP-LOSS) tại ${current_price:,.2f} | PnL: ${profit:,.2f} ({profit_pct:.2f}%) | Phí: ${fee:,.2f}")
                position_size = 0
                trade_history.append({"Date": current_date, "Action": "SELL_SL", "Price": current_price, "PnL": profit})
                daily_portfolio_values.append(capital)
                continue
                
            elif current_price >= current_take_profit and current_take_profit > 0:
                action = "SELL"
                reasoning = "Kích hoạt Take-Profit chốt lời."
                print(f"🧠 AI Quyết định: {action}")
                print(f"💡 Lý do: {reasoning}")
                
                sell_value = position_size * current_price
                fee = sell_value * trading_fee
                capital += (sell_value - fee)
                profit = (sell_value - fee) - (position_size * position_entry_price)
                profit_pct = (profit / (position_size * position_entry_price)) * 100
                print(f"🔴 THỰC THI: BÁN (TAKE-PROFIT) tại ${current_price:,.2f} | PnL: ${profit:,.2f} ({profit_pct:.2f}%) | Phí: ${fee:,.2f}")
                position_size = 0
                trade_history.append({"Date": current_date, "Action": "SELL_TP", "Price": current_price, "PnL": profit})
                daily_portfolio_values.append(capital)
                continue

        # Gọi AI Agent đưa ra quyết định
        current_position_status = 1 if position_size > 0 else 0
        decision = agent.analyze_and_trade(recent_data, current_position_status)
        
        action = decision.get("action", "HOLD")
        reasoning = decision.get("reasoning", "No reason provided")
        confidence = decision.get("confidence_score", 5)
        sl_pct = decision.get("stop_loss_pct", 0.05)
        tp_pct = decision.get("take_profit_pct", 0.10)
        
        print(f"🧠 AI Quyết định: {action} (Tự tin: {confidence}/10)")
        print(f"💡 Lý do: {reasoning}")
        
        # Xử lý giao dịch với Position Sizing (Không All-in)
        if action == "BUY" and position_size == 0:
            # Position Sizing dựa trên độ tự tin (Confidence)
            # Giả sử đánh tối đa 50% vốn nếu tự tin 10/10
            invest_ratio = (confidence / 10.0) * 0.5
            invest_amount = capital * invest_ratio
            fee = invest_amount * trading_fee
            net_invest = invest_amount - fee
            
            position_size = net_invest / current_price
            position_entry_price = current_price
            capital -= invest_amount
            
            # Cài đặt SL/TP
            current_stop_loss = current_price * (1 - sl_pct)
            current_take_profit = current_price * (1 + tp_pct)
            
            print(f"🟢 THỰC THI: MUA {position_size:.4f} BTC tại ${current_price:,.2f} | Vốn dùng: ${invest_amount:,.2f} | Phí: ${fee:,.2f}")
            print(f"🛡️  Cài đặt SL: ${current_stop_loss:,.2f} (-{sl_pct*100}%) | TP: ${current_take_profit:,.2f} (+{tp_pct*100}%)")
            trade_history.append({"Date": current_date, "Action": "BUY", "Price": current_price})
            
        elif action == "SELL" and position_size > 0:
            # Bán chốt lời/cắt lỗ chủ động
            sell_value = position_size * current_price
            fee = sell_value * trading_fee
            profit = (sell_value - fee) - (position_size * position_entry_price)
            profit_pct = (profit / (position_size * position_entry_price)) * 100
            
            capital += (sell_value - fee)
            print(f"🔴 THỰC THI: BÁN tại ${current_price:,.2f} | PnL: ${profit:,.2f} ({profit_pct:.2f}%) | Phí: ${fee:,.2f}")
            position_size = 0
            trade_history.append({"Date": current_date, "Action": "SELL", "Price": current_price, "PnL": profit})
            
        else:
            print("⚪ THỰC THI: ĐỨNG NGOÀI (HOLD)")
            
        # Ghi nhận giá trị tài khoản hàng ngày để tính Max Drawdown và Sharpe
        daily_portfolio_values.append(capital + (position_size * current_price))
            
    # Kết thúc backtest, tính toán tổng tài sản và các chỉ số nâng cao
    if position_size > 0:
        sell_value = position_size * df.iloc[-1]['Close']
        fee = sell_value * trading_fee
        capital += (sell_value - fee)
        position_size = 0

    final_portfolio_value = capital
    roi = ((final_portfolio_value - initial_capital) / initial_capital) * 100
    
    # Tính các chỉ số chuyên gia
    portfolio_series = pd.Series(daily_portfolio_values)
    daily_returns = portfolio_series.pct_change().dropna()
    
    # 1. Sharpe Ratio (Giả sử risk-free rate = 0)
    sharpe_ratio = 0
    if daily_returns.std() > 0:
        sharpe_ratio = np.sqrt(365) * (daily_returns.mean() / daily_returns.std())
        
    # 2. Max Drawdown
    cumulative_returns = (1 + daily_returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min() * 100 if not drawdown.empty else 0
    
    # 3. Win Rate
    winning_trades = len([t for t in trade_history if "PnL" in t and t["PnL"] > 0])
    total_closed_trades = len([t for t in trade_history if "PnL" in t])
    win_rate = (winning_trades / total_closed_trades * 100) if total_closed_trades > 0 else 0
    
    print("\n=========================================")
    print("📊 KẾT QUẢ BACKTEST (TIÊU CHUẨN CHUYÊN GIA)")
    print(f"Vốn ban đầu: ${initial_capital:,.2f}")
    print(f"Tổng tài sản cuối cùng: ${final_portfolio_value:,.2f}")
    print(f"Tỷ suất lợi nhuận (ROI): {roi:.2f}%")
    print(f"📈 Sharpe Ratio (Annualized): {sharpe_ratio:.2f}")
    print(f"📉 Max Drawdown: {max_drawdown:.2f}%")
    print(f"🎯 Tỷ lệ thắng (Win Rate): {win_rate:.2f}% ({winning_trades}/{total_closed_trades} lệnh)")
    print("=========================================")
    
    # Lưu vào SQLite System Logs
    try:
        db = SystemDB()
        db.log_backtest_report(
            ticker=ticker,
            start_date=df.iloc[window_size]['Date'],
            end_date=df.iloc[-1]['Date'],
            initial=initial_capital,
            final=final_portfolio_value,
            roi=roi,
            sharpe=sharpe_ratio,
            max_dd=max_drawdown,
            win_rate=win_rate
        )
        db.close()
        print("💾 Đã lưu kết quả Backtest vào Database (system_logs.db).")
    except Exception as e:
        print(f"⚠️ Lỗi khi lưu Database: {e}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    db_path = base_dir.parent.parent / "data" / "trading_market.db"
    
    if db_path.exists():
        run_backtest()
    else:
        print("❌ Không tìm thấy file dữ liệu trading_market.db. Hãy chạy data_fetcher.py trước.")
