import os
import sys
import urllib.request
import urllib.parse
import json
from pathlib import Path
from dotenv import load_dotenv

# Fix console encoding
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_youtube_api():
    print("="*50)
    print("🚀 YOUTUBE DATA API v3 - PING TEST")
    print("="*50)

    # 1. Load .env
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)

    # Tìm các biến môi trường có thể là YT API key
    api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("YT_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ LỖI: Không tìm thấy YOUTUBE_API_KEY trong file .env!")
        print("💡 Gợi ý: Hãy mở file .env và thêm dòng: YOUTUBE_API_KEY=YOUR_KEY_HERE")
        return

    print("✅ Đã tìm thấy API Key trong .env. Bắt đầu gọi API...")
    
    # 2. Call API (Lấy video đang trending tại US)
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=1&key={api_key}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                items = data.get("items", [])
                
                print("\n✅ KẾT QUẢ TỪ GOOGLE: API KEY HỢP LỆ VÀ ĐANG HOẠT ĐỘNG TỐT!")
                if items:
                    video = items[0]
                    snippet = video.get("snippet", {})
                    stats = video.get("statistics", {})
                    print("-" * 50)
                    print(f"📺 Top 1 Trending Video hiện tại:")
                    print(f"📌 Tựa đề: {snippet.get('title')}")
                    print(f"👤 Kênh: {snippet.get('channelTitle')}")
                    print(f"👀 Lượt xem: {int(stats.get('viewCount', 0)):,} views")
                    print(f"👍 Lượt thích: {int(stats.get('likeCount', 0)):,} likes")
                    print("-" * 50)
                else:
                    print("⚠️ Trả về mảng rỗng, nhưng API Key không bị lỗi.")
            else:
                print(f"❌ LỖI TỪ GOOGLE: HTTP Status {response.status}")
                
    except urllib.error.HTTPError as e:
        print(f"❌ LỖI API (HTTP {e.code}):")
        error_info = e.read().decode('utf-8')
        try:
            err_json = json.loads(error_info)
            msg = err_json.get("error", {}).get("message", error_info)
            print(f"   => {msg}")
        except:
            print(f"   => {error_info}")
        print("\n💡 Gợi ý: Kiểm tra lại API Key xem có copy nhầm khoảng trắng không, hoặc key đã được bật Youtube Data API v3 chưa.")
    except Exception as e:
        print(f"❌ LỖI HỆ THỐNG: {e}")

if __name__ == "__main__":
    test_youtube_api()
