"""
Storyteller Agent:
Nhiệm vụ: Viết System Prompt và First Message (Bối cảnh mở đầu).
Logic: Tiếp nhận ý tưởng của người dùng (Theme), chuyển thể thành văn phong kể chuyện.
"""

from typing import Dict
from src.base_agent import BaseAgent

STORYTELLER_PROMPT = """
Bạn là một Bậc thầy kể chuyện (Storyteller) chuyên nghiệp của game nhập vai (RPG).
Nhiệm vụ của bạn là tạo ra phần "System Prompt" và "First Message" cho một thẻ thế giới (World Card) của phần mềm SillyTavern dựa trên ý tưởng của người dùng.

THÔNG TIN INPUT TỪ NGƯỜI DÙNG:
- Tên thế giới / Chủ đề (Theme): {theme}
- Mô tả chi tiết: {details}
- Các tính năng hệ thống sẽ có trong thế giới: {features}
- Phong cách kể chuyện (Style): {style}

YÊU CẦU CHO TỪNG PHẦN:
1. "system_prompt": 
- Một đoạn văn ngắn gọn, súc tích (khoảng 3-5 câu), đóng vai trò thiết lập quy tắc cho AI đóng vai Game Master (GM).
- Bắt đầu bằng lệnh trực tiếp, ví dụ: "Bạn là hệ thống quản trò của thế giới [Tên Thế Giới]..." hoặc "Đây là một thế giới [Thể loại]..."
- Phải đề cập đến các tính năng hệ thống (ví dụ nếu có Gacha thì dặn AI xử lý Gacha).

2. "first_message":
- Lời chào đầu tiên khi người chơi (User) bước vào thế giới này. Đóng vai trò thiết lập bối cảnh (Setting the scene).
- Viết theo phong cách {style}.
- Hãy sử dụng biến {{{{char}}}} để đại diện cho người dẫn chuyện/hệ thống, và {{{{user}}}} để gọi người chơi. Việc dùng 2 ngoặc nhọn là BẮT BUỘC.
- Độ dài khoảng 2-4 đoạn văn, miêu tả chi tiết không gian, màu sắc, âm thanh xung quanh người chơi để họ dễ hình dung. Phải lồng ghép các chi tiết từ "Mô tả chi tiết" của người dùng vào.

OUTPUT BẮT BUỘC (Tr format chuẩn JSON, không thừa text ngoài JSON):
{{
    "system_prompt": "Nội dung system prompt ở đây... Chào mừng {{{{user}}}}...",
    "first_message": "Nội dung first message ở đây... {{{{char}}}} đứng nhìn {{{{user}}}}..."
}}
"""

class StorytellerAgent(BaseAgent):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        # Dùng model xịn hơn một chút để viết văn hay
        super().__init__(model_name="gemini-3.1-pro-preview", temperature=0.8)
        
    def generate_narrative_context(self, user_idea: Dict) -> Dict[str, str]:
        """
        Tạo System Prompt và First Message từ ý tưởng người dùng bằng Gemini.
        """
        # Hỗ trợ Dynamic Quest Generation (Giai đoạn 3)
        quest_context = ""
        if user_idea.get("dynamic_quest", False):
            quest_context = "\n[TÍNH NĂNG ĐẶC BIỆT: NHIỆM VỤ ĐỘNG]\nNgười dùng đã yêu cầu sinh ra Nhiệm vụ động (Dynamic Quest). Bạn BẮT BUỘC phải chèn một [Bảng Nhiệm Vụ] (Quest Board) vào cuối `first_message`. Bảng nhiệm vụ này phải có 3-5 nhiệm vụ cụ thể, phù hợp với cốt truyện bạn vừa vẽ ra. Mỗi nhiệm vụ cần có Tên, Mô tả ngắn và Phần thưởng dự kiến."

        prompt = STORYTELLER_PROMPT.format(
            theme=user_idea.get("theme", "Thế giới vô danh"),
            details=user_idea.get("details", "Không có chi tiết."),
            features=", ".join(user_idea.get("features", ["Không có tính năng đặc biệt"])),
            style=user_idea.get("style", "Sử thi")
        )
        prompt += quest_context
        
        response_text = self._call_llm(prompt, is_json=True)
        result = self._parse_json_response(response_text)
        
        if result and isinstance(result, dict):
            return result
            
        # Fallback an toàn nếu API lỗi
        return {
            "system_prompt": f"Bạn là hệ thống quản lý thế giới {user_idea.get('theme', '')}.",
            "first_message": f"{{char}} chào mừng {{user}} đến với thế giới. Bối cảnh: {user_idea.get('details', '')}"
        }
