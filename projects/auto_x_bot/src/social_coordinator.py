import asyncio
import sys
import os
from pathlib import Path
import json

# Setup PYTHONPATH
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(BASE_DIR))

# Fix encoding cho Windows console
import sys
import io
if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# Import modules
try:
    from projects.ceo_agent.marketing_intel import MarketingAgent
    from projects.auto_x_bot.src.browser_bot import XBrowserBot
    from projects.ai_trading_agent.src.social_scraper import fetch_reddit_crypto_sentiment
    from projects.ai_trading_agent.src.analysis_to_social import AnalysisAgent
    from projects.ai_trading_agent.src.technical_engine import TechnicalEngine
except ImportError as e:
    print(f"❌ Loi import: {e}")
    sys.exit(1)

async def social_mining_cycle():
    print("🔄 --- BAT DAU CHU KY SOCIAL MINING (TRADING + MARKETING) ---")
    
    # 1. Thu thập tín hiệu giao dịch từ Trading Agent
    print("📈 Đang phân tích tín hiệu Trading...")
    try:
        engine = TechnicalEngine()
        # Mock signal since this is an example integration
        tech_data = {
            "signal": "BUY",
            "reasons": ["RSI Oversold", "Strong Momentum"],
            "current_price": 65000.0,
            "symbol": "BTC-USD"
        }
        trading_agent = AnalysisAgent()
        trading_report = trading_agent.execute(tech_data)
        trading_tweet = getattr(trading_report, 'tweet_summary', None) or trading_report.get('tweet_summary', '')
    except Exception as e:
        print(f"⚠️ Lỗi lấy tín hiệu Trading: {e}")
        trading_tweet = ""

    # 2. Thu thập dữ liệu Market Sentiment
    print("🧐 Đang phân tích Social Sentiment...")
    social_data = await fetch_reddit_crypto_sentiment(limit=5)
    m_agent = MarketingAgent()
    insights = m_agent.execute(social_data)
    
    # 3. Tổng hợp nội dung Tweet
    marketing_tweet = insights.get('suggested_content', "Vương triều AI Sovereign đang trỗi dậy mạnh mẽ! 🚀 #Web3 #AI")
    tweet_text = trading_tweet if trading_tweet else marketing_tweet
    
    # Gioi han 280 ky tu cho X
    if len(tweet_text) > 280:
        tweet_text = tweet_text[:277] + "..."
    
    print(f"📝 Content de xuat: {tweet_text}")
    
    # 3. Dang Tweet qua trinh duyet
    print("🐦 Dang thuc thi dang bai len X...")
    x_bot = XBrowserBot()
    success = await x_bot.post_tweet_browser(tweet_text)
    
    if success:
        print("✅ Chu ky Social Mining hoan tat thanh cong!")
    else:
        print("⚠️ Co loi trong qua trinh dang bai.")

if __name__ == "__main__":
    asyncio.run(social_mining_cycle())
