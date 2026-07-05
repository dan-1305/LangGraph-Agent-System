import sys
from pathlib import Path
from typing import Any

root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.base_agent import BaseAgent

class BaseGeminiAgent(BaseAgent):
    """
    Class cơ sở đã được refactor để kế thừa trực tiếp từ BaseAgent chuẩn của hệ thống,
    tận dụng hệ thống Circuit Breaker và JSON parsing tự động.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        super().__init__(
            name="SillyTavernAgent",
            role="Writer",
            model_name=model_name,
            temperature=temperature,
            agent_label="tier-1"
        )
        
    def _ai_handler(self, *args, **kwargs):
        pass

    def _logic_handler(self, *args, **kwargs):
        pass

    def _call_gemini(self, prompt: str, is_json: bool = True) -> str:
        """
        Gửi prompt đến LLM sử dụng hệ thống gọi API đã chuẩn hóa.
        Hàm này vẫn trả về chuỗi JSON thô (string) để tương thích ngược với code cũ,
        nhưng thực tế nó đã dùng `is_json=False` (hoặc True nếu không sao) của BaseAgent.
        """
        # Nếu muốn chuỗi string như cũ:
        try:
            # Dùng _call_llm_with_retry nhưng nhận chuỗi string về
            # Vì BaseAgent trả về Dict nếu is_json=True, ta convert ngược lại thành json string
            # để không làm vỡ code cũ của dự án SillyTavern.
            result = self._call_llm_with_retry(prompt, is_json=is_json)
            import json
            if isinstance(result, dict) or isinstance(result, list):
                return json.dumps(result, ensure_ascii=False)
            return result
        except Exception as e:
            print(f"❌ Error calling LLM API: {str(e)}")
            return ""

    def _parse_json_response(self, response_text: str) -> Any:
        """Sử dụng logic parse chuẩn từ BaseAgent."""
        return super()._parse_json_response(response_text)
