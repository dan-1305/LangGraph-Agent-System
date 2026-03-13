import time
import schedule
import subprocess
import os
import sys
from datetime import datetime
import threading

# Configure paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# Project paths
REAL_ESTATE_SCRAPER_PATH = os.path.join(BASE_DIR, "projects", "universal_web_scraper", "src", "batdongsan_playwright.py")
DATA_FETCHER_PATH = os.path.join(BASE_DIR, "projects", "ai_trading_agent", "data_fetcher.py")
LIVE_ADVISOR_PATH = os.path.join(BASE_DIR, "projects", "ai_trading_agent", "live_advisor.py")

print("==========================================================")
print("   🚀 HỆ THỐNG SCHEDULER TỔNG HỢP (MAIN SCHEDULER) 🚀")
print("==========================================================")
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Scheduler đã khởi động!")

# Track states
scrape_run_count = 0
TOTAL_SCRAPE_RUNS = 10

def run_in_thread(func):
    """Decorator to run jobs in separate threads so they don't block each other"""
    def wrapper():
        thread = threading.Thread(target=func)
        thread.start()
    return wrapper

@run_in_thread
def scrape_job():
    """Job cào dữ liệu BĐS mỗi 30 phút"""
    global scrape_run_count
    
    if scrape_run_count >= TOTAL_SCRAPE_RUNS:
        print("\n[Scraper] Đã hoàn thành mục tiêu chiến dịch cào BĐS. Ngừng chạy tác vụ này.")
        return schedule.CancelJob
        
    scrape_run_count += 1
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{current_time}] === [Scraper] Đang chạy lần {scrape_run_count}/{TOTAL_SCRAPE_RUNS} ===")
    
    try:
        result = subprocess.run(
            [sys.executable, REAL_ESTATE_SCRAPER_PATH], 
            capture_output=False,
            cwd=BASE_DIR
        )
        
        if result.returncode != 0:
            print(f"[!] [Scraper] Cảnh báo: Lần {scrape_run_count} gặp lỗi. Đang dọn dẹp Chrome zombie...")
            if os.name == 'nt':
                os.system("taskkill /f /im chrome.exe /t >nul 2>&1")
                os.system("taskkill /f /im chromium.exe /t >nul 2>&1")
        else:
            print(f"[OK] [Scraper] Lần {scrape_run_count} hoàn tất. Dữ liệu đã được đẩy vào SQLite.")
            
    except Exception as e:
        print(f"[!] [Scraper] Lỗi khi thực thi script: {e}")

@run_in_thread
def daily_trading_job():
    """Job Trading AI chạy 07:00 sáng hằng ngày"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{current_time}] === [AI Trading] BẮT ĐẦU CHU TRÌNH GIAO DỊCH NGÀY MỚI ===")
    
    try:
        print("[AI Trading] 🔄 Đang cập nhật dữ liệu OHLCV và Fear & Greed...")
        subprocess.run(
            [sys.executable, DATA_FETCHER_PATH], 
            capture_output=False,
            cwd=BASE_DIR
        )
        
        print("[AI Trading] 🧠 Đang gọi AI Live Advisor phân tích và đặt lệnh...")
        subprocess.run(
            [sys.executable, LIVE_ADVISOR_PATH], 
            capture_output=False,
            cwd=BASE_DIR
        )
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ [AI Trading] HOÀN TẤT CHU TRÌNH GIAO DỊCH.")
    except Exception as e:
        print(f"[!] [AI Trading] Lỗi hệ thống khi chạy Scheduler: {e}")

# Lập lịch
schedule.every(30).minutes.do(scrape_job)
schedule.every().day.at("07:00").do(daily_trading_job)

if __name__ == "__main__":
    print("\nCác tác vụ đã lên lịch:")
    print(" - Cào BĐS: Mỗi 30 phút")
    print(" - AI Trading: 07:00 sáng hàng ngày")
    
    # Giữ script chạy ngầm
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Đã tắt Main Scheduler!")
        sys.exit(0)
