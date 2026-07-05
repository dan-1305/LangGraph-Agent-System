import os
import sys
import datetime
from typing import TypedDict, List, Annotated
from pathlib import Path

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Thiết lập đường dẫn root
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from src.factory.config import create_fallback_chain
from projects.real_execution_simulator.tools import execute_terminal_command, read_file_content

# --- TOOLS THÊM CHO CEO ---
from langchain_core.tools import tool

@tool
def list_files_in_directory(directory_path: str = ".") -> str:
    """Liệt kê các file trong một thư mục cụ thể để CEO có thể khám phá dự án."""
    try:
        abs_path = os.path.join(root_dir, directory_path)
        if not os.path.exists(abs_path):
            return f"Lỗi: Không tìm thấy thư mục {directory_path}"
        files = os.listdir(abs_path)
        return f"Các file trong {directory_path}:\n" + "\n".join(files)
    except Exception as e:
        return f"Lỗi: {str(e)}"

@tool
def read_ceo_lore() -> str:
    """Đọc file bộ nhớ dài hạn (Long-term Memory) của CEO để nhớ lại các bài học cũ."""
    lore_path = os.path.join(root_dir, "logs", "CEO_LORE.md")
    if not os.path.exists(lore_path):
        return "CEO Lore chưa có dữ liệu. Đây là ngày huấn luyện đầu tiên."
    with open(lore_path, "r", encoding="utf-8") as f:
        return f.read()

@tool
def summon_agent(agent_role: str, task_description: str) -> str:
    """Triệu hồi (Summon) một Agent khác (ví dụ QA_Auditor, Code_Reviewer, Trader) để nhờ phân tích/làm giúp một task. Trả về kết quả của Agent đó."""
    print(f"\n[Multi-Agent] CEO đang triệu hồi {agent_role} để thực hiện: {task_description}")
    
    # Ở đây chúng ta giả lập phản hồi nhanh của Agent con bằng LLM để tránh chuỗi đệ quy (Recursive call) gây sập hệ thống
    llm = create_fallback_chain(["label:tier-2"], temperature=0.3)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Bạn là {role}. Sếp của bạn (CEO) vừa giao cho bạn nhiệm vụ: {task}. Hãy đưa ra phản hồi/báo cáo của bạn dựa trên kiến thức hiện tại của mình."),
    ])
    chain = prompt | llm
    result = chain.invoke({"role": agent_role, "task": task_description})
    return f"Báo cáo từ {agent_role}: {result.content}"

CEO_TOOLS = [execute_terminal_command, read_file_content, list_files_in_directory, read_ceo_lore, summon_agent]

# --- STATE ĐỊNH NGHĨA ---
class CEOTrainingState(TypedDict):
    messages: Annotated[List[BaseMessage], "add_messages"]
    epoch: int
    max_epochs: int
    daily_focus: str
    reflection: str

# --- NODE 1: THE CEO EXPLORATION ---
def ceo_node(state: CEOTrainingState):
    print(f"\n[CEO] Đang suy nghĩ (Epoch {state['epoch']}/{state['max_epochs']})...")
    
    if state["epoch"] >= state["max_epochs"]:
        return {"messages": [AIMessage(content="Đã kết thúc lượt huấn luyện hôm nay. Bắt đầu Reflection.")], "epoch": state["epoch"]}
        
    system_prompt = """Bạn là CEO của LangGraph Agent System.
Hôm nay là: {current_date}
Mục tiêu huấn luyện hôm nay (Daily Focus): {daily_focus}

NHIỆM VỤ CỦA BẠN:
1. Bạn đang sống trong môi trường thực. Bạn có các tool để gõ Terminal (execute_terminal_command), đọc code (read_file_content), và khám phá thư mục (list_files_in_directory).
2. MULTI-AGENT TEAMING: Bạn có quyền gọi tool `summon_agent` để hỏi ý kiến các Agent khác (như Code_Reviewer, QA_Auditor) về chất lượng file code trước khi chạy.
3. Hãy tự do vọc vạch thư mục dự án tương ứng với mục tiêu hôm nay. Ví dụ: Nếu mục tiêu là Auto Affiliate Video, hãy tìm file trong thư mục projects/auto_affiliate_video và thử chạy nó (bằng .venv\Scripts\python.exe).
4. Nếu chạy gặp lỗi, hãy đọc code, tìm hiểu lý do tại sao lỗi.
5. Khi bạn cảm thấy đã thu thập đủ dữ liệu và hiểu được cách vận hành hoặc nguyên nhân lỗi của project đó, hãy output chính xác từ: "TRAINING_COMPLETED" và tóm tắt ngắn gọn.

QUAN TRỌNG: Hãy luôn gọi tool read_ceo_lore trước khi làm để tránh lặp lại sai lầm ngày hôm qua.
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    # Dùng model xịn cho CEO (nhưng ánh xạ qua proxy để tiết kiệm)
    llm = create_fallback_chain(["label:tier-2"], temperature=0.5)
    llm_with_tools = llm.bind_tools(CEO_TOOLS)
    
    chain = prompt | llm_with_tools
    
    response = chain.invoke({
        "current_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "daily_focus": state["daily_focus"],
        "messages": state["messages"]
    })
    
    return {"messages": [response], "epoch": state["epoch"] + 1}

# --- NODE 2: CONDITIONAL ROUTING ---
def ceo_router(state: CEOTrainingState):
    last_message = state["messages"][-1]
    
    if hasattr(last_message, 'tool_calls') and len(last_message.tool_calls) > 0:
        return "tools"
        
    if isinstance(last_message, AIMessage) and "TRAINING_COMPLETED" in last_message.content:
        return "reflect"
        
    if state["epoch"] >= state["max_epochs"]:
        return "reflect"
        
    return "ceo"

# --- NODE 3: LONG-TERM MEMORY (LORE) ---
def reflect_node(state: CEOTrainingState):
    print("\n[CEO] Đang viết nhật ký vào Long-term Memory (CEO_LORE.md)...")
    messages = state["messages"]
    
    # Trích xuất nội dung từ toàn bộ các bước để tạo reflection
    summary_prompt = ChatPromptTemplate.from_messages([
        ("system", "Bạn là một AI thông minh. Dựa vào cuộc hội thoại sau, hãy tóm tắt BÀI HỌC RÚT RA (Những cái gì chạy được, cái gì lỗi, làm sao để chạy đúng) trong vòng 3-5 gạch đầu dòng. Điều này sẽ được lưu vào não bộ vĩnh viễn của CEO để ngày mai chạy auto."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    llm = create_fallback_chain(["label:tier-2"], temperature=0.1)
    chain = summary_prompt | llm
    reflection_msg = chain.invoke({"messages": messages})
    
    lore_path = os.path.join(root_dir, "logs", "CEO_LORE.md")
    
    # Ghi đè hoặc append vào Lore
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lore_entry = f"\n\n### [{timestamp}] Focus: {state['daily_focus']}\n{reflection_msg.content}\n"
    
    with open(lore_path, "a", encoding="utf-8") as f:
        f.write(lore_entry)
        
    return {"reflection": reflection_msg.content}

# --- GRAPH BUILDER ---
builder = StateGraph(CEOTrainingState)

builder.add_node("ceo", ceo_node)
builder.add_node("tools", ToolNode(CEO_TOOLS))
builder.add_node("reflect", reflect_node)

builder.set_entry_point("ceo")
builder.add_conditional_edges("ceo", ceo_router, ["tools", "reflect", "ceo"])
builder.add_edge("tools", "ceo")
builder.add_edge("reflect", END)

ceo_training_graph = builder.compile()

# --- MAIN RUNNER ---
def run_nightly_training(focus_topic: str):
    print("="*60)
    print("🌙 KHỞI ĐỘNG CEO NIGHTLY TRAINING MATRIX 🌙")
    print(f"Mục tiêu huấn luyện đêm nay: {focus_topic}")
    print("="*60)
    
    initial_state = {
        "messages": [HumanMessage(content="Hệ thống đã bắt đầu. Ngài hãy khởi động quá trình học nghiệm.")],
        "epoch": 0,
        "max_epochs": 3,  # Giảm xuống 3 để tránh ngốn API Free Tier và treo hệ thống
        "daily_focus": focus_topic,
        "reflection": ""
    }
    
    final_state = ceo_training_graph.invoke(initial_state)
    print("\n\n✅ KẾT QUẢ HUẤN LUYỆN (ĐÃ LƯU VÀO LORE):")
    print(final_state["reflection"])

if __name__ == "__main__":
    # Test thử một chủ đề
    run_nightly_training("Khám phá cách chạy Auto Affiliate Video và xử lý lỗi nếu có")
