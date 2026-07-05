import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Setup sys.path cho Monorepo
base_dir = Path(__file__).resolve().parent.parent.parent
if str(base_dir) not in sys.path:
    sys.path.insert(0, str(base_dir))

from projects.sovereign_academy.tutor_agent import CodeTutorAgent

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PROFILE_PATH = os.path.join(DATA_DIR, "learning_profile.json")

def load_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_profile(profile):
    with open(PROFILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4, ensure_ascii=False)

def update_spaced_repetition(profile, filename, score):
    # Rất cơ bản: 
    # Score 3/3: ôn lại sau 3 ngày
    # Score 2/3: ôn lại sau 1 ngày
    # Score <2: ôn lại ngay ngày mai
    now = datetime.now()
    if filename not in profile:
        profile[filename] = {"reviews": 0, "last_score": score, "next_review": ""}
    
    profile[filename]["reviews"] += 1
    profile[filename]["last_score"] = score
    
    if score == 3:
        days = 3 * profile[filename]["reviews"]
    elif score == 2:
        days = 1 * profile[filename]["reviews"]
    else:
        days = 1
        
    next_date = now + timedelta(days=days)
    profile[filename]["next_review"] = next_date.strftime("%Y-%m-%d")
    
    print(f"\n[Spaced Repetition] Đã lưu kết quả. Lịch ôn tập tiếp theo cho bài này: {profile[filename]['next_review']}")
    save_profile(profile)

def run_lesson(tutor, filename, profile):
    print(f"\n{'='*50}")
    print(f"📖 BÀI HỌC: {os.path.basename(filename)}")
    print(f"{'='*50}")
    
    # 1. Read code
    code = tutor.read_code(filename)
    
    # 2. Explain
    print("\n[1/2] Đang tải lời giải thích từ Gia sư AI...")
    explanation = tutor.explain_code(code, filename)
    print("\n--- LỜI GIẢI THÍCH (FEYNMAN TECHNIQUE) ---\n")
    print(explanation)
    print("\n-------------------------------------------")
    input("\nBấm Enter khi bạn đã đọc xong và sẵn sàng làm Quiz...")
    
    # 3. Quiz
    print("\n[2/2] Đang tải câu hỏi trắc nghiệm...")
    quiz_data = tutor.generate_quiz(code, filename)
    
    if not quiz_data or "questions" not in quiz_data:
        print("❌ Lỗi khi sinh bài tập trắc nghiệm.")
        return
        
    questions = quiz_data["questions"]
    score = 0
    
    for i, q in enumerate(questions):
        print(f"\n❓ Câu {i+1}: {q.get('question')}")
        options = q.get("options", [])
        for opt in options:
            print(f"   {opt.get('id')}. {opt.get('text')}")
            
        ans = input("Nhập đáp án của bạn (A/B/C/D): ").strip().upper()
        correct_ans = q.get('correct_option_id', '').upper()
        
        if ans == correct_ans:
            print("✅ Chính xác!")
            score += 1
        else:
            print(f"❌ Sai rồi. Đáp án đúng là {correct_ans}.")
            
        print(f"💡 Giải thích: {q.get('explanation')}")
        time.sleep(1)
        
    print(f"\n🏆 KẾT QUẢ BÀI KIỂM TRA: {score}/{len(questions)}")
    
    # 4. Spaced Repetition
    update_spaced_repetition(profile, filename, score)

def main():
    print("🎓 CHÀO MỪNG ĐẾN VỚI SOVEREIGN ACADEMY 🎓")
    tutor = CodeTutorAgent()
    profile = load_profile()
    
    while True:
        print("\nMENU CHÍNH:")
        print("1. Học một file Core ngẫu nhiên")
        print("2. Chỉ định một file để học")
        print("3. Ôn tập bài cũ (Spaced Repetition)")
        print("4. Thoát")
        
        choice = input("Chọn chức năng (1-4): ").strip()
        
        if choice == '1':
            try:
                f = tutor.get_random_core_file()
                run_lesson(tutor, f, profile)
            except Exception as e:
                print(f"Lỗi: {e}")
                
        elif choice == '2':
            f = input("Nhập đường dẫn file (ví dụ: core/process_watchdog.py): ").strip()
            full_path = os.path.join(base_dir, f)
            if os.path.exists(full_path):
                run_lesson(tutor, full_path, profile)
            else:
                print("❌ File không tồn tại!")
                
        elif choice == '3':
            now_str = datetime.now().strftime("%Y-%m-%d")
            to_review = []
            for f, data in profile.items():
                if data.get("next_review") and data["next_review"] <= now_str:
                    to_review.append(f)
                    
            if not to_review:
                print("\n🎉 Tuyệt vời! Hôm nay bạn không có bài nào cần ôn tập.")
            else:
                print(f"\n📚 Bạn có {len(to_review)} bài cần ôn tập hôm nay:")
                for i, f in enumerate(to_review):
                    print(f"{i+1}. {os.path.basename(f)}")
                
                sel = input("Bạn muốn ôn bài nào? (Nhập số, hoặc 0 để hủy): ").strip()
                if sel.isdigit() and 0 < int(sel) <= len(to_review):
                    run_lesson(tutor, to_review[int(sel)-1], profile)
                    
        elif choice == '4':
            print("Hẹn gặp lại! Chúc bạn học tốt.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()