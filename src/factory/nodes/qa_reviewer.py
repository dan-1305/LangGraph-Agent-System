import os
import re
from pathlib import Path
from typing import Dict, Any

from langchain_core.messages import HumanMessage
from src.factory.state import FactoryState
from src.factory.tools.file_tools import list_project_files, read_file_content
from src.factory.tools.vision_tools import extract_video_frames_base64
from src.factory.config import create_fallback_chain
from src.token_tracker import track_llm_usage

class QAReviewer:
    """
    Sub-system chuyên trách thực hiện QA (Quality Assurance) cho các dự án.
    Đây là phiên bản tích hợp (migration) từ ai_qa_agent cũ.
    """

    def __init__(self) -> None:
        """Khởi tạo các mô hình LLM với Load Balancing."""
        flash_model_list = ["gemini-3-flash-preview", "gemini-2.5-flash"]
        pro_model_list = ["gemini-3.1-pro-preview", "gemini-3-pro-preview", "gemini-2.5-pro"]
        
        self.llm_flash = create_fallback_chain(flash_model_list, temperature=0.2, max_tokens=2048)
        self.llm_pro = create_fallback_chain(pro_model_list, temperature=0.2, max_tokens=4096)

    async def evaluate(self, project_path: str, test_results: str) -> str:
        """Chạy tuần tự các bước kiểm tra và trả về báo cáo cuối cùng."""
        print(f"Dang quet cau truc project: {project_path}")
        tree = list_project_files(project_path, max_depth=3)
        
        # 1. Code Review
        print("[Code Reviewer] Dang phan tich ma nguon...")
        sample_code = ""
        count = 0
        path = Path(project_path)
        for p in path.rglob("*.py"):
            if "venv" in str(p) or "__pycache__" in str(p) or "node_modules" in str(p): continue
            sample_code += f"\n--- File: {p.name} ---\n"
            sample_code += read_file_content(str(p))
            count += 1
            if count >= 3:
                break
        code_prompt = f"Cấu trúc:\n{tree}\nCode mẫu:\n{sample_code}\nĐánh giá chất lượng (PEP8, Type Hint, Docstring)."
        code_resp = await self.llm_flash.ainvoke(code_prompt)
        
        # 2. Architecture
        print("[Architecture Critic] Dang danh gia kien truc...")
        arch_prompt = f"Cấu trúc:\n{tree}\nĐánh giá kiến trúc thư mục, file cấu hình."
        arch_resp = await self.llm_flash.ainvoke(arch_prompt)
        
        # 3. Performance
        print("[Performance Analyst] Dang tim kiem bao cao hieu suat...")
        perf_data = ""
        for p in path.rglob("*.md"):
            if "REPORT" in p.name.upper() or "SUMMARY" in p.name.upper():
                perf_data += read_file_content(str(p))[:4000]
                break
        if not perf_data:
            perf_data = "Không tìm thấy dữ liệu hiệu suất."
        perf_prompt = f"Tài liệu hiệu suất:\n{perf_data}\nPhân tích và đánh giá hiệu suất dự án."
        perf_resp = await self.llm_flash.ainvoke(perf_prompt)
        
        # 4. Product Review
        print("[Product Reviewer] Dang danh gia san pham (Video/Images)...")
        video_files = list(path.rglob("*.mp4"))
        prod_report = "Không tìm thấy file video."
        if video_files:
            print(f"   -> Tìm thấy video: {video_files[0].name}")
            frames = extract_video_frames_base64(str(video_files[0]), 3)
            if frames:
                content = [{"type": "text", "text": "Đánh giá chất lượng video dựa trên các khung hình này (tỷ lệ, phụ đề, thẩm mỹ)."}]
                for frame in frames:
                    content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{frame}"}})
                try:
                    prod_resp = await self.llm_flash.ainvoke([HumanMessage(content=content)])
                    prod_report = prod_resp.content
                except Exception as e:
                    prod_report = f"Lỗi Vision AI: {e}"
        
        # 5. Tổng hợp
        print("[Chief QA Manager] Dang tong hop bao cao...")
        from datetime import datetime
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        final_prompt = f"""Bạn là Giám đốc QA. Hôm nay là {current_date}.
Báo cáo:
1. Code Review: {code_resp.content}
2. Architecture: {arch_resp.content}
3. Performance: {perf_resp.content}
4. Product: {prod_report}
5. Kết quả Test (PyTest):
{test_results}

Hãy tổng hợp BÁO CÁO QA TOÀN DIỆN bằng Tiếng Việt.
LUẬT CHẤM ĐIỂM NGHIÊM NGẶT CỦA CÔNG TY:
- Nếu 'Kết quả Test' báo FAILED hoặc có Stack Trace báo lỗi, ĐIỂM TỐI ĐA CHỈ ĐƯỢC 4/10.
- Nếu 'Kết quả Test' phát hiện code test lùa gà (chỉ dùng assert True mà không test logic thật) hoặc không có test, ĐÁNH TRƯỢT VỀ 0/10.
- Chỉ khi PyTest PASSED đàng hoàng và code có Type Hinting + Docstrings đầy đủ thì mới được phép cho trên 8.0/10.

Bắt buộc có cấu trúc:
# BÁO CÁO QA PROJECT: {Path(project_path).name}
**Ngày lập báo cáo:** {current_date}
## 1. Điểm đánh giá tổng quan (Trên thang 10)
## 2. Nhận xét Kiến trúc & Code Quality
## 3. Đánh giá Hiệu suất & Sản phẩm đầu ra
## 4. Chi tiết Lỗi PyTest (Nếu có)
## 5. Các vấn đề nghiêm trọng
## 6. Đề xuất hành động
"""
        final_resp = await self.llm_pro.ainvoke(final_prompt)
        return final_resp.content

def extract_score(report: str) -> float:
    """Trích xuất điểm số từ báo cáo."""
    matches = re.findall(r'([0-9.]+)\s*/\s*10', report)
    if matches:
        try:
            return float(matches[-1])
        except ValueError:
            pass
    return 0.0

async def qa_node(state: FactoryState) -> Dict[str, Any]:
    print("\n=======================================================")
    print(f"[QA Node] Dang soi loi ma nguon va cham diem...")
    
    project_path = state.get("project_path", "")
    test_results = state.get("test_results", "Không có dữ liệu test.")
    
    if not project_path:
        return {"qa_report_summary": "Error: project_path is empty", "qa_score": 0.0}
        
    reviewer = QAReviewer()
    report = await reviewer.evaluate(project_path, test_results)
    score = extract_score(report)
    
    print(f"Bao cao QA hoan tat! Diem: {score}/10")
    
    # Ghi báo cáo ra file cho Dashboard đọc
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    project_name = Path(project_path).name
    report_file = reports_dir / f"QA_{project_name}.md"
    try:
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)
    except Exception as e:
        print(f"⚠️ Khong the ghi file bao cao QA: {e}")

    return {
        "qa_report_summary": report,
        "qa_score": score
    }
