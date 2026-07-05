from langchain_core.tools import tool
from pathlib import Path
import sys

if sys.platform == "win32" and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Đảm bảo có thể import từ projects
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

try:
    from projects.knowledge_base_agent.src.rag_agent import RAGAgent
    rag_agent_instance = RAGAgent()
except Exception as e:
    print(f"[!] Không thể khởi tạo RAG Agent Tool: {e}")
    rag_agent_instance = None

@tool
def search_research_papers(query: str) -> str:
    """
    Tìm kiếm kiến thức chuyên sâu từ Tàng Kinh Các (Knowledge Database).
    Sử dụng Tool này khi cần tìm hiểu về các chiến lược Marketing, thuật toán AI (ReAct, Chain of Thought), 
    hoặc phương pháp Đầu tư Chứng khoán (Trading).
    
    Args:
        query (str): Câu hỏi hoặc từ khóa cần tìm kiếm (Ví dụ: "Cách viết Hook giật gân là gì?").
    """
    if not rag_agent_instance:
        return "Lỗi: Không thể kết nối với Knowledge Base Database."
        
    try:
        # Gọi thẳng RAG Agent để trả về câu trả lời đã được tổng hợp
        return rag_agent_instance.query(query)
    except Exception as e:
        return f"Lỗi khi truy vấn Database: {str(e)}"
