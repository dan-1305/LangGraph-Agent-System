import os
import time
from datetime import datetime
from pathlib import Path
import sys

# Force UTF-8 encoding for Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup sys.path cho Monorepo
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from projects.sovereign_academy.tutor_agent import CodeTutorAgent
from projects.sovereign_academy.main import load_profile, run_lesson
def one_click_run():
    print("="*60)
    print("🚀 SOVEREIGN ACADEMY - 1-CLICK LEARNING ENGINE 🚀")
    print("="*60)
    
    tutor = CodeTutorAgent()
    profile = load_profile()
    
    now_str = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Kiểm tra Spaced Repetition (Due for Review)
    to_review = []
    for file_path, data in profile.items():
        if data.get("next_review") and data["next_review"] <= now_str:
            to_review.append(file_path)
            
    if to_review:
        # Nếu có bài cần ôn, ưu tiên bài ôn cũ nhất (ít được review nhất hoặc ngẫu nhiên)
        import random
        selected_file = random.choice(to_review)
        print(f"\n[!] Báo động Spaced Repetition: Bạn có {len(to_review)} bài cần ôn tập hôm nay!")
        print(f"Hệ thống đã tự động chọn bài ưu tiên nhất: {os.path.basename(selected_file)}")
        time.sleep(2)
        run_lesson(tutor, selected_file, profile)
    else:
        # 2. Học bài mới (Random Core File)
        print("\n[+] Hôm nay không có bài ôn tập! Khởi tạo bài học mới hoàn toàn...")
        time.sleep(1)
        try:
            random_file = tutor.get_random_core_file()
            run_lesson(tutor, random_file, profile)
        except Exception as e:
            print(f"❌ Lỗi khi lấy file mới: {e}")
            
    print("\n" + "="*60)
    print("✅ Đã hoàn thành phiên học 1-Click! Hãy tắt cửa sổ này hoặc nhấn phím bất kỳ để thoát.")
    print("="*60)
    input() # Giữ cửa sổ terminal mở

if __name__ == "__main__":
    one_click_run()