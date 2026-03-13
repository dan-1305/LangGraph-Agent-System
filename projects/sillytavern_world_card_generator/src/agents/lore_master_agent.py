"""
Lore Master Agent:
Nhiệm vụ: Tự động sinh ra các mục (entries) cho Lorebook dựa trên ý tưởng người dùng.
Logic: Phân tích theme thành các thành tố chính (Nhân vật, Hệ thống, Chủng tộc, Vật phẩm) và viết mô tả lore (lịch sử) cho từng cái.
"""

from typing import List, Dict
from src.base_agent import BaseAgent

LORE_MASTER_PROMPT = """
Bạn là một chuyên gia kiến trúc sư thế giới giả tưởng (Lore Master).
Nhiệm vụ của bạn là sinh ra MỘT MẢNG JSON chứa ít nhất 5-10 mục Lorebook (Character Book) dựa trên thông tin do người dùng cung cấp.

THÔNG TIN INPUT TỪ NGƯỜI DÙNG:
- Tên thế giới / Chủ đề (Theme): {theme}
- Mô tả chi tiết: {details}
- Các tính năng hệ thống sẽ có trong thế giới: {features}

YÊU CẦU:
1. Đọc thật kỹ "Mô tả chi tiết". Nếu người dùng miêu tả các NHÂN VẬT cụ thể (VD: mẹ, em gái, chị gái), bạn BẮT BUỘC phải tạo ra MỖI MỤC LOREBOOK RIÊNG cho từng nhân vật đó (bao gồm Tên dự đoán, tính cách, ngoại hình, vai trò trong gia đình/thế giới).
2. Ngoài nhân vật, hãy phân tách và tạo thêm lore về các khía cạnh:
   - Chủng tộc (Races)
   - Hệ thống quyền lực/Ma thuật (Magic/Tech System)
   - Địa điểm quan trọng (Locations)
3. Cấu trúc mỗi mục (entry):
   - `key`: Duy nhất, bằng tiếng Anh, viết thường, không dấu cách (vd: "sister_tsundere", "magic_system").
   - `secondary_keys`: Mảng các từ khóa (tiếng Việt hoặc tiếng Anh) để trigger lore này. (VD: ["chị gái", "sister"]).
   - `content`: Nội dung miêu tả chi tiết, sinh động, chuẩn xác.
   - `priority`: Số nguyên từ 10-20. (Nhân vật thì để 20, địa điểm thì 10).
   - `enabled`: true.

OUTPUT BẮT BUỘC (Trả về MẢNG JSON, không thừa text ngoài JSON):
[
  {{
    "key": "mother_figure",
    "secondary_keys": ["mẹ", "mama"],
    "content": "Mẹ của main, một người phụ nữ 35 tuổi nhưng vẫn giữ được nét thanh xuân. Tính cách ôn hòa, rất chiều chuộng con trai... [Image Prompt: A beautiful 35-year-old mother, gentle smile, youthful, highly detailed, anime style]",
    "priority": 20,
    "enabled": true
  }},
  {{
    "key": "combat_system",
    "secondary_keys": ["chiến đấu", "sức mạnh"],
    "content": "Hệ thống chiến đấu dựa trên mana...",
    "priority": 10,
    "enabled": true
  }}
]
"""

class LoreMasterAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        # Dùng model xịn hơn để suy luận nhân vật sâu sắc
        super().__init__(model_name="gemini-3.1-pro-preview", temperature=0.7)
        
    def generate_lorebook(self, user_idea: Dict) -> List[Dict]:
        """
        Tạo danh sách Lorebook entries bằng Gemini.
        Hỗ trợ RAG (đọc file mẫu) và Auto-balancing.
        """
        import os
        from pathlib import Path
        import json
        
        # 1. RAG Thu nhỏ: Đọc file mẫu nếu có
        template_ref = user_idea.get("template_reference", "Không")
        template_context = ""
        if template_ref != "Không":
            try:
                template_path = Path(__file__).resolve().parent.parent.parent / "data" / "templates" / "world_card" / template_ref
                if template_path.exists():
                    with open(template_path, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                        # Trích xuất một phần Lorebook mẫu để làm context (tránh quá dài)
                        sample_entries = template_data.get("data", {}).get("character_book", {}).get("entries", [])[:3]
                        template_context = f"\n\n[HỌC LỎM VĂN PHONG TỪ FILE MẪU '{template_ref}']\nHãy bắt chước cấu trúc và văn phong chi tiết, tà đạo của các thẻ mẫu sau đây:\n{json.dumps(sample_entries, ensure_ascii=False, indent=2)}\n"
            except Exception as e:
                print(f"Lỗi đọc file mẫu RAG: {e}")

        # 2. Quy tắc Auto-Balancing
        balance_context = ""
        if user_idea.get("auto_balance", False):
            balance_context = "\n\n[QUY TẮC CÂN BẰNG RPG]\nKhi tạo các chỉ số (HP, MP, STR, AGI...) cho nhân vật hoặc quái vật, BẮT BUỘC phải cân bằng. Tổng điểm chỉ số cơ bản không vượt quá 100 điểm. Nếu một chỉ số quá cao (VD: STR 90) thì các chỉ số khác phải cực kỳ thấp (phế). Hãy ghi rõ chỉ số vào trong content."

        # 3. Hỗ trợ Image Prompt (Giai đoạn 3)
        image_context = ""
        if user_idea.get("image_prompt", False):
            image_context = "\n\n[TÍNH NĂNG ĐẶC BIỆT: IMAGE PROMPT GENERATOR]\nNgười dùng đã yêu cầu sinh Image Prompt. Ở CUỐI MỖI NỘI DUNG (content) của mục Lorebook về Nhân Vật hoặc Địa Điểm, bạn BẮT BUỘC phải thêm một đoạn `[Image Prompt: <mô tả chi tiết bằng tiếng Anh chuẩn Stable Diffusion/Midjourney, ngăn cách bằng dấu phẩy, ví dụ: 1girl, high quality, anime style, ...>]`."

        # 4. Build Prompt
        prompt = LORE_MASTER_PROMPT.format(
            theme=user_idea.get("theme", "Thế giới vô danh"),
            details=user_idea.get("details", "Không có chi tiết."),
            features=", ".join(user_idea.get("features", ["Không có tính năng đặc biệt"]))
        )
        prompt += template_context + balance_context + image_context
        
        response_text = self._call_llm(prompt, is_json=True)
        result = self._parse_json_response(response_text)
        
        formatted_entries = []
        if result and isinstance(result, list):
            for idx, item in enumerate(result):
                entry = {
                    "id": idx,
                    "keys": item.get("secondary_keys", []) + [item.get("key", "")],
                    "secondary_keys": [],
                    "comment": item.get("key", f"entry_{idx}"),
                    "content": item.get("content", ""),
                    "constant": False,
                    "selective": True,
                    "insertion_order": 100,
                    "enabled": True,
                    "position": "before_char",
                    "use_regex": True,
                    "extensions": {
                        "position": 0,
                        "exclude_recursion": True,
                        "display_index": idx,
                        "probability": 100,
                        "useProbability": True,
                        "depth": 4,
                        "selectiveLogic": 0,
                        "group": "",
                        "group_override": False,
                        "group_weight": 100,
                        "prevent_recursion": True,
                        "delay_until_recursion": False,
                        "vectorized": False
                    }
                }
                formatted_entries.append(entry)
            return formatted_entries
            
        # Fallback an toàn nếu API lỗi
        return [{
            "id": 0,
            "keys": ["error"],
            "secondary_keys": [],
            "comment": "error_fallback",
            "content": "API Error: Không thể tạo Lorebook. Vui lòng kiểm tra lại cấu hình Gemini.",
            "constant": False,
            "selective": True,
            "insertion_order": 100,
            "enabled": True,
            "position": "before_char",
            "use_regex": True,
            "extensions": {"position": 0, "exclude_recursion": True, "display_index": 0}
        }]

# Coder chưa cần gọi LLM vội vì code Regex/UI cần độ chính xác cao.
# Tương lai sẽ tích hợp RAG để bốc Template Regex cho chuẩn.
def generate_lore_mock(user_idea: Dict):
    agent = LoreMasterAgent()
    return agent.generate_lorebook(user_idea)
