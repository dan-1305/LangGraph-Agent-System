import psutil
import time
import os
import sys
import io
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

from core_utilities.notification_gateway import send_alert

import logging
from logging.handlers import RotatingFileHandler

# Thiết lập RotatingFileHandler cho log
log_dir = os.path.join(base_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "watchdog.log")
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[handler, logging.StreamHandler()])

# Cấu hình giới hạn
RAM_LIMIT_MB = 1000  # 1GB (Zombie browser)
SYSTEM_CPU_LIMIT_PCT = 90.0 # 90% CPU
SYSTEM_RAM_MIN_AVAILABLE_GB = 1.0 # 1GB RAM còn lại
MAX_UPTIME_HOURS = 2  # Chạy quá 2 tiếng là kill
TARGET_PROCESSES = ["chrome.exe", "chromium.exe", "msedge.exe"] # Tên process trình duyệt
# Trên Linux/Mac có thể là chrome, chromium, msedge không có đuôi .exe

def is_zombie_browser(proc: psutil.Process) -> bool:
    """Kiểm tra xem đây có phải là Zombie Process Browser từ Playwright/Selenium không"""
    try:
        # Check nếu tên nằm trong danh sách target
        name = proc.name().lower()
        if any(t in name for t in TARGET_PROCESSES):
            # Check tham số dòng lệnh xem có phải chạy ngầm (headless) không
            try:
                cmdline = " ".join(proc.cmdline()).lower()
                # Playwright/Selenium thường dùng các flag headless hoặc remote-debugging
                if "--headless" in cmdline or "--remote-debugging-port" in cmdline or "playwright" in cmdline:
                    return True
            except psutil.AccessDenied:
                pass
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    return False

def check_system_health():
    """Kiểm tra tổng thể CPU và RAM hệ thống để cảnh báo (Task 2.3)"""
    cpu_percent = psutil.cpu_percent(interval=2)
    mem = psutil.virtual_memory()
    mem_available_gb = mem.available / (1024 ** 3)
    
    alert_triggered = False
    alert_msg = "🚨 CẢNH BÁO TÀI NGUYÊN HỆ THỐNG QUÁ TẢI 🚨\n"
    
    if cpu_percent > SYSTEM_CPU_LIMIT_PCT:
        alert_msg += f"- CPU Usage: {cpu_percent}%\n"
        alert_triggered = True
        
    if mem_available_gb < SYSTEM_RAM_MIN_AVAILABLE_GB:
        alert_msg += f"- RAM Available: {mem_available_gb:.2f} GB\n"
        alert_triggered = True
        
    if alert_triggered:
        logging.warning(alert_msg.strip())
        send_alert(alert_msg.strip(), level="ERROR", component="WATCHDOG_HEALTH")
    else:
        logging.info(f"Hệ thống ổn định: CPU {cpu_percent}%, RAM Available {mem_available_gb:.2f}GB")

def check_and_kill_zombies():
    logging.info("==================================================")
    logging.info("🛡️ KÍCH HOẠT ĐẶC VỤ Y TẾ (PROCESS WATCHDOG)")
    logging.info("==================================================")
    
    killed_count = 0
    total_freed_mb = 0
    killed_details = []

    for proc in psutil.process_iter(['pid', 'name', 'create_time', 'memory_info']):
        try:
            if is_zombie_browser(proc):
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                create_time = proc.info['create_time']
                uptime_hours = (time.time() - create_time) / 3600
                
                # Điều kiện tiêu diệt: Ngốn RAM quá cao HOẶC chạy ngầm quá lâu
                if mem_mb > RAM_LIMIT_MB or uptime_hours > MAX_UPTIME_HOURS:
                    reason = f"Ngốn {mem_mb:.0f}MB RAM" if mem_mb > RAM_LIMIT_MB else f"Treo {uptime_hours:.1f} tiếng"
                    proc_name = proc.info['name']
                    pid = proc.info['pid']
                    
                    logging.info(f"🔫 Phát hiện Zombie [{proc_name} | PID: {pid}]. Lý do: {reason}. Đang tiêu diệt...")
                    proc.kill()
                    
                    killed_count += 1
                    total_freed_mb += mem_mb
                    killed_details.append(f"- <b>{proc_name}</b> (PID {pid}): {reason}")
                    
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if killed_count > 0:
        logging.info(f"✅ Đã dọn dẹp {killed_count} tiến trình ma, giải phóng {total_freed_mb:.0f} MB RAM.")
        # Báo cáo lên Telegram
        details_str = "\n".join(killed_details)
        alert_msg = (
            f"Đặc vụ Y tế vừa thực hiện đợt càn quét!\n"
            f"🧹 <b>Đã tiêu diệt:</b> {killed_count} Zombie Process\n"
            f"💾 <b>Giải phóng:</b> {total_freed_mb:.0f} MB RAM\n"
            f"Chi tiết:\n{details_str}"
        )
        send_alert(alert_msg, level="WARNING", component="WATCHDOG")
    else:
        logging.info("✅ Hệ thống sạch sẽ, không phát hiện Zombie Process nào ngốn RAM.")

def watchdog_loop():
    while True:
        check_system_health()
        check_and_kill_zombies()
        time.sleep(60) # Kiểm tra mỗi phút một lần

if __name__ == "__main__":
    watchdog_loop()
