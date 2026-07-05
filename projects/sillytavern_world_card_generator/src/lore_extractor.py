import os
import json
import re
import asyncio
import sys
import io
from pathlib import Path
from dotenv import load_dotenv

# Đảm bảo src vào sys.path để import thư viện lõi
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.factory.config import create_fallback_chain
from langchain_core.messages import SystemMessage, HumanMessage

# Force stdout to be UTF-8 for Windows console
if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# --- Giai đoạn 1: Refactor & Cấu hình ---

dotenv_path = root_dir / '.env'
load_dotenv(dotenv_path=dotenv_path)

INPUT_DIR = os.path.abspath('projects/sillytavern_world_card_generator/data/world_card')
OUTPUT_DIR = os.path.abspath('projects/sillytavern_world_card_generator/docs')
PROCESSED_LOG = os.path.join(OUTPUT_DIR, 'processed_log.txt')

# Khởi tạo Fallback Chain thay vì dùng client OpenAI trần
llm = create_fallback_chain(
    model_list=["gemini-2.5-pro", "gemini-2.5-flash"],
    temperature=0.5
)

# --- Giai đoạn 2: Tách bạch Logic thành các "Tools" ---

def read_json_file(filepath: str) -> dict | None:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def build_llm_prompt(data: dict) -> list:
    card_name = data.get('name', 'Không có tên')
    description = data.get('description', '')
    first_mes = data.get('first_mes', '')

    # Lấy data trong spec v3 (ưu tiên hơn)
    character_book_content = ""
    if 'data' in data and isinstance(data['data'], dict):
        card_name = data['data'].get('name', card_name)
        description = data['data'].get('description', description)
        first_mes = data['data'].get('first_mes', first_mes)
        
        # Trích xuất toàn bộ nội dung từ character_book (thường chứa Lore chính)
        if 'character_book' in data['data'] and isinstance(data['data']['character_book'], dict):
            entries = data['data']['character_book'].get('entries', [])
            for entry in entries:
                if 'content' in entry:
                    character_book_content += f"\n--- {entry.get('comment', 'Entry')} ---\n"
                    character_book_content += entry['content'] + "\n"

    system_prompt = """Bạn là một chuyên gia phân tích và tóm tắt World Card cho SillyTavern. Nhiệm vụ của bạn là đọc dữ liệu JSON được cung cấp, dịch các phần tiếng Trung sang tiếng Việt (giữ lại tên gốc trong ngoặc), và tạo một bản tóm tắt chi tiết dưới dạng Markdown theo đúng cấu trúc yêu cầu.
Hãy bám sát cấu trúc sau:
# Tổng hợp Lore từ World Card: [Tên gốc] ([Tên đã dịch])
## 1. Thông tin nhân vật: [Tên nhân vật]
*   **Tuổi:** ...
*   **Danh tính:** ...
### Ngoại hình:
*   **Tổng thể:** ...
*   **Số đo:** ...
*   **Đặc điểm nổi bật:** ...
### Tính cách & Hành vi:
*   **Cốt lõi:** ...
*   **Ưu điểm:** ...
*   **Khuyết điểm:** ...
*   **Thói quen & Tật xấu:** ...
### Quan hệ với con trai ({{user}}):
*    ...
## 2. Bối cảnh & Tình huống Mở đầu
*   **Địa điểm:** ...
*   **First Message:** ...
## 3. Các cơ chế khác
*   **Tavern Helper & MVU:** ... (Nếu có)
*   **Zod Schema:** ... (Nếu có)
*   **World Info:** ... (Nếu có)

CHỈ trả về nội dung file Markdown. KHÔNG thêm lời dẫn, giải thích hay bất kỳ văn bản nào khác.
"""
    
    user_prompt = f"""## Dữ liệu World Card:
**Tên Card (name):** {card_name}
**Mô tả (description/lorebook):**
{description}
**Lời chào đầu (first_mes):**
{first_mes}

**Sách Nhân vật / Bối cảnh Thế giới (character_book):**
{character_book_content}
---
Hãy tóm tắt theo đúng định dạng đã hướng dẫn.
"""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

async def call_llm_api(messages: list) -> str | None:
    try:
        langchain_messages = [
            SystemMessage(content=messages[0]["content"]),
            HumanMessage(content=messages[1]["content"])
        ]
        
        # Dùng ainvoke vì luồng này đang chạy asyncio
        response = await llm.ainvoke(langchain_messages)
        
        # Track token usage
        try:
            from src.token_tracker import track_llm_usage
            model_name = getattr(llm, 'model', 'unknown') if hasattr(llm, 'model') else 'fallback_chain_model'
            track_llm_usage(response, "sillytavern_world_card_generator", model_name)
        except Exception:
            pass
            
        return response.content.strip()
    except Exception as e:
        print(f"❌ [Circuit Breaker] Fallback kích hoạt do lỗi API: {e}")
        return None

def write_markdown_file(filepath: str, content: str, original_name: str) -> bool:
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        log_processed_file(f"{original_name}.json")
        return True
    except IOError:
        return False

def get_output_filename(md_content: str, original_name: str) -> str:
    h1_match = re.search(r'#\s*Tổng hợp Lore từ World Card:\s*(.*)', md_content)
    if h1_match:
        title = h1_match.group(1).strip()
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        return f"WORLDCARD_{safe_title}.md"
    
    safe_original_name = re.sub(r'[<>:"/\\|?*]', '', original_name)
    return f"WORLDCARD_{safe_original_name}.md"
    
def has_chinese_chars(text: str) -> bool:
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def get_processed_files() -> set:
    if not os.path.exists(PROCESSED_LOG):
        return set()
    with open(PROCESSED_LOG, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def log_processed_file(filename: str):
    with open(PROCESSED_LOG, 'a', encoding='utf-8') as f:
        f.write(filename + '\n')

async def agent_process_card(filepath: str):
    original_filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
    card_data = read_json_file(filepath)
    if not card_data: return
    prompt_messages = build_llm_prompt(card_data)
    md_content = await call_llm_api(prompt_messages)
    if not md_content: 
        return
    output_filename = get_output_filename(md_content, original_filename_no_ext)
    output_filepath = os.path.join(OUTPUT_DIR, output_filename)
    if write_markdown_file(output_filepath, md_content, original_filename_no_ext):
        # Safe ASCII print for status
        print("SUCCESS")
    else:
        print("WRITE_ERROR")

async def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    processed_files = get_processed_files()
    tasks = []

    if not os.path.exists(INPUT_DIR):
        print("Input directory not found.")
        return
        
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith('.json') and has_chinese_chars(filename) and filename not in processed_files:
            filepath = os.path.join(INPUT_DIR, filename)
            tasks.append(agent_process_card(filepath))

    if not tasks:
        print("No new files to process.")
        return

    print(f"Found {len(tasks)} files. Processing one by one...")
    
    for i, task in enumerate(tasks):
        sys.stdout.write(f"[{i+1}/{len(tasks)}] ")
        sys.stdout.flush()
        await task
        # Add a small delay between tasks to avoid rate limits
        await asyncio.sleep(2)
        
    print("\nDone.")

if __name__ == "__main__":
    asyncio.run(main())
