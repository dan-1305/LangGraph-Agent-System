import json
from src.base_agent import BaseAgent

class LLMAutopsy(BaseAgent):
    def __init__(self):
        # Hệ thống BaseAgent đã tự lo GCLI/CatieCLI URL và API Key, Cache, Tenacity
        super().__init__(model_name="label:tier-2", temperature=0.2)
            
    def _ai_handler(self, state: dict) -> dict:
        return state

    def _logic_handler(self, state: dict) -> dict:
        return state

    def analyze_crash(self, target_module: str, traceback_str: str) -> dict:
        """
        Gửi Traceback cho LLM phân tích nguyên nhân và cách sửa.
        Tránh đốt token, chỉ lấy đúng trọng tâm.
        """
        prompt = f"""Ngươi là QA Chaos Agent (Chuyên gia tìm diệt Bug).
Một module vừa bị Fuzzing làm cho Crash.

Module: {target_module}
Traceback:
{traceback_str[-1500:]}

Yêu cầu (Trả về ĐÚNG ĐỊNH DẠNG JSON):
{{
    "cause": "Nguyên nhân gốc rễ (1 câu)",
    "action": "Cách sửa chữa ngắn gọn"
}}
"""
        try:
            # Dùng method có sẵn để tận hưởng Retry, Cache, Fallback
            result = self._call_llm_with_retry(prompt, is_json=True)
            if isinstance(result, str):
                try:
                    return json.loads(result)
                except json.JSONDecodeError:
                    return {
                        "cause": result[:100],
                        "action": "Xem chi tiết text."
                    }
            return result
        except Exception as e:
            return {
                "cause": f"Lỗi gọi LLM: {str(e)}",
                "action": "Manual check"
            }
