import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import httpx
import asyncio
import threading

class TelegramAlertHandler(logging.Handler):
    """
    Custom Logging Handler to send ERROR/CRITICAL logs to Telegram.
    Uses httpx to send messages asynchronously without blocking the main thread.
    """
    def __init__(self):
        super().__init__()
        self.bot_token = os.getenv("TELE_TOKEN")
        self.chat_id = os.getenv("CHAT_ID")
        self.api_url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"

    def emit(self, record):
        if not self.bot_token or not self.chat_id:
            return

        try:
            log_entry = self.format(record)
            message = f"🚨 *SYSTEM ALERT*\n\n```log\n{log_entry}\n```"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "MarkdownV2"
            }
            
            # Run the API call in a separate thread so it doesn't block
            threading.Thread(target=self._send_message, args=(payload,), daemon=True).start()
        except Exception:
            self.handleError(record)

    def _send_message(self, payload):
        try:
            with httpx.Client(timeout=5.0) as client:
                client.post(self.api_url, json=payload)
        except Exception as e:
            # We don't want to log the error using the logger to avoid infinite loops,
            # so we just ignore Telegram delivery failures.
            pass

def get_logger(name: str) -> logging.Logger:
    """
    Tạo và trả về một logger tập trung cho dự án.
    Hỗ trợ Rotate Log để không làm đầy ổ cứng.
    """
    logger = logging.getLogger(name)
    
    # Chỉ thêm handler nếu chưa có để tránh duplicate log
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Thư mục logs ở gốc dự án
        base_dir = Path(__file__).resolve().parent.parent
        log_dir = base_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / "system_core.log"
        
        # Format chuẩn
        formatter = logging.Formatter(
            '%(asctime)s - [%(name)s] - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler 1: Ghi ra file với cơ chế Rotate (Tối đa 5MB/file, giữ 3 file cũ)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # Handler 2: In ra Console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Handler 3: Telegram Alert (chỉ bắt level ERROR trở lên)
        telegram_handler = TelegramAlertHandler()
        telegram_handler.setLevel(logging.ERROR)
        telegram_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        logger.addHandler(telegram_handler)
        
    return logger
