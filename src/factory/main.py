
import time
import io
import contextlib
import sys
from pathlib import Path

# Setup Path để đảm bảo root được nhận diện
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

# Ironclad Safeguard (MỐC 15): Dọn dẹp Git State trước khi chạy LangGraph
try:
    from tools.system.git_manager import GitManager
    GitManager.ensure_clean_state()
except ImportError as e:
    print(f"⚠️ Warning: Could not run Ironclad Safeguard. {e}")

from langgraph.graph import StateGraph, END
from src.factory.state import FactoryState
from src.factory.nodes.router_agent import router_node
from src.factory.nodes.qa_agent import qa_node

# --- Mock Nodes cho các module chưa hoàn thiện ---
def product_ba_node(state: FactoryState):
    print("--- [Mock] Product BA Kích hoạt ---")
    return state

def overlord_graph(state: FactoryState):
    print("--- [Mock] Overlord Kích hoạt ---")
    return state

def production_graph(state: FactoryState):
    print("--- [Mock] Software Production Kích hoạt ---")
    return state

def debate_graph(state: FactoryState):
    print("--- [Mock] Debate Graph Kích hoạt ---")
    return state
# -----------------------------------------------

def primary_router(state: FactoryState) -> str:
    """
    Lớp bảo vệ đầu tiên: Phân luồng ngay từ đầu để tránh nhét rác vào Overlord.
    """
    route = state.get("selected_workflow", "ROUTE_NORMAL")
    if route == "ROUTE_RAG":
        print("--- MetaGraph: Nhảy sang luồng Tra cứu RAG (QA Agent) ---")
        return "ROUTE_RAG"
    elif route == "ROUTE_LOGS":
        print("--- MetaGraph: Nhảy sang luồng Đọc Logs/Sửa lỗi ---")
        return "ROUTE_LOGS"
    elif route == "ROUTE_WORKFLOW":
        print("--- MetaGraph: Nhảy sang luồng AI Workflow Agent ---")
        return "ROUTE_WORKFLOW"
    else:
        print("--- MetaGraph: Nhảy sang luồng Sản xuất cốt lõi (Overlord) ---")
        return "ROUTE_NORMAL"

def route_to_workflow(state: FactoryState) -> str:
    """
    Routes to the appropriate sub-workflow based on the Overlord's decision.
    """
    selected_workflow = state.get("selected_workflow", "software_production")
    
    # Circuit Breaker: Kiểm tra xem đã vượt quá số lần retry cho phép chưa
    retry_count = state.get("revision_count", 0)
    MAX_RETRIES = 2
    if retry_count >= MAX_RETRIES:
        print(f"--- 🛑 CIRCUIT BREAKER TRIPPED ---")
        print(f"Sub-agent đã vượt quá giới hạn retry ({MAX_RETRIES} lần). Ngừng ép buộc để tránh infinite loop.")
        return "halt_execution"
        
    print(f"--- MetaGraph Router: Routing to '{selected_workflow}' workflow ---")
    if "debate" in selected_workflow:
        return "scientific_debate"
    return "software_production"

def post_prd_update(state: FactoryState):
    """
    Update state after PRD generation.
    This function will be a node that follows product_ba_node.
    """
    print("--- State Updater: Updating state with PRD ---")
    prd = state.get("product_requirements_document")
    if prd:
        state["request"] = prd
    print(f"DEBUG: State keys after update: {state.keys()}")
    return state

# --- Khai báo Node Mới cho Codebase Audit Pipeline ---
from src.factory.nodes.architecture_critic import architecture_critic_node
from projects.project_manager_sentry.manager_agent import ProjectManagerAgent

def project_manager_node(state: FactoryState):
    print("--- [Project Manager] Kích hoạt ---")
    pm = ProjectManagerAgent()
    # Mock logic Báo cáo tổng hợp
    report = f"✅ Báo cáo Audit Dự án {state.get('project_name')}\n"
    report += f"Path: {state.get('project_path')}\n"
    report += f"Kết quả từ Architecture Critic & QA Agent đã được ghi nhận."
    state["response"] = report
    return state
# ----------------------------------------------------

def build_meta_graph():
    """
    Builds the main "meta-graph" that orchestrates all other workflows.
    Bao gồm tích hợp luồng Codebase Audit Pipeline.
    """
    meta_graph = StateGraph(FactoryState)

    meta_graph.add_node("semantic_router", router_node)
    meta_graph.add_node("product_ba", product_ba_node)
    from src.factory.nodes.context_manager import context_manager_node
    meta_graph.add_node("context_manager", context_manager_node)
    from src.factory.nodes.principles_gate import principles_gate_node
    meta_graph.add_node("principles_gate", principles_gate_node)
    meta_graph.add_node("qa_agent", qa_node)
    meta_graph.add_node("architecture_critic", architecture_critic_node)
    meta_graph.add_node("project_manager", project_manager_node)
    meta_graph.add_node("update_state_with_prd", post_prd_update)
    meta_graph.add_node("overlord", overlord_graph)
    meta_graph.add_node("software_production", production_graph)
    meta_graph.add_node("scientific_debate", debate_graph)
    
    meta_graph.set_entry_point("semantic_router")
    
    meta_graph.add_edge("semantic_router", "context_manager")
    
    # Conditional Edges mới: Sau khi lấy Context, chia nhánh theo yêu cầu
    def context_router(state: FactoryState):
        route = state.get("selected_workflow", "ROUTE_NORMAL")
        # Nhánh mới cho Use-case Codebase Audit
        if route == "ROUTE_CODEBASE_AUDIT":
            return "ROUTE_CODEBASE_AUDIT"
        return "ROUTE_NORMAL"

    meta_graph.add_conditional_edges(
        "context_manager",
        context_router,
        {
            "ROUTE_CODEBASE_AUDIT": "architecture_critic",
            "ROUTE_NORMAL": "principles_gate"
        }
    )

    # --- Pipeline cho Codebase Audit & Auto-Remediation ---
    from src.factory.nodes.remediation_agent import remediation_node
    from src.factory.nodes.sandbox_validator import sandbox_validator_node
    from src.factory.nodes.patch_generator import git_patch_node
    
    meta_graph.add_node("remediation_agent", remediation_node)
    meta_graph.add_node("sandbox_validator", sandbox_validator_node)
    meta_graph.add_node("patch_generator", git_patch_node)
    
    meta_graph.add_edge("architecture_critic", "qa_agent")
    
    # QAAgent xuất report xong, thay vì báo cáo thẳng, giờ chuyển cho Kỹ sư sửa lỗi
    meta_graph.add_edge("qa_agent", "remediation_agent")
    meta_graph.add_edge("remediation_agent", "sandbox_validator")
    
    # Vòng lặp Sandbox - Remediation (Loop Breaker tích hợp)
    def sandbox_router(state: FactoryState):
        if state.get("sandbox_success", False):
            return "SUCCESS"
            
        # Circuit Breaker: Kiểm tra xem đã vượt quá số lần retry cho phép chưa
        retry_count = state.get("revision_count", 0)
        MAX_RETRIES = int(os.getenv("AGENT_MAX_REMEDIATION_LOOPS", "2"))
        if retry_count >= MAX_RETRIES:
            print(f"--- 🛑 CIRCUIT BREAKER TRIPPED ---")
            print(f"SandboxValidator đã Fail {MAX_RETRIES} lần. Dừng lặp, xuất patch thô.")
            return "SUCCESS" # Buộc đi tiếp để xuất report
            
        print("--- ⚠️ Sandbox Failed. Đẩy lại cho RemediationAgent sửa... ---")
        return "RETRY"

    meta_graph.add_conditional_edges(
        "sandbox_validator",
        sandbox_router,
        {
            "SUCCESS": "patch_generator",
            "RETRY": "remediation_agent"
        }
    )
    
    meta_graph.add_edge("patch_generator", "project_manager")
    meta_graph.add_edge("project_manager", END)
    # -----------------------------------

    meta_graph.add_conditional_edges(
        "principles_gate",
        primary_router,
        {
            "ROUTE_RAG": "qa_agent", # Trả lời RAG ngay lập tức rồi kết thúc
            "ROUTE_LOGS": END, # Tạm thời end (sẽ nối tới luồng Auto-Fixer sau)
            "ROUTE_NORMAL": "product_ba"
        }
    )
    
    meta_graph.add_edge("product_ba", "update_state_with_prd")
    meta_graph.add_edge("update_state_with_prd", "overlord")

    meta_graph.add_conditional_edges(
        "overlord",
        route_to_workflow,
        {
            "software_production": "software_production",
            "scientific_debate": "scientific_debate",
            "halt_execution": END
        }
    )

    meta_graph.add_edge("software_production", END)
    meta_graph.add_edge("scientific_debate", END)
    
    return meta_graph

async def main(mode="new", project_name="LangGraph_Agent_System", user_requirement="", file_path=""):
    print("==================================================")
    print("AI SOFTWARE FACTORY - META-GRAPH")
    print("==================================================")
    
    meta_graph = build_meta_graph()
    app = meta_graph.compile()

    print("--- Running AI Factory ---")
    print(f"Mode: {mode}")
    print(f"Project: {project_name}")
    print(f"Request: {user_requirement}\n")

    import uuid
    initial_state = {
        "user_requirement": user_requirement,
        "product_requirements_document": "",
        "file_path": file_path if file_path else str(Path.cwd()),
        "project_name": project_name,
        "mode": mode,
        "request_id": str(uuid.uuid4()),
        "project_path": str(Path.cwd() / "projects" / project_name),
        "planned_architecture_ptr": "",
        "draft_code_ptr": "",
        "test_results_ptr": "",
        "performance_metrics_ptr": "",
        "qa_report_ptr": "",
        "qa_score": 0.0,
        "fix_plan_ptr": "",
        "request": "",
        "constitution_ptr": "",
        "code_context": "",
        "selected_workflow": "",
        "available_tools": [],
        "plan_ptr": "",
        "critique_ptr": "",
        "revision_count": 0,
        "response": "",
    }

    print("Invoking Factory Graph...\n")
    
    report_output = io.StringIO()
    with contextlib.redirect_stdout(report_output):
        config = {"recursion_limit": 150}
        
        try:
            final_state = await app.ainvoke(initial_state, config)
            print("\n--- META-GRAPH RUN COMPLETE! ---")
            print("Final workflow execution has finished.")
        except Exception as e:
            print(f"\nAn error occurred: {e}")

    # --- Save and Print Report ---
    report_path = Path("reports") / f"factory_run_{mode}_{time.strftime('%Y%m%d_%H%M%S')}.md"
    report_path.parent.mkdir(exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🎓 AI Factory - Execution Report\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Mode:** `{mode}`\n")
        f.write(f"**Project:** `{project_name}`\n")
        f.write(f"**Request:** `{user_requirement}`\n\n")
        f.write("---\n\n")
        f.write("## Full Execution Log\n\n")
        f.write("```log\n")
        f.write(report_output.getvalue())
        f.write("\n```\n")
    
    print(f"\n\nReport saved to {report_path}")
    print("\n--- Test Run Summary ---")
    print(report_output.getvalue())


if __name__ == "__main__":
    import asyncio
    import argparse
    
    parser = argparse.ArgumentParser(description="Run AI Factory")
    parser.add_argument("--mode", type=str, default="new", help="Mode: new, qa_only, debate")
    parser.add_argument("--project", type=str, default="LangGraph_Agent_System", help="Project name")
    parser.add_argument("--req", type=str, default="", help="User requirement")
    parser.add_argument("--file", type=str, default="", help="File path for debate mode")
    
    args = parser.parse_args()
    asyncio.run(main(mode=args.mode, project_name=args.project, user_requirement=args.req, file_path=args.file))
