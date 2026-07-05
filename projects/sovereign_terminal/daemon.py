import asyncio
import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from projects.sovereign_terminal.core.config import Config
from tools.system.awaken import generate_morning_briefing
from tools.system.workflow_engine import WorkflowEngine
from projects.ai_trading_agent.src.whale_alert import WhaleAlertMonitor
from core_utilities.http_client import HTTPClient
import os

async def send_telegram_message(message: str):
    """Gửi tin nhắn qua Telegram dùng TELE_TOKEN và CHAT_ID."""
    from dotenv import load_dotenv
    load_dotenv()
    tele_token = os.getenv("TELE_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if tele_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message
            }
            HTTPClient.post(url, json=payload, timeout=10.0)
            print("[DAEMON] Đã gửi thông báo qua Telegram.")
        except Exception as e:
            print(f"[DAEMON ERROR] Không thể gửi Telegram: {e}")

async def task_morning_briefing():
    """Chạy báo cáo buổi sáng."""
    print("[DAEMON] Đang chạy Morning Briefing...")
    # 1. Chạy hàm generate_morning_briefing có sẵn gửi qua Telegram
    generate_morning_briefing()
    
    # 2. Chạy workflow chain nếu cần
    print("[DAEMON] Đang chạy Workflow 'morning_awaken' (nếu tồn tại)...")
    try:
        engine = WorkflowEngine()
        result = engine.run_chain("morning_awaken")
        print(f"[DAEMON] Workflow Result: {result}")
    except Exception as e:
        print(f"[DAEMON ERROR] {e}")

async def run_forever():
    """Chạy vòng lặp vô tận (Daemon) - Level 4 Event-Driven."""
    print("🚀 [DAEMON] Khởi động Sovereign Daemon Mode...")
    print("Vòng lặp đang chạy. Nhấn Ctrl+C để thoát.")
    
    # Chu kỳ quét Whale Alert: 60 phút / 1 lần
    whale_interval = 60 * 60
    last_whale_check = 0

    while True:
        import time
        now = time.time()

        # 1. Whale Alert Trigger
        if now - last_whale_check >= whale_interval:
            print("[DAEMON] 🐋 Kích hoạt quét Whale Alert...")
            last_whale_check = now
            try:
                monitor = WhaleAlertMonitor()
                summary = monitor.get_whale_alert_summary(hours=1) # Chỉ quét trong 1 giờ qua
                # Nếu có cảnh báo thực sự (không phải mảng rỗng hoặc No alert)
                if "WHALE ALERT" in summary and "No significant whale movements" not in summary:
                    print("[DAEMON] 🐋 Phát hiện Whale Alert! Gửi Telegram...")
                    await send_telegram_message(summary)
                else:
                    print("[DAEMON] 🐋 Không có biến động Whale lớn trong 1h qua.")
            except Exception as e:
                print(f"[DAEMON ERROR] Lỗi khi chạy Whale Alert: {e}")

        # Tương lai: Thêm các Event Trigger khác (VD: Farm Airdrop lúc 2h sáng)
        
        await asyncio.sleep(60) # Main loop sleep 1 phút

def main():
    parser = argparse.ArgumentParser(description="Sovereign Terminal Daemon")
    parser.add_argument("--task", type=str, help="Tên task cần chạy ngay lập tức rồi thoát.")
    args = parser.parse_args()

    if args.task == "morning_briefing":
        asyncio.run(task_morning_briefing())
    elif args.task:
        print(f"[DAEMON ERROR] Task không được hỗ trợ: {args.task}")
    else:
        # Nếu không có tham số, chạy mãi mãi
        try:
            asyncio.run(run_forever())
        except KeyboardInterrupt:
            print("\n[DAEMON] Đã dừng Daemon.")

if __name__ == "__main__":
    main()
