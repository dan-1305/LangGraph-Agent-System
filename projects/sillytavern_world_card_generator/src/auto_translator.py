import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Base Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(BASE_DIR / ".env")

from projects.sillytavern_world_card_generator.src.agents.base_agent import BaseAgent

TRANSLATE_PROMPT = """
Bạn là một trợ lý dịch thuật chuyên nghiệp, đặc biệt am hiểu về bối cảnh Game RPG, Anime, và Visual Novel.
Nhiệm vụ của bạn là dịch đoạn văn bản sau sang Tiếng Việt.

QUY TẮC CỰC KỲ QUAN TRỌNG (NẾU VI PHẠM SẼ GÂY LỖI PHẦN MỀM):
1. TUYỆT ĐỐI GIỮ NGUYÊN các biến số của phần mềm SillyTavern. Ví dụ: {{char}}, {{user}}, <StatusPlaceHolderImpl/>, các đoạn code regex, các macro ẩn.
2. KHÔNG thay đổi định dạng Markdown (như dấu **, *, #).
3. KHÔNG tự ý thêm bớt nội dung. Chỉ dịch chính xác nghĩa của từ.
4. Giữ nguyên văn phong (Nếu là văn phong cổ trang, hãy dùng từ Hán Việt. Nếu là văn phong hiện đại, hãy dùng từ tự nhiên).
5. Chỉ trả về văn bản đã dịch, không kèm theo lời chào hay giải thích nào khác.

[VĂN BẢN GỐC CẦN DỊCH]:
{text}
"""

class AutoTranslatorAgent(BaseAgent):
    def __init__(self):
        # Dùng model flash để dịch cho nhanh và tiết kiệm chi phí
        super().__init__(model_name="label:tier-2", temperature=0.1)
        
    def translate_text(self, text: str) -> str:
        if not text or not text.strip():
            return text
        
        # Nếu text quá ngắn hoặc chỉ toàn ký tự đặc biệt/tiếng Việt thì bỏ qua (kiểm tra đơn giản)
        # Tạm thời cứ gửi hết lên LLM, LLM sẽ tự xử lý
        prompt = TRANSLATE_PROMPT.format(text=text)
        
        try:
            result = self._call_llm(prompt, is_json=False)
            return result.strip()
        except Exception as e:
            print(f"❌ Lỗi dịch thuật: {e}")
            return text

def translate_card(input_file: Path, output_file: Path):
    print(f"🔄 Đang dịch thẻ: {input_file.name}...")
    translator = AutoTranslatorAgent()
    
    with open(input_file, "r", encoding="utf-8") as f:
        card_data = json.load(f)
        
    data_node = card_data.get("data", card_data)
    
    # Dịch Description
    if data_node.get("description"):
        print("   - Dịch Description...")
        data_node["description"] = translator.translate_text(data_node["description"])
        
    # Dịch First Message
    if data_node.get("first_mes"):
        print("   - Dịch First Message...")
        data_node["first_mes"] = translator.translate_text(data_node["first_mes"])
        
    # Dịch Personality
    if data_node.get("personality"):
        print("   - Dịch Personality...")
        data_node["personality"] = translator.translate_text(data_node["personality"])
        
    # Dịch Scenario
    if data_node.get("scenario"):
        print("   - Dịch Scenario...")
        data_node["scenario"] = translator.translate_text(data_node["scenario"])
        
    # Lưu lại
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(card_data, f, ensure_ascii=False, indent=4)
        
    print(f"✅ Đã lưu bản dịch tại: {output_file.name}")

def batch_translate(input_dir: str, output_dir: str, limit: int = 5):
    in_path = Path(input_dir)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for file in os.listdir(in_path):
        if not file.endswith(".json"):
            continue
            
        in_file = in_path / file
        out_file = out_path / file
        
        # Bỏ qua nếu đã dịch rồi
        if out_file.exists():
            continue
            
        translate_card(in_file, out_file)
        count += 1
        
        if count >= limit:
            print(f"\n⏸️ Đã đạt giới hạn {limit} thẻ. Dừng để tránh rate limit.")
            break

if __name__ == "__main__":
    WORLD_CARD_DIR = BASE_DIR / "projects" / "sillytavern_world_card_generator" / "data" / "world_card"
    WORLD_CARD_VI_DIR = BASE_DIR / "projects" / "sillytavern_world_card_generator" / "data" / "world_card_vi"
    
    print("🚀 BẮT ĐẦU CHẠY AUTO TRANSLATOR BATCH...")
    # Chạy thử 2 thẻ đầu tiên
    batch_translate(WORLD_CARD_DIR, WORLD_CARD_VI_DIR, limit=2)
