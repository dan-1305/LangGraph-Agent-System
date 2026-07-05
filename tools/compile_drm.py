from setuptools import setup
from Cython.Build import cythonize
import os

"""
Script dịch mã nguồn Python (.py) sang thư viện C (.pyd / .so) chống dịch ngược.
Cách dùng:
python compile_drm.py build_ext --inplace
"""

# Tìm đường dẫn tới core/drm_validator.py
target_file = os.path.join(os.path.dirname(__file__), "..", "core", "drm_validator.py")

setup(
    name='Jarvis DRM',
    ext_modules=cythonize(target_file, compiler_directives={'language_level': "3"})
)
print("✅ Cython Build Script Ready! Chạy lệnh: uv run python tools/compile_drm.py build_ext --inplace để compile.")
