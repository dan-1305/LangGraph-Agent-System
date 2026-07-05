import os
import sys
import sqlite3
import datetime
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

# Bỏ qua ép kiểu ở đây để không bị xung đột TextIOWrapper

# Import from local project
auto_x_bot_path = base_dir / "projects" / "auto_x_bot" / "src"
if str(auto_x_bot_path) not in sys.path:
    sys.path.insert(0, str(auto_x_bot_path))

from x_api_client import XApiClient
from content_generator import ContentGenerator

# Dùng path tương đối để import từ project khác (Trading Agent)
ai_trading_path = base_dir / "projects" / "ai_trading_agent" / "src"
if str(ai_trading_path) not in sys.path:
    sys.path.insert(0, str(ai_trading_path))

from news_scraper import fetch_cointelegraph_news
from core_utilities.notification_gateway import send_alert

def log_to_db(tweet_id: str, content: str, status: str):
    """Lưu lịch sử đăng Tweet vào database."""
    db_path = base_dir / "data" / "system_logs.db"
    db_path.parent.mkdir(exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path, timeout=10.0)
        conn.execute('PRAGMA journal_mode=WAL;')
        
        # Tạo bảng nếu chưa có
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Auto_X_Logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tweet_id TEXT,
                content TEXT,
                status TEXT
            )
        """)
        
        conn.execute("""
            INSERT INTO Auto_X_Logs (tweet_id, content, status)
            VALUES (?, ?, ?)
        """, (tweet_id, content, status))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Lỗi ghi log database: {e}")

def main():
    print("==================================================")
    print("🚀 BẮT ĐẦU CHU TRÌNH AUTO-X CONTENT CREATOR")
    print("==================================================")
    
    # Khởi tạo API
    x_client = XApiClient()
    
    # 1. Cào tin tức
    print("📰 Đang cào tin tức nóng nhất thị trường...")
    news_items = fetch_cointelegraph_news(limit=5)
    
    if not news_items or len(news_items) == 0 or "Không thể lấy tin tức" in news_items[0]:
        print("⚠️ Không có tin tức, hoặc bị lỗi mạng. Sẽ dùng tin tức mặc định.")
        news_items = ["Cá voi đang gom mạnh Bitcoin ở vùng giá hiện tại.", "Thị trường dự báo sóng gió tuần tới."]
    else:
        print(f"✅ Đã lấy được {len(news_items)} tin tức.")
        
    # 2. Sinh Content
    print("🧠 Đang gọi AI (Gemini) để suy nghĩ Tweet...")
    generator = ContentGenerator()
    tweet_content = generator.generate_crypto_tweet(news_items)
    
    print("\n📝 NỘI DUNG TWEET DỰ KIẾN:")
    print("-" * 50)
    print(tweet_content)
    print("-" * 50)
    print(f"Độ dài: {len(tweet_content)} ký tự.\n")
    
    if len(tweet_content) > 280:
        print("⚠️ Cảnh báo: Tweet vượt quá 280 ký tự, có thể bị lỗi khi đăng.")
    
    # 3. Đăng bài lên X
    if not x_client.is_connected:
        print("⏸️ BỎ QUA BƯỚC ĐĂNG BÀI: Bạn chưa cung cấp đủ Twitter API Keys trong .env.")
        print("💾 Lưu nháp vào Database...")
        log_to_db("DRAFT", tweet_content, "DRAFT_NO_API_KEY")
        send_alert(f"📝 <b>[Auto-X]</b> Đã sinh bản nháp Tweet (Chưa đăng vì thiếu API Key):\n<i>{tweet_content}</i>", level="WARNING", component="AUTO-X")
        return

    print("🐦 Đang gửi lệnh đăng bài lên X...")
    tweet_id = x_client.post_tweet(tweet_content)
    
    if tweet_id:
        print(f"✅ Đăng thành công! Tweet ID: {tweet_id}")
        log_to_db(str(tweet_id), tweet_content, "SUCCESS")
        send_alert(f"✅ <b>[Auto-X]</b> Đã đăng Tweet thành công!\nID: {tweet_id}\nNội dung: <i>{tweet_content}</i>", level="INFO", component="AUTO-X")
    else:
        print("❌ Đăng bài thất bại.")
        log_to_db("ERROR", tweet_content, "FAILED")
        send_alert(f"❌ <b>[Auto-X]</b> Đăng Tweet THẤT BẠI. Xem log để biết chi tiết.", level="CRITICAL", component="AUTO-X")

if __name__ == "__main__":
    main()
