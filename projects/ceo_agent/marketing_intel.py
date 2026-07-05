import asyncio
from src.base_agent import BaseAgent
from projects.ai_trading_agent.src.social_scraper import fetch_reddit_crypto_sentiment
from pydantic import BaseModel
from typing import List, Dict

class MarketingInsight(BaseAgent, BaseModel):
    pain_points: List[str]
    marketing_hooks: List[str]
    suggested_content: str

class MarketingAgent(BaseAgent):
    """
    Agent chuyen phan tich thi truong va sinh noi dung Marketing.
    """
    def __init__(self):
        super().__init__(model_name="gemini-3.1-flash-lite")

    def _logic_handler(self, data: str) -> Dict:
        return {"error": "AI failed to generate insights"}

    def _ai_handler(self, social_data: List[str]) -> MarketingInsight:
        prompt = f"""
        Ban la mot Product Marketing Manager xuat sac.
        Dua tren du lieu tu mang xa hoi sau day, hay phan tich noi dau (pain points) cua nguoi dung 
        va de xuat cac "Marketing Hooks" (loi chao hang) cho 2 san pham cua chung ta:
        1. AI Disk Cleaner (Don rac o C sieu toc)
        2. Godot Game Translator (Dich game bang AI)

        DU LIEU XA HOI:
        {social_data}

        YEU CAU:
        - Tim ra nhung loi than phien ve viec day o cung hoac game khong co tieng Viet/Anh.
        - Viet noi dung quang cao thu hut cho moi san pham.
        """
        return self._call_llm(prompt, is_json=True, schema=MarketingInsight)

async def main():
    print("📢 Marketing Intelligence Agent dang khoi dong...")
    # 1. Lay du lieu thi truong (Gia lap hoac thuc te tu Reddit)
    social_data = await fetch_reddit_crypto_sentiment(limit=10)
    
    # 2. Phan tich Insights
    agent = MarketingAgent()
    insights = agent.execute(social_data)
    
    # 3. Luu bao cao
    import json
    report_path = "reports/MARKETING_INSIGHTS_REPORT.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(insights, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Da xuat bao cao Marketing tai: {report_path}")

if __name__ == "__main__":
    asyncio.run(main())
