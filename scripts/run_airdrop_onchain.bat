@echo off
title Airdrop On-chain Bot - Stealth Engine
color 0B

echo ========================================================
echo   🚀 AIRDROP GUERRILLA - FULL AUTO ON-CHAIN
echo ========================================================
echo.

:: Đảm bảo đang đứng ở thư mục gốc
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf8

:: Kích hoạt môi trường ảo (nếu có)
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo [⏳] Dang khoi dong Stealth Engine Automation...
:: Chạy luồng On-chain ngầm 100% bằng CLI
uv run python C:\Users\Admin\Desktop\WorkSpace\Project\LangGraph_Agent_System\projects\airdrop_guerrilla\src\modes\full_auto_cli.py

echo.
echo ✅ HOAN TAT PHIEN CAY CUOC!
echo (Cua so nay se tu dong dong sau 15 giay...)
timeout /t 15 >nul