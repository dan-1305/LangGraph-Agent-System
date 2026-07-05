import os
import random
import glob
from typing import List, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import sys

# Force UTF-8 encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup sys.path cho Monorepo
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from src.base_agent import BaseAgent
from tools.system.rag_query import query_rag_return_context

class QuizOption(BaseModel):
    id: str = Field(description="Mã đáp án (A, B, C, D)")
    text: str = Field(description="Nội dung đáp án")

class QuizQuestion(BaseModel):
    question: str = Field(description="Nội dung câu hỏi")
    options: List[QuizOption] = Field(description="Danh sách các lựa chọn")
    correct_option_id: str = Field(description="Mã đáp án đúng (A, B, C, D)")
    explanation: str = Field(description="Giải thích tại sao đáp án này đúng")

class Quiz(BaseModel):
    questions: List[QuizQuestion] = Field(description="Danh sách các câu hỏi trắc nghiệm (tối đa 3 câu)")

class CodeTutorAgent(BaseAgent):
    """
    [ROLE: Code Tutor / Sovereign Academy]
    Chuyên gia giảng dạy code nội bộ, áp dụng kỹ thuật Feynman.
    """
    def __init__(self):
        super().__init__(name="CodeTutorAgent", role="Tutor", model_name="gemini-3.1-flash-lite")

    def _ai_handler(self, *args, **kwargs):
        pass

    def _logic_handler(self, *args, **kwargs):
        pass

    def get_random_core_file(self) -> str:
        """Lấy ngẫu nhiên 1 file Python từ core/ hoặc core_utilities/"""
        core_path = os.path.join(base_dir, "core", "**", "*.py")
        utils_path = os.path.join(base_dir, "core_utilities", "**", "*.py")
        
        files = glob.glob(core_path, recursive=True) + glob.glob(utils_path, recursive=True)
        # Loại bỏ các file __init__.py hoặc test
        files = [f for f in files if "__init__" not in f and "test_" not in os.path.basename(f)]
        
        if not files:
            raise FileNotFoundError("Không tìm thấy file Python nào trong core/ hoặc core_utilities/")
            
        return random.choice(files)

    def read_code(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Giới hạn dòng nếu file quá dài để bảo vệ Token Window (Phòng ngừa LLMAPIError)
            lines = content.splitlines()
            if len(lines) > 150:
                content = "\n".join(lines[:150]) + "\n... [Code đã được rút gọn do quá dài] ..."
            return content

    def explain_code(self, code: str, filename: str) -> str:
        # Lấy thêm bối cảnh từ Bách khoa toàn thư hoặc Hệ thống RAG
        rag_context = query_rag_return_context(f"Giải thích file {filename} và các thành phần liên quan", n_results=2)
        
        prompt = f"""
        [ROLE: Senior Architectural Tutor & Code Reviewer]
        Nhiệm vụ của bạn là phân tích và giải thích file code `{filename}` thuộc hệ thống Sovereign LangGraph cho một Software Engineer / Maintainer.
        
        [RAG CONTEXT (Từ System Docs)]:
        {rag_context}
        
        YÊU CẦU NGUYÊN TẮC (STRICT GUIDELINES):
        1. BỎ QUA VĂN MẪU & ĐỊNH NGHĨA SƠ CẤP: Tuyệt đối không giải thích những khái niệm cơ bản (VD: HTTP là gì, if/else là gì).
        
        2. TUYỆT ĐỐI KHÔNG "BỐC PHÉT" KIẾN THỨC (ZERO HALLUCINATION) VÀ CẤM OVER-ENGINEERING:
           - Phân biệt RẠCH RÒI giữa Multi-threading (`threading.Thread`) và Asyncio (`async/await`). Không được nhầm lẫn việc spawn Thread là Async.
           - Không được tự bịa ra lỗ hổng bảo mật vô lý (Ví dụ: Đọc `.env` là chuẩn 12-Factor, KHÔNG PHẢI lỗ hổng. `https` là đã mã hóa).
           - CẤM Over-engineering: Đây là Local LangGraph Agent System chạy trên PC. Việc dùng SQLite và JSON là chủ ý thiết kế gọn nhẹ. Tuyệt đối không chê bai SQLite/JSON và cấm gợi ý đổi sang MongoDB hay PostgreSQL trừ khi thực sự cần thiết.
           - Chỉ ra các chi tiết tối ưu "chí mạng" nhỏ nhất (Ví dụ: `if not logger.handlers:` để chống duplicate logs, hoặc vòng lặp chống Infinite Loop).
        
        3. DEEP DIVE VÀO KỸ THUẬT VÀ DOMAIN LOGIC (MÁU VÀ THỊT):
           - Domain Logic (Logic Nghiệp vụ): Phải đọc kỹ các chuỗi string, các điều kiện `if/else` để giải thích cốt lõi thuật toán. (Ví dụ: Nếu code check "stage 2", "tích lũy", hãy giải thích nó đang áp dụng logic/nguyên lý gì).
           - Luồng xử lý (Data Flow): Phân tích luồng chạy của code từng bước một cách ngắn gọn, mượt mà.
           - Bảng Đánh đổi Kỹ thuật (Technical Trade-offs): Tại sao lại dùng kiến trúc hiện tại? Ưu và nhược điểm là gì?
           - Thiết kế An toàn (Safety-by-Design): Code này có chống được Infinite Loop, Memory Leak hay Race Condition không? Việc gán `daemon=True` có tác dụng gì?
           - Gợi ý Tối ưu cực hạn (Extreme Optimization): Đề xuất cách code ngắn hơn, chạy nhanh hơn (Ví dụ: dùng QueueHandler thay vì spawn Thread liên tục, gỡ bỏ import thừa).
        
        CODE CẦN PHÂN TÍCH:
        ```python
        {code}
        ```
        """
        print("[+] Đang biên soạn bài giảng (Senior Architect & Reviewer Mode)...")
        return self._call_llm(prompt)

    def generate_quiz(self, code: str, filename: str) -> dict:
        prompt = f"""
        Dựa vào đoạn code Python từ file `{filename}` dưới đây, hãy tạo ra một bài trắc nghiệm (Quiz) gồm 3 câu hỏi để kiểm tra mức độ hiểu bài.
        
        YÊU CẦU:
        1. Câu hỏi tập trung vào logic cốt lõi, cách sử dụng hoặc kiến trúc của code.
        2. Cung cấp 4 đáp án A, B, C, D cho mỗi câu.
        3. Chỉ định rõ đáp án đúng và kèm theo lời giải thích ngắn gọn.
        
        CODE:
        ```python
        {code}
        ```
        """
        print("[+] Đang tạo bài tập trắc nghiệm...")
        # Sử dụng structured output
        quiz_data = self._call_llm(prompt, schema=Quiz)
        return quiz_data

if __name__ == "__main__":
    tutor = CodeTutorAgent()
    f = tutor.get_random_core_file()
    print(f"File ngẫu nhiên: {f}")
    code = tutor.read_code(f)
    print("Testing LLM Explain...")
    print(tutor.explain_code(code, f))
    print("Testing LLM Quiz...")
    print(tutor.generate_quiz(code, f))
