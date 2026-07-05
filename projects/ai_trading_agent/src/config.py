import os
from pathlib import Path
from dotenv import load_dotenv

# Load biến môi trường từ file .env ở thư mục gốc của workspace
# Giả sử cấu trúc: workspace/.env và workspace/projects/ai_trading_agent/src/config.py
BASE_DIR = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = BASE_DIR.parent.parent
load_dotenv(WORKSPACE_DIR / ".env")

class Config:
    """
    Quản lý cấu hình tập trung cho AI Trading Agent.
    Tất cả các tham số và API keys được load từ biến môi trường hoặc giá trị mặc định.
    """
    
    # 1. API Keys & Endpoints
    GCLI_API_KEY = os.getenv("GCLI_API_KEY")
    GCLI_BASE_URL = os.getenv("GCLI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
    
    BINANCE_TESTNET_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
    BINANCE_TESTNET_SECRET = os.getenv("BINANCE_TESTNET_SECRET")
    USE_BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "False").lower() in ('true', '1', 'yes')
    
    WHALE_ALERT_API_KEY = os.getenv("WHALE_ALERT_API_KEY")
    
    TELE_TOKEN = os.getenv("TELE_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    # 2. Trading Parameters
    TRADE_TICKERS_STR = os.getenv("TRADE_TICKERS", "BTC-USD,ETH-USD,SOL-USD")
    TRADE_TICKERS = [t.strip() for t in TRADE_TICKERS_STR.split(',')]
    
    # Paper Trading / Backtest Defaults
    INITIAL_CAPITAL = float(os.getenv("INITIAL_CAPITAL", "10000"))
    TIMEFRAME = os.getenv("TIMEFRAME", "1h")
    
    # 3. Paths
    DATA_DIR = BASE_DIR / "data"
    DOCS_DIR = BASE_DIR / "docs"
    BACKTEST_DIR = BASE_DIR / "backtest"
    
    # Database
    DB_PATH = DATA_DIR / "trading_market.db"
    
    @classmethod
    def validate(cls):
        """Kiểm tra các biến môi trường quan trọng."""
        missing = []
        if not cls.GCLI_API_KEY:
            missing.append("GCLI_API_KEY")
        
        # Nếu dùng Real/Testnet Trading thì cần Binance Key
        # Nếu chỉ chạy Backtest/Paper Trading offline thì có thể không cần (tùy logic)
        
        if missing:
            print(f"⚠️ Cảnh báo: Thiếu các biến môi trường: {', '.join(missing)}")
            print("   Vui lòng kiểm tra file .env tại thư mục gốc.")

# Tạo thư mục data nếu chưa tồn tại
Config.DATA_DIR.mkdir(parents=True, exist_ok=True)
