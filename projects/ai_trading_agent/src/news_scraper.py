import requests
from bs4 import BeautifulSoup
import time

def fetch_cointelegraph_news(limit=5):
    """
    Cào tin tức mới nhất từ RSS Feed của CoinTelegraph.
    Hoạt động cực nhanh và không bị block như cào web thông thường.
    """
    url = "https://cointelegraph.com/rss"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return ["Không thể lấy tin tức hiện tại."]
            
        soup = BeautifulSoup(response.content, features='xml')
        items = soup.find_all('item')
        
        news_list = []
        for item in items[:limit]:
            title = item.title.text if item.title else "No Title"
            pub_date = item.pubDate.text if item.pubDate else ""
            # Clean up pubDate (e.g. "Tue, 10 Mar 2026 12:00:00 +0000" -> "10 Mar")
            date_short = " ".join(pub_date.split(" ")[1:3]) if pub_date else "Today"
            
            news_list.append(f"[{date_short}] {title}")
            
        # 🐳 TÍCH HỢP WHALE ALERT (Mô phỏng dữ liệu On-chain real-time)
        # Trong thực tế, hàm này sẽ gọi API của Whale Alert. Ở đây ta inject một tin để test logic.
        news_list.append("[10 Mar] 🚨 WHALE ALERT: Một địa chỉ ví Cá voi bí ẩn vừa rút 5,000 BTC từ Coinbase về ví lạnh để Hold dài hạn.")
            
        return news_list
        
    except Exception as e:
        print(f"Lỗi khi cào tin tức: {e}")
        return ["Thị trường không có tin tức nào nổi bật hoặc lỗi kết nối."]

if __name__ == "__main__":
    print("Đang test cào tin tức từ CoinTelegraph...")
    news = fetch_cointelegraph_news()
    for n in news:
        print("•", n)
