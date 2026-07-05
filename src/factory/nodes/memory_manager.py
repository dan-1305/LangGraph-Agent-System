import os
import json
import time
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from src.factory.state import FactoryState
from src.factory.config import create_fallback_chain

def truncate_text(text: str, max_lines: int = 50) -> str:
    lines = text.split('\n')
    if len(lines) <= max_lines:
        return text
    return '\n'.join(lines[-max_lines:]) + "\n... (truncated)"

def memory_manager_node(state: FactoryState) -> Dict[str, Any]:
    print("[Memory Manager] Dang don dep va ghi log loi vao file (Disk-as-State)...")
    
    flash_model_list = ["gemini-3-flash-preview", "gemini-2.5-flash"]
    llm = create_fallback_chain(flash_model_list, temperature=0.1, max_tokens=1024)
    
    qa_report = state.get("qa_report_summary", "")
    
    # Write full QA report to disk instead of keeping in memory
    log_dir = "logs/tasks"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = int(time.time())
    log_file = f"{log_dir}/error_attempt_{timestamp}.txt"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(qa_report)
    
    error_pointers = state.get("error_pointers", [])
    error_pointers.append(log_file)
    
    # Generate a very short summary for the LLM
    truncated_report = truncate_text(qa_report, 20)
    prompt = f"""Mày là một kỹ sư dọn dẹp bộ nhớ (Memory Trimming).
Dưới đây là một đoạn lỗi vừa xảy ra:

Lỗi mới nhất: {truncated_report}

Nhiệm vụ: Tóm tắt lại dưới 100 chữ:
1. Đã thử phương pháp gì?
2. Lỗi cuối cùng là gì?
Chỉ trả về chuỗi văn bản tóm tắt."""

    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    new_summary = response.content
    
    print(f"[Memory Manager] Da luu pointer {log_file} va tao summary:\n{new_summary[:100]}...\n")
    
    return {"error_pointers": error_pointers, "qa_report_summary": new_summary}
