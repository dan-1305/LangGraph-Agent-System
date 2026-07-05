import os
from pathlib import Path
import sys

# Setup sys.path cho Monorepo
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from core_utilities.http_client import HTTPClient
from bs4 import BeautifulSoup
import argparse
from src.base_agent import BaseAgent

# Force UTF-8
import io
if hasattr(sys.stdout, "reconfigure"):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

class GameWebScraper(BaseAgent):
    def __init__(self):
        super().__init__(name="GameWebScraper", role="Scraper")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _ai_handler(self, *args, **kwargs):
        pass

    def _logic_handler(self, *args, **kwargs):
        pass

    def scrape_url(self, url):
        """Cào nội dung văn bản từ một URL."""
        print(f"🌐 Đang cào dữ liệu từ: {url}...")
        try:
            response = HTTPClient.get(url, headers=self.headers, timeout=20.0, use_httpx=True)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Loại bỏ script và style
            for script in soup(["script", "style"]):
                script.extract()
            
            text = soup.get_text(separator='\n')
            
            # Làm sạch text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return clean_text
        except Exception as e:
            print(f"❌ Lỗi khi cào web: {e}")
            return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Game Web Scraper")
    parser.add_argument("--url", required=True, help="URL cần cào")
    parser.add_argument("--output", required=True, help="Đường dẫn file lưu kết quả")
    
    args = parser.parse_args()
    
    scraper = GameWebScraper()
    content = scraper.scrape_url(args.url)
    
    if content:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Đã lưu nội dung cào được vào: {args.output}")
