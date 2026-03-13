from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from .state import AgentState
from .Node import planner_node, architect_node, worker_node, reviewer_node

def should_continue(state: AgentState) -> str:
    """
    Điều kiện rẽ nhánh: Kiểm tra xem có cần quay lại Architect để sửa lỗi không.
    """
    # CIRCUIT BREAKER: Nếu lặp quá 3 lần, tự động dừng để tránh tốn Token và lặp vô tận.
    if state.get("revision_count", 0) >= 3:
        print("\n[CIRCUIT BREAKER] Đã vượt quá 3 lần chỉnh sửa. Hệ thống tự động DỪNG lại để con người can thiệp.")
        return "end"

    # Nếu kết quả có chữ ERROR hoặc Reviewer chưa hài lòng thì bắt làm lại
    if "ERROR" in state["execution_log"] or "OK" not in state["review_feedback"][:20].upper():
        return "continue"
        
    return "end"

def create_workflow() -> StateGraph:
    """
    Tạo và cấu hình luồng chạy (workflow) cho LangGraph.
    
    Returns:
        StateGraph (đã compile): Workflow sẵn sàng để chạy.
    """
    # Khởi tạo bộ nhớ tạm
    memory = MemorySaver()
    
    workflow = StateGraph(AgentState)

    # Thêm các nút hành động
    workflow.add_node("planner", planner_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("worker", worker_node)
    workflow.add_node("reviewer", reviewer_node)

    # Thiết lập đường đi
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "architect")
    workflow.add_edge("architect", "worker")
    workflow.add_edge("worker", "reviewer")

    # Thêm logic rẽ nhánh có điều kiện
    workflow.add_conditional_edges(
        "reviewer",
        should_continue,
        {
            "continue": "architect",
            "end": END
        }
    )

    return workflow.compile(checkpointer=memory)
