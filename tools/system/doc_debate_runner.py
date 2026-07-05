import sys
from pathlib import Path

# Add root to pythonpath
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.base_agent import BaseAgent

REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"

# Danh sách các file tài liệu cốt lõi cần đọc
CORE_DOCS = [
    "README.md",
    "context/ARCHITECTURE.md",
    "context/ROADMAP.md",
    "context/JARVIS_CHRONICLES.md",
    "docs/PENDING_TECH_DEBT.md",
    "docs/V3_EXPANSION_PLAN.md"
]

class SkepticAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)
        
    def _ai_handler(self, docs_content: str) -> str:
        prompt = f"""
[ROLE: THE SKEPTIC QA AUDITOR]
Bạn là một kiểm toán viên kỹ thuật cực kỳ khó tính và soi mói. Hãy đọc bộ tài liệu dự án dưới đây.
Nhiệm vụ của bạn là VẠCH LÁ TÌM SÂU:
1. Tìm ra những điểm mâu thuẫn giữa các file (ví dụ: file này nói A nhưng file kia nói B).
2. Tìm ra những thông tin có vẻ đã lỗi thời (outdated) hoặc nợ kỹ thuật (Tech Debt) bị bỏ quên.
3. Chỉ trích thẳng thắn những điểm yếu kém trong kiến trúc hoặc lộ trình hiện tại.

[BỘ TÀI LIÊU DỰ ÁN]:
{docs_content}

[OUTPUT]: 
Trả về bài phản biện sắc bén của bạn dưới dạng Markdown.
"""
        return self._call_llm(prompt)

    def _logic_handler(self, docs_content: str) -> str:
        return "Lỗi: Không thể kết nối GCLI để chạy Role Skeptic."

class DefenderAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)
        
    def _ai_handler(self, docs_content: str, skeptic_critique: str) -> str:
        prompt = f"""
[ROLE: THE DEFENDER ARCHITECT]
Bạn là Kiến trúc sư trưởng bảo vệ dự án. Một gã QA Auditor (Skeptic) vừa đưa ra những lời chỉ trích gay gắt về bộ tài liệu của bạn.
Nhiệm vụ của bạn là PHẢN BIỆN LẠI:
1. Giải thích lý do (Trade-off) tại sao hệ thống lại được thiết kế hoặc ghi chép như vậy (do thiếu ngân sách, do ưu tiên sinh tồn thay vì hoàn hảo, v.v.).
2. Đề xuất các giải pháp kỹ thuật thực tế để vá những lỗ hổng mà Skeptic chỉ ra, nhưng phải dựa trên tinh thần Bootstrapping (không tốn tiền).

[BÀI CHỈ TRÍCH CỦA SKEPTIC]:
{skeptic_critique}

[OUTPUT]: 
Trả về bài bảo vệ và đề xuất giải pháp của bạn dưới dạng Markdown.
"""
        return self._call_llm(prompt)

    def _logic_handler(self, docs_content: str, skeptic_critique: str) -> str:
        return "Lỗi: Không thể kết nối GCLI để chạy Role Defender."

class SynthesizerAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-1", **kwargs)
        
    def _ai_handler(self, skeptic_critique: str, defender_response: str) -> str:
        prompt = f"""
[ROLE: THE OVERLORD SYNTHESIZER]
Bạn là Thẩm phán tối cao. Bạn vừa chứng kiến một cuộc tranh luận nảy lửa giữa QA Auditor (Skeptic) và Kiến trúc sư (Defender) về bộ tài liệu của dự án.
Nhiệm vụ của bạn là ĐÚC KẾT RA BẢN PHÂN TÍCH CỰC THỰC DỤNG:
1. Tóm tắt ngắn gọn cuộc tranh luận (Nhìn nhận khách quan).
2. Đưa ra PHÁN QUYẾT CUỐI CÙNG: Những file Markdown nào thực sự đang bị outdate và cần Admin sửa tay ngay lập tức?
3. Đề xuất Action Plan (Kế hoạch hành động 3 bước) thực dụng nhất để dự án đi tiếp mà không bị vướng bận.

[SKEPTIC CRITIQUE]:
{skeptic_critique}

[DEFENDER RESPONSE]:
{defender_response}

[OUTPUT]: 
Trả về bản đúc kết cuối cùng dưới dạng Markdown, có cấu trúc rõ ràng, chuyên nghiệp.
"""
        return self._call_llm(prompt)

    def _logic_handler(self, skeptic_critique: str, defender_response: str) -> str:
        return "Lỗi: Không thể kết nối GCLI để chạy Role Synthesizer."

def main():
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    print("🚀 Bắt đầu Cuộc Hội Chẩn Khoa Học (The Doc Debate)...")
    
    base_dir = Path(__file__).resolve().parent.parent.parent
    docs_content = ""
    
    # Đọc gộp tất cả các file
    for doc_path in CORE_DOCS:
        full_path = base_dir / doc_path
        if full_path.exists():
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Giới hạn nội dung mỗi file để tránh tràn context (tối đa 4000 chars/file)
                docs_content += f"\n\n--- BẮT ĐẦU FILE: {doc_path} ---\n{content[:4000]}\n--- KẾT THÚC FILE: {doc_path} ---\n"
                print(f"📦 Đã nạp file: {doc_path}")
        else:
            print(f"⚠️ Không tìm thấy file: {doc_path}")
            
    print("\n🧠 Kích hoạt [Vòng 1]: The Skeptic QA Auditor đang săi soi...")
    skeptic = SkepticAgent()
    critique = skeptic.execute(docs_content=docs_content)
    print("   ✅ Skeptic đã hoàn tất bản cáo trạng!")
    
    print("\n🛡️ Kích hoạt [Vòng 2]: The Defender Architect đang lập luận bảo vệ...")
    defender = DefenderAgent()
    defense = defender.execute(docs_content=docs_content, skeptic_critique=critique)
    print("   ✅ Defender đã hoàn tất bài bào chữa!")
    
    print("\n⚖️ Kích hoạt [Vòng 3]: The Overlord Synthesizer đang đúc kết phán quyết...")
    synthesizer = SynthesizerAgent()
    final_report = synthesizer.execute(skeptic_critique=critique, defender_response=defense)
    print("   ✅ Overlord đã ra phán quyết!")
    
    # Ghi xuất báo cáo
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "DOC_DEBATE_ANALYSIS.md"
    
    full_markdown = f"""# 🏛️ BIÊN BẢN HỘI CHẨN KHOA HỌC (THE DOC DEBATE)
*Ngày tạo: Tự động qua GCLI Delegation*

## 🎙️ VÒNG 1: CÁO TRẠNG TỪ SKEPTIC QA AUDITOR
{critique}

---
## 🛡️ VÒNG 2: LỜI BÀO CHỮA TỪ DEFENDER ARCHITECT
{defense}

---
## ⚖️ VÒNG 3: PHÁN QUYẾT TỐI CAO TỪ OVERLORD SYNTHESIZER
{final_report}
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
        
    print(f"\n✅ Đã lưu toàn bộ biên bản tranh luận tại: {report_path}")
    print("💡 Cline có thể gọi 'read_file' để đọc file trên.")

if __name__ == "__main__":
    main()
