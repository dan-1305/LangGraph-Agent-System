@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf8
title Khởi động Hệ thống AI Mì Ăn Liền
color 0A
echo.
echo ==============================================================
echo        HỆ THỐNG ĐANG KHỞI ĐỘNG - VUI LÒNG ĐỢI GIÂY LÁT...
echo ==============================================================
echo.

:: 1. Kiem tra xem co 'uv' hoac python chua
where uv >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] Phat hien trinh quan ly 'uv'. Dang cap nhat moi truong...
    :: uv sync tu dong doc pyproject.toml va cai the thieu
    call uv sync >nul 2>nul
    
    echo [OK] Đang khởi động Local Proxy Server (Hạ tầng API)...
    start /b uv run python projects/local_proxy_server/main.py >nul 2>nul
    
    :: Đợi proxy khởi động
    timeout /t 2 >nul
    
    echo [OK] Đang kích hoạt Master Dashboard...
    :: Chay ngam bang pythonw.exe hoac bat tab an
    start /b uv run streamlit run web_dashboard.py --server.headless true >nul 2>nul
    
    echo.
    echo Hoan tat! Giao dien se tu mo tren trinh duyet cua ban.
    echo (Neu khong tu mo, hay truy cap: http://localhost:8501)
    timeout /t 3 >nul
    exit
) else (
    echo [CANH BAO] Khong tim thay 'uv'. Dang thu tim kiem 'python' thuong...
    where python >nul 2>nul
    if %ERRORLEVEL% equ 0 (
        echo [OK] Đã thấy 'python'. Đang cài đặt dependencies...
        pip install -r requirements.txt >nul 2>nul
        
        echo [OK] Đang khởi động Local Proxy Server...
        start /b python projects/local_proxy_server/main.py >nul 2>nul
        timeout /t 2 >nul
        
        echo [OK] Đang kích hoạt Master Dashboard...
        start /b python -m streamlit run web_dashboard.py --server.headless true >nul 2>nul
        timeout /t 3 >nul
        exit
    ) else (
        color 0C
        echo [LOI] Khong tim thay Python! 
        echo Vui long chay bang moi truong Portable Python duoc dong goi kem.
        pause
        exit /b 1
    )
)
