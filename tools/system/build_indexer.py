import os
import shutil
import glob
from pathlib import Path
import sys

# Add root to pythonpath
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.base_agent import BaseAgent

class IndexerAgent(BaseAgent):
    def __init__(self, **kwargs):
        super().__init__(model_name="label:tier-2", **kwargs)
        
    def _ai_handler(self, file_content: str) -> str:
        # Giới hạn nội dung đọc để tránh tràn context
        content_preview = file_content[:1500] 
        prompt = f"""
[ROLE: LIBRARIAN / INDEXER]
Nhiệm vụ: Đọc đoạn nội dung sau và tóm tắt thành ĐÚNG 1 CÂU NGẮN GỌN (dưới 20 chữ) mô tả chủ đề chính của file này.
Ví dụ: "Phân tích yêu cầu tạo bot Discord Airdrop." hoặc "Sửa lỗi crash khi load thư viện pydantic."

Nội dung file:
{content_preview}

Output yêu cầu: CHỈ TRẢ VỀ CÂU TÓM TẮT. Không cần giải thích thêm.
"""
        response = self._call_llm(prompt, is_json=False)
        return response.strip()

    def _logic_handler(self, file_content: str) -> str:
        # Fallback: Lấy dòng đầu tiên không trống
        lines = file_content.split('\n')
        for line in lines:
            if line.strip() and not line.startswith('#'):
                return line.strip()[:100] + "..."
        return "Bản ghi không xác định."

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print("🚀 Bắt đầu quét thư mục analysis_user/ để tạo Indexer (Tier 2 Warm Memory)...")
    
    base_dir = Path(__file__).resolve().parent.parent.parent / "analysis_user"
    raw_logs_dir = base_dir / "raw_logs"
    index_file = base_dir / "User_Inputs_Index.md"
    
    if not base_dir.exists():
        print("❌ Không tìm thấy thư mục analysis_user/")
        return
        
    raw_logs_dir.mkdir(exist_ok=True)
    
    md_files = glob.glob(str(base_dir / "User_Input_Analysis_*.md"))
    
    if not md_files:
        print("⚠️ Không tìm thấy file User_Input_Analysis_*.md nào cần gom.")
        return
        
    print(f"📦 Tìm thấy {len(md_files)} file. Đang khởi động AI Indexer Agent...")
    
    agent = IndexerAgent()
    index_entries = []
    
    for i, file_path in enumerate(md_files):
        filename = os.path.basename(file_path)
        print(f"[{i+1}/{len(md_files)}] Đang tóm tắt: {filename}...")
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        summary = agent.execute(file_content=content)
        # Fallback thêm nếu summary rỗng do LLM lỗi
        if not summary:
            summary = "Không thể trích xuất tóm tắt."
            
        # Thêm vào danh sách Index
        index_entries.append(f"- **[{summary}]** -> `raw_logs/{filename}`")
        
        # Move file vào raw_logs
        shutil.move(file_path, raw_logs_dir / filename)
        
    print("\n📝 Đang ghi file Index...")
    with open(index_file, "w", encoding="utf-8") as f:
        f.write("# 📚 MỤC LỤC PHÂN TÍCH YÊU CẦU NGƯỜI DÙNG (WARM MEMORY)\n\n")
        f.write("*File này đóng vai trò là The Indexer Pattern. Khi cần tra cứu, hãy đọc tóm tắt ở đây và trỏ đường dẫn tới file cụ thể trong thư mục `raw_logs/` để đọc chi tiết.*\n\n")
        f.write("## 🗂️ Danh sách File:\n")
        for entry in index_entries:
            f.write(entry + "\n")
            
    print(f"✅ Hoàn tất! Đã dọn dẹp {len(md_files)} file vào `raw_logs/` và tạo mục lục tại `User_Inputs_Index.md`.")

if __name__ == "__main__":
    main()
