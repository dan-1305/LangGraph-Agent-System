@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf8
echo 🚀 Đang khởi động Godot Game Translator...
uv run streamlit run app.py --server.port 8502
pause
