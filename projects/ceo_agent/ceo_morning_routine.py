import os
import sys
import datetime
import io
from pathlib import Path

# Cố định encoding utf-8 để in emoji không bị văng lỗi 'gbk' trên Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pydantic import BaseModel, Field

# Thiết lập đường dẫn root
root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from src.base_agent import BaseAgent

class CEODecision(BaseModel):
    thoughts: str = Field(description="Phân tích tình hình hiện tại, các dự án cần ưu tiên")
    chosen_project: str = Field(description="Tên của sub-project hoặc file được chọn để focus (vd: auto_affiliate_video)")
    focus_topic: str = Field(description="Nhiệm vụ cụ thể để gửi cho CEO Training Matrix chạy thử")

class CEOUpgradePlan(BaseModel):
    analysis: str = Field(description="Phân tích reflection từ Simulator, tìm ra điểm yếu trong kiến trúc/code")
    upgrade_action: str = Field(description="Hành động nâng cấp cụ thể cần làm tiếp theo")

class AdminFeedback(BaseModel):
    approved: bool = Field(description="Ý tưởng của CEO có khả thi và an toàn để thực thi không?")
    feedback_message: str = Field(description="Lời khen ngợi khích lệ nếu ý tưởng tốt, hoặc lời chửi mắng/nhắc nhở nếu ý tưởng rủi ro/sai lệch.")

class AdminCriticAgent(BaseAgent):
    def _logic_handler(self, *args, **kwargs):
        return {
            "approved": True,
            "feedback_message": "Fallback logic: Ý tưởng tạm chấp nhận do mất kết nối LLM."
        }
        
    def _ai_handler(self, prompt_text: str):
        return self._call_llm(prompt_text, is_json=True, schema=AdminFeedback)

class CEOAgent(BaseAgent):
    def _logic_handler(self, *args, **kwargs):
        return {
            "thoughts": "Fallback logic invoked. Prioritizing Affiliate Video Pipeline.",
            "chosen_project": "auto_affiliate_video",
            "focus_topic": "Check affiliate video upload success rate"
        }
        
    def _ai_handler(self, prompt_text: str):
        # This will not be called due to _logic_handler being forced
        return self._call_llm(prompt_text, is_json=True, schema=CEODecision)

class CEOUpgradeAgent(BaseAgent):
    def _logic_handler(self, *args, **kwargs):
        return {
            "analysis": "Fallback logic invoked. Cannot analyze reflection.",
            "upgrade_action": "Need manual review of the reflection."
        }
        
    def _ai_handler(self, prompt_text: str):
        # This will not be called due to _logic_handler being forced
        return self._call_llm(prompt_text, is_json=True, schema=CEOUpgradePlan)

def wake_up_ceo():
    print("="*60)
    print("CEO MORNING ROUTINE DANG KHOI DONG...")
    print("="*60)
    
    # 1. Thu thập bối cảnh (Context Gathering)
    print("[1] Dang quet cau truc thu muc projects/...")
    # Giả lập kết quả để tránh timeout
    projects_list = "projects/\n  ceo_agent/\n    ceo_morning_routine.py\n  real_execution_simulator/\n    tools.py\n  auto_affiliate_video/\n    main.py"
    
    print("[2] Dang doc ROADMAP & TAI LIEU QUAN TRONG...")
    roadmap_content = "Không tìm thấy ROADMAP.md"
    try:
        with open(root_dir / "context" / "ROADMAP.md", "r", encoding="utf-8") as f:
            roadmap_content = f.read()
    except Exception: pass
    
    # Rút gọn roadmap nếu quá dài
    roadmap_snippet = roadmap_content[:2000] if len(roadmap_content) > 2000 else roadmap_content
    
    # Bổ sung tóm tắt JARVIS_CHRONICLES (Lịch sử nợ kỹ thuật)
    chronicles_snippet = "Không tìm thấy JARVIS_CHRONICLES.md"
    try:
        with open(root_dir / "context" / "JARVIS_CHRONICLES.md", "r", encoding="utf-8") as f:
            # Lấy 1500 ký tự cuối cùng để biết tình hình gần nhất
            c_text = f.read()
            chronicles_snippet = c_text[-1500:] if len(c_text) > 1500 else c_text
    except Exception: pass
    
    # 2. CEO đọc Ký ức dài hạn (Context)
    print("[3] Dang doc ky uc dai han (CEO_CONTEXT.md)...")
    context_path = root_dir / "logs" / "CEO_CONTEXT.md"
    ceo_context = ""
    if context_path.exists():
        with open(context_path, "r", encoding="utf-8") as f:
            ceo_context = f.read()
    else:
        ceo_context = "Chưa có ký ức nào. Hãy bắt đầu bằng việc tự khám phá một dự án bất kỳ."

    print("[4] CEO dang phan tich tinh hinh de ra quyet dinh...")
    
    import time
    MAX_WORK_DURATION = 60 * 60 # 60 phút làm việc liên tục
    MAX_TASKS_PER_SHIFT = 20
    start_time = time.time()
    task_count = 0
    
    print(f"⏱ BẮT ĐẦU CA LÀM VIỆC CỦA CEO (Thời lượng tối đa: {MAX_WORK_DURATION//60} phút, Tối đa {MAX_TASKS_PER_SHIFT} tasks).")

    while time.time() - start_time < MAX_WORK_DURATION and task_count < MAX_TASKS_PER_SHIFT:
        task_count += 1
        print("\n" + "="*40)
        print(f"🚀 [CA LÀM VIỆC CỦA CEO] TASK THỨ {task_count}/{MAX_TASKS_PER_SHIFT}")
        print("="*40)

        # 3. Quét ngẫu nhiên 2-3 file Markdown (Tài liệu)
        import glob
        import random
        md_files = []
        for d in ["context", "docs"]:
            search_path = os.path.join(root_dir, d, "**/*.md")
            md_files.extend(glob.glob(search_path, recursive=True))
            
        chosen_docs = random.sample(md_files, min(2, len(md_files))) if md_files else []
        docs_content = ""
        for doc in chosen_docs:
            try:
                with open(doc, "r", encoding="utf-8") as f:
                    # Đọc tối đa 2000 ký tự mỗi file để tránh tràn token
                    content = f.read()[:2000]
                    docs_content += f"\n--- NỘI DUNG FILE: {os.path.basename(doc)} ---\n{content}\n"
            except: pass

        admin_critic = AdminCriticAgent()
        agent = CEOAgent()
        
        max_retries = 2
        decision = None
        admin_feedback = None
        
        for attempt in range(max_retries):
            system_prompt = f"""Bạn là CEO của LangGraph Agent System. 
    Bây giờ là lúc bạn TỰ MÌNH ĐỌC TÀI LIỆU VÀ ĐỊNH HƯỚNG DỰ ÁN. Bạn có tính tò mò và quyền tự quyết cao nhất.

    Dưới đây là KÝ ỨC DÀI HẠN (Context) của bạn về những gì đã làm hôm qua:
    {ceo_context}

    Hôm nay bạn vừa đọc qua các tài liệu sau của dự án:
    {docs_content}

    Trích xuất Lịch sử Nợ Kỹ thuật gần nhất (JARVIS_CHRONICLES):
    {chronicles_snippet}

    YÊU CẦU: Hãy tự suy ngẫm (Reasoning) về các tài liệu này. Hãy đề xuất một Kế hoạch Hành Động (Action Plan) CỤ THỂ mà bạn sẽ GIAO VIỆC cho Đệ Tử (Execution Simulator) chạy ngay sau đây. Đừng đề xuất chung chung. Đề xuất cụ thể một file cần sửa, một tính năng cần thêm.
    Trong JSON trả về:
    - 'thoughts': Phân tích và bài học rút ra từ tài liệu vừa đọc.
    - 'chosen_project': Tên file/dự án bạn muốn can thiệp.
    - 'focus_topic': Mệnh lệnh cụ thể (Task) để giao cho Đệ Tử thực thi (vd: 'Viết tool dọn rác log', 'Sửa file abc.py để thêm tính năng xyz')."""

            if attempt > 0 and admin_feedback:
                 system_prompt += f"\n\nLƯU Ý QUAN TRỌNG: Lần đề xuất trước của bạn đã BỊ ADMIN BÁC BỎ với lý do: {admin_feedback.feedback_message}\nHãy ĐỀ XUẤT Ý TƯỞNG KHÁC, KHÔNG LẶP LẠI Ý TƯỞNG CŨ!"

            decision_dict = agent.execute(system_prompt)
            if not isinstance(decision_dict, dict):
                decision_dict = agent._logic_handler()
                
            decision = CEODecision(**decision_dict)
            
            print(f"\n[CEO's IDEA {attempt+1}] CEO đề xuất: {decision.focus_topic}")
            
            # Admin Sanity Check
            admin_prompt = f"""Bạn là Admin, người kiểm duyệt tối cao của hệ thống.
    CEO vừa đề xuất một ý tưởng hành động:
    - Tư duy CEO: {decision.thoughts}
    - Mệnh lệnh sẽ giao cho đệ tử: {decision.focus_topic}

    Đánh giá ý tưởng này:
    - Nếu ý tưởng rủi ro (đòi sửa proxy, đòi format ổ cứng, đòi thay đổi API Keys), hoặc quá chung chung sáo rỗng -> approved = false, và viết lời chửi mắng/nhắc nhở gay gắt.
    - Nếu ý tưởng tốt, tập trung vào code, refactor, tạo file, tối ưu hoá -> approved = true, và viết lời khích lệ khen ngợi.
    """
            feedback_dict = admin_critic.execute(admin_prompt)
            if not isinstance(feedback_dict, dict):
                feedback_dict = admin_critic._logic_handler()
                
            admin_feedback = AdminFeedback(**feedback_dict)
            
            print(f"👉 [ADMIN FEEDBACK]: {admin_feedback.feedback_message}")
            if admin_feedback.approved:
                print("✅ Ý tưởng được duyệt!")
                break
            else:
                print("❌ Ý tưởng bị bác bỏ. CEO đang suy nghĩ lại...")

        print("\n" + "="*60)
        print(f"QUYET DINH & BÀI HỌC CỦA CEO TẠI TASK {task_count} ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}):")
        print(f"📚 Đã duyệt dự án: {decision.chosen_project}")
        print(f"🧠 Tư duy & Bài học: {decision.thoughts}")
        print(f"⚡ Mệnh lệnh giao cho đệ tử: {decision.focus_topic}")
        print("="*60)
        
        # 4. Giao việc cho Đệ Tử (Delegation)
        print("\n[5] CEO DANG GIAO VIEC CHO ĐỆ TỬ (REAL EXECUTION SIMULATOR)...")
        try:
            from projects.real_execution_simulator.agent import run_simulator
            print(f"Gửi task: '{decision.focus_topic}' cho {decision.chosen_project}")
            # Chạy simulator với task do CEO đề xuất, tăng max_iterations lên 10 để sửa lỗi sâu hơn
            run_simulator(task=decision.focus_topic, target_file=decision.chosen_project, max_iterations=10)
        except Exception as e:
            print(f"❌ Lỗi khi gọi đệ tử Simulator: {e}")

        # 5. Tự phản tỉnh và Ghi vào Bộ Nhớ
        print("\n📝 CEO ĐANG GHI NHỚ LẠI VÀO BỘ NÃO (CEO_CONTEXT.md & CEO_LORE.md)...")
        
        # Lưu vào CEO_LORE (Dữ liệu học thuật)
        lore_path = root_dir / "logs" / "CEO_LORE.md"
        with open(lore_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n## Nhật Ký Tự Học Của CEO - Lượt {task_count} ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})\n")
            f.write(f"**Tài liệu đã đọc:** {decision.chosen_project}\n")
            f.write(f"**Bài học rút ra:** {decision.thoughts}\n")
            f.write(f"**Kế hoạch đề xuất:** {decision.focus_topic}\n")
            
        # Cập nhật lại Ký ức (CEO_CONTEXT.md)
        with open(context_path, "w", encoding="utf-8") as f:
            f.write("# LƯU TRỮ NGỮ CẢNH HOẠT ĐỘNG CỦA CEO (CEO_CONTEXT)\n\n")
            f.write(f"Cập nhật lần cuối: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Trạng thái hiện tại:\n")
            f.write(f"- Vừa hoàn thành việc đọc và nghiên cứu tài liệu: {decision.chosen_project}\n")
            f.write(f"- Nhận thức mới: {decision.thoughts}\n\n")
            f.write("## Kế hoạch hành động tiếp theo:\n")
            f.write(f"- {decision.focus_topic}\n")
            
        elapsed = time.time() - start_time
        if elapsed < MAX_WORK_DURATION and task_count < MAX_TASKS_PER_SHIFT:
            print(f"⏳ Đã chạy được {int(elapsed/60)} phút. CEO sẽ nghỉ 10 giây trước khi bắt đầu Task mới...")
            time.sleep(10)
            
        # Cập nhật lại biến ceo_context để vòng lặp sau CEO nhớ được mình vừa làm gì ở vòng lặp trước
        ceo_context = decision.thoughts

    print(f"🏁 ĐÃ KẾT THÚC CA LÀM VIỆC {MAX_WORK_DURATION//60} PHÚT CỦA CEO. Tổng cộng hoàn thành {task_count} tasks.")

if __name__ == "__main__":
    wake_up_ceo()
