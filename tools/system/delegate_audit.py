import os
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

target_md = "docs/archive_data/analysis_user/All_User_Inputs_Combined_SFW.md"
# Or maybe it's in projects/History_Cline/analysis_user/All_User_Inputs_Combined_SFW.md
history_md = "projects/History_Cline/analysis_user/All_User_Inputs_Combined_SFW.md"

if os.path.exists(history_md):
    file_to_read = history_md
elif os.path.exists(target_md):
    file_to_read = target_md
else:
    print("Cannot find All_User_Inputs_Combined_SFW.md")
    exit(1)

with open(file_to_read, 'r', encoding='utf-8') as f:
    content = f.read()

# Split by '## File:'
blocks = re.split(r'(?=## File:)', content)

# We want to extract insights without burning tokens in Cline.
# Since we need to use Gemini API, let's setup google.generativeai if available,
# or we use the local BaseAgent.
# Since we don't know the exact structure of BaseAgent, let's try google.generativeai directly.
try:
    from google import genai
    from google.genai import types
    print("Using google-genai library.")
    client = genai.Client(
        api_key=os.getenv('GCLI_API_KEY') or os.getenv('GEMINI_API_KEY'),
        http_options={'base_url': os.getenv('GCLI_BASE_URL') or 'https://generativelanguage.googleapis.com'}
    )
    USE_OLD = False
except ImportError:
    try:
        import google.generativeai as genai
        print("Using old google.generativeai library.")
        genai.configure(
            api_key=os.getenv('GCLI_API_KEY') or os.getenv('GEMINI_API_KEY'),
            client_options={'api_endpoint': os.getenv('GCLI_BASE_URL')} if os.getenv('GCLI_BASE_URL') else None
        )
        USE_OLD = True
    except ImportError:
        print("No google generativeai library found. Install it first.")
        exit(1)

prompt_template = """
Đóng vai Cognitive Reverse-Engineer. Đọc đoạn log sau và trích xuất ra các bài học đệ quy.
[REQUIRED OUTPUT SCHEMA FOR PROFILER]
Mỗi phát hiện phải được trình bày thành 1 dòng trong bảng Markdown với 3 cột:
| Phát hiện (Observation) | Nguyên nhân gốc (Root Cause) | Hành động khắc phục (Action Item) |

Chỉ xuất ra các dòng của bảng (bắt đầu bằng dấu |), không cần xuất header của bảng, không cần giải thích.
Nếu đoạn log không có lỗi, không có phản ứng cảm xúc, không có bài học gì đáng giá, hãy trả về rỗng (hoặc chữ NONE).
Không phân tích các log quá cơ bản. Chỉ phân tích các log có sự cố, chửi thề, đứt gãy kiến trúc, hoặc thay đổi tư duy mạnh.

Log:
{log_content}
"""

matrix_rows = []

print(f"Total blocks to process: {len(blocks)}")
for i, block in enumerate(blocks):
    if len(block.strip()) < 100: continue
    
    # Take chunk
    if len(block) > 10000:
        block = block[:10000] # truncate to avoid too big payload
        
    prompt = prompt_template.format(log_content=block)
    
    try:
        if USE_OLD:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            text = response.text
        else:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            text = response.text
            
        text = text.strip()
        if text and "NONE" not in text and "|" in text:
            # Clean up the output to only keep table rows
            lines = text.split('\n')
            for line in lines:
                if line.startswith('|') and 'Phát hiện' not in line and '---' not in line:
                    matrix_rows.append(line)
        print(f"Processed block {i+1}/{len(blocks)}")
    except Exception as e:
        print(f"Error processing block {i+1}: {e}")

# Append to REFLECTIONS_AND_EVOLUTION.md
ref_file = "context/REFLECTIONS_AND_EVOLUTION.md"
if matrix_rows:
    with open(ref_file, 'a', encoding='utf-8') as f:
        f.write("\n")
        for row in matrix_rows:
            f.write(row + "\n")
    print(f"Appended {len(matrix_rows)} new insights to {ref_file}")
else:
    print("No new insights found.")


