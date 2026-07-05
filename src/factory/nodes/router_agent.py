from src.base_agent import BaseAgent
import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Dict, Any
from src.factory.state import FactoryState

from pydantic import BaseModel, Field

class RouterDecision(BaseModel):
    route: str = Field(description="Một trong các giá trị: ROUTE_RAG, ROUTE_LOGS, ROUTE_NORMAL, ROUTE_HALT, ROUTE_CODEBASE_AUDIT, ROUTE_WORKFLOW")
    is_context_sufficient: bool = Field(description="Đánh giá xem ngữ cảnh/yêu cầu đã đủ rõ ràng chưa (True/False)")
    missing_info: str = Field(description="Nếu is_context_sufficient là False, ghi rõ thông tin nào bị thiếu (ví dụ: Tên file, thông báo lỗi)")
    reasoning: str = Field(description="Lý do ngắn gọn tại sao chọn route này")
    complexity: str = Field(description="Đánh giá độ phức tạp của task: LOW, MEDIUM, HIGH")
    recommended_model: str = Field(description="Đề xuất model phù hợp: gemini-3.1-flash-lite cho LOW/MEDIUM, claude-3-5-sonnet-20241022 cho HIGH")

class SemanticRouter(BaseAgent):
    """
    Enterprise-Grade Semantic Router (LLM-based) with Zero-Guessing Logic.
    """
    def __init__(self):
        super().__init__(name="SemanticRouter", role="Router", model_name="gemini-3.1-flash-lite", temperature=0.1)
        
    def route_query(self, query: str) -> Dict[str, Any]:
        if not query:
            return {"route": "ROUTE_HALT", "is_context_sufficient": False, "missing_info": "Query trống", "reasoning": "Không có yêu cầu"}
            
        prompt = f"""
        Nhiệm vụ: Phân loại câu hỏi/yêu cầu của người dùng vào 1 trong 5 nhánh xử lý (ROUTE).
        ĐỒNG THỜI, bạn phải áp dụng nguyên tắc ZERO-GUESSING: Tuyệt đối không đoán mò. Nếu yêu cầu thiếu file path cụ thể (đối với code fix) hoặc thiếu context cần thiết, bạn phải đánh dấu is_context_sufficient = False.
        
        1. ROUTE_RAG: Câu hỏi tra cứu tài liệu, kiến trúc, hệ thống.
        2. ROUTE_LOGS: Đọc file log, fix bug. YÊU CẦU: Phải có thông báo lỗi hoặc path file log.
        3. ROUTE_NORMAL: Các tác vụ chung (viết code mới, thảo luận). YÊU CẦU: Phải có scope rõ ràng.
        4. ROUTE_HALT: Khi bạn không hiểu yêu cầu, hoặc thiếu quá nhiều context để tiếp tục.
        5. ROUTE_CODEBASE_AUDIT: Dành cho yêu cầu phân tích toàn bộ dự án, audit mã nguồn, xem xét kiến trúc tổng thể. Ví dụ: "Hãy audit project X", "Kiểm tra kiến trúc của Y".
        6. ROUTE_WORKFLOW: Dành cho các yêu cầu chạy tool hệ thống, review code, commit code, audit tự động (Workflow Engine).
        
        Ngoài ra, hãy đánh giá ĐỘ PHỨC TẠP của task (LOW, MEDIUM, HIGH) và đề xuất MODEL PHÙ HỢP (ví dụ: "gemini-3.1-flash-lite" cho các task đơn giản để tiết kiệm chi phí, "claude-3-5-sonnet-20241022" cho logic phức tạp/code mới).
        
        Câu hỏi của người dùng:
        "{query}"
        """
        
        print("[SemanticRouter] Đang phân tích Context & phân luồng (Zero-Guessing)...")
        try:
            decision = self._call_llm(prompt, is_json=False, schema=RouterDecision)
            if decision and "route" in decision:
                if not decision.get("is_context_sufficient", True):
                    decision["route"] = "ROUTE_HALT"
                return decision
            else:
                return {"route": "ROUTE_HALT", "is_context_sufficient": False, "missing_info": "LLM Schema Error", "reasoning": "Lỗi schema"}
        except Exception as e:
            error_msg = str(e).lower()
            if "429" in error_msg or "too many requests" in error_msg or "quota" in error_msg:
                print(f"[SemanticRouter] 🛑 LỖI API QUOTA / RATE LIMIT (429). Kích hoạt Graceful Degradation.")
                return {"route": "ROUTE_QUOTA_EXHAUSTED", "is_context_sufficient": False, "missing_info": f"Quota Exhausted: {e}", "reasoning": "Lỗi 429/Quota"}
            return {"route": "ROUTE_HALT", "is_context_sufficient": False, "missing_info": f"API Error: {e}", "reasoning": "Lỗi API khác"}

    def _ai_handler(self, *args, **kwargs) -> Any:
        pass

    def _logic_handler(self, *args, **kwargs) -> Any:
        pass

def router_node(state: FactoryState):
    print("--- [Semantic Router] Kích hoạt ---")
    router = SemanticRouter()
    res = router.route_query(state.get("user_requirement", ""))
    
    route = res.get("route", "ROUTE_HALT")
    is_sufficient = res.get("is_context_sufficient", False)
    missing = res.get("missing_info", "")
    
    complexity = res.get("complexity", "MEDIUM")
    recommended_model = res.get("recommended_model", "gemini-3.1-flash-lite")
    
    print(f"[RouterAgent] Quyết định rẽ nhánh: {route} (Sufficient: {is_sufficient})")
    print(f"[RouterAgent] Độ phức tạp: {complexity} | Đề xuất Model: {recommended_model}")
    
    if route == "ROUTE_QUOTA_EXHAUSTED":
        print(f"[RouterAgent] ⚠️ GRACEFUL DEGRADATION: LLM chính cạn Quota. Đang lưu trạng thái vào SQLite MCP...")
        try:
            import sqlite3
            from datetime import datetime
            
            # Khởi tạo db nếu chưa có
            db_path = "circuit_breaker.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS quota_exhaustion_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    failed_node TEXT,
                    error_message TEXT,
                    state_dump TEXT
                )
            ''')
            # Ghi log checkpoint dạng JSON của toàn bộ state
            import json
            try:
                state_json = json.dumps(dict(state))
            except Exception:
                state_json = str(dict(state))
                
            cursor.execute('''
                INSERT INTO quota_exhaustion_logs (timestamp, failed_node, error_message, state_dump)
                VALUES (?, ?, ?, ?)
            ''', (datetime.now().isoformat(), "SemanticRouter", missing, state_json))
            conn.commit()
            conn.close()
            print(f"[RouterAgent] ✅ Trạng thái đã được lưu an toàn vào bảng quota_exhaustion_logs trong {db_path}.")
        except Exception as e:
            print(f"[RouterAgent] ❌ Lỗi khi ghi log SQLite: {e}")
            
        return {"selected_workflow": "ROUTE_QUOTA_EXHAUSTED", "error": f"Cạn Quota: {missing}"}
        
    if not is_sufficient or route == "ROUTE_HALT":
        print(f"[RouterAgent] 🛑 HALT EXECUTION: Thiếu context! Vui lòng cung cấp: {missing}")
        return {
            "selected_workflow": "ROUTE_HALT", 
            "error": f"Thiếu thông tin: {missing}",
            "complexity": complexity,
            "recommended_model": recommended_model
        }
    
    return {
        "selected_workflow": route,
        "complexity": complexity,
        "recommended_model": recommended_model
    }
