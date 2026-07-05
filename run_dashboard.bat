@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf8

echo ===================================================
echo   KHOI DONG JARVIS OBSERVABILITY DASHBOARD
echo ===================================================
echo.
echo Dang mo Streamlit UI tren trinh duyet...

uv run streamlit run tools/ui/dashboard_app.py

pause
