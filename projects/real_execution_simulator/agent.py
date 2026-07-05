import os
import json
from typing import TypedDict, List, Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Thêm path để import config
import sys
from pathlib import Path
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))
from src.factory.config import create_fallback_chain

from projects.real_execution_simulator.tools import EXECUTION_TOOLS

# 1. State Definition
class SimulatorState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    task: str
    target_file: str
    iteration: int
    max_iterations: int
    is_success: bool
    reflection: str

# 2. Agent Node (The Thinker/Coder)
def agent_node(state: SimulatorState):
    print(f"\n--- [Iteration {state['iteration']}/{state['max_iterations']}] THINKING ---")
    
    # Ràng buộc số lần lặp
    if state["iteration"] >= state["max_iterations"]:
        print("Đã đạt giới hạn lặp. Force Quit.")
        return {"messages": [AIMessage(content="Tôi đã thử quá nhiều lần mà vẫn thất bại.")], "is_success": False}
        
    system_prompt = """Bạn là một Senior Python Developer / SRE Commander xuất sắc.
Nhiệm vụ của bạn là: {task}
Mục tiêu cuối cùng là file '{target_file}' phải chạy thành công (exit code 0).

Bạn có quyền gọi các tools:
1. `execute_terminal_command`: Chạy file. Ghi nhớ, LUÔN DÙNG `.venv\Scripts\python.exe <file>` để chạy thay vì `uv run python` để tránh lỗi Access Denied trên Windows.
2. `read_file_content`: Đọc nội dung file nếu có lỗi xảy ra.
3. `rewrite_entire_file`: Sửa lại toàn bộ code file đó để vá lỗi (Tool này tự động tạo file .bak để backup).
4. `restore_backup`: Phục hồi lại file từ bản backup (.bak) nếu bạn sửa lỗi sai và làm code hỏng nặng hơn.

Quy trình làm việc (Self-Correction Loop):
Bước 1: Dùng execute_terminal_command để chạy file.
Bước 2: Nếu exit_code != 0, đọc stderr, sau đó dùng read_file_content đọc file lỗi.
Bước 3: Phân tích lỗi, sửa code và dùng rewrite_entire_file ghi đè lại.
Bước 4: Chạy lại execute_terminal_command. Nếu lỗi nặng hơn, dùng `restore_backup` rồi thử lại cách khác.
Bước 5: Lặp lại tới khi exit_code = 0.

NẾU chạy lệnh thấy exit_code = 0 (Thành công), hãy output "TASK_COMPLETED" và tóm tắt lại những gì bạn đã sửa.
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    # Bọc fallback để an toàn 429
    # Dùng model Pro để tăng khả năng sửa lỗi phức tạp và tiêu thụ Quota Pro
    llm = create_fallback_chain(["gemini-3.1-pro-preview", "gemini-2.5-pro", "gemini-2.5-flash"], temperature=0.2)
    # Bind tools vào LLM
    llm_with_tools = llm.bind_tools(EXECUTION_TOOLS)
    
    chain = prompt | llm_with_tools
    
    response = chain.invoke({
        "task": state["task"],
        "target_file": state["target_file"],
        "messages": state["messages"]
    })
    
    print(f"Agent response: {response.content}")
    if hasattr(response, 'tool_calls') and response.tool_calls:
        print(f"Agent requested tools: {response.tool_calls}")
        
    return {"messages": [response], "iteration": state["iteration"] + 1}

# 3. Checker Node (Routing)
def should_continue(state: SimulatorState):
    messages = state["messages"]
    last_message = messages[-1]
    
    # Nếu có tool call -> chuyển sang ToolNode
    if hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        return "tools"
        
    # Nếu agent báo hoàn thành
    if isinstance(last_message, AIMessage) and "TASK_COMPLETED" in last_message.content:
        return "reflect"
        
    # Nếu hết lượt
    if state["iteration"] >= state["max_iterations"]:
        return "reflect"
        
    # Default thì quay lại agent
    return "agent"

# 4. Reflection Node (Lưu Bài Học)
def reflect_node(state: SimulatorState):
    print("\n--- REFLECTION ---")
    messages = state["messages"]
    last_message = messages[-1]
    
    success = "TASK_COMPLETED" in last_message.content if isinstance(last_message, AIMessage) else False
    
    reflection = f"Kết quả: {'THÀNH CÔNG' if success else 'THẤT BẠI'}\n"
    reflection += f"Số lần thử: {state['iteration']}\n"
    reflection += "Bài học rút ra: " + (last_message.content if isinstance(last_message, AIMessage) else "Không có")
    
    # Lưu reflection xuống đĩa
    log_dir = root_dir / "logs" / "execution_simulator"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    with open(log_dir / f"reflection_{os.path.basename(state['target_file'])}.txt", "w", encoding="utf-8") as f:
        f.write(reflection)
        
    return {"is_success": success, "reflection": reflection}

# Build Graph
builder = StateGraph(SimulatorState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(EXECUTION_TOOLS))
builder.add_node("reflect", reflect_node)

builder.set_entry_point("agent")
builder.add_conditional_edges("agent", should_continue, ["tools", "reflect", "agent"])
builder.add_edge("tools", "agent")
builder.add_edge("reflect", END)

graph = builder.compile()

# Test runner
def run_simulator(task: str, target_file: str, max_iterations: int = 10):
    initial_state = {
        "messages": [HumanMessage(content=f"Hãy thực thi và sửa lỗi file: {target_file}")],
        "task": task,
        "target_file": target_file,
        "iteration": 0,
        "max_iterations": max_iterations,
        "is_success": False,
        "reflection": ""
    }
    
    final_state = graph.invoke(initial_state)
    print("\n\n=== KẾT QUẢ CUỐI CÙNG ===")
    print(final_state["reflection"])
    return final_state
