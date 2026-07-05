from typing import Dict, Any
from langchain_core.messages import HumanMessage
from src.factory.state import FactoryState
from src.factory.config import create_fallback_chain

async def triage_issues_and_plan(qa_report: str, test_results: str, llm) -> str:
    """Technical Director: Phân loại lỗi và lên kế hoạch sửa chữa."""
    prompt = f"""Bạn là Technical Director (Giám đốc Kỹ thuật).
Dưới đây là Báo cáo QA của dự án:
{qa_report}

Dưới đây là Log lỗi test (PyTest Stack Trace) nếu có:
{test_results}

Nhiệm vụ của bạn:
1. SÀNG LỌC (Triage): Phân tích báo cáo QA và đặc biệt là Log Lỗi Test, CHỈ CHỌN ra những lỗi có thể tự động sửa an toàn bằng công cụ lập trình (ví dụ: tạo file .gitignore, .env.example, sửa lỗi import, thêm logging, sửa lỗi PEP8, thêm Type Hinting/Docstring, sửa lỗi logic nhỏ gây Failed Test).
2. LỌC BỎ: Tuyệt đối KHÔNG chọn các lỗi quá phức tạp (như xây dựng lại toàn bộ database kiến trúc lớn) vì AI Coder cấp dưới sẽ bị quá tải.
3. LÊN KẾ HOẠCH (Execution Plan): Viết một bản chỉ thị cực kỳ chi tiết, chia thành các Bước (Step 1, Step 2...). Trong mỗi bước, hãy chỉ rõ:
   - Tên file cần sửa.
   - Hành động cần làm (đọc file, ghi đè, tìm và thay thế).
   - Mã code cụ thể cần thay thế (Đặc biệt: nếu có lỗi Stack Trace, hãy trích xuất đúng dòng bị lỗi và chỉ định code thay thế).

Bản chỉ thị này sẽ được giao cho một AI Software Engineer (Auto-Fixer) thi hành. Hãy viết lệnh thật dứt khoát và rõ ràng. KHÔNG cần giải thích dài dòng, chỉ cần Action Plan.
"""
    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return response.content

async def triage_director_node(state: FactoryState) -> Dict[str, Any]:
    print("\n=======================================================")
    print("[Technical Director Node] Dang doc bao cao QA va len Ke hoach sua loi...")
    
    qa_report = state.get("qa_report_summary", "")
    test_results = state.get("test_results", "")
    
    if not qa_report:
        return {"fix_plan": "Không có báo cáo QA để xử lý."}

    pro_model_list = ["gemini-3.1-pro-preview", "gemini-3-pro-preview", "gemini-2.5-pro"]
    llm = create_fallback_chain(pro_model_list, temperature=0.1, max_tokens=4096)
    
    execution_plan = await triage_issues_and_plan(qa_report, test_results, llm)
    print("\n[Ban chi thi cua Giam doc]:\n" + execution_plan + "\n")
    
    return {"fix_plan": execution_plan}
