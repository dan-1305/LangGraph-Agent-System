import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
import random
import re
from fake_useragent import UserAgent

class BaseScraper:
    def __init__(self, log_file: str, raw_data_path: str):
        self.log_file = Path(log_file)
        self.raw_data_path = Path(raw_data_path)
        
        # Đảm bảo thư mục tồn tại
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.raw_data_path.parent.mkdir(parents=True, exist_ok=True)

    def get_scraped_pages(self) -> set:
        """Đọc danh sách các trang đã cào thành công từ log file."""
        if not self.log_file.exists():
            return set()
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            return set(int(p) for p in lines if p.strip().isdigit())

    def add_scraped_page(self, page: int):
        """Ghi nhận một trang đã cào thành công."""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{page}\n")

    def clean_old_data(self):
        """Xóa dữ liệu rác (Area < 10, District chứa tên đường) khỏi file gộp."""
        if not self.raw_data_path.exists():
            return
        df = pd.read_csv(self.raw_data_path)
        bad_rows = df['District'].str.contains('Đường|Quốc lộ|hẻm|Hẻm', case=False, na=False) | (df['Area_m2'] < 10)
        df_clean = df[~bad_rows]
        df_clean.to_csv(self.raw_data_path, index=False, encoding='utf-8')

    def incremental_merge(self, new_data: list, output_csv: str):
        """Gộp dữ liệu mới vào output_csv nội bộ và raw_data.csv của mô hình."""
        if not new_data:
            print("⚠️ Không có dữ liệu mới để merge.")
            return
            
        df_new = pd.DataFrame(new_data)
        
        # 1. Lưu đè / gộp vào file local của dự án cào
        out_path = Path(output_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_path.exists():
            df_local = pd.read_csv(out_path)
            df_combined = pd.concat([df_local, df_new], ignore_index=True)
        else:
            df_combined = df_new
        # Drop duplicates nội bộ
        df_combined = df_combined.drop_duplicates(subset=['Title', 'Price_VND', 'Area_m2'])
        df_combined.to_csv(out_path, index=False, encoding='utf-8')
        
        # 2. Gộp vào raw_data.csv của mô hình (Incremental Merge)
        self.clean_old_data()
        if self.raw_data_path.exists():
            df_main = pd.read_csv(self.raw_data_path)
            common_cols = [c for c in df_new.columns if c in df_main.columns]
            merged_df = pd.concat([df_main, df_new[common_cols]], ignore_index=True)
            merged_df = merged_df.drop_duplicates(subset=['Title', 'Price_VND', 'Area_m2'])
            merged_df.to_csv(self.raw_data_path, index=False, encoding='utf-8')
            print(f"✅ Đã gộp thành công. Tổng số dòng Dataset mô hình hiện tại: {len(merged_df)}")
        else:
            df_new.to_csv(self.raw_data_path, index=False, encoding='utf-8')
            print(f"✅ Đã tạo mới Dataset mô hình. Tổng số dòng: {len(df_new)}")

class AlonhadatParser(BaseScraper):
    DISTRICTS_DONGNAI = [
        "Biên Hòa", "Long Thành", "Nhơn Trạch", "Trảng Bom", "Vĩnh Cửu", 
        "Thống Nhất", "Cẩm Mỹ", "Định Quán", "Xuân Lộc", "Tân Phú", "Long Khánh"
    ]

    def __init__(self, log_file: str, raw_data_path: str, output_csv: str):
        super().__init__(log_file, raw_data_path)
        self.output_csv = output_csv
        self.ua = UserAgent(os='windows', browsers=['chrome', 'edge', 'firefox']) # Giả lập máy tính Windows để tránh lộ OS khác nhau liên tục

    def build_headers(self):
        # Fake IP để đánh lừa Cloudflare / WAF
        fake_ip = f"{random.randint(11,190)}.{random.randint(1,250)}.{random.randint(1,250)}.{random.randint(1,250)}"
        return {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com.vn/',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': fake_ip,
            'Client-IP': fake_ip
        }

    def scrape_page(self, page: int) -> list:
        if page == 1:
            url = 'https://alonhadat.com.vn/can-ban-nha-dat/dong-nai'
        else:
            url = f'https://alonhadat.com.vn/can-ban-nha-dat/dong-nai/trang-{page}'
            
        print(f"Đang cào trang {page}: {url}...")
        data = []
        try:
            # Dùng requests.get độc lập để không dính dáng cookie (State-less scraping)
            response = requests.get(url, headers=self.build_headers(), timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            property_items = soup.find_all('article', class_='property-item')
            
            if not property_items:
                print("⚠️ Không tìm thấy tin đăng nào (Có thể bị block hoặc hết trang).")
                return None  # Trả về None để báo hiệu dừng/bị block
                
            for item in property_items:
                # Title
                title_el = item.find('h3', class_='property-title')
                title = title_el.text.strip() if title_el else ""
                
                # Price
                price = 0.0
                price_el = item.find('span', itemprop='price')
                if price_el and price_el.has_attr('content'):
                    try:
                        price = float(price_el['content'])
                    except ValueError:
                        pass
                
                # Area
                area = 0.0
                area_match = re.search(r'(?i)(?:dt|diện tích)?\s*(\d+[\.,]?\d*)\s*m2', title)
                if area_match:
                    try:
                        area = float(area_match.group(1).replace(',', '.'))
                    except ValueError:
                        pass
                else:
                    desc_el = item.find('p', class_='brief')
                    if desc_el:
                        area_match_desc = re.search(r'(?i)(?:dt|diện tích|ngang)?\s*(\d+[\.,]?\d*)\s*m2', desc_el.text)
                        if area_match_desc:
                            try:
                                area = float(area_match_desc.group(1).replace(',', '.'))
                            except ValueError:
                                pass
                
                if area == 0.0 or price == 0.0:
                    continue
                        
                # District
                district = ""
                address_el = item.find('p', class_='new-address')
                search_text = (address_el.text if address_el else item.text).lower()
                
                for d in self.DISTRICTS_DONGNAI:
                    if d.lower() in search_text:
                        district = d
                        break
                if not district:
                    for d in self.DISTRICTS_DONGNAI:
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
        except Exception as e:
            print(f"❌ Lỗi HTTP khi cào trang {page}: {e}")
            return None

    def run_guerrilla(self, max_pages=500, batch_size=10):
        """Chiến thuật Cào Du Kích: Trộn trang, cào từng batch nhỏ rồi nghỉ."""
        scraped = self.get_scraped_pages()
        all_pages = set(range(1, max_pages + 1))
        remaining_pages = list(all_pages - scraped)
        
        if not remaining_pages:
            print("✅ Đã cào toàn bộ 500 trang mục tiêu!")
            return
            
        # Xáo trộn thứ tự trang
        random.shuffle(remaining_pages)
        target_batch = remaining_pages[:batch_size]
        
        print(f"🚀 Chiến thuật DU KÍCH: Chọn ngẫu nhiên {len(target_batch)} trang để cào trong lượt này...")
        print(f"📄 Các trang mục tiêu: {target_batch}")
        
        all_new_data = []
        for page in target_batch:
            data = self.scrape_page(page)
            if data is None:
                print("🛑 Dừng Batch sớm do nghi ngờ bị block hoặc lỗi mạng.")
                break
                
            if len(data) > 0:
                all_new_data.extend(data)
                # Ghi log thành công
                self.add_scraped_page(page)
            
            # Ngủ 3.5-7.5 giây ngẫu nhiên
            sleep_time = random.uniform(3.5, 7.5)
            time.sleep(sleep_time)
            
        print(f"🏁 Đã kết thúc đợt Du Kích. Tổng số tin lấy được: {len(all_new_data)}")
        if all_new_data:
            self.incremental_merge(all_new_data, self.output_csv)

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    output_csv = base_dir / "data" / "output" / "alonhadat_dongnai.csv"
    log_file = base_dir / "data" / "output" / "scraped_pages.log"
    real_estate_csv = base_dir.parent / "real_estate_prediction" / "data" / "raw_data.csv"
    
    scraper = AlonhadatParser(str(log_file), str(real_estate_csv), str(output_csv))
    # Chạy 1 batch 100 trang để tăng tốc độ cào
    scraper.run_guerrilla(max_pages=500, batch_size=15)
