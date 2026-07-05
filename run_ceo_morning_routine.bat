@echo off
title CEO Morning Routine - LangGraph Agent System
color 0A

echo ========================================================
echo   LANGGRAPH AGENT SYSTEM - CEO MORNING ROUTINE
echo ========================================================
echo.

:: Đảm bảo đang đứng ở thư mục gốc
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf8

:: Chạy script bằng môi trường uv (hoặc .venv)
echo Dang khoi dong CEO Agent...
.venv\Scripts\python.exe projects\ceo_agent\ceo_morning_routine.py

echo.
pause
