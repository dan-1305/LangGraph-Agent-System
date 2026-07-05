import sys
import os
from pathlib import Path
from typing import List, Dict, Any
from pydantic import BaseModel

# Thêm root dự án vào sys.path để import BaseAgent
root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(root_dir))

from src.base_agent import BaseAgent

class TranslationSchema(BaseModel):
    translations: Dict[str, str]

class GodotTranslator(BaseAgent):
    """Agent specialized in translating Japanese game strings to Vietnamese."""

    def __init__(self, model_name: str = "gemini-3.1-pro-preview", **kwargs):
        # Sử dụng model gemini chuẩn hệ thống (đã được fix trong BaseAgent)
        super().__init__(model_name=model_name, **kwargs)

    def _logic_handler(self, texts: List[str]) -> Dict[str, str]:
        """Fallback Path: Return original texts (no translation) if AI fails."""
        return {text: f"[TL] {text}" for text in texts}

    def _ai_handler(self, texts: List[str]) -> Dict[str, str]:
        """Optimal Path: Use LLM to translate strings."""
        if not texts:
            return {}

        prompt = f"""
        Bạn là một chuyên gia dịch thuật game (Game Localizer) từ tiếng Nhật sang tiếng Việt.
        Nhiệm vụ: Dịch danh sách các chuỗi ký tự sau đây sang tiếng Việt.
        Yêu cầu:
        1. Giữ nguyên các mã điều khiển (control codes) nếu có (ví dụ: %s, \\n, [color]...).
        2. Dịch sát nghĩa nhưng phải mượt mà, phù hợp với ngữ cảnh game người lớn/tình cảm.
        3. Kết quả trả về phải là một JSON object với key là chuỗi gốc và value là chuỗi đã dịch.

        DANH SÁCH CHUỖI CẦN DỊCH:
        {texts}
        """
        
        result = self._call_llm(prompt, is_json=True, schema=TranslationSchema)
        if result and "translations" in result:
            return result["translations"]
        # Nếu model trả về JSON phẳng (không có key translations)
        if result and isinstance(result, dict) and len(result) > 0:
            return result
        return {}


    def translate_batch(self, texts: List[str]) -> Dict[str, str]:
        """Execute translation with batching."""
        return self.execute(texts)

if __name__ == "__main__":
    # Test with real extracted texts
    # Using gemini-3.1-pro-preview as requested for high quality
    translator = GodotTranslator(model_name="gemini-3.1-pro-preview")
    test_texts = ["画面リサイズ設定", "自動変更", "等倍"]
    results = translator.translate_batch(test_texts)
    
    # Sử dụng sys.stdout.buffer để tránh lỗi encoding trên Windows console
    import sys
    sys.stdout.buffer.write(f"Original: {test_texts}\n".encode('utf-8'))
    sys.stdout.buffer.write(f"Translated: {results}\n".encode('utf-8'))
