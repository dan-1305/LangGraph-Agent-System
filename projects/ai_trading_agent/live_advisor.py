import pandas as pd
import warnings
import sqlite3
import sys
from pathlib import Path
import io

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Bỏ qua cảnh báo Pydantic
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')

# Setup sys.path
# Root của toàn bộ hệ thống LangGraph
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

# Thêm thư mục src gốc vào sys.path để import các module cốt lõi (database, v.v.)
root_src_dir = base_dir / "src"
if str(root_src_dir) not in sys.path:
    sys.path.insert(0, str(root_src_dir))

# Thêm thư mục src của ai_trading_agent vào path để hỗ trợ import trực tiếp các file
ai_trading_src_dir = Path(__file__).resolve().parent / "src"
if str(ai_trading_src_dir) not in sys.path:
    sys.path.insert(0, str(ai_trading_src_dir))

# Import theo đúng cấu trúc của ai_trading_agent
import database as Database_Module
SystemDB = Database_Module.SystemDB

import config as Config_Module
Config = Config_Module.Config

import analytics as Analytics_Module
Analytics = Analytics_Module.Analytics

import langgraph_agent as Langgraph_Module
MultiAgentTradingSystem = Langgraph_Module.MultiAgentTradingSystem

from news_scraper import fetch_cointelegraph_news
from binance_executor import BinanceExecutor
from fundamental_fetcher import FundamentalAnalyzer
from mini_backtest import run_mini_backtest
from github_fetcher import fetch_github_trending_crypto
from social_scraper import fetch_reddit_crypto_sentiment
from portfolio_optimizer import optimize_portfolio

def get_latest_market_data(tickers=None, days=5, ml_days=200):
    """Lấy dữ liệu đa tài sản từ SQLite. Kèm theo dữ liệu thô cho ML Prediction."""
    if tickers is None:
        tickers = Config.TRADE_TICKERS
    print("🔄 Đang đọc dữ liệu thị trường đa tài sản từ Database...")
    db_path = base_dir / "data" / "trading_market.db"
    
    if not db_path.exists():
        print("❌ Database không tồn tại. Vui lòng chạy data_fetcher.py trước.")
        return None, None
        
    conn = sqlite3.connect(db_path, timeout=20.0)
    conn.execute('PRAGMA journal_mode=WAL;')
    
    combined_data_str = ""
    historical_data_df = {}
    
    for ticker in tickers:
        table_name = ticker.replace("-", "_")
        try:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            # Lấy các cột quan trọng cho Prompt
            recent_df = df[['Date', 'Close', 'Volume', 'SMA_20', 'SMA_50', 'RSI_14', 'FNG_Value', 'FNG_Class']].tail(days).reset_index(drop=True)
            combined_data_str += f"\n--- {ticker} ---\n"
            combined_data_str += recent_df.to_string(index=False) + "\n"
            
            # Chuẩn bị dữ liệu cho ML Model (Não Trái)
            ml_df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].tail(ml_days).copy()
            # Standardize column names cho ML Model
            ml_df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
            historical_data_df[ticker] = ml_df.to_dict(orient='records')
            
        except Exception:
            print(f"⚠️ Không tìm thấy bảng {table_name} trong Database.")
            
    conn.close()
    return combined_data_str, historical_data_df

def get_latest_news(ticker="BTC-USD"):
    """Lấy tin tức mới nhất từ CoinTelegraph."""
    print("📰 Đang cào tin tức nóng nhất về Crypto...")
    # Bỏ qua tham số ticker vì CoinTelegraph RSS trả về tin tức chung của thị trường
    news_list = fetch_cointelegraph_news(limit=5)
    return news_list

def get_trading_lore():
    """Đọc Ký ức giao dịch dài hạn để làm RAG Context"""
    print("🧠 Đang truy xuất Ký ức Giao dịch (TRADING_LORE) và Bài học Minervini...")
    lore_path = base_dir / "logs" / "TRADING_LORE.md"
    lore_content = ""
    if lore_path.exists():
        with open(lore_path, "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip() and len(content.splitlines()) > 5:
                lore_content = "\n--- BÀI HỌC QUÁ KHỨ (TRADING LORE) ---\n" + content[-2000:] # Lấy 2000 char cuối

    # Giả lập RAG Query (Quest 3 yêu cầu query RAG sách Minervini)
    # Trong môi trường thật, sẽ gọi subprocess tới tools/system/rag_query.py "Mark Minervini Trading Rules"
    rag_context = "\n--- RAG CONTEXT (Sách Trading) ---\n"
    rag_context += "Luật Minervini: KHÔNG BAO GIỜ bình quân giá xuống (Average Down). Luôn có Stop Loss. Chờ VCP Pattern.\n"
    
    return lore_content + rag_context

def run_live_advisor():
    analytics = Analytics()
    start_time = analytics.start_time
    
    print("==================================================")
    print("🤖 LIVE ADVISOR: HỆ THỐNG CỐ VẤN TRADING ĐA TÀI SẢN")
    print("==================================================")
    
    tickers = Config.TRADE_TICKERS
    
    # 1. Kéo dữ liệu giá
    multi_asset_data_str, historical_data_df = get_latest_market_data(tickers)
    if not multi_asset_data_str:
        print("❌ Lỗi kéo dữ liệu giá.")
        return
        
    # Kéo bộ nhớ dài hạn
    lore_and_rag = get_trading_lore()
    
    # 2. Kéo tin tức Sentiment & Alternative Data (GitHub, Reddit)
    news_list = get_latest_news()
    
    reddit_posts = fetch_reddit_crypto_sentiment(limit=3)
    github_repos = fetch_github_trending_crypto(days=7, limit=3)
    
    # Gom chung vào news_list cho Sentiment Agent xử lý
    news_list.extend(reddit_posts)
    news_list.extend(github_repos)
    
    # 3. Kéo Phân tích cơ bản & Tâm lý Bầy đàn
    print("📈 Đang phân tích Biên độ an toàn (Fundamental Analysis)...")
    fundamental_analyzer = FundamentalAnalyzer()
    fundamental_report = fundamental_analyzer.generate_fundamental_report(tickers)
    
    # 4. Tính toán Tỷ trọng Tối ưu bằng MPT (Mean-Variance Optimization)
    mpt_result = optimize_portfolio(tickers, days=30)
    if mpt_result:
        mpt_str = "\n--- GỢI Ý TỶ TRỌNG TỐI ƯU TỪ MPT (HÃY THAM KHẢO) ---\n"
        for coin, w in mpt_result['allocation'].items():
            mpt_str += f"{coin}: {w*100:.1f}%\n"
        mpt_str += f"Sharpe Ratio dự kiến: {mpt_result['sharpe_ratio']:.2f}\n"
        fundamental_report += mpt_str
    
    print("\n--- DỮ LIỆU THỊ TRƯỜNG & ON-CHAIN ---")
    print(multi_asset_data_str)
    
    if lore_and_rag:
        print("\n" + lore_and_rag)
    
    print("\n" + fundamental_report)
    
    print("\n--- TIN TỨC THỊ TRƯỜNG (SENTIMENT) ---")
    for news in news_list:
        print(f"• {news}")
        
    print("\n🔗 Lấy số dư tài khoản từ Binance...")
    executor = BinanceExecutor()
    current_portfolio = executor.get_current_portfolio()

    print("\n🧠 Đang khởi động Hệ thống Đa Đặc vụ (LangGraph Multi-Agent)...")
    agent = MultiAgentTradingSystem()
    
    # Ghép Lore vào Fundamental report để nạp vào Context chung
    combined_fundamental = fundamental_report + "\n" + lore_and_rag
    
    decision = agent.analyze_and_trade(multi_asset_data_str, current_portfolio, news_list=news_list, fundamental_data=combined_fundamental, historical_data_df=historical_data_df)
    
    # Ghi log thời gian phân tích
    analytics.log_execution_time("AI Analysis", start_time)
    
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
    
    # Validation Gate: Mini-Backtest
    if allocation:
        print("\n🛡️ ĐANG CHẠY VALIDATION GATE (MINI-BACKTEST 7 NGÀY)...")
        bt_result = run_mini_backtest(allocation, days=7)
        
        if "error" not in bt_result:
            print(f"   - Lợi nhuận dự kiến : {bt_result['total_return_pct']:.2f}%")
            print(f"   - Sharpe Ratio      : {bt_result['sharpe_ratio']:.2f}")
            print(f"   - Max Drawdown      : {bt_result['max_drawdown_pct']:.2f}%")
            
            if not bt_result['is_passed']:
                print("\n❌ CẢNH BÁO: CHIẾN LƯỢC KHÔNG QUA ĐƯỢC VALIDATION GATE!")
                print("Lý do: Lợi nhuận < -5% hoặc Sharpe Ratio < -1.0 trong 7 ngày qua.")
                print("Hành động: HỦY VÀO LỆNH. Chuyển 100% danh mục về USDT.")
                allocation = {"USDT": 1.0}
                decision['confidence_score'] = 0
                decision['reasoning'] = "Bị chặn bởi Validation Gate (Mini-Backtest thất bại)."
            else:
                print("\n✅ VALIDATION GATE: PASSED. Cho phép thực thi lệnh.")
        else:
            print(f"⚠️ Không thể chạy backtest: {bt_result.get('error')}. Vẫn tiếp tục thực thi.")
            
    # Thực thi lệnh trên Binance (Paper hoặc Live Testnet)
    if not allocation:
        print("\n⏸️ BỎ QUA GIAO DỊCH: AI quyết định HOLD hoặc API gặp lỗi.")
    else:
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