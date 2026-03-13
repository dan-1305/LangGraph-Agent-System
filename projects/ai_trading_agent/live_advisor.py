import os
import yfinance as yf
import pandas as pd
from datetime import datetime
import warnings
import sqlite3
import sys
from pathlib import Path

# Bỏ qua cảnh báo Pydantic
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')

# Setup sys.path
# base_dir: c:/Users/Admin/Desktop/WorkSpace/Project/LangGraph_Agent_System
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

# Thêm ai_trading_agent/src vào sys.path
ai_trading_src_dir = Path(__file__).resolve().parent / "src"
if str(ai_trading_src_dir) not in sys.path:
    sys.path.insert(0, str(ai_trading_src_dir))

# Import database từ src/ (thư mục gốc project)
from src.database import SystemDB

# Import các file trading agent từ ai_trading_agent/src/
from langgraph_agent import MultiAgentTradingSystem
from news_scraper import fetch_cointelegraph_news
from binance_executor import BinanceExecutor
from fundamental_fetcher import FundamentalAnalyzer

def get_latest_market_data(tickers=None, days=5):
    """Lấy dữ liệu đa tài sản từ SQLite."""
    if tickers is None:
        tickers_str = os.getenv("TRADE_TICKERS", "BTC-USD,ETH-USD,SOL-USD")
        tickers = [t.strip() for t in tickers_str.split(',')]
    print(f"🔄 Đang đọc dữ liệu thị trường đa tài sản từ Database...")
    db_path = base_dir / "data" / "trading_market.db"
    
    if not db_path.exists():
        print("❌ Database không tồn tại. Vui lòng chạy data_fetcher.py trước.")
        return None
        
    conn = sqlite3.connect(db_path)
    
    combined_data_str = ""
    for ticker in tickers:
        table_name = ticker.replace("-", "_")
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            # Lấy các cột quan trọng
            recent_df = df[['Date', 'Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI_14', 'FNG_Value', 'FNG_Class']].tail(days).reset_index(drop=True)
            combined_data_str += f"\n--- {ticker} ---\n"
            combined_data_str += recent_df.to_string(index=False) + "\n"
        except Exception:
            print(f"⚠️ Không tìm thấy bảng {table_name} trong Database.")
            
    conn.close()
    return combined_data_str

def get_latest_news(ticker="BTC-USD"):
    """Lấy tin tức mới nhất từ CoinTelegraph."""
    print(f"📰 Đang cào tin tức nóng nhất về Crypto...")
    # Bỏ qua tham số ticker vì CoinTelegraph RSS trả về tin tức chung của thị trường
    news_list = fetch_cointelegraph_news(limit=5)
    return news_list

def run_live_advisor():
    print("==================================================")
    print("🤖 LIVE ADVISOR: HỆ THỐNG CỐ VẤN TRADING ĐA TÀI SẢN")
    print("==================================================")
    
    tickers_str = os.getenv("TRADE_TICKERS", "BTC-USD,ETH-USD,SOL-USD")
    tickers = [t.strip() for t in tickers_str.split(',')]
    
    # 1. Kéo dữ liệu giá
    multi_asset_data_str = get_latest_market_data(tickers)
    if not multi_asset_data_str:
        print("❌ Lỗi kéo dữ liệu giá.")
        return
        
    # 2. Kéo tin tức Sentiment
    news_list = get_latest_news()
    
    # 3. Kéo Phân tích cơ bản & Tâm lý Bầy đàn
    print(f"📈 Đang phân tích Biên độ an toàn (Fundamental Analysis)...")
    fundamental_analyzer = FundamentalAnalyzer()
    fundamental_report = fundamental_analyzer.generate_fundamental_report(tickers)
    
    print("\n--- DỮ LIỆU THỊ TRƯỜNG & ON-CHAIN ---")
    print(multi_asset_data_str)
    
    print("\n" + fundamental_report)
    
    print("\n--- TIN TỨC THỊ TRƯỜNG (SENTIMENT) ---")
    for news in news_list:
        print(f"• {news}")
        
    print("\n🔗 Lấy số dư tài khoản từ Binance...")
    executor = BinanceExecutor()
    current_portfolio = executor.get_current_portfolio()

    print("\n🧠 Đang khởi động Hệ thống Đa Đặc vụ (LangGraph Multi-Agent)...")
    agent = MultiAgentTradingSystem()
    
    decision = agent.analyze_and_trade(multi_asset_data_str, current_portfolio, news_list=news_list, fundamental_data=fundamental_report)
    
    print("\n==================================================")
    print("🔔 QUYẾT ĐỊNH PHÂN BỔ VỐN CỦA AI (PORTFOLIO ALLOCATION)")
    print("==================================================")
    allocation = decision.get('allocation', {})
    for coin, weight in allocation.items():
        print(f"  - {coin:<5}: {weight * 100:>5.1f}%")
        
    print(f"\nĐộ tự tin         : {decision.get('confidence_score', 0)} / 10")
    print("\nLÝ DO (Reasoning):")
    print(f"💬 {decision.get('reasoning', 'N/A')}")
    print("==================================================")
    
    # Thực thi lệnh trên Binance (Paper hoặc Live Testnet)
    if allocation:
        executor.execute_allocation(allocation, decision.get('confidence_score', 0))
    
    # Ghi nhận vào log cho vui (Dùng action lưu chuỗi tỷ trọng)
    try:
        alloc_str = str(allocation)
        db = SystemDB()
        db.log_trading_decision(
            ticker="PORTFOLIO",
            price=0,
            action=alloc_str,
            confidence=decision.get('confidence_score', 0),
            sl=0,
            tp=0,
            reasoning=decision.get('reasoning', 'N/A')
        )
        db.close()
        print("💾 Đã lưu báo cáo phân bổ vốn vào Database (system_logs.db).")
    except Exception as e:
        print(f"⚠️ Lỗi khi lưu Database: {e}")

if __name__ == "__main__":
    run_live_advisor()