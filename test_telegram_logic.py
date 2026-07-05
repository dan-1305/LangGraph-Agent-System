import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from projects.sovereign_terminal.gateways.telegram_bot import initialize_system, process_message

async def main():
    print("=== BAT DAU TEST TELEGRAM LOGIC ===")
    await initialize_system()
    
    chat_id = 123456
    
    print("\n[Admin] Liệt kê các file trong thư mục projects/sovereign_terminal/")
    response = await process_message("Liệt kê các file trong thư mục projects/sovereign_terminal/", chat_id)
    print(f"\n[Bot] {response}")
    
    print("\n[Admin] Hãy chạy trigger_factory_workflow để kiểm tra dự án này với requirement 'Khởi tạo file test'")
    response = await process_message("Hãy chạy trigger_factory_workflow cho mode 'new', project 'sovereign_terminal' với requirement 'Khởi tạo file test dummy'", chat_id)
    print(f"\n[Bot] {response}")

if __name__ == "__main__":
    asyncio.run(main())
