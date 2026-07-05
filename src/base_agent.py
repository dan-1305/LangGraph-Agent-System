import os
import json
import re
from typing import Any, Optional, Type, TypeVar
from pathlib import Path
import warnings
from abc import ABC, abstractmethod

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
from pydantic import BaseModel, ValidationError
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

T = TypeVar('T', bound=BaseModel)

class LLMAPIError(Exception):
    """Lỗi khi gọi API LLM (Rate Limit, Server Error...)"""
    pass

class SchemaValidationError(Exception):
    """Lỗi khi LLM sinh JSON sai Schema (Ảo giác cấu trúc)"""
    pass

class BlankHallucinationError(Exception):
    """Lỗi khi LLM trả về rỗng (Ảo giác trống rỗng)"""
    pass

class BaseAgent(ABC):
    """
    Class cơ sở (Base Class) chung cho tất cả các Agent trong LangGraph_Agent_System.
    Cung cấp các kết nối LLM được chuẩn hóa thông qua langchain_openai.ChatOpenAI.
    
    Tích hợp 3 vũ khí sinh tồn (Survival Engineering):
    1. Circuit Breaker Shield (Tenacity Exponential Backoff) chống đứt gãy mạng.
    2. Schema Enforcer Gauntlet (Pydantic) chống ảo giác cấu trúc dữ liệu.
    3. Context Anchor (Blank Check) chống ảo giác trả về chuỗi rỗng.
    """
    def __init__(self, model_name: str = "gemini-3-flash-preview", temperature: float = 0.7, agent_label: str = "tier-2", **kwargs):
        base_url = os.getenv("GCLI_BASE_URL")
        api_key = os.getenv("GCLI_API_KEY")
        
        if not api_key:
            print("⚠️ WARNING: Không tìm thấy GCLI_API_KEY trong .env. Vui lòng kiểm tra lại.")
            
        # Chuẩn hóa base_url cho langchain_openai (xóa /chat/completions nếu có)
        if base_url and base_url.endswith("/chat/completions"):
            base_url = base_url.replace("/chat/completions", "")
        elif base_url and base_url.endswith("/chat/completions/"):
            base_url = base_url.replace("/chat/completions/", "")

        # Use the label as the model name so the Proxy can route it
        actual_model_name = f"label:{agent_label}" if agent_label else model_name

        self.llm = ChatOpenAI(
            model=actual_model_name,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
            **kwargs
        )
        
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_random_exponential(multiplier=1.5, max=30),
        retry=retry_if_exception_type((LLMAPIError, BlankHallucinationError, SchemaValidationError))
    )
    def _call_llm_with_retry(self, prompt: str, is_json: bool = False, schema: Optional[Type[T]] = None) -> Any:
        """
        Luồng gọi LLM khép kín với đầy đủ cơ chế Retry và dán nhãn Agent.
        """
        from src.api_gateway import gateway
        
        module_name = self.__class__.__name__
            
        current_prompt = prompt
        
        # Thử lấy từ cache trước
        schema_json_str = ""
        if schema:
            try:
                schema_json_str = schema.schema_json()
            except AttributeError:
                schema_json_str = json.dumps(schema.model_json_schema())
        
        cached_result = gateway.get_cached_response(current_prompt, schema_json_str)
        if cached_result:
            print("[API Gateway] Cache HIT - Token Saved!")
            return json.loads(cached_result) if schema or is_json else cached_result

        
        # Nếu có schema Pydantic, ưu tiên dùng tính năng Structured Output của Langchain
        if schema:
            try:
                structured_llm = self.llm.with_structured_output(schema)
                try:
                    response = structured_llm.invoke(current_prompt)
                    result_dict = None
                    if hasattr(response, 'dict'):
                        result_dict = response.dict()
                    elif hasattr(response, 'model_dump'):
                        result_dict = response.model_dump()
                    else:
                        result_dict = response
                        
                    # Lưu vào cache
                    gateway.save_to_cache(current_prompt, json.dumps(result_dict), schema_json_str)
                    return result_dict
                except Exception as e:
                    err_msg = str(e).lower()
                    if "429" in err_msg or "quota" in err_msg or "rate limit" in err_msg or "503" in err_msg:
                        raise LLMAPIError(f"API Rate Limit: {e}")
                    print(f"⚠️ Structured Output failed ({str(e)[:50]}). Fallback to Regex Parser...")
            except Exception:
                pass # Provider không support .with_structured_output()

        # Kích hoạt Schema Enforcer Gauntlet (Fallback Mode)
        if is_json or schema:
            current_prompt += "\n\n[QUAN TRỌNG] VUI LÒNG TRẢ VỀ DUY NHẤT ĐỊNH DẠNG JSON CHUẨN. KHÔNG CÓ BẤT KỲ VĂN BẢN NÀO BÊN NGOÀI."
            if schema:
                try:
                    schema_json = schema.schema_json()
                except AttributeError:
                    schema_json = json.dumps(schema.model_json_schema())
                current_prompt += f"\n\nSCHEMA BẮT BUỘC (TUYỆT ĐỐI KHÔNG ĐỔI TÊN KEY HOẶC THIẾU KEY):\n{schema_json}"

        # Gọi LLM Text Mode
        try:
            response = self.llm.invoke(current_prompt)
            content = response.content.strip()
        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "quota" in err_msg or "rate limit" in err_msg or "503" in err_msg:
                raise LLMAPIError(f"API Rate Limit: {e}")
            raise LLMAPIError(f"Unexpected API Error: {e}")

        # Kích hoạt Context Anchor (Chống Blank Hallucination)
        if not content or len(content) < 5:
            raise BlankHallucinationError("Response too short or blank.")

        # Xử lý JSON nếu được yêu cầu
        if is_json or schema:
            parsed_dict = self._extract_json_from_text(content)
            if not parsed_dict:
                raise SchemaValidationError("Invalid JSON structure")
            
            if schema:
                try:
                    try:
                        validated_data = schema.parse_obj(parsed_dict)
                        result_dict = validated_data.dict()
                    except AttributeError:
                        validated_data = schema.model_validate(parsed_dict)
                        result_dict = validated_data.model_dump()
                        
                    gateway.save_to_cache(current_prompt, json.dumps(result_dict), schema_json_str)
                    return result_dict
                except ValidationError as ve:
                    raise SchemaValidationError(f"Schema Validation Failed: {ve}")
                    
            gateway.save_to_cache(current_prompt, json.dumps(parsed_dict), schema_json_str)
            return parsed_dict
            
        gateway.save_to_cache(current_prompt, content, schema_json_str)
        return content

    def _extract_json_from_text(self, text: str) -> Optional[Any]:
        """Tách JSON ra khỏi Markdown Code blocks an toàn."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            try:
                match = re.search(r'(\{.*\}|\[.*\])', text, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
            except Exception:
                pass
        return None

    def _call_llm(self, prompt: str, is_json: bool = False, schema: Optional[Type[T]] = None) -> Any:
        """Wrapper an toàn bọc Try-Except ngoài cùng cho hệ thống"""
        try:
            return self._call_llm_with_retry(prompt, is_json=is_json, schema=schema)
        except Exception as e:
            print(f"[Circuit Breaker] LLM failed completely: {e}")
            return ""

    def _parse_json_response(self, response_text: str, schema: Optional[Type[T]] = None) -> Optional[Any]:
        if not response_text:
            return None
        parsed = self._extract_json_from_text(response_text)
        if schema and parsed:
            try:
                try:
                    return schema.parse_obj(parsed).dict()
                except AttributeError:
                    return schema.model_validate(parsed).model_dump()
            except ValidationError:
                return None
        return parsed

    @abstractmethod
    def _ai_handler(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    def _logic_handler(self, *args, **kwargs) -> Any:
        pass

    def execute(self, *args, **kwargs) -> Any:
        """
        Mô hình Cầu Dao Điện (Circuit Breaker Pattern).
        """
        try:
            result = self._ai_handler(*args, **kwargs)
            if result:
                return result
            return self._logic_handler(*args, **kwargs)
        except Exception as e:
            print(f"[Circuit Breaker] Fallback to logic due to: {e}")
            return self._logic_handler(*args, **kwargs)
