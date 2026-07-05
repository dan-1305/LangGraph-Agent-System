import requests
from datetime import datetime, timedelta

def fetch_github_trending_crypto(days=7, limit=5):
    """
    Lấy danh sách các repository liên quan đến crypto/blockchain 
    đang trending (nhiều sao nhất) trên GitHub trong `days` ngày qua.
    """
    date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    query = f"(topic:crypto OR topic:blockchain OR topic:web3 OR topic:bitcoin OR topic:ethereum OR topic:solana) created:>{date_from}"
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    print(f"🐙 Đang cào GitHub Trending Repos (từ {date_from})...")
    
    trending_list = []
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            for item in items[:limit]:
                repo_name = item.get("name")
                desc = item.get("description")
                stars = item.get("stargazers_count")
                lang = item.get("language")
                trending_list.append(f"Repo: {repo_name} | Stars: {stars} | Lang: {lang} | Desc: {desc}")
        else:
            print(f"⚠️ GitHub API lỗi: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Lỗi kết nối GitHub API: {e}")
        
    return trending_list

if __name__ == "__main__":
    repos = fetch_github_trending_crypto()
    for r in repos:
        print(r)
