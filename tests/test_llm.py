import sys
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.base_agent import BaseAgent

class TestAgent(BaseAgent):
    def __init__(self):
        super().__init__(name='test', role='test')
    def _ai_handler(self, *args, **kwargs): pass
    def _logic_handler(self, *args, **kwargs): pass

agent = TestAgent()
print("Model:", agent.llm.model_name)
try:
    res = agent._call_llm("Hello, respond with yes")
    print("Response:", res)
except Exception as e:
    print("Error:", e)