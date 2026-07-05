# jarvis_core/ai_agent.py
import os
import time
import json
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta

import sys
from dotenv import load_dotenv
from pathlib import Path

# Đảm bảo import được thư viện lõi của hệ thống
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.config import create_fallback_chain

# Import GLOBAL_KEY_MANAGER từ key_manager.py thay vì duplicate (Có thể dần deprecate)
from jarvis_core.key_manager import GLOBAL_KEY_MANAGER

# Tự động tìm về thư mục gốc của dự án (Jarvis/)
base_path = Path(__file__).resolve().parent.parent
env_path = root_dir / '.env' # Trỏ thẳng về env gốc của UV Workspace

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    logging.warning(f"KHÔNG TÌM THẤY file .env tại: {env_path}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
CACHE_TTL = 3600

class AIService:
    """
    Core AI Service - Trái tim của Jarvis.
    Đã được đồng bộ hóa (Refactored) với kiến trúc lõi LangGraph Agent System V2
    thông qua create_fallback_chain.
    """

    def __init__(self, key_manager = None):
        self.key_manager = key_manager or GLOBAL_KEY_MANAGER
        self.cache = {}
        self.cache_ttl = CACHE_TTL
        
        # Đồng bộ hóa: Dùng Fallback Chain của hệ thống thay vì tự viết Retry/Key Rotation
        self.llm = create_fallback_chain(
            model_list=['gemini-2.5-flash-lite', 'gemini-2.5-flash'],
            temperature=0.7
        )

    def _get_cached_response(self, prompt: str, model: str) -> Optional[str]:
        """Kiểm tra xem câu hỏi này đã có trong cache chưa."""
        cache_key = f"{model}:{hash(prompt)}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            # Kiểm tra hạn sử dụng (TTL)
            if (datetime.now() - cached['timestamp']).seconds < self.cache_ttl:
                return cached['response']
            # Xóa cache hết hạn
            del self.cache[cache_key]
        return None

    def _update_cache(self, prompt: str, model: str, response: str):
        """Lưu câu trả lời vào cache."""
        cache_key = f"{model}:{hash(prompt)}"
        self.cache[cache_key] = {
            'response': response,
            'timestamp': datetime.now()
        }
        # Dọn dẹp cache nếu quá lớn (giữ 1000 mục mới nhất)
        if len(self.cache) > 1000:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

    def generate_response(self, prompt: str, model: str = None) -> str:
        """Hàm chính để tạo phản hồi (Có Cache + Đồng bộ Fallback Chain)."""
        model = model or "gemini-2.5-flash-lite"

        # 1. Check Cache
        if cached := self._get_cached_response(prompt, model):
            logger.info("-> Serving from Cache (Tốc độ ánh sáng!)")
            return cached

        # 2. Gọi qua Fallback Chain chung
        try:
            response = self.llm.invoke(prompt)
            content = response.content.strip()
            
            # Track Token Usage nếu hệ thống hỗ trợ
            try:
                from src.token_tracker import track_llm_usage
                model_name = getattr(self.llm, 'model', 'unknown') if hasattr(self.llm, 'model') else 'fallback_chain_model'
                track_llm_usage(response, "jarvis-rpg-assistant", model_name)
            except Exception:
                pass
                
            self._update_cache(prompt, model, content)
            return content
            
        except Exception as e:
            logger.error(f"Fallback Chain thất bại: {str(e)}")
            raise RuntimeError(f"Hệ thống lõi LangGraph từ chối phục vụ. Lỗi: {str(e)}")


# Global instance
ai_service = AIService()


# --- Public API (Các hàm cho module khác gọi) ---

def ask_jarvis(prompt: str) -> str:
    """Hàm giao tiếp cơ bản với Jarvis."""
    try:
        return ai_service.generate_response(prompt)
    except Exception as e:
        logger.error(f"Critical Error in ask_jarvis: {str(e)}")
        return "Xin lỗi The Builder, hệ thống AI đang gặp sự cố kết nối. Vui lòng kiểm tra Log."


def evaluate_evolution(current_profile: dict, completed_tasks: str) -> dict:
    """
    Đánh giá nhiệm vụ để tính XP/HP (RPG System).
    Có xử lý JSON an toàn.
    """
    prompt = f"""
    Bạn là Gamemaster của hệ thống RPG đời thực. Hãy đánh giá các nhiệm vụ sau:
    {completed_tasks}

    Profile hiện tại:
    {json.dumps(current_profile, indent=2)}

    Yêu cầu:
    - Phân tích độ khó của task để tính XP (Dễ: 10-20, Trung bình: 30-50, Khó: 50-100).
    - Nếu task không hoàn thành tốt, trừ HP.
    - Trả về DUY NHẤT một chuỗi JSON thuần (không markdown) với định dạng:
    {{
        "xp_gained": int,
        "hp_change": int,
        "new_status": "string",
        "message": "Lời nhận xét ngắn gọn, hài hước kiểu IT/DevOps"
    }}
    """

    try:
        raw_response = ai_service.generate_response(prompt)

        # --- CLEANUP JSON (Quan trọng) ---
        # Gemini hay trả về ```json ... ```, phải cắt bỏ
        clean_json = raw_response.strip()
        if clean_json.startswith("```"):
            clean_json = clean_json.split("```")[1]
        if clean_json.startswith("json"):
            clean_json = clean_json[4:]
        clean_json = clean_json.strip()
        # ---------------------------------

        result = json.loads(clean_json)
        return {
            'xp_gained': result.get('xp_gained', 0),
            'hp_change': result.get('hp_change', 0),
            'new_status': result.get('new_status', 'active'),
            'message': result.get('message', 'Nhiệm vụ đã được cập nhật!')
        }
    except json.JSONDecodeError:
        logger.error(f"Lỗi Parse JSON từ AI: {raw_response}")
        return {
            'xp_gained': 10,  # Fallback: Cho ít XP an ủi
            'hp_change': 0,
            'new_status': current_profile.get('status', 'active'),
            'message': 'AI bị ngáo JSON, nhưng tôi vẫn cộng cho bạn 10 XP an ủi!'
        }
    except Exception as e:
        logger.error(f"Error in evaluate_evolution: {str(e)}")
        return {
            'xp_gained': 0,
            'hp_change': 0,
            'new_status': current_profile.get('status', 'active'),
            'message': 'Lỗi hệ thống khi đánh giá nhiệm vụ.'
        }


if __name__ == "__main__":
    # Test nhanh khi chạy trực tiếp file này
    print("--- Test Key Rotation & AI ---")
    try:
        print(ask_jarvis("Chào Jarvis, hãy giới thiệu ngắn gọn về bạn bằng 1 câu."))
    except Exception as e:
        print(f"Test Failed: {e}")