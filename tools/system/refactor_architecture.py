import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def move_if_exists(src, dst):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
        print(f"Moved {src.name} to {dst}")

def delete_if_exists(target):
    if target.exists():
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
        print(f"Deleted {target.name}")

def main():
    print("--- DỌN DẸP ROOT DIRECTORY ---")
    guides_dir = ROOT_DIR / "docs" / "guides"
    guides_dir.mkdir(parents=True, exist_ok=True)
    
    docs_to_move = [
        "AI_ONBOARDING_GUIDE.md",
        "CAREER_STRATEGY.md",
        "CONTEXT_SUMMARY.md",
        "INSTRUCTIONS.md",
        "MASTER_GUIDE.md"
    ]
    
    for doc in docs_to_move:
        move_if_exists(ROOT_DIR / doc, guides_dir / doc)
        
    delete_if_exists(ROOT_DIR / "temp_scaffold.py")
    delete_if_exists(ROOT_DIR / "langgraph_agent_system.egg-info")
    
    move_if_exists(ROOT_DIR / "scheduler", ROOT_DIR / "src" / "scheduler")
    move_if_exists(ROOT_DIR / "run_live_trading_now.bat", ROOT_DIR / "projects" / "ai_trading_agent" / "run_live_trading_now.bat")
    
    print("--- DỌN DẸP THƯ MỤC PROJECTS ---")
    delete_if_exists(ROOT_DIR / "projects" / "data")
    delete_if_exists(ROOT_DIR / "projects" / "ai_qa_agent")
    
    bot_dir = ROOT_DIR / "bot"
    if not bot_dir.exists():
        move_if_exists(ROOT_DIR / "projects" / "telegram_controller", bot_dir)
        
    print("--- CHUẨN HÓA CÁC SUB-PROJECTS ---")
    projects_dir = ROOT_DIR / "projects"
    for item in projects_dir.iterdir():
        if item.is_dir() and not item.name.startswith("_"):
            src_dir = item / "src"
            src_dir.mkdir(exist_ok=True)
            
            # Tạo các thư mục chuẩn nếu chưa có
            (item / "tests").mkdir(exist_ok=True)
            (item / "docs").mkdir(exist_ok=True)
            (item / "data").mkdir(exist_ok=True)
            
            # Di chuyển các file .py lang thang vào src/
            for py_file in item.glob("*.py"):
                if py_file.name not in ["setup.py", "dashboard.py"]:
                    move_if_exists(py_file, src_dir / py_file.name)
                    
    print("Dọn dẹp hoàn tất!")

if __name__ == "__main__":
    main()
