import os
import argparse
from pathlib import Path
import sys

# Setup sys.path cho Monorepo
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

# Force UTF-8 for Windows Console
import io
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from projects.universal_game_vault.src.scraper import GameWebScraper

class GameVaultDispatcher:
    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent
        self.data_dir = self.project_root / "data"
        self.scraper = GameWebScraper()

    def ensure_game_structure(self, game_name):
        """Tạo cấu trúc thư mục chuẩn cho một game mới."""
        game_path = self.data_dir / game_name
        subdirs = ["wiki", "raw", "database"]
        
        for subdir in subdirs:
            (game_path / subdir).mkdir(parents=True, exist_ok=True)
            
        print(f"✅ Đã kiểm tra/khởi tạo cấu trúc cho game: {game_name}")
        return game_path

    def process_input(self, game_name, input_content=None, url=None, file_path=None):
        """Xử lý đầu vào từ Admin từ nhiều nguồn khác nhau."""
        game_path = self.ensure_game_structure(game_name)
        raw_dir = game_path / "raw"
        
        if url:
            content = self.scraper.scrape_url(url)
            if content:
                # Trích xuất tên file từ URL đơn giản
                filename = url.split("/")[-1] or "web_content"
                output_file = raw_dir / f"scrape_{filename}_{os.urandom(2).hex()}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Đã cào và lưu vào: {output_file}")

        if file_path:
            # Nếu là file có sẵn, ta có thể copy vào raw/ nếu cần, hoặc chỉ ghi nhận
            print(f"📂 Đã ghi nhận file tài liệu: {file_path}")

        if input_content:
            raw_file = raw_dir / f"input_{os.urandom(4).hex()}.txt"
            with open(raw_file, "w", encoding="utf-8") as f:
                f.write(input_content)
            print(f"📥 Đã lưu nội dung text vào: {raw_file}")
        
        print("🧠 Hệ thống đã sẵn sàng phân tích toàn bộ kho dữ liệu trong 'raw/'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Game Vault Dispatcher")
    parser.add_argument("--game", required=True, help="Tên game (snake_case)")
    parser.add_argument("--input", help="Nội dung tài liệu text")
    parser.add_argument("--url", help="URL cần cào dữ liệu")
    parser.add_argument("--file", help="Đường dẫn file tài liệu")
    
    args = parser.parse_args()
    
    dispatcher = GameVaultDispatcher()
    dispatcher.process_input(
        game_name=args.game, 
        input_content=args.input, 
        url=args.url, 
        file_path=args.file
    )
