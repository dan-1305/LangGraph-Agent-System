import pandas as pd
from projects.ai_trading_agent.src.technical_engine import TechnicalEngine
from src.base_agent import BaseAgent
from pydantic import BaseModel
from typing import List

class MarketAnalysisReport(BaseAgent, BaseModel):
    analysis_text: str
    key_points: List[str]
    tweet_summary: str

class AnalysisAgent(BaseAgent):
    """
    Agent chuyen chuyen hoa cac tin hieu ky thuat thanh bai phan tich chuyen sau.
    """
    def __init__(self):
        super().__init__(model_name="gemini-3.1-pro-preview")

    def _logic_handler(self, data: dict) -> dict:
        return {"error": "AI analysis failed"}

    def _ai_handler(self, tech_data: dict) -> MarketAnalysisReport:
        prompt = f"""
        Ban la mot Senior Market Analyst tai mot quy dau tu Crypto lon.
        Dua tren du lieu ky thuat sau day, hay viet mot bai phan tich ngan gon nhung chuyen sau:
        {tech_data}

        YEU CAU:
        1. Giai thich y nghia cua cac chi bao (RSI, MACD, SMA).
        2. Dua ra nhan dinh ve xu huong tiep theo.
        3. Viet mot ban tom tat duoi 280 ky tu (kem hashtag) de dang len X.com.
        """
        return self._call_llm(prompt, is_json=True, schema=MarketAnalysisReport)

if __name__ == "__main__":
    # Gia lap du lieu tu TechnicalEngine
    engine = TechnicalEngine()
    # Trong thuc te se lay tu DB, o day ta dung mockup de test
    mock_tech_data = {
        "signal": "BUY",
        "reasons": ["RSI Oversold (28.5 < 30)", "Long-term Bullish Trend (SMA50 > SMA200)"],
        "current_price": 65000.5,
        "rsi": 28.5,
        "macd": 150.2,
        "symbol": "BTC-USD"
    }
    
    agent = AnalysisAgent()
    report = agent.execute(mock_tech_data)
    
    # [FIX] Tranh loi AttributeError khi AI tra ve Dict fallback (Circuit Breaker)
    print("\n--- MARKET ANALYSIS ---")
    if hasattr(report, 'analysis_text'):
        print(report.analysis_text)
    elif isinstance(report, dict) and 'analysis_text' in report:
        print(report['analysis_text'])
    else:
        print(f"⚠️ [FALLBACK] Tin hieu: {mock_tech_data.get('signal')} - {mock_tech_data.get('reasons')}")

    print("\n--- TWEET SUMMARY ---")
    if hasattr(report, 'tweet_summary'):
        print(report.tweet_summary)
    elif isinstance(report, dict) and 'tweet_summary' in report:
        print(report['tweet_summary'])
    else:
        print(f"⚠️ [FALLBACK TWEET] #{mock_tech_data.get('symbol')} Signal: {mock_tech_data.get('signal')} 🚀 #Crypto #Trading")
