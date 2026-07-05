import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

base_dir = Path(__file__).resolve().parent.parent

def generate_markdown_report():
    """Tạo báo cáo hiệu suất từ dữ liệu Paper Trade trong Database."""
    db_path = base_dir.parent.parent / "data" / "system_logs.db"
    
    if not db_path.exists():
        print("❌ Không tìm thấy database system_logs.db")
        return
        
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql("SELECT * FROM Paper_Trade_Portfolio ORDER BY timestamp", conn)
    except Exception as e:
        print(f"Lỗi đọc dữ liệu: {e}")
        conn.close()
        return
        
    conn.close()
    
    if df.empty or len(df) < 2:
        print("⚠️ Chưa đủ dữ liệu giao dịch để tạo báo cáo.")
        return
        
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Tính các chỉ số
    initial_value = df.iloc[0]['total_usdt_value']
    final_value = df.iloc[-1]['total_usdt_value']
    total_roi = (final_value - initial_value) / initial_value * 100
    
    # Tính Daily Returns và Sharpe Ratio
    df['date'] = df['timestamp'].dt.date
    daily_values = df.groupby('date')['total_usdt_value'].last()
    daily_returns = daily_values.pct_change().dropna()
    
    if len(daily_returns) > 0 and daily_returns.std() > 0:
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * np.sqrt(365)
    else:
        sharpe_ratio = 0.0
        
    # Tính Max Drawdown
    if len(daily_values) > 0:
        cum_returns = (1 + daily_returns).cumprod()
        rolling_max = cum_returns.expanding().max()
        drawdowns = (cum_returns - rolling_max) / rolling_max
        max_dd = drawdowns.min() * 100 if not drawdowns.empty else 0.0
    else:
        max_dd = 0.0
        
    # Tạo Markdown
    report_content = f"""# 📈 BÁO CÁO HIỆU SUẤT AI TRADING AGENT
*Ngày tạo báo cáo: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

## 1. Tổng quan danh mục (Paper Trading)
- **Vốn khởi điểm:** ${initial_value:,.2f}
- **Vốn hiện tại:** ${final_value:,.2f}
- **Lợi nhuận tổng (ROI):** {total_roi:+.2f}%
- **Sharpe Ratio (Annualized):** {sharpe_ratio:.2f}
- **Max Drawdown:** {max_dd:.2f}%

## 2. Trạng thái phân bổ hiện tại
Dữ liệu chốt tại thời điểm: {df.iloc[-1]['timestamp']}
- **USDT:** ${df.iloc[-1]['usdt_bal']:,.2f}
- **BTC:** {df.iloc[-1]['btc_bal']:.4f}
- **ETH:** {df.iloc[-1]['eth_bal']:.4f}
- **SOL:** {df.iloc[-1]['sol_bal']:.4f}

## 3. Lịch sử giá trị tài sản 10 ngày gần nhất
"""
    recent_daily = daily_values.tail(10)
    for date, val in recent_daily.items():
        report_content += f"- {date}: ${val:,.2f}\n"
        
    report_content += "\n---\n*Báo cáo được tạo tự động bởi Hệ thống LangGraph Agent.*"
    
    docs_dir = base_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    report_path = docs_dir / "LATEST_PERFORMANCE_REPORT.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"✅ Đã tạo báo cáo thành công tại: {report_path}")

if __name__ == "__main__":
    generate_markdown_report()
