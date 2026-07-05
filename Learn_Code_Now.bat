@echo off
title Sovereign Academy - 1 Click Code Tutor
color 0A

:: Chuyển đến thư mục chứa file .bat này (gốc dự án)
cd /d "%~dp0"

echo =======================================================
echo    KHOI DONG SOVEREIGN ACADEMY (1-CLICK LEARNING)
echo =======================================================
echo.
echo Dang kiem tra bai tap can on...
echo.

uv run python -X utf8 projects/sovereign_academy/one_click_learn.py

echo.
pause
