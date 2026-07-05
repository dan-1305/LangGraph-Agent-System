from src.base_agent import BaseAgent
from pathlib import Path
import sys

# Setup sys.path
base_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

class GameAIProcessor(BaseAgent):
    def __init__(self, game_name):
        super().__init__(agent_name=f"GameProcessor_{game_name}")
        self.game_name = game_name
        self.project_root = Path(__file__).resolve().parent.parent
        self.game_data_path = self.project_root / "data" / game_name

    def analyze_document(self, raw_content):
        """Sử dụng LLM để phân tích tài liệu và phân loại thực thể."""
        prompt = f"""
        Bạn là một chuyên gia phân tích dữ liệu Game. Hãy phân tích tài liệu sau đây về game '{self.game_name}'.
        Hãy trích xuất các thông tin về: Character, Lore, Mechanic, Item.
        Trả về kết quả dưới dạng JSON cấu trúc.
        
        Tài liệu:
        {raw_content}
        """
        # Đây là placeholder, trong thực tế sẽ gọi self._call_llm_with_retry(prompt)
        print(f"🤖 AI đang phân tích dữ liệu cho game {self.game_name}...")
        return {"status": "success", "message": "Dữ liệu đã được phân tích (Placeholder)"}

    def update_wiki(self, structured_data):
        """Cập nhật các file Markdown trong thư mục wiki/."""
        wiki_path = self.game_data_path / "wiki"
        # Logic tạo file .md dựa trên structured_data
        print(f"📝 Đang cập nhật Wiki tại {wiki_path}...")
