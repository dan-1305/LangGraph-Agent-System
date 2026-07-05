@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf8
set PYTHONPATH=%PYTHONPATH%;%CD%
echo ==========================================================
echo    🚀 KICH HOAT SCHEDULER TONG HOP V2 (SMART CATCH-UP) 🚀
echo ==========================================================
echo Dang khoi chay Scheduler...

uv run python scheduler/main_scheduler.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ [LOI] Scheduler bi dung dot ngot.
    pause
)
