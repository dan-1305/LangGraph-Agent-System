import os
import json
import re
import sys
import io
from pathlib import Path
from datetime import datetime

# Fix encoding issue for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

# --- CONFIGURATION ---
LIVE_TASKS_DIR = Path(os.environ.get('APPDATA', '')) / "Code" / "User" / "globalStorage" / "saoudrizwan.claude-dev" / "tasks"
REMOTE_TASKS_DIR = Path("D:/Users/Admin/Downloads/LangGraphStorage/Intellectual_Property/History_Cline/ALL_Chat/NewChat")
OUTPUT_FILE = Path("analysis_user/all_user_input_v4.md")

# NSFW words to censor (based on v3)
nsfw_words = [
    r'\bđụ\b', r'\bđịt\b', r'\blồn\b', r'\bcặc\b', r'\bbuồi\b',
    r'\bdái\b', r'\bđĩ\b', r'\bđĩ điếm\b', r'\bvcl\b', r'\bvkl\b', r'\bcc\b',
    r'\bđm\b', r'\bđmm\b', r'\bđcm\b', r'\bdcm\b', r'\bvãi l\b', r'\bđéo\b',
    r'\bchó đẻ\b', r'\bbitch\b', r'\bfuck\b', r'\bshit\b', r'\bdick\b',
    r'\bsex\b', r'\bporn\b', r'\bpornstar\b', r'\bnude\b', r'\bnudes\b'
]
nsfw_pattern = re.compile('|'.join(nsfw_words), flags=re.IGNORECASE)

# Keywords to detect AI generated prompts
ai_indicators = [
    "Cline,", "Hãy đóng vai", "**TÓM TẮT", "Tóm tắt phiên làm việc hiện tại:",
    "Nhiệm vụ của bạn là refactor lại theo đúng",
    "Phiên làm việc này sắp kết thúc. Bạn hãy thực hiện nghi thức",
    "tôi muốn nâng cấp toàn bộ hệ thống lên Cấp độ 4"
]

def censor_nsfw(text):
    if not text: return ""
    return nsfw_pattern.sub('***', text)

def is_ai_prompt(text):
    if not text: return False
    return any(indicator in text for indicator in ai_indicators)

def extract_from_dir(tasks_dir, limit=20):
    all_inputs = []
    if not tasks_dir.exists():
        print(f"Directory {tasks_dir} not found.")
        return []
        
    # Sort by task_id (timestamp) descending
    task_folders = sorted([f for f in tasks_dir.iterdir() if f.is_dir() and f.name.isdigit()], key=lambda x: x.name, reverse=True)
    
    for task_folder in task_folders[:limit]:
        task_id = task_folder.name
        ui_msg_file = task_folder / "ui_messages.json"
        
        if not ui_msg_file.exists():
            continue
            
        try:
            with open(ui_msg_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            
            inputs_in_task = []
            for msg in messages:
                # Extract initial task
                if msg.get("type") == "say" and msg.get("say") == "task":
                    text = msg.get("text", "")
                    ts = msg.get("ts", 0)
                    inputs_in_task.append((ts, text))
                # Extract user feedback
                elif msg.get("type") == "say" and msg.get("say") == "user_feedback":
                    text = msg.get("text", "")
                    ts = msg.get("ts", 0)
                    inputs_in_task.append((ts, text))
                # Extract text from human role if it's an api_conversation_history format (unlikely in ui_messages but for safety)
                elif msg.get("role") == "user":
                    text = msg.get("content", "")
                    ts = msg.get("ts", 0)
                    inputs_in_task.append((ts, text))
            
            if inputs_in_task:
                all_inputs.append({"task_id": task_id, "inputs": inputs_in_task, "source": str(tasks_dir.name)})
        except Exception as e:
            print(f"Error processing {task_id}: {e}")
            
    return all_inputs

def main():
    print("🚀 Starting User Input Extraction V4...")
    
    # Extract from live storage (highest priority)
    live_inputs = extract_from_dir(LIVE_TASKS_DIR, limit=15)
    
    # Extract from remote storage (backup/older chats)
    remote_inputs = extract_from_dir(REMOTE_TASKS_DIR, limit=10)
    
    # Merge and avoid duplicates by task_id
    seen_ids = set()
    merged_inputs = []
    
    for task in live_inputs + remote_inputs:
        if task["task_id"] not in seen_ids:
            merged_inputs.append(task)
            seen_ids.add(task["task_id"])
            
    # Sort by task_id descending
    merged_inputs.sort(key=lambda x: x["task_id"], reverse=True)
    
    # Write to file
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# 📝 ALL USER INPUT V4 - CLINE HISTORY\n\n")
        f.write(f"**Trích xuất lúc:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Nguồn:** Live History (%APPDATA%) & Remote Backup (D: drive)\n\n")
        f.write("---\n\n")
        
        for task_data in merged_inputs:
            task_id = task_data["task_id"]
            source = task_data["source"]
            f.write(f"## 🛠️ Task: {task_id} (Source: {source})\n\n")
            
            for i, (ts, text) in enumerate(task_data["inputs"], 1):
                clean_text = censor_nsfw(text)
                ai_marker = "> 🤖 **[AI-GENERATED PROMPT]**\n" if is_ai_prompt(text) else ""
                
                # Format timestamp
                try:
                    dt_str = datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    dt_str = str(ts)
                    
                f.write(f"### 💬 Input {i} - [{dt_str}]\n")
                f.write(f"{ai_marker}\n")
                f.write(f"```text\n{clean_text}\n```\n\n")
            
            f.write("---\n\n")
            
    print(f"✅ Finished! Extracted {len(merged_inputs)} tasks into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
