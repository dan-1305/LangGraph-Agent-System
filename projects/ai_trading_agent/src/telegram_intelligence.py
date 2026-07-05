from core_utilities.http_client import HTTPClient
import asyncio
from src.base_agent import BaseAgent
from pydantic import BaseModel
from typing import List, Dict

class TelegramSentiment(BaseAgent, BaseModel):
    sentiment_score: float # -1.0 to 1.0
    key_signals: List[str]
    market_mood: str # BULLISH, BEARISH, NEUTRAL

class TelegramIntelligenceAgent(BaseAgent):
    """
    Agent chuyen phan tich tam ly thi truong tu cac tin nhan Telegram.
    """
    def __init__(self):
        super().__init__(model_name="gemini-3.1-flash-lite")

    def _logic_handler(self, data: str) -> dict:
        return {"sentiment_score": 0, "market_mood": "NEUTRAL"}

    def _ai_handler(self, messages: List[str]) -> TelegramSentiment:
        prompt = f"""
        Ban la mot chuyen gia phan tich tam ly thi truong Crypto.
        Hay phan tich danh sach cac tin nhan tu cac channel Telegram sau day:
        {messages}

        YEU CAU:
        1. Cham diem tam ly tong the tu -1 (Cuc ky tieu cuc) den 1 (Cuc ky tich cuc).
        2. Liet ke cac tin hieu quan trong (vi du: Whale mua manh, tin xau ve san...).
        3. Ket luan mood cua thi truong hien tai.
        """
        return self._call_llm(prompt, is_json=True, schema=TelegramSentiment)

async def main():
    print("🛰️ Telegram Intelligence Agent dang khoi dong...")
    # Mo phong du lieu tu cac channel Telegram (Trong thuc te se dung Scraper/Webhook)
    mock_messages = [
        "Whale Alert: 50,000 BTC moved from unknown wallet to Binance",
        "Cointelegraph: SEC approves new Ethereum ETF framework",
        "VIP Signals: BTC looking very bullish on 4H chart, target 70k",
        "FUD: Exchange XYZ suspected of insolvency"
    ]
    
    agent = TelegramIntelligenceAgent()
    analysis = agent.execute(mock_messages)
    
    print("\n--- TELEGRAM SENTIMENT ANALYSIS ---")
    print(f"Score: {analysis.sentiment_score}")
    print(f"Mood: {analysis.market_mood}")
    print(f"Signals: {analysis.key_signals}")

if __name__ == "__main__":
    asyncio.run(main())
