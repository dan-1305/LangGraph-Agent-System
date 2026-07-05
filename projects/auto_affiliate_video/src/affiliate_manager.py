from core_utilities.http_client import HTTPClient
import os
from src.config import GlobalConfig

class AffiliateManager:
    """Module quản lý việc lấy link Affiliate từ mạng AccessTrade."""
    
    def __init__(self):
        self.api_url = GlobalConfig.get("AT_BASE_URL", "https://api.accesstrade.vn/v1")
        self.access_key = GlobalConfig.get("AT_ACCESS_KEY", "")
        self.campaigns = GlobalConfig.get("TARGET_CAMPAIGN_IDS", "shopee,lazada").split(",")
        
    def generate_affiliate_link(self, product_url: str) -> str:
        """
        Tạo link rút gọn Affiliate thông qua API của AccessTrade.
        Nếu API lỗi hoặc thiếu cấu hình, trả về link dự phòng.
        """
        if not self.access_key or not product_url:
            return "https://shopee.vn/flash_sale" # Dự phòng
            
        headers = {
            "Authorization": f"Token {self.access_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": product_url,
            "campaign": self.campaigns[0] if self.campaigns else "shopee"
        }
        
        try:
            # Lưu ý: Đây là giả lập endpoint tạo deeplink của AccessTrade. 
            # Tài liệu thực tế: https://developer.accesstrade.vn
            response = HTTPClient.post(f"{self.api_url}/deeplinks", headers=headers, json=payload, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get("short_link", product_url)
            else:
                print(f"⚠️ AccessTrade API lỗi {response.status_code}: Dùng link gốc.")
                return product_url
        except Exception as e:
            print(f"⚠️ Lỗi gọi AccessTrade: {e}")
            return "https://shopee.vn/flash_sale"
