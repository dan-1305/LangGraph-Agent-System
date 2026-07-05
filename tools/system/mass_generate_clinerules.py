import os
import glob

def generate_domain_rules():
    projects_dir = "projects"
    # List all subdirectories
    subdirs = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
    
    # Exclude __pycache__ and those we already manually created
    exclude = ['__pycache__', 'ai_trading_agent', 'airdrop_guerrilla', 'qa_chaos_agent']
    
    for subdir in subdirs:
        if subdir in exclude:
            continue
            
        rule_path = os.path.join(projects_dir, subdir, ".clinerules")
        
        # Name format: replace underscores and dashes with spaces, uppercase
        agent_name = subdir.replace('_', ' ').replace('-', ' ').upper()
        
        template = f"""# {agent_name} - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA {agent_name}.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `{subdir}`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.
"""
        
        with open(rule_path, "w", encoding="utf-8") as f:
            f.write(template)
            
        print(f"[SUCCESS] Da tao file: {rule_path}")

if __name__ == "__main__":
    generate_domain_rules()
