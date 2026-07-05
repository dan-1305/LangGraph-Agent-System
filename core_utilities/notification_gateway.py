import os
import requests
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

def send_alert(message: str, level: str = "INFO", component: str = "SYSTEM"):
    """Gửi cảnh báo qua Telegram"""
    token = os.getenv("TELE_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    
    if not token or not chat_id:
        return False
        
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    emoji = "ℹ️"
    if level == "WARNING":
        emoji = "⚠️"
    elif level == "ERROR":
        emoji = "🚨"
        
    formatted_msg = f"[{emoji} {component}] {level}\n\n{message}"
    
    try:
        payload = {
            "chat_id": chat_id,
            "text": formatted_msg,
            "parse_mode": "HTML"
        }
        # Nếu gửi HTML lỗi thì gửi plain text
        res = requests.post(url, json=payload, timeout=10.0)
        if not res.ok:
            payload["parse_mode"] = ""
            requests.post(url, json=payload, timeout=10.0)
        return True
    except Exception as e:
        print(f"Failed to send Telegram alert: {e}")
        return False
