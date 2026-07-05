import sys
import asyncio
from pathlib import Path

# Thêm root vào sys.path để chạy ở mọi nơi
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.main import main

def run_headless_agent():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print("="*60)
    print("🚀 SOVEREIGN HEADLESS TERMINAL (PoC)")
    print("="*60)
    
    req = sys.argv[1] if len(sys.argv) > 1 else "hãy chạy regression guard để test code cho tôi"
    print(f"USER REQUEST: {req}\n")
    
    # Kích hoạt trực tiếp Meta-Graph của AI Software Factory
    asyncio.run(main(mode="new", project_name="LangGraph_Agent_System", user_requirement=req, file_path="src/base_agent.py"))

if __name__ == "__main__":
    run_headless_agent()
