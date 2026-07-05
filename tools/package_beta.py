import os
import zipfile
from pathlib import Path

def create_beta_zip():
    base_dir = Path(__file__).resolve().parent.parent
    zip_name = base_dir / "Polymorphic_VideoBot_Beta.zip"
    
    print(f"📦 Đang đóng gói bản Beta: {zip_name.name}...")
    
    # Chỉ định các thư mục/file sẽ được nạp vào
    # Bỏ qua các thư mục như logs, chromadb, v.v.
    include_paths = [
        "projects/auto_affiliate_video/",
        "core/",
        "src/",
        "tools/",
        "run.bat",
        "pyproject.toml",
        ".env.example"
    ]
    
    exclude_patterns = ["__pycache__", ".pytest_cache", ".git", ".venv", "output", "background_videos", ".log"]
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for p in include_paths:
            path = base_dir / p
            if path.is_file():
                arcname = path.relative_to(base_dir)
                zipf.write(path, arcname)
                print(f"  + Added file: {arcname}")
            elif path.is_dir():
                for root, dirs, files in os.walk(path):
                    # Lọc bỏ thư mục không cần thiết
                    dirs[:] = [d for d in dirs if not any(x in d for x in exclude_patterns)]
                    
                    for file in files:
                        if any(x in file for x in exclude_patterns) or file.endswith('.pyc'):
                            continue
                        
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(base_dir)
                        zipf.write(file_path, arcname)
    
    print(f"✅ Đã tạo thành công {zip_name} ({os.path.getsize(zip_name) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    create_beta_zip()
