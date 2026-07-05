import PyInstaller.__main__
import os
from pathlib import Path

# Đường dẫn thư mục gốc
base_dir = Path(__file__).resolve().parent

# File entry point
main_script = str(base_dir / "main_run.py")

print("🚀 Khởi động luồng Build PyInstaller cho Godot Translator...")

# Để PyInstaller đóng gói thành công Streamlit, cần gom thêm thư mục streamlit, pydantic...
# Tuy nhiên vì đây là script build cơ bản, ta sẽ dùng tham số onedir để an toàn hơn là onefile.
# Onefile thường bị lỗi giải nén temp quá lâu đối với Streamlit.

try:
    PyInstaller.__main__.run([
        main_script,
        '--name=Godot_Translator_Pro',
        '--windowed', # Ẩn cửa sổ console đen, chỉ chạy ngầm (nếu cần show console để debug thì bỏ)
        '--noconfirm',
        '--clean',
        '--distpath=' + str(base_dir / "dist"),
        '--workpath=' + str(base_dir / "build"),
        # Thêm các dependency ẩn nếu có
        '--hidden-import=streamlit',
        '--hidden-import=pydantic',
        '--hidden-import=langchain_openai'
    ])
    print("✅ Đã Build thành công file .exe thương mại. Vui lòng kiểm tra thư mục 'dist/'.")
except Exception as e:
    print(f"❌ Lỗi Build: {e}")
