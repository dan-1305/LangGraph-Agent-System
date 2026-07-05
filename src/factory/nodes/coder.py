from typing import Dict, Any
from langgraph.prebuilt import create_react_agent
from src.factory.state import FactoryState
from src.factory.tools.system_tools import read_file, write_file, run_command
from src.factory.config import create_fallback_chain

async def coder_node(state: FactoryState) -> Dict[str, Any]:
    project_path = state.get("project_path", "")
    planned_architecture = state.get("planned_architecture", "")
    
    print(f"\n=======================================================")
    print(f"👨‍💻 [Coder Node] Khởi động AI Coder cho dự án: {project_path}")
    print(f"=======================================================")
    
    if not planned_architecture:
        print("⚠️ Không có bản thiết kế. Bỏ qua Coder.")
        return {"modified_files": ["Skipped"]}

    pro_model_list = ["gemini-3.1-pro-preview", "gemini-3-pro-preview", "gemini-2.5-pro"]
    llm = create_fallback_chain(pro_model_list, temperature=0.1, max_tokens=4096)
    
    tools = [read_file, write_file, run_command]
    agent_executor = create_react_agent(llm, tools)
    
    system_prompt = f"""Bạn là một AI Software Engineer bậc thầy.
Khu vực làm việc (Project Root) của bạn là: {project_path}

Đây là Bản thiết kế kiến trúc từ Technical Lead:
{planned_architecture}

Nhiệm vụ của bạn:
1. Đọc bản thiết kế và tạo cấu trúc thư mục tương ứng. Bạn có thể dùng `run_command` (ví dụ `mkdir -p ...` trên Linux hoặc `mkdir ...` trên Windows) hoặc công cụ `write_file` (sẽ tự động tạo thư mục cha).
2. Sinh mã nguồn cho các file theo thiết kế bằng tool `write_file`. Lưu ý đường dẫn file phải bắt đầu bằng `{project_path}/`. Ví dụ: `{project_path}/src/main.py`.
3. Nhớ tạo các file cơ bản như `.env.example`, `.gitignore`, `requirements.txt`.
4. Nếu số lượng file quá nhiều, ưu tiên tạo các file chính trước (Core Logic) rồi đến các file phụ.

CẢNH BÁO TỐI QUAN TRỌNG:
- BẮT BUỘC phải dùng Tool Calling (`write_file`, `run_command`). Tuyệt đối không giả lập text markdown suông.
- QUY TẮC CHẬM MÀ CHẮC: Bạn CHỈ ĐƯỢC PHÉP gọi MỘT (1) tool duy nhất trong mỗi lần phản hồi.
- Đảm bảo mã nguồn Python có Type Hinting, Docstring và đúng chuẩn PEP8.
"""
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": "Tiến hành tạo file theo bản thiết kế ngay bây giờ."}]
    
    try:
        # Tăng recursion limit vì có thể cần tạo nhiều file
        result = await agent_executor.ainvoke({"messages": messages}, config={"recursion_limit": 40})
        
        final_text = ""
        for msg in reversed(result["messages"]):
            if hasattr(msg, 'content') and isinstance(msg.content, str) and msg.content.strip():
                final_text = msg.content
                break
                
        print(f"\n✅ [Coder] Đã hoàn thành sinh mã nguồn cho dự án:\n{final_text}")
        return {"modified_files": ["Coding Completed"]}
    except Exception as e:
        print(f"\n❌ [Coder] Lỗi trong quá trình code: {e}")
        return {"modified_files": [f"Coding Failed: {e}"]}
