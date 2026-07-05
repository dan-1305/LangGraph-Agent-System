import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

def generate_flagship_roadmap():
    reports_dir = base_dir / "projects" / "ai_qa_agent" / "reports"
    flagship_projects = ["ai_trading_agent", "auto_affiliate_video", "sillytavern_world_card_generator"]
    
    combined_content = ""
    for proj in flagship_projects:
        md_file = reports_dir / f"{proj}_QA.md"
        if md_file.exists():
            combined_content += f"\n\n================ {proj} ================\n"
            combined_content += md_file.read_text(encoding="utf-8")[:4000]
            
    print("🧠 Đang phân tích và cập nhật định hướng phát triển (Roadmap) cho TOP 3 Dự án...")
    
    llm = ChatOpenAI(
        model="gemini-2.5-pro",
        base_url=os.getenv("GCLI_BASE_URL"),
        api_key=os.getenv("GCLI_API_KEY"),
        temperature=0.2
    )
    
    prompt = f"""Bạn là Giám đốc Sản phẩm (CPO) của công ty.
Dưới đây là BÁO CÁO QA MỚI NHẤT của 3 dự án trọng điểm sau khi đội ngũ Dev đã tiến hành đợt "Củng cố Nền tảng" (Thêm Config, Analytics, sửa lỗi Import, v.v.):
{combined_content}

Nhiệm vụ của bạn là dựa vào báo cáo mới này để cập nhật TÀI LIỆU LỘ TRÌNH PHÁT TRIỂN (ROADMAP). Hãy tập trung vào những "LỖI CÒN TỒN ĐỌNG" hoặc "TÍNH NĂNG NÂNG CAO" tiếp theo cần làm.

Định dạng Markdown:
# 🚀 CẬP NHẬT FLAGSHIP PROJECTS ROADMAP (PHASE 2)

## 1. AI Trading Agent
- Điểm QA hiện tại: ...
- [ ] Tính năng A: ... (Mô tả lý do)
- [ ] Tính năng B: ...

## 2. Auto Affiliate Video
- Điểm QA hiện tại: ...
- [ ] Tính năng A: ...
- [ ] Tính năng B: ...

## 3. SillyTavern World Card Generator
- Điểm QA hiện tại: ...
- [ ] Tính năng A: ...
- [ ] Tính năng B: ...

Yêu cầu: Viết cụ thể, nhắm thẳng vào các tính năng kỹ thuật nâng cao hoặc các khoản "Nợ kỹ thuật" (Technical Debt) còn sót lại (Ví dụ: Thêm Type Hinting, Viết Unit Test, Chuyển sang dùng Database Vector nào đó, v.v.).
"""
    
    try:
        response = llm.invoke(prompt)
        out_path = base_dir / "docs" / "FLAGSHIP_ROADMAP_PHASE2.md"
        out_path.parent.mkdir(exist_ok=True)
        out_path.write_text(response.content, encoding="utf-8")
        print(f"✅ Đã tạo thành công Roadmap Phase 2 tại: {out_path}")
    except Exception as e:
        print(f"❌ Lỗi khi gọi LLM: {e}")

if __name__ == "__main__":
    generate_flagship_roadmap()