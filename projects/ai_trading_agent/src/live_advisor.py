import logging
import pandas as pd
import warnings
import sqlite3
import sys
from pathlib import Path

# Bỏ qua cảnh báo Pydantic
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')


# Cấu hình logging
import os

storage_dir = os.getenv("STORAGE_DIR")
if storage_dir:
    log_dir = Path(storage_dir) / "logs"
else:
    log_dir = Path(__file__).resolve().parent / "data"
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(str(log_dir / "live_advisor.log"), encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("LiveAdvisor")

from src.database import SystemDB # type: ignore  # QA-Agent-Note: File này tồn tại ở root của hệ sinh thái LangGraph_Agent_System
from src.config import Config
from src.analytics import Analytics
from src.langgraph_agent import MultiAgentTradingSystem
from src.news_scraper import fetch_cointelegraph_news
from src.binance_executor import BinanceExecutor
from src.fundamental_fetcher import FundamentalAnalyzer
from backtest.mini_backtest import run_mini_backtest
from src.github_fetcher import fetch_github_trending_crypto
from src.social_scraper import fetch_reddit_crypto_sentiment
from src.portfolio_optimizer import optimize_portfolio

def get_latest_market_data(tickers: list = None, days: int = 5) -> str | None:
    """
    Lấy dữ liệu đa tài sản từ SQLite.
    
    Args:
        tickers (list, optional): Danh sách các cặp coin cần lấy dữ liệu. Mặc định là None.
        days (int, optional): Số ngày dữ liệu cần lấy. Mặc định là 5.
        
    Returns:
        str | None: Chuỗi chứa dữ liệu định dạng dễ đọc cho LLM, hoặc None nếu lỗi.
    """
    if tickers is None:
        tickers = Config.TRADE_TICKERS
    logger.info("🔄 Đang đọc dữ liệu thị trường đa tài sản từ Database...")
    db_path = Config.DB_PATH
    
    if not db_path.exists():
        logger.error("❌ Database không tồn tại. Vui lòng chạy data_fetcher.py trước.")
        return None
        
    conn = sqlite3.connect(db_path, timeout=20.0)
    conn.execute('PRAGMA journal_mode=WAL;')
    
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
            logger.warning(f"⚠️ Không tìm thấy bảng {table_name} trong Database.")
            
    conn.close()
    return combined_data_str

def get_latest_news(ticker: str = "BTC-USD") -> list:
    """
    Lấy tin tức mới nhất từ CoinTelegraph để phân tích Sentiment.
    
    Args:
        ticker (str): Tên coin (hiện tại không ảnh hưởng vì lấy tin chung).
        
    Returns:
        list: Danh sách các tin tức giật gân nhất.
    """
    logger.info("📰 Đang cào tin tức nóng nhất về Crypto...")
    # Bỏ qua tham số ticker vì CoinTelegraph RSS trả về tin tức chung của thị trường
    news_list = fetch_cointelegraph_news(limit=5)
    return news_list

def run_live_advisor() -> None:
    """
    Hàm thực thi chính của Live Advisor.
    Kéo dữ liệu, tin tức, gọi hệ thống Multi-Agent đánh giá và thực thi lệnh (hoặc mô phỏng).
    """
    analytics = Analytics()
    start_time = analytics.start_time
    
    logger.info("==================================================")
    logger.info("🤖 LIVE ADVISOR: HỆ THỐNG CỐ VẤN TRADING ĐA TÀI SẢN")
    logger.info("==================================================")
    
    tickers = Config.TRADE_TICKERS
    
    # 1. Kéo dữ liệu giá
    multi_asset_data_str = get_latest_market_data(tickers)
    if not multi_asset_data_str:
        logger.error("❌ Lỗi kéo dữ liệu giá.")
        return
        
    # 2. Kéo tin tức Sentiment & Alternative Data (GitHub, Reddit)
    news_list = get_latest_news()
    
    reddit_posts = fetch_reddit_crypto_sentiment(limit=3)
    github_repos = fetch_github_trending_crypto(days=7, limit=3)
    
    # Gom chung vào news_list cho Sentiment Agent xử lý
    news_list.extend(reddit_posts)
    news_list.extend(github_repos)
    
    # 3. Kéo Phân tích cơ bản & Tâm lý Bầy đàn
    logger.info("📈 Đang phân tích Biên độ an toàn (Fundamental Analysis)...")
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
    
    logger.info("\n--- DỮ LIỆU THỊ TRƯỜNG & ON-CHAIN ---")
    logger.info(multi_asset_data_str)
    
    logger.info("\n" + fundamental_report)
    
    logger.info("\n--- TIN TỨC THỊ TRƯỜNG (SENTIMENT) ---")
    for news in news_list:
        logger.info(f"• {news}")
        
    logger.info("\n🔗 Lấy số dư tài khoản từ Binance...")
    executor = BinanceExecutor()
    current_portfolio = executor.get_current_portfolio()

    logger.info("\n🧠 Đang khởi động Hệ thống Đa Đặc vụ (LangGraph Multi-Agent)...")
    agent = MultiAgentTradingSystem()
    
    decision = agent.analyze_and_trade(multi_asset_data_str, current_portfolio, news_list=news_list, fundamental_data=fundamental_report)
    
    # Ghi log thời gian phân tích
    analytics.log_execution_time("AI Analysis", start_time)
    
    logger.info("\n==================================================")
    logger.info("🔔 QUYẾT ĐỊNH PHÂN BỔ VỐN CỦA AI (PORTFOLIO ALLOCATION)")
    logger.info("==================================================")
    allocation = decision.get('allocation', {})
    for coin, weight in allocation.items():
        logger.info(f"  - {coin:<5}: {weight * 100:>5.1f}%")
        
    logger.info(f"\nĐộ tự tin         : {decision.get('confidence_score', 0)} / 10")
    logger.info("\nLÝ DO (Reasoning):")
    logger.info(f"💬 {decision.get('reasoning', 'N/A')}")
    logger.info("==================================================")
    
    # Validation Gate: Mini-Backtest
    if allocation:
        logger.info("\n🛡️ ĐANG CHẠY VALIDATION GATE (MINI-BACKTEST 7 NGÀY)...")
        bt_result = run_mini_backtest(allocation, days=7)
        
        if "error" not in bt_result:
            logger.info(f"   - Lợi nhuận dự kiến : {bt_result['total_return_pct']:.2f}%")
            logger.info(f"   - Sharpe Ratio      : {bt_result['sharpe_ratio']:.2f}")
            logger.info(f"   - Max Drawdown      : {bt_result['max_drawdown_pct']:.2f}%")
            
            if not bt_result['is_passed']:
                logger.warning("\n❌ CẢNH BÁO: CHIẾN LƯỢC KHÔNG QUA ĐƯỢC VALIDATION GATE!")
                logger.warning("Lý do: Lợi nhuận < -5% hoặc Sharpe Ratio < -1.0 trong 7 ngày qua.")
                logger.warning("Hành động: HỦY VÀO LỆNH. Chuyển 100% danh mục về USDT.")
                allocation = {"USDT": 1.0}
                decision['confidence_score'] = 0
                decision['reasoning'] = "Bị chặn bởi Validation Gate (Mini-Backtest thất bại)."
            else:
                logger.info("\n✅ VALIDATION GATE: PASSED. Cho phép thực thi lệnh.")
        else:
            logger.warning(f"⚠️ Không thể chạy backtest: {bt_result.get('error')}. Vẫn tiếp tục thực thi.")
            
    # Thực thi lệnh trên Binance (Paper hoặc Live Testnet)
    if not allocation:
        logger.info("\n⏸️ BỎ QUA GIAO DỊCH: AI quyết định HOLD hoặc API gặp lỗi.")
    else:
        sl_pct = decision.get('stop_loss_pct', 5.0)
        tp_pct = decision.get('take_profit_pct', 15.0)
        executor.execute_allocation(
            allocation, 
            confidence=decision.get('confidence_score', 0),
            stop_loss_pct=sl_pct,
            take_profit_pct=tp_pct
        )
    
    # Ghi nhận vào log
    try:
        alloc_str = str(allocation)
        db = SystemDB()
        db.log_trading_decision(
            ticker="PORTFOLIO",
            price=0,
            action=alloc_str,
            confidence=decision.get('confidence_score', 0),
            sl=decision.get('stop_loss_pct', 0),
            tp=decision.get('take_profit_pct', 0),
            reasoning=decision.get('reasoning', 'N/A')
        )
        db.close()
        logger.info("💾 Đã lưu báo cáo phân bổ vốn vào Database (system_logs.db).")
    except Exception as e:
        logger.error(f"⚠️ Lỗi khi lưu Database: {e}")

if __name__ == "__main__":
    run_live_advisor()
