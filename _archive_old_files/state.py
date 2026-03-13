from typing import TypedDict

class AgentState(TypedDict):
    """
    Quản lý trạng thái chung của hệ thống Agents trong quá trình xử lý.
    """
    task: str              # Yêu cầu gốc của bài toán
    csv_info: str          # Cấu trúc của file dữ liệu
    plan: str              # Kế hoạch tổng thể do Planner tạo
    architecture: str      # Thiết kế kỹ thuật chi tiết của Architect
    draft: str             # Code Python do Worker sinh ra
    execution_log: str     # Kết quả chạy code hoặc lỗi từ Worker
    review_feedback: str   # Đánh giá của Reviewer
    revision_count: int    # Số lần chỉnh sửa để chống lặp vô hạn
    error_log_path: str    # Đường dẫn tới file error_log.md để ghi log lỗi
    summary_history: str   # Tóm tắt lịch sử các lỗi để tránh tràn bộ nhớ
