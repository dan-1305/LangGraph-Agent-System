@echo off
chcp 65001 >nul
echo ==================================================
echo      🤖 KÍCH HOẠT AI TRADING BẰNG TAY / TASK SCHEDULER
echo ==================================================
cd /d "%~dp0"

:: Kích hoạt môi trường ảo nếu có
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

echo.
echo [1/2] Đang cập nhật dữ liệu thị trường mới nhất...
python projects\ai_trading_agent\src\data_fetcher.py

echo.
echo [2/2] Đang gọi AI phân tích và bắn lệnh...
python projects\ai_trading_agent\live_advisor.py

echo.
echo ✅ HOÀN TẤT CHU TRÌNH GIAO DỊCH!
echo (Cửa sổ này sẽ tự động đóng sau 15 giây...)
timeout /t 15 >nul
