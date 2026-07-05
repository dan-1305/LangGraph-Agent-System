import schedule
import time
import subprocess
from pathlib import Path
import sys

def job():
    print("\n" + "="*50)
    print("⏰ [SCHEDULER] Kích hoạt Job Tự động tạo Video Affiliate...")
    print("="*50)
    
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    cmd = f"uv run --package auto_affiliate_video python projects/auto_affiliate_video/src/main.py --product \"Khóa học ChatGPT Toàn tập\" --features \"Viết code, Lên kịch bản, Tự động hóa\""
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=str(base_dir))
        print("✅ [SCHEDULER] Hoàn thành Job ngày hôm nay.")
    except subprocess.CalledProcessError as e:
        print(f"❌ [SCHEDULER] Lỗi khi chạy Job: {e}")

if __name__ == "__main__":
    print("🕒 Bộ đếm lịch (Scheduler) đang chạy. Lịch đặt vào 20:00 mỗi ngày...")
    schedule.every().day.at("20:00").do(job)
    
    # Chế độ TEST
    if "--test" in sys.argv:
        print("🔧 [TEST MODE] Chạy thử Job ngay lập tức...")
        job()
    else:
        while True:
            schedule.run_pending()
            time.sleep(60)
