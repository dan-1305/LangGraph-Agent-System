import sys
import io
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.state import FactoryState
# Import hàm query đã tối ưu ở mốc trước
from tools.system.rag_query import query_rag_return_context

def context_manager_node(state: FactoryState):
    """
    Just-In-Time Context Manager.
    Dựa vào route đã được Semantic Router chọn, bơm đúng lượng data cần thiết vào State.
    """
    print("--- [Context Manager] Kích hoạt ---")
    route = state.get("selected_workflow", "ROUTE_NORMAL")
    user_query = state.get("user_requirement", "")
    
    injected_context = ""
    
    if route == "ROUTE_RAG":
        print(f"[Context Manager] Đang truy xuất JIT Context từ VectorDB cho câu hỏi: '{user_query}'...")
        # Gọi RAG query, lấy top 3
        # Hàm query_rag_return_context sẽ được viết bổ sung trong tools/system/rag_query.py
        try:
            # Lọc theo domain context/docs
            jic = query_rag_return_context(user_query, top_k=3)
            
            # Nếu hàm trả về lỗi từ ChromaDB
            if "❌" in jic or "Lỗi" in jic:
                raise Exception(jic)
                
            injected_context = f"\n[JIT KNOWLEDGE BASE]\n{jic}\n[/JIT KNOWLEDGE BASE]\n"
            print("[Context Manager] Đã bơm xong JIT ngữ cảnh (RAG) vào RAM.")
            
        except Exception as e:
            print(f"⚠️ [Context Manager] Lỗi truy xuất RAG: {e}")
            print(f"🔄 [Fallback] Kích hoạt Phương pháp Truyền thống: Cấp đường dẫn file thô.")
            
            # Cấp phát JIT Tools đọc file
            available_tools = ["read_file", "search_files", "list_files"]
            state["available_tools"] = available_tools
            
            injected_context = (
                "\n[JIT KNOWLEDGE BASE - FALLBACK]\n"
                "Hệ thống RAG hiện đang không khả dụng.\n"
                "Bạn BẮT BUỘC phải dùng các tool đọc file (read_file) để tự mình đọc các tài liệu cốt lõi sau đây "
                "nhằm thu thập ngữ cảnh cho câu trả lời của mình:\n"
                "- context/ARCHITECTURE.md\n"
                "- context/JARVIS_CHRONICLES.md\n"
                "- context/ROADMAP.md\n"
                "Tuyệt đối KHÔNG ĐƯỢC trả lời bừa khi chưa đọc file!\n"
                "[/JIT KNOWLEDGE BASE - FALLBACK]\n"
            )
            
    elif route == "ROUTE_LOGS":
        print(f"[Context Manager] Chuẩn bị JIT Tools cho việc đọc Log...")
        # Lọc danh sách Tool. Ở đây giả lập việc chỉ cấp quyền ĐỌC, cấm GHI.
        available_tools = ["read_file", "search_files", "list_files"]
        injected_context = "\n[JIT TOOLS]\nBạn chỉ được cấp quyền sử dụng các công cụ sau để gỡ lỗi: " + ", ".join(available_tools) + "\nTuyệt đối không được chỉnh sửa mã nguồn cho đến khi có lệnh.\n[/JIT TOOLS]\n"
        # Gắn danh sách tool vào state để Node LLM tiếp theo biết đường bind_tools
        state["available_tools"] = available_tools
        
    else:
        print(f"[Context Manager] Route Normal. Cấp phát JIT Tools cơ bản...")
        available_tools = ["read_file", "write_to_file", "replace_in_file", "execute_command"]
        injected_context = "\n[JIT TOOLS]\nBạn là Coder. Bạn được cấp full quyền thao tác file: " + ", ".join(available_tools) + "\n[/JIT TOOLS]\n"
        state["available_tools"] = available_tools
        
    # Cập nhật context vào state
    state["code_context"] = injected_context
    return state
