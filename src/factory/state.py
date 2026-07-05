from typing import TypedDict, List, Tuple

class FactoryState(TypedDict):
    """
    Trạng thái trung tâm cho Hệ thống AI Software Factory.
    Lưu trữ toàn bộ thông tin từ khâu lên ý tưởng, code, test, đến QA và sửa lỗi.
    """
    request_id: str
    project_path: str
    project_name: str
    user_requirement: str
    product_requirements_document: str
    mode: str
    
    # --- Coding Phase ---
    planned_architecture_ptr: str  # Trỏ tới file (Disk)
    draft_code_ptr: str            # Trỏ tới file
    
    # --- Testing Phase ---
    test_results_ptr: str          # Trỏ tới file log
    performance_metrics_ptr: str   # Trỏ tới file json
    
    # --- QA Phase ---
    qa_report_ptr: str             # Trỏ tới file md
    qa_score: float                # Giữ nguyên vì là số (nhẹ)
    
    # --- Fix Phase ---
    fix_plan_ptr: str              # Trỏ tới file md
    
    # --- JIT Phase & Overlord ---
    request: str                   # Tóm tắt siêu ngắn (< 100 chữ)
    constitution_ptr: str          # Trỏ tới constitution.md
    code_context: str              # Context JIT siêu mỏng (<= 3 chunks)
    selected_workflow: str         # Route Enum
    available_tools: List[str]     # JIT Tools schemas list
    complexity: str                # LOW, MEDIUM, HIGH
    recommended_model: str         # Tên model được đề xuất
    
    plan_ptr: str                  # Trỏ tới plan.md
    critique_ptr: str              # Trỏ tới critique.md
    revision_count: int            # Cầu dao chống lặp
    response: str                  # Final response

class DebateState(TypedDict):
    """
    Trạng thái cho workflow "Hội đồng Phản biện AI".
    """
    file_path: str
    file_content: str
    debate_history: List[Tuple[str, str]]
    action_plan: str
