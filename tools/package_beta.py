import os
import shutil
import subprocess
from pathlib import Path

def create_portable_package(project_name: str):
    print(f"📦 Đang đóng gói {project_name} thành bản Portable...")
    # Lấy root_dir chuẩn từ file hiện tại (giả sử nó nằm trong /tools hoặc /)
    file_path = Path(__file__).resolve()
    if file_path.parent.name == "tools":
        root_dir = file_path.parent.parent
    else:
        root_dir = file_path.parent
        
    project_dir = root_dir / "projects" / project_name
    dist_dir = root_dir / "dist" / project_name
    
    if not project_dir.exists():
        print(f"  [!] Khong tim thay thu muc project: {project_dir}")
        return

    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True)
    
    # 1. Copy source code
    print("  - Copying source code...")
    for item in project_dir.iterdir():
        if item.name in ["__pycache__", "venv", ".venv", "dist", "build"]:
            continue
        if item.is_dir():
            shutil.copytree(item, dist_dir / item.name)
        else:
            shutil.copy2(item, dist_dir / item.name)
            
    # 2. Copy src (nếu cần thiết cho BaseAgent)
    if project_name == "godot_translator":
         print("  - Injecting core src dependency...")
         src_dir = root_dir / "src"
         target_src = dist_dir / "src"
         if src_dir.exists():
             shutil.copytree(src_dir, target_src)

    # 3. Tạo file setup_env.bat
    print("  - Creating setup_env.bat...")
    setup_bat = f"""@echo off
chcp 65001 >nul
echo 🛠️ Dang thiet lap moi truong Portable cho {project_name}...
curl -LsSf https://astral.sh/uv/install.ps1 | powershell -Command -
set PATH=%PATH%;%USERPROFILE%\\.cargo\\bin
uv venv
uv pip install -r requirements.txt
echo ✅ Moi truong da san sang!
pause
"""
    with open(dist_dir / "setup_env.bat", "w", encoding="utf-8") as f:
        f.write(setup_bat)

    print(f"✅ Da tao ban thiet lap tai: {dist_dir}")

if __name__ == "__main__":
    create_portable_package("disk_cleaner")
    create_portable_package("godot_translator")
