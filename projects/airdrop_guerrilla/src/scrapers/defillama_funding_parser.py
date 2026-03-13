import os
import sys
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

# Đưa thư mục gốc (projects/airdrop_guerrilla) vào sys.path để có thể import các module
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

from src.utils.base_scraper import BaseScraper
from src.analysis.scoring import AlphaAnalyzer
from src.utils.notifier import TelegramNotifier

class DefiLlamaParser(BaseScraper):
    """
    Trình cào dữ liệu Live từ API của DefiLlama (raises endpoint).
    """
    def __init__(self, log_file: str):
        super().__init__(log_file)
        self.api_url = "https://api.llama.fi/raises"

    def fetch_live_raises(self) -> List[Dict[str, Any]]:
        """
        Gọi API thực tế từ DefiLlama và xử lý dữ liệu trả về.
        
        Returns:
            List[Dict]: Danh sách 100 dự án gọi vốn mới nhất đã chuẩn hóa cấu trúc.
        """
        print("📥 Đang lấy dữ liệu Live từ DefiLlama API...")
        response = self.fetch_url(self.api_url)
        
        if not response:
            print("❌ Lỗi: Không thể kết nối đến API DefiLlama.")
            return []
            
        try:
            data = response.json()
            raises = data.get("raises", [])
            
            if not raises:
                print("⚠️ API trả về danh sách rỗng!")
                return []
                
            # Print sample to see structure
            print(f"Sample data from API: {raises[0]}")
                
            # Sắp xếp theo ngày mới nhất (date là unix timestamp), lấy 100 dự án gần nhất
            raises = sorted(raises, key=lambda x: x.get('date', 0), reverse=True)[:100]
            
            normalized_data = []
            for item in raises:
                name = item.get("name", "Unknown")
                amount = item.get("amount") or 0.0  # Có thể API trả về null
                category = item.get("category", "Unknown")
                
                # Gom chung leadInvestors và otherInvestors
                lead_investors = item.get("leadInvestors", []) or []
                other_investors = item.get("otherInvestors", []) or []
                all_investors = lead_investors + other_investors
                
                # Bỏ qua các dự án không công bố số tiền (Amount = 0)
                if amount <= 0:
                    continue
                    
                # API DefiLlama thường trả về amount là đơn vị Triệu (Millions) hoặc đôi lúc là số tuyệt đối.
                # Nếu amount < 1000, khả năng rất cao là đang tính bằng triệu USD (VD: 5.5 -> 5.5M USD)
                actual_funding = float(amount)
                if actual_funding < 10000:
                    actual_funding = actual_funding * 1_000_000
                    
                normalized_data.append({
                    "project_name": name,
                    "sector": category,
                    "funding_usd": actual_funding,
                    "investors": all_investors,
                    "risk_factor": 1.0  # Mặc định = 1.0 cho mọi dự án
                })
                
            return normalized_data
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý JSON từ API: {e}")
            return []

    def run_live_pipeline(self, output_csv: str):
        """
        Khởi chạy chu trình Cào -> Phân tích -> Lưu trữ cho Phase 2.
        """
        print("🚀 Khởi động Scraper (Live API Mode)...")
        
        # 1. Cào dữ liệu Live
        raw_data = self.fetch_live_raises()
        
        if not raw_data:
            print("🛑 Dừng Pipeline do không có dữ liệu đầu vào.")
            return
            
        # 2. Phân tích và chấm điểm
        print("🧠 Đang chấm điểm Alpha Score cho 100 dự án gần nhất...")
        analyzed_data = AlphaAnalyzer.analyze_projects(raw_data)
        
        # 3. Xuất báo cáo CSV
        print("💾 Đang xuất báo cáo ra file CSV...")
        df = pd.DataFrame(analyzed_data)
        
        # Format lại cột investors thành chuỗi để lưu CSV dễ dàng
        df['investors'] = df['investors'].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)
        
        # Đảm bảo thư mục lưu trữ tồn tại
        out_path = Path(output_csv)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(out_path, index=False, encoding='utf-8')
        print(f"✅ Đã lưu thành công tại: {out_path}")
        
        # 4. Kiểm tra Alert và In Top 5 Vua Alpha ra Terminal
        print("\n🏆 TOP 5 DỰ ÁN 'VUA ALPHA' HÔM NAY (Trong 100 dự án mới nhất):")
        print("-" * 80)
        
        notifier = TelegramNotifier()
        
        # In Top 5 ra Terminal
        top_5 = analyzed_data[:5]
        for idx, project in enumerate(top_5, 1):
            name = project['project_name']
            funding = project['funding_usd'] / 1_000_000
            score = project['alpha_score']
            investors = ", ".join(project['investors']) if project['investors'] else "Chưa công bố"
            
            print(f"{idx}. {name} | Lĩnh vực: {project['sector']}")
            print(f"   💰 Funding: {funding:.1f}M USD | 🏦 VCs: {investors}")
            print(f"   🔥 Alpha Score: {score} Điểm")
            print("-" * 80)

        # Gửi thông báo Telegram cho những dự án có điểm > 1200
        print("\n🚨 Kiểm tra các kèo siêu tiềm năng (> 1200 điểm)...")
        alerts_sent = 0
        for project in analyzed_data:
            score = project['alpha_score']
            if score > 1200:
                print(f"🔔 Gửi thông báo kèo: {project['project_name']} (Điểm: {score})")
                
                # Auto-Research: Tìm thêm thông tin Social cho các siêu kèo (> 1500 điểm)
                if score > 1500:
                    print(f"   🔎 Kích hoạt Auto-Research cho Siêu Kỳ Lân: {project['project_name']}...")
                    # TODO: Viết logic cào Twitter, Discord từ Web hoặc API trung gian
                    # Tạm thời append mock data để biểu diễn luồng
                    project['twitter_link'] = f"https://twitter.com/search?q={project['project_name'].replace(' ', '')}"
                    project['discord_link'] = "TBD"
                
                notifier.send_alpha_alert(project)
                alerts_sent += 1
                
        if alerts_sent == 0:
            print("Chưa có dự án nào vượt mốc 1200 điểm hôm nay.")

if __name__ == "__main__":
    log_path = str(base_dir / "data" / "output" / "airdrop_api.log")
    output_csv = str(base_dir / "data" / "output" / "alpha_leads_today.csv")
    
    parser = DefiLlamaParser(log_path)
    parser.run_live_pipeline(output_csv)
