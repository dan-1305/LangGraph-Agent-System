import os
import sys
import time
import json
from pathlib import Path
from datetime import datetime

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent

from src.factory.config import create_fallback_chain

from src.factory.config import create_fallback_chain

LOG_FILE = BASE_DIR / "logs" / "drip_feed_stats.json"

def load_stats():
    if LOG_FILE.exists():
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"total_requests": 0, "tasks_completed": {"affiliate": 0, "dataset": 0}, "last_run": None}

def save_stats(stats):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(stats, f, indent=4)
    except Exception as e:
        print(f"Lỗi khi lưu stats: {e}")

def run_drip_feed():
    print("==========================================================")
    print("💧 [DRIP-FEEDER] BẮT ĐẦU VẮT KIỆT API FREE TIER (15 RPM) 💧")
    print("==========================================================")
    
    llm = create_fallback_chain(model_list=["gemini-2.5-flash", "gemini-2.5-flash-lite"], temperature=0.7)
    
    task_cycle = ["affiliate", "dataset"]
    cycle_index = 0
    
    output_dir = BASE_DIR / "data" / "drip_feed_output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    while True:
        stats = load_stats()
        task = task_cycle[cycle_index]
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 🚀 Đang thực thi task: {task.upper()}")
        
        try:
            if task == "affiliate":
                prompt = "Viết 1 kịch bản video ngắn TikTok (dưới 60s) review một thiết bị công nghệ hoặc chủ đề thú vị bất kỳ. Chỉ trả về text kịch bản, chia cảnh rõ ràng."
                resp = llm.invoke(prompt)
                
                with open(output_dir / "affiliate_scripts.txt", "a", encoding="utf-8") as f:
                    f.write(f"\n\n--- Kịch bản {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                    f.write(resp.content)
                    
            elif task == "dataset":
                prompt = "Tạo 3 cặp câu hỏi và câu trả lời (Q&A) về kỹ năng lập trình Python hoặc Trading cho AI Agent. Trả về đúng format JSON array: [{\"question\": \"...\", \"answer\": \"...\"}] KHÔNG chứa text nào khác ngoài JSON."
                resp = llm.invoke(prompt)
                
                with open(output_dir / "synthetic_qa.jsonl", "a", encoding="utf-8") as f:
                    clean_content = resp.content.replace("```json", "").replace("```", "").strip()
                    if clean_content.startswith("["):
                        try:
                            qa_list = json.loads(clean_content)
                            for qa in qa_list:
                                f.write(json.dumps(qa, ensure_ascii=False) + "\n")
                        except Exception as e:
                            f.write(json.dumps({"raw_response": clean_content}, ensure_ascii=False) + "\n")
                    else:
                        f.write(json.dumps({"raw_response": clean_content}, ensure_ascii=False) + "\n")
            
            # Cập nhật số liệu
            stats["total_requests"] = stats.get("total_requests", 0) + 1
            if "tasks_completed" not in stats:
                stats["tasks_completed"] = {"affiliate": 0, "dataset": 0}
            stats["tasks_completed"][task] = stats["tasks_completed"].get(task, 0) + 1
            stats["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_stats(stats)
            
            print(f"✅ Hoàn thành task {task}. Dữ liệu lưu tại: data/drip_feed_output")
            
        except Exception as e:
            print(f"❌ Lỗi khi thực thi task {task} (có thể do API Rate Limit): {e}")
            
        # Xoay vòng task
        cycle_index = (cycle_index + 1) % len(task_cycle)
        
        # Ngủ 3 phút (180 giây) = max 480 request/ngày
        print("💤 Đang ngủ 3 phút để tránh Rate Limit API...")
        time.sleep(180)

if __name__ == "__main__":
    try:
        run_drip_feed()
    except KeyboardInterrupt:
        print("\n🛑 Đã dừng hệ thống Drip-Feeder.")
        sys.exit(0)
