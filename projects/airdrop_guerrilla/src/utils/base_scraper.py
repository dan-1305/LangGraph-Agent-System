import os
import time
import random
from pathlib import Path
from typing import Set, Dict, Any, Optional
import requests
from fake_useragent import UserAgent

class BaseScraper:
    """
    BaseScraper: Lớp cơ sở (Base Class) chuyên dụng cho việc cào dữ liệu (Web Scraping).
    Tích hợp các cơ chế Anti-Bot mạnh mẽ: Random User-Agent, Random Sleep, và Quản lý Lịch sử (Stateful).
    """
    def __init__(self, log_file: str):
        """
        Khởi tạo BaseScraper.
        
        Args:
            log_file (str): Đường dẫn đến file lưu trữ danh sách các trang/URL đã cào thành công.
        """
        self.log_file = Path(log_file)
        # Đảm bảo thư mục chứa file log tồn tại
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.ua = UserAgent(os='windows', browsers=['chrome', 'edge', 'firefox'])

    def get_scraped_items(self) -> Set[str]:
        """
        Đọc danh sách các items (trang/URL/ID) đã cào thành công từ log file.
        
        Returns:
            Set[str]: Tập hợp các ID hoặc số trang đã được cào.
        """
        if not self.log_file.exists():
            return set()
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return set(line.strip() for line in lines if line.strip())

    def add_scraped_item(self, item_id: str) -> None:
        """
        Ghi nhận một item (trang/URL/ID) đã cào thành công vào file log.
        
        Args:
            item_id (str): ID, số trang, hoặc URL định danh.
        """
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{item_id}\n")

    def build_headers(self) -> Dict[str, str]:
        """
        Tạo HTTP Headers ngẫu nhiên với IP spoofing và User-Agent mới để vượt qua WAF (Web Application Firewall).
        
        Returns:
            Dict[str, str]: Dictionary chứa các Headers tiêu chuẩn.
        """
        # Giả mạo IP tĩnh ngẫu nhiên
        fake_ip = f"{random.randint(11,190)}.{random.randint(1,250)}.{random.randint(1,250)}.{random.randint(1,250)}"
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,application/json,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': fake_ip,
            'Client-IP': fake_ip
        }

    def sleep_random(self, min_seconds: float = 3.0, max_seconds: float = 8.0) -> None:
        """
        Tạm dừng thực thi một khoảng thời gian ngẫu nhiên để giả lập thao tác của con người.
        
        Args:
            min_seconds (float): Thời gian chờ tối thiểu.
            max_seconds (float): Thời gian chờ tối đa.
        """
        sleep_time = random.uniform(min_seconds, max_seconds)
        time.sleep(sleep_time)

    def fetch_url(self, url: str) -> Optional[requests.Response]:
        """
        Thực hiện HTTP GET Request một cách an toàn (State-less) với Exponential Backoff.
        Retry tối đa 3 lần nếu gặp lỗi 429 hoặc 5xx.
        
        Args:
            url (str): URL cần lấy dữ liệu.
            
        Returns:
            Optional[requests.Response]: Trả về object Response nếu thành công, None nếu thất bại.
        """
        max_retries = 3
        backoff_times = [60, 300, 900]  # Thời gian chờ tương ứng cho mỗi lần retry (giây)
        
        for attempt in range(max_retries + 1):
            try:
                response = requests.get(url, headers=self.build_headers(), timeout=15)
                response.raise_for_status()
                return response
                
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 429 or 500 <= status_code < 600:
                    if attempt < max_retries:
                        sleep_time = backoff_times[attempt]
                        print(f"⚠️ Gặp lỗi {status_code}. Hệ thống tạm nghỉ {sleep_time}s trước khi thử lại (Lần {attempt + 1}/{max_retries})...")
                        time.sleep(sleep_time)
                        continue
                print(f"❌ Lỗi HTTP khi truy cập {url}: {e}")
                return None
                
            except requests.exceptions.RequestException as e:
                print(f"❌ Lỗi mạng khi truy cập {url}: {e}")
                return None
        return None
