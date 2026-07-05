from src.base_agent import BaseAgent

class WhaleTrackerAgent(BaseAgent):
    def __init__(self):
        super().__init__(model_name="label:tier-1", temperature=0.1)

    def _ai_handler(self, state: dict) -> dict:
        return {"action_advised": "HOLD", "reason": "No data", "is_danger": False}
        
    def _logic_handler(self, state: dict) -> dict:
        return {"action_advised": "HOLD", "reason": "No data", "is_danger": False}

    def scrape_whale_data(self):
        return []
        
    def execute(self, alerts):
        return self._logic_handler({})
