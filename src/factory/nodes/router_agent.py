import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Dict, Any
from src.factory.state import FactoryState

class SemanticRouter:
    """
    Enterprise-Grade Semantic Router.
    Không dùng API, chỉ so khớp keyword tĩnh bằng quy tắc. Cực nhẹ (0ms).
    """
    def __init__(self):
        # Từ khóa định tuyến tĩnh
        self.routes = {
            "ROUTE_RAG": [
                "kiến trúc", "tài liệu", "lịch sử", "mốc", "milestone", 
                "roadmap", "kế hoạch", "chronicles", "hiến pháp", "constitution",
                "hệ thống", "system", "rag", "vector"
            ],
            "ROUTE_LOGS": [
                "lỗi", "bug", "crash", "treo", "fix", "sửa lỗi", "traceback",
                "log", "logs", "error", "timeout", "exception"
            ],
            # Mặc định là ROUTE_NORMAL
        }
        
    def route_query(self, query: str) -> Dict[str, Any]:
        if not query:
            return {"route": "ROUTE_NORMAL", "reasoning": "Query trống"}
            
        q_lower = query.lower()
        
        # Kiểm tra từng tuyến đường
        for route_name, keywords in self.routes.items():
            for kw in keywords:
                if kw in q_lower:
                    return {"route": route_name, "reasoning": f"Khớp từ khóa tĩnh: '{kw}'"}
                    
        return {"route": "ROUTE_NORMAL", "reasoning": "Không khớp keyword đặc thù"}

def router_node(state: FactoryState):
    print("--- [Semantic Router] Kích hoạt (Không dùng API) ---")
    router = SemanticRouter()
    res = router.route_query(state.get("user_requirement", ""))
    route = res.get("route", "ROUTE_NORMAL")
    print(f"[RouterAgent] Quyết định rẽ nhánh: {route} (Lý do: {res.get('reasoning')})")
    
    # Ghi tạm vào 1 biến state nào đó, hoặc ta có thể return dictionary để update state
    # Nhưng vì đây là Node đầu tiên, ta cần update state để hàm add_conditional_edges đọc
    return {"selected_workflow": route}