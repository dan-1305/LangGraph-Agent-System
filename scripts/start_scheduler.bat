@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf8
cd /d "%~dp0\.."
uv run python scheduler/main_scheduler.py
