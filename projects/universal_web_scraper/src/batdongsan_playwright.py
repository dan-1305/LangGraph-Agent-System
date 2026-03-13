import os
import sys
import pandas as pd
import time
import random
import re
import sqlite3
from pathlib import Path
from playwright.sync_api import sync_playwright

# Tính đường dẫn thư mục gốc
base_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(base_dir))

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

class BatDongSanPlaywrightScraper:
    def __init__(self, output_csv: str, raw_data_db: str):
        self.output_csv = Path(output_csv)
        self.raw_data_db = Path(raw_data_db)
        self.districts_dongnai = [
            "Biên Hòa", "Long Thành", "Nhơn Trạch", "Trảng Bom", "Vĩnh Cửu", 
            "Thống Nhất", "Cẩm Mỹ", "Định Quán", "Xuân Lộc", "Tân Phú", "Long Khánh"
        ]

    def get_scraped_pages(self) -> set:
        log_file = self.output_csv.parent / "scraped_batdongsan.log"
        if not log_file.exists():
            return set()
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return set(int(p) for p in lines if p.strip().isdigit())

    def add_scraped_page(self, page: int):
        log_file = self.output_csv.parent / "scraped_batdongsan.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{page}\n")

    def parse_page_data(self, page) -> list:
        try:
            page.wait_for_selector(".js__card-title", timeout=15000)
        except:
            print("⚠️ Không tìm thấy tin đăng nào. Có thể do load chậm hoặc Cloudflare chặn.")
            return []
            
        items = page.locator(".js__product-link-for-product-id")
        
        count = items.count()
        data = []
        
        for i in range(count):
            item = items.nth(i)
            
            # 1. Title
            title_el = item.locator(".js__card-title")
            title = title_el.inner_text().strip() if title_el.count() > 0 else ""
            
            if not title:
                continue
                
            # 2. Price
            price_text = ""
            price_el = item.locator(".re__card-config-price")
            if price_el.count() > 0:
                price_text = price_el.inner_text().strip().lower()
                
            price_vnd = 0.0
            if "tỷ" in price_text:
                val = re.search(r'([\d.,]+)', price_text)
                if val:
                    price_vnd = float(val.group(1).replace(',', '.')) * 1_000_000_000
            elif "triệu" in price_text and "m²" not in price_text:
                val = re.search(r'([\d.,]+)', price_text)
                if val:
                    price_vnd = float(val.group(1).replace(',', '.')) * 1_000_000
            elif "thỏa thuận" in price_text:
                continue # Bỏ qua giá thỏa thuận
                
            # 3. Area
            area_text = ""
            area_el = item.locator(".re__card-config-area")
            if area_el.count() > 0:
                area_text = area_el.inner_text().strip()
                
            area_m2 = 0.0
            val = re.search(r'([\d.,]+)', area_text)
            if val:
                area_m2 = float(val.group(1).replace(',', '.'))
                
            if price_vnd == 0.0 or area_m2 == 0.0:
                continue
                
            # 4. Location / District
            district = ""
            loc_el = item.locator(".re__card-location span").last
            loc_text = loc_el.inner_text().lower() if loc_el.count() > 0 else ""
            
            for d in self.districts_dongnai:
                if d.lower() in loc_text:
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
                    'Price_VND': price_vnd,
                    'Area_m2': area_m2,
                    'District': district,
                    'Province': "Đồng Nai"
                })
                
        return data

    def run_guerrilla(self, max_pages=500, batch_size=2):
        scraped = self.get_scraped_pages()
        all_pages = set(range(1, max_pages + 1))
        remaining_pages = list(all_pages - scraped)
        
        if not remaining_pages:
            print("✅ Đã cào toàn bộ 500 trang mục tiêu của Batdongsan!")
            return
            
        random.shuffle(remaining_pages)
        target_pages = remaining_pages[:batch_size]
        
        print(f"🚀 Chiến thuật DU KÍCH (Batdongsan): Chọn ngẫu nhiên {len(target_pages)} trang để cào trong lượt này...")
        print(f"📄 Các trang mục tiêu: {target_pages}")

        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        
        all_data = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=ua, viewport={'width': 1366, 'height': 768})
            page = context.new_page()
            
            for page_num in target_pages:
                if page_num == 1:
                    url = 'https://batdongsan.com.vn/ban-nha-dat-dong-nai'
                else:
                    url = f'https://batdongsan.com.vn/ban-nha-dat-dong-nai/p{page_num}'
                    
                print(f"\n🌍 Đang truy cập trang {page_num}: {url}")
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=45000)
                    
                    # Hành vi con người để đánh lừa Cloudflare
                    PlaywrightStealth.human_pause(2.0, 5.0)
                    PlaywrightStealth.random_scroll(page, 2, 4)
                    
                    # Kiểm tra Cloudflare block
                    if "cloudflare" in page.content().lower() or "just a moment" in page.content().lower():
                        print("⚠️ Cảnh báo: Cloudflare đang kiểm tra, chờ thêm 10s...")
                        page.wait_for_timeout(10000)
                        
                    # Trích xuất dữ liệu
                    page_data = self.parse_page_data(page)
                    if page_data:
                        print(f"✅ Trang {page_num}: Lấy được {len(page_data)} tin đăng chuẩn.")
                        all_data.extend(page_data)
                        self.add_scraped_page(page_num)
                    else:
                        # Nếu ko lấy được (do cloudflare chặn), dừng luôn batch này để bảo vệ IP
                        print("🛑 Nghi ngờ bị Cloudflare Block. Dừng Batch sớm để an toàn!")
                        break
                        
                except Exception as e:
                    print(f"❌ Lỗi khi cào trang {page_num}: {e}")
                    
            browser.close()
            
        if all_data:
            self.save_and_merge(all_data)

    def save_and_merge(self, data):
        df_new = pd.DataFrame(data)
        
        # Lưu ra CSV output
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
        if self.output_csv.exists():
            df_local = pd.read_csv(self.output_csv)
            df_combined = pd.concat([df_local, df_new], ignore_index=True)
        else:
            df_combined = df_new
            
        df_combined = df_combined.drop_duplicates(subset=['Title', 'Price_VND', 'Area_m2'])
        df_combined.to_csv(self.output_csv, index=False, encoding='utf-8')
        print(f"\n💾 Đã lưu file trung gian tại: {self.output_csv}")
        
        # Gộp vào Database tổng của Mô hình
        try:
            self.raw_data_db.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(self.raw_data_db)
            
            # Đọc data cũ nếu có
            try:
                df_main = pd.read_sql_query("SELECT * FROM Properties", conn)
                common_cols = [c for c in df_new.columns if c in df_main.columns]
                merged_df = pd.concat([df_main, df_new[common_cols]], ignore_index=True)
            except Exception:
                merged_df = df_new
                
            merged_df = merged_df.drop_duplicates(subset=['Title', 'Price_VND', 'Area_m2'])
            
            # Lọc bỏ rác
            bad_rows = merged_df['District'].str.contains('Đường|Quốc lộ|hẻm|Hẻm', case=False, na=False) | (merged_df['Area_m2'] < 10)
            merged_df = merged_df[~bad_rows]
            
            merged_df.to_sql('Properties', conn, if_exists='replace', index=False)
            conn.close()
            print(f"🎉 Đã gộp vào SQLite thành công! Tổng số dòng Dataset BĐS hiện tại: {len(merged_df)}")
            
        except Exception as e:
            print(f"❌ Lỗi ghi vào Database SQLite: {e}")

if __name__ == "__main__":
    out_csv = base_dir / "projects" / "universal_web_scraper" / "data" / "output" / "batdongsan_dongnai_pw.csv"
    raw_db = base_dir / "data" / "real_estate.db"
    
    scraper = BatDongSanPlaywrightScraper(str(out_csv), str(raw_db))
    
    # Chạy Du kích: Mỗi lần mở máy cào đúng 2 trang rồi chuồn
    scraper.run_guerrilla(max_pages=500, batch_size=2)
