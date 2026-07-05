import os
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from src.factory.state import FactoryState

# Import các nodes thực tế
from src.factory.nodes.planner import planner_node
from src.factory.nodes.coder import coder_node
from src.factory.nodes.tester import tester_node
from src.factory.nodes.qa_reviewer import qa_node
from src.factory.nodes.triage_director import triage_director_node
from src.factory.nodes.auto_fixer import auto_fixer_node
from src.factory.nodes.memory_manager import memory_manager_node

async def router_node(state: FactoryState) -> Dict[str, Any]:
    """Node định tuyến ban đầu dựa trên chế độ (mode)."""
    return {}

def route_start(state: FactoryState) -> str:
    if state.get("mode") == "qa_only":
        print("[Router] Che do QA_ONLY: Bo qua Planner & Coder, tien thang vao TESTER!")
        return "tester"
    print("[Router] Che do NEW: Bat dau tu Planner...")
    return "planner"

def check_qa_score(state: FactoryState) -> str:
    """Điều kiện lặp (Conditional Edge)."""
    score = state.get("qa_score", 0.0)
    rev_count = state.get("revision_count", 0)
    
    if score >= 8.0:
        print(f"Du an da dat chuan {score}/10! Hoan tat.")
        return "end"
    
    if rev_count >= 9:
        print("Da dat gioi han sua loi (9 lan). Dung he thong de tranh vong lap.")
        return "end"
        
    if rev_count > 0 and rev_count % 3 == 0:
        print(f"Da thu {rev_count} lan chua thanh cong. Chay Memory Manager de don dep log...")
        return "memory_manager"
        
    print(f"Diem moi dat {score}/10. Chuyen sang Giam doc de len ke hoach sua lai...")
    return "triage"

def build_factory_graph():
    """Khởi tạo toàn bộ dây chuyền sản xuất phần mềm khép kín."""
    workflow = StateGraph(FactoryState)
    
    # Thêm các khâu (Nodes)
    workflow.add_node("router", router_node)
    workflow.add_node("planner", planner_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("tester", tester_node)
    workflow.add_node("qa", qa_node)
    workflow.add_node("triage_director", triage_director_node)
    workflow.add_node("memory_manager", memory_manager_node)
    workflow.add_node("auto_fixer", auto_fixer_node)
    
    # Nối dây chuyền (Edges)
    workflow.set_entry_point("router")
    
    workflow.add_conditional_edges(
        "router",
        route_start,
        {
            "planner": "planner",
            "tester": "tester"
        }
    )
    
    workflow.add_edge("planner", "coder")
    workflow.add_edge("coder", "tester")
    workflow.add_edge("tester", "qa")
    
    # Conditional Edge sau bước QA
    workflow.add_conditional_edges(
        "qa",
        check_qa_score,
        {
            "end": END,
            "memory_manager": "memory_manager",
            "triage": "triage_director"
        }
    )
    
    workflow.add_edge("memory_manager", "triage_director")
    workflow.add_edge("triage_director", "auto_fixer")
    workflow.add_edge("auto_fixer", "tester") # Sửa xong quay lại test và QA
    
    return workflow.compile()
