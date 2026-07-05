import sys
from pathlib import Path
import json

# Thêm Root Path vào PYTHONPATH để import được các module của dự án
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.factory.workflows.daily_health_loop import build_daily_health_graph
from src.base_agent import BaseAgent

class ContextDelegatorAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)
        
    def _ai_handler(self, log_data: str) -> str:
        prompt = f"""
[ROLE: TRIAGE DIRECTOR / CONTEXT DELEGATOR]
Nhiệm vụ: Bạn vừa nhận được log của 5 lần chạy thử vòng lặp CI/CD "The Self-Evolving Daily Loop".
Thay vì để hệ thống tải toàn bộ dữ liệu này vào bộ nhớ của Cline, hãy tóm tắt nó thành một file Markdown siêu ngắn gọn.
Đánh giá:
1. Có điểm nào bất thường không? (Warden có bắt được lỗi không? Architect đề xuất có hợp lý không?)
2. Độ ổn định của 5 vòng lặp.

Logs (5 loops):
{log_data}

Trả về định dạng JSON chứa 1 trường 'summary' (nội dung Markdown hoàn chỉnh).
"""
        response = self._call_llm(prompt, is_json=True)
        parsed = self._parse_json_response(response)
        if parsed and "summary" in parsed:
            return parsed["summary"]
        return "# Lỗi phân tích GCLI Delegation."

    def _logic_handler(self, log_data: str) -> str:
        return "# Logic Fallback: Không thể kết nối Gemini để tóm tắt."

def main():
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    print("🚀 Bắt đầu giả lập 5 vòng lặp The Self-Evolving Daily Loop...")
    graph = build_daily_health_graph()
    
    collected_logs = []
    
    for i in range(1, 6):
        print(f"\n--- VÒNG LẶP THỨ {i} ---")
        initial_state = {
            "health_report": "",
            "improvement_proposal": "",
            "warden_decision": "",
            "patch_success": False,
            "test_success": False
        }
        
        # Chạy Graph
        final_state = graph.invoke(initial_state)
        
        # Gom nhặt log
        loop_log = {
            "loop_num": i,
            "architect_proposal": final_state.get("improvement_proposal"),
            "warden_decision": final_state.get("warden_decision"),
            "patch_success": final_state.get("patch_success")
        }
        collected_logs.append(loop_log)
    
    print("\n🧠 Kích hoạt GCLI Delegation (Gemini 3.1 Pro Preview) để phân tích sâu...")
    delegator = ContextDelegatorAgent()
    summary_markdown = delegator.execute(log_data=json.dumps(collected_logs, indent=2))
    
    # Đảm bảo thư mục reports tồn tại
    reports_dir = Path(__file__).resolve().parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    report_path = reports_dir / "daily_health_test_results.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(summary_markdown)
        
    print(f"✅ Đã lưu kết quả phân tích siêu ngắn gọn tại: {report_path}")
    print("💡 Cline có thể gọi 'read_file' để đọc file trên thay vì đọc log khổng lồ.")

if __name__ == "__main__":
    main()
