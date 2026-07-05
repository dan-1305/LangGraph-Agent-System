import requests

def fetch_reddit_crypto_sentiment(limit=5):
    """
    Cào các hot posts từ r/CryptoCurrency để phân tích Social Sentiment.
    Không cần API Key, chỉ cần custom User-Agent.
    """
    url = f"https://www.reddit.com/r/CryptoCurrency/hot.json?limit={limit}"
    
    # Reddit yêu cầu custom User-Agent để tránh bị block (Error 429/403)
    # Không dùng fake Chrome UA vì Reddit sẽ chặn 403. Phải dùng đúng chuẩn: <platform>:<app ID>:<version>
    headers = {
        "User-Agent": "windows:langgraph_trading_agent:v2.0 (by /u/ai_admin)"
    }
    
    print("🗣️ Đang cào Social Sentiment từ Reddit (r/CryptoCurrency)...")
    
    posts_list = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            children = data.get("data", {}).get("children", [])
            for child in children:
                post = child.get("data", {})
                title = post.get("title", "")
                score = post.get("score", 0)
                num_comments = post.get("num_comments", 0)
                
                # Bỏ qua các pinned post (thường là daily discussion)
                if post.get("stickied", False):
                    continue
                    
                posts_list.append(f"Reddit: {title} | Upvotes: {score} | Comments: {num_comments}")
        else:
            print(f"⚠️ Reddit API lỗi: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Lỗi kết nối Reddit API: {e}")
        
    return posts_list[:limit]

if __name__ == "__main__":
    posts = fetch_reddit_crypto_sentiment()
    for p in posts:
        print(p)
