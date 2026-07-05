@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf8

echo ========================================
echo   Gemini CLI Demo
echo ========================================
echo.
echo Đảm bảo bạn đã thêm API key vào root .env file:
echo   GCLI_API_KEY=your_actual_api_key_here
echo.
echo Các lệnh demo:
echo.
echo 1. Basic usage:
echo    uv run python main.py "Hello, world!"
echo.
echo 2. Use specific model:
echo    uv run python main.py "Explain quantum computing" --model gemini-1.5-pro
echo.
echo 3. Pipe input:
echo    echo "What is Python?" | uv run python main.py
echo.
echo ========================================
echo.
pause