
from core_utilities.http_client import HTTPClient
from .config import TELE_TOKEN, CHAT_ID


def send_message(text):
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    # Tắt markdown để tránh lỗi ký tự lạ từ AI
    payload = {'chat_id': CHAT_ID, 'text': text}

    try:
        response = HTTPClient.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("📩 Đã gửi tin nhắn Telegram!")
        else:
            print(f"⚠️ Lỗi gửi tin: {response.text}")
    except Exception as e:
        print(f"❌ Lỗi kết nối Telegram: {e}")
