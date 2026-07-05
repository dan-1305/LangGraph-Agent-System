from setuptools import setup
from Cython.Build import cythonize
import os
import sys

# Danh sách các file logic quan trọng cần bảo vệ
# Chúng ta sẽ biên dịch chúng sang .pyd (Windows) hoặc .so (Linux)
files_to_compile = [
    "dist/godot_translator/core/translator.py",
    "dist/godot_translator/core/extractor.py",
    "dist/godot_translator/core/injector.py",
    "dist/godot_translator/src/base_agent.py"
]

def run_cython():
    print("🛡️ Đang kích hoạt Cython DRM để bảo vệ mã nguồn...")
    for file_path in files_to_compile:
        if not os.path.exists(file_path):
            print(f"  [!] Khong tim thay: {file_path}")
            continue
            
        print(f"  - Dang bien dich: {file_path}")
        try:
            # Cythonize file
            setup(
                ext_modules=cythonize(file_path, language_level="3"),
                script_args=["build_ext", "--inplace"]
            )
            print(f"  ✅ Bien dich thanh cong: {file_path}")
        except Exception as e:
            print(f"  [!] Loi khi bien dich {file_path}: {e}")

if __name__ == "__main__":
    run_cython()
