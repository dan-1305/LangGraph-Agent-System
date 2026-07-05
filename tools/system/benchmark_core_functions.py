import os
import sys
import time
from pathlib import Path

# Add root to sys path
root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(root))

from tools.system.global_function_auditor import performance_profiler
from src.base_agent import BaseAgent
from tools.system.rag_ingest import get_file_hash

# Tạo một Mock Agent để test phương thức parse JSON
class MockAgent(BaseAgent):
    def __init__(self):
        # Không cần call super().__init__ nếu không muốn init LLM thực
        pass
        
    def _ai_handler(self, *args, **kwargs):
        pass
    def _logic_handler(self, *args, **kwargs):
        pass

@performance_profiler
def test_json_extraction():
    agent = MockAgent()
    markdown_json = "```json\n{\"test\": 123, \"nested\": {\"a\": [1,2,3]}}\n```"
    # Giả lập lặp 100 lần để đo performance
    for _ in range(100):
        agent._extract_json_from_text(markdown_json)

@performance_profiler
def test_file_hashing():
    test_file = root / "temp_workspace" / "perf_test.txt"
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text("Hello world " * 1000)
    
    for i in range(100):
        get_file_hash(test_file)

def main():
    print("🚀 Đang chạy Benchmark cho các hàm cốt lõi...")
    test_json_extraction()
    test_file_hashing()
    print("✅ Hoàn tất Benchmark. Đã xuất báo cáo ra reports/FUNCTION_PERFORMANCE_AUDIT.md")

if __name__ == "__main__":
    main()
