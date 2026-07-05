import time
import schedule
import subprocess
import os
import sys
import io
import json
import logging
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Configure paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# [CRITICAL] Cài đặt import cho môi trường cục bộ
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Force stdout to be UTF-8 for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# [QUAN TRỌNG] Thiết lập PYTHONPATH cho toàn bộ môi trường
os.environ["PYTHONPATH"] = BASE_DIR + os.pathsep + os.environ.get("PYTHONPATH", "")

# Setup Logging
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"scheduler_{datetime.now().strftime('%Y-%m')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("MainScheduler")

# Project paths
REAL_ESTATE_SCRAPER_PATH = os.path.join(BASE_DIR, "projects", "universal_web_scraper", "src", "batdongsan_playwright.py")
DATA_FETCHER_PATH = os.path.join(BASE_DIR, "projects", "ai_trading_agent", "src", "data_fetcher.py")
LIVE_ADVISOR_PATH = os.path.join(BASE_DIR, "projects", "ai_trading_agent", "live_advisor.py")
AIRDROP_GUERRILLA_PATH = os.path.join(BASE_DIR, "projects", "airdrop_guerrilla", "src", "modes", "full_auto_cli.py")

# State Management cho cơ chế chạy bù (Catch-up)
STATE_FILE = os.path.join(LOG_DIR, "scheduler_state.json")

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding='utf-8') as f:
                return json.load(f)
        except: pass
    return {}

def save_state(state):
    try:
        with open(STATE_FILE, "w", encoding='utf-8') as f:
            json.dump(state, f, indent=4)
    except Exception as e:
        logger.error(f"Lỗi khi lưu state: {e}")

def update_job_state(job_name):
    state = load_state()
    state[f"last_{job_name}_date"] = datetime.now().strftime("%Y-%m-%d")
    save_state(state)

# Helper function for subprocess with retry and logging
def run_with_retry_and_log(cmd: list, cwd: str, timeout: int, max_retries: int = 2, job_name: str = "Job"):
    """
    Run a subprocess with capture_output, retry on failure, and return (success_bool, error_snippet)
    """
    # Đồng bộ môi trường cho subprocess - Cực kỳ quan trọng
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = BASE_DIR + os.pathsep + current_env.get("PYTHONPATH", "")
    current_env["PYTHONIOENCODING"] = "utf-8"

    for attempt in range(1, max_retries + 1):
        logger.info(f"[{job_name}] Attempt {attempt}/{max_retries}...")
        try:
            # Dùng executable để gọi script python
            full_cmd = [sys.executable] + cmd if not str(cmd[0]).endswith('.exe') else cmd
            
            result = subprocess.run(full_cmd, cwd=cwd, timeout=timeout, capture_output=True, text=True, encoding='utf-8', errors='replace', env=current_env)
            if result.returncode == 0:
                logger.info(f"[{job_name}] Attempt {attempt} successful.")
                return True, ""
            else:
                err_text = result.stderr.strip() if result.stderr.strip() else result.stdout.strip()
                err_snippet = err_text[-500:]
                logger.warning(f"[{job_name}] Attempt {attempt} failed with code {result.returncode}.\nSnippet: {err_snippet}")
                
                if attempt == max_retries:
                    return False, err_snippet
                
                logger.info(f"[{job_name}] Waiting 30s before retry...")
                time.sleep(30)
                
        except subprocess.TimeoutExpired:
            logger.error(f"[{job_name}] Attempt {attempt} timed out (> {timeout}s).")
            if attempt == max_retries:
                return False, "TIMEOUT_EXPIRED"
            time.sleep(10)
        except Exception as e:
            logger.error(f"[{job_name}] Attempt {attempt} crash: {e}")
            if attempt == max_retries:
                return False, str(e)
            time.sleep(10)
            
    return False, "UNKNOWN_ERROR"

# Telegram Alert
def send_telegram_alert(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not token or not chat_id:
        logger.warning("Không có TELEGRAM_BOT_TOKEN hoặc CHAT_ID để gửi cảnh báo.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        logger.error(f"Lỗi khi gửi Telegram: {e}")


# Track states
scrape_run_count = 0
TOTAL_SCRAPE_RUNS = 10
executor = ThreadPoolExecutor(max_workers=1)

def run_queued(func):
    """Decorator để đẩy job vào hàng đợi của ThreadPoolExecutor"""
    def wrapper():
        executor.submit(func)
    return wrapper

@run_queued
def scrape_job():
    global scrape_run_count
    if scrape_run_count >= TOTAL_SCRAPE_RUNS:
        logger.info("[Scraper] Đã hoàn thành mục tiêu. Ngừng chạy tác vụ.")
        return schedule.CancelJob
        
    scrape_run_count += 1
    logger.info(f"=== [Scraper] Đang chạy lần {scrape_run_count}/{TOTAL_SCRAPE_RUNS} ===")
    
    success, err_log = run_with_retry_and_log([REAL_ESTATE_SCRAPER_PATH], BASE_DIR, 1800, max_retries=2, job_name="Scraper")
    if success:
        logger.info(f"[Scraper] Lần {scrape_run_count} hoàn tất.")
    else:
        logger.error("[Scraper] Thất bại hoàn toàn sau các lượt thử.")
        err_msg = str(err_log).replace('<', '<').replace('>', '>')
        send_telegram_alert(f"⚠️ <b>[Scraper]</b> Thất bại!\n<pre>{err_msg}</pre>")

@run_queued
def daily_trading_job():
    logger.info("=== [AI Trading] BẮT ĐẦU CHU TRÌNH GIAO DỊCH NGÀY MỚI ===")
    
    current_env = os.environ.copy()
    current_env["PYTHONPATH"] = BASE_DIR + os.pathsep + current_env.get("PYTHONPATH", "")
    current_env["PYTHONIOENCODING"] = "utf-8"

    logger.info("[AI Trading] Đang cập nhật dữ liệu OHLCV...")
    subprocess.run([sys.executable, DATA_FETCHER_PATH], cwd=BASE_DIR, timeout=600, env=current_env)
    
    logger.info("[AI Trading] Đang gọi AI Live Advisor phân tích...")
    success, err_log = run_with_retry_and_log([LIVE_ADVISOR_PATH], BASE_DIR, 1200, max_retries=2, job_name="AI Trading Advisor")
    
    if success:
        logger.info("✅ [AI Trading] HOÀN TẤT CHU TRÌNH.")
        update_job_state("trading")
    else:
        logger.error("[AI Trading] Thất bại hoàn toàn.")
        err_msg = str(err_log).replace('<', '<').replace('>', '>')
        send_telegram_alert(f"⚠️ <b>[AI Trading]</b> Thất bại!\n<i>Lỗi:</i>\n<pre>{err_msg}</pre>")

@run_queued
def airdrop_job():
    logger.info("=== [Airdrop Guerrilla] BẮT ĐẦU CÀY AIRDROP (FULL-AUTO) ===")
    
    success, err_log = run_with_retry_and_log([AIRDROP_GUERRILLA_PATH], BASE_DIR, 3600, max_retries=2, job_name="Airdrop Guerrilla")
    
    if success:
        logger.info("✅ [Airdrop Guerrilla] Hoàn tất phiên cày cuốc On-chain.")
        update_job_state("airdrop")
        send_telegram_alert("✅ <b>[Airdrop Guerrilla]</b> Hoàn thành phiên cày cuốc On-chain thành công!")
    else:
        logger.error("[Airdrop Guerrilla] Thất bại hoàn toàn.")
        err_msg = str(err_log).replace('<', '<').replace('>', '>')
        send_telegram_alert(f"⚠️ <b>[Airdrop Guerrilla]</b> Thất bại!\n<i>Lỗi:</i>\n<pre>{err_msg}</pre>")

# Thử load OmniOverlord sử dụng import tuyệt đối
try:
    import src.factory.nodes.omni_overlord as omni_module
    overlord_instance = omni_module.OmniOverlord()
except Exception as e:
    logger.error(f"Failed to load OmniOverlord: {e}")
    overlord_instance = None

@run_queued
def omni_overlord_watchdog():
    if not overlord_instance:
        return
    logger.info("=== [Omni Overlord] KÍCH HOẠT WATCHDOG ===")
    decision = overlord_instance.check_market_pulse()
    
    if decision.get("emergency_trading"):
        logger.warning(f"🚨 OVERLORD TRIGGER: {decision.get('reason')}")
        send_telegram_alert(f"🚨 <b>[OMNI OVERLORD] KÍCH HOẠT KHẨN CẤP AI TRADING!</b>\nLý do: {decision.get('reason')}")
        daily_trading_job()
    elif decision.get("guerrilla_airdrop_boost"):
        logger.info(f"⚡ OVERLORD TRIGGER: {decision.get('reason')}")
        send_telegram_alert(f"⚡ <b>[OMNI OVERLORD] KÍCH HOẠT CÀY AIRDROP GẤP!</b>\nLý do: {decision.get('reason')}")
        airdrop_job()
    else:
        logger.info("[Omni Overlord] Thị trường bình ổn.")

def check_missed_jobs():
    """Kiểm tra xem khi khởi động máy có bị lỡ job nào của ngày hôm nay không."""
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    now_hour = datetime.now().hour

    logger.info("🔍 Đang rà soát các tác vụ bị nhỡ trong ngày...")
    
    # AI Trading hẹn chạy lúc 07:00
    if now_hour >= 7 and state.get("last_trading_date") != today:
        logger.info("⚡ Phát hiện nhỡ lịch AI Trading! Đang kích hoạt chạy bù...")
        send_telegram_alert("⚡ <b>[Scheduler]</b> Phát hiện mở máy trễ, tự động chạy bù AI Trading!")
        daily_trading_job()

    # Airdrop Guerrilla hẹn chạy lúc 19:00
    if now_hour >= 19 and state.get("last_airdrop_date") != today:
        logger.info("⚡ Phát hiện nhỡ lịch Airdrop! Đang kích hoạt chạy bù...")
        send_telegram_alert("⚡ <b>[Scheduler]</b> Phát hiện mở máy trễ, tự động chạy bù Airdrop Guerrilla!")
        airdrop_job()

# Lập lịch
schedule.every(1).hours.do(omni_overlord_watchdog)
schedule.every(30).minutes.do(scrape_job)
schedule.every().day.at("07:00").do(daily_trading_job)
schedule.every().day.at("19:00").do(airdrop_job)

if __name__ == "__main__":
    logger.info("==========================================================")
    logger.info("   🚀 HỆ THỐNG SCHEDULER TỔNG HỢP V2 (SMART CATCH-UP) 🚀")
    logger.info("==========================================================")
    
    # Kiểm tra job chạy bù ngay khi vừa bật
    check_missed_jobs()
    
    logger.info("Các tác vụ đã lên lịch:")
    logger.info(" - Omni Overlord Watchdog: Mỗi 1 giờ")
    logger.info(" - Cào BĐS: Mỗi 30 phút")
    logger.info(" - AI Trading: 07:00 sáng hàng ngày")
    logger.info(" - Airdrop Guerrilla: 19:00 tối hàng ngày")
    logger.info(" (Mode: Single-Worker Queue - Ngăn quá tải CPU, Log ghi vào /logs)\n")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("🛑 Đã nhận lệnh tắt. Đang chờ các tác vụ hoàn tất...")
        executor.shutdown(wait=True)
        logger.info("Đã tắt Main Scheduler an toàn!")
        sys.exit(0)
