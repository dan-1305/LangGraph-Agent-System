import os
import json
import re
from typing import Dict, Any, Optional
from pathlib import Path
import warnings

# Bỏ qua cảnh báo Pydantic V1 do Langchain chưa nâng cấp đồng bộ
warnings.filterwarnings('ignore', category=UserWarning, module='langchain_core')
warnings.filterwarnings('ignore', category=UserWarning, module='pydantic')

# Load biến môi trường
env_path = Path(__file__).resolve().parent.parent / '.env'
try:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

from langchain_openai import ChatOpenAI

class BaseAgent:
    """
    Class cơ sở (Base Class) chung cho tất cả các Agent trong LangGraph_Agent_System.
    Cung cấp các kết nối LLM được chuẩn hóa thông qua langchain_openai.ChatOpenAI.
    """
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7, **kwargs):
        base_url = os.getenv("GCLI_BASE_URL")
        api_key = os.getenv("GCLI_API_KEY")
        
        if not api_key:
            print("⚠️ WARNING: Không tìm thấy GCLI_API_KEY trong .env. Vui lòng kiểm tra lại.")
            
        self.llm = ChatOpenAI(
            model=model_name,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
            **kwargs
        )
        
    def _call_llm(self, prompt: str, is_json: bool = False) -> str:
        """
        Gửi prompt đến LLM thông qua ChatOpenAI và trả về chuỗi kết quả.
        Tự động hướng dẫn mô hình xuất JSON nếu cần.
        """
        try:
            if is_json and "JSON" not in prompt:
                prompt += "\n\nVUI LÒNG TRẢ VỀ KẾT QUẢ DƯỚI DẠNG ĐỊNH DẠNG JSON CHUẨN. KHÔNG THÊM BẤT KỲ VĂN BẢN NÀO BÊN NGOÀI JSON."
                
            response = self.llm.invoke(prompt)
            return response.content
            
        except Exception as e:
            print(f"❌ Error calling LLM API (ChatOpenAI): {str(e)}")
            return ""

    def _parse_json_response(self, response_text: str) -> Optional[Any]:
        """
        Cố gắng parse chuỗi trả về thành JSON một cách an toàn.
        Sử dụng Regex để trích xuất JSON trong trường hợp LLM sinh ra text thừa.
        """
        if not response_text:
            return None
            
        text = response_text.strip()
        
        # 1. Thử parse trực tiếp
        try:
            # Loại bỏ markdown code blocks nếu có
            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            return json.loads(text.strip())
        except json.JSONDecodeError:
            pass # Nếu lỗi thì đi tiếp xuống cách 2
            
        # 2. Dùng regex để tìm khối JSON (Bắt đầu bằng { hoặc [)
        try:
            match = re.search(r'(\{.*\}|\[.*\])', response_text, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
        except Exception as e:
            print(f"❌ Regex JSON parsing failed: {e}")

        # In ra lỗi nếu không parse được
        print(f"❌ Could not parse JSON from response.")
        print(f"Raw Response: {response_text[:200]}...") 
        return None