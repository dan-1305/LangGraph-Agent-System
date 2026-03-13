import os
import sys
import pandas as pd
import time
import random
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# Tính đường dẫn thư mục gốc
base_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(base_dir))

# Chứa các hàm Stealth
class PlaywrightStealth:
    @staticmethod
    def random_scroll(page, min_scrolls=2, max_scrolls=5):
        scrolls = random.randint(min_scrolls, max_scrolls)
        for _ in range(scrolls):
            direction = 1 if random.random() < 0.7 else -1
            distance = random.randint(300, 800) * direction
            try:
                page.mouse.wheel(0, distance)
                time.sleep(random.uniform(1.0, 3.0))
            except:
                pass
            
    @staticmethod
    def human_pause(min_sec=3.0, max_sec=6.0):
        time.sleep(random.uniform(min_sec, max_sec))

class AlonhadatPlaywrightScraper:
    def __init__(self, output_csv: str, raw_data_path: str):
        self.output_csv = Path(output_csv)
        self.raw_data_path = Path(raw_data_path)
        self.districts_dongnai = [
            "Biên Hòa", "Long Thành", "Nhơn Trạch", "Trảng Bom", "Vĩnh Cửu", 
            "Thống Nhất", "Cẩm Mỹ", "Định Quán", "Xuân Lộc", "Tân Phú", "Long Khánh"
        ]

    def parse_page_data(self, page) -> list:
        # Chờ các phần tử xuất hiện
        try:
            page.wait_for_selector("article.property-item", timeout=15000)
        except:
            print("⚠️ Không tìm thấy property-item nào. Có thể do load chậm hoặc chặn.")
            return []
            
        items = page.locator("article.property-item")
        count = items.count()
        
        data = []
        for i in range(count):
            item = items.nth(i)
            
            # Title
            title_el = item.locator("h3.property-title")
            title = title_el.inner_text().strip() if title_el.count() > 0 else ""
            
            # Price
            price_el = item.locator("span[itemprop='price']")
            price = 0.0
            if price_el.count() > 0:
                content_attr = price_el.get_attribute("content")
                if content_attr:
                    try:
                        price = float(content_attr)
                    except ValueError:
                        pass
                        
            # Area (từ Title hoặc Description)
            area = 0.0
            area_match = re.search(r'(?i)(?:dt|diện tích)?\s*(\d+[\.,]?\d*)\s*m2', title)
            if area_match:
                try:
                    area = float(area_match.group(1).replace(',', '.'))
                except ValueError:
                    pass
            else:
                desc_el = item.locator("p.brief")
                if desc_el.count() > 0:
                    desc_text = desc_el.inner_text()
                    area_match_desc = re.search(r'(?i)(?:dt|diện tích|ngang)?\s*(\d+[\.,]?\d*)\s*m2', desc_text)
                    if area_match_desc:
                        try:
                            area = float(area_match_desc.group(1).replace(',', '.'))
                        except ValueError:
                            pass
            
            if area == 0.0 or price == 0.0:
                continue
                
            # District
            district = ""
            address_el = item.locator("p.new-address")
            search_text = address_el.inner_text().lower() if address_el.count() > 0 else item.inner_text().lower()
            
            for d in self.districts_dongnai:
                if d.lower() in search_text:
                    district = d
                    break
            if not district:
                for d in self.districts_dongnai:
                    if d.lower() in title.lower():
                        district = d
                        break
                        
            if district:
                data.append({
                    'Title': title,
                    'Price_VND': price,
                    'Area_m2': area,
                    'District': district,
                    'Province': "Đồng Nai"
                })
        return data

    def run_scraper(self, target_pages: list):
        # Thiết lập user_agent cố định để không bị loạn session
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        
        all_data = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=ua, viewport={'width': 1366, 'height': 768})
            page = context.new_page()
            
            print("🚀 Bắt đầu cào Alonhadat bằng Playwright (Anti-Bot Bypass)...")
            
            for page_num in target_pages:
                if page_num == 1:
                    url = 'https://alonhadat.com.vn/can-ban-nha-dat/dong-nai'
                else:
                    url = f'https://alonhadat.com.vn/can-ban-nha-dat/dong-nai/trang-{page_num}'
                    
                print(f"\n🌍 Đang truy cập trang {page_num}: {url}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    
                    # Hành vi con người để đánh lừa Cloudflare
                    PlaywrightStealth.human_pause(2.0, 4.0)
                    PlaywrightStealth.random_scroll(page, 2, 4)
                    
                    # Check captcha/Cloudflare
                    if "captcha" in page.url.lower() or page.locator("iframe[src*='cloudflare']").count() > 0:
                        print("⚠️ Phát hiện Captcha/Cloudflare! Đang chờ xem có tự động giải được không...")
                        page.wait_for_timeout(10000)
                        
                    # Lấy dữ liệu
                    page_data = self.parse_page_data(page)
                    print(f"✅ Đã cào được {len(page_data)} tin đăng hợp lệ.")
                    all_data.extend(page_data)
                    
                except Exception as e:
                    print(f"❌ Lỗi khi cào trang {page_num}: {e}")
                    
            browser.close()
            
        if all_data:
            self.save_and_merge(all_data)
            
    def save_and_merge(self, data):
        df_new = pd.DataFrame(data)
        
        # Lưu ra CSV output của scraper
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
        if self.output_csv.exists():
            df_local = pd.read_csv(self.output_csv)
            df_combined = pd.concat([df_local, df_new], ignore_index=True)
        else:
            df_combined = df_new
            
        df_combined = df_combined.drop_duplicates(subset=['Title', 'Price_VND', 'Area_m2'])
        df_combined.to_csv(self.output_csv, index=False, encoding='utf-8')
        
        # Gộp vào Dataset AI
        if self.raw_data_path.exists():
            df_main = pd.read_csv(self.raw_data_path)
            common_cols = [c for c in df_new.columns if c in df_main.columns]
            merged_df = pd.concat([df_main, df_new[common_cols]], ignore_index=True)
            merged_df = merged_df.drop_duplicates(subset=['Title', 'Price_VND', 'Area_m2'])
            
            # Lọc bỏ rác
            bad_rows = merged_df['District'].str.contains('Đường|Quốc lộ|hẻm|Hẻm', case=False, na=False) | (merged_df['Area_m2'] < 10)
            merged_df = merged_df[~bad_rows]
            
            merged_df.to_csv(self.raw_data_path, index=False, encoding='utf-8')
            print(f"\n🎉 Đã gộp thành công! Tổng số dòng Dataset BĐS hiện tại: {len(merged_df)}")
        else:
            df_new.to_csv(self.raw_data_path, index=False, encoding='utf-8')
            print(f"\n🎉 Đã tạo mới Dataset. Tổng số dòng: {len(df_new)}")

if __name__ == "__main__":
    out_csv = base_dir / "projects" / "universal_web_scraper" / "data" / "output" / "alonhadat_dongnai_pw.csv"
    raw_csv = base_dir / "projects" / "real_estate_prediction" / "data" / "raw_data.csv"
    
    scraper = AlonhadatPlaywrightScraper(str(out_csv), str(raw_csv))
    
    # Test cào 3 trang ngẫu nhiên (chống ban)
    test_pages = [101, 105, 120]
    scraper.run_scraper(test_pages)
