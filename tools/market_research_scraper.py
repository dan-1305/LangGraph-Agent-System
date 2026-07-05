import urllib.request
import urllib.parse
import json
import time
import os

def scrape_reddit(subreddit, query):
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={urllib.parse.quote(query)}&restrict_sr=1&sort=relevance"
    req = urllib.request.Request(
        url, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    try:
        time.sleep(1) # Be nice to Reddit API
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('data', {}).get('children', [])
    except Exception as e:
        print(f"Error scraping {subreddit}: {e}")
        return []

def main():
    print("🚀 Khởi động Scraper Cào dữ liệu thị trường...")
    results = []
    
    # 1. Nhu cầu Video AI
    print("Đang quét r/Tiktokhelp...")
    posts = scrape_reddit("Tiktokhelp", "ai video editor expensive")
    for p in posts[:5]:
        results.append(f"- [Video AI] {p['data']['title']} (Score: {p['data']['score']})")

    # 2. Nhu cầu Dịch Game
    print("Đang quét r/IndieGaming...")
    posts = scrape_reddit("IndieGaming", "localization translate cost")
    for p in posts[:5]:
        results.append(f"- [Game Translation] {p['data']['title']} (Score: {p['data']['score']})")
        
    # 3. Nhu cầu Nuôi X/Twitter
    print("Đang quét r/Twitter...")
    posts = scrape_reddit("Twitter", "auto post bot banned")
    for p in posts[:5]:
        results.append(f"- [X Bot] {p['data']['title']} (Score: {p['data']['score']})")
        
    if not results:
        results.append("- Không lấy được dữ liệu do Reddit chặn (429/403). Sẽ dùng dữ liệu mô phỏng dựa trên xu hướng thực tế.")
        
    with open("IdeaAndBlueprint/market_scraped_data.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(results))
    print("✅ Đã lưu kết quả vào IdeaAndBlueprint/market_scraped_data.txt")

if __name__ == "__main__":
    import sys
    import io
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
    elif sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        
    main()
