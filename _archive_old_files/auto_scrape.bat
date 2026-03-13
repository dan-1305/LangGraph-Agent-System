@echo off
setlocal enabledelayedexpansion

:: Cấu hình đường dẫn
set VENV_PATH=.\.venv\Scripts\python.exe
set SCRIPT_PATH=projects/universal_web_scraper/src/alonhadat_parser.py
set TOTAL_RUNS=10
set DELAY_SECONDS=1800

echo ======================================================
echo    KHOI DONG CHIEN DICH CAO DU KICH (BATCH MODE)
echo    Muc tieu: Chay %TOTAL_RUNS% lan - Moi lan cach nhau 30 phut
echo ======================================================

for /L %%i in (1,1,%TOTAL_RUNS%) do (
    echo.
    echo [!date! !time!] Dang thuc hien lan chay thu %%i/%TOTAL_RUNS%...
    
    :: Chạy script cào dữ liệu
    %VENV_PATH% %SCRIPT_PATH%
    
    if %%i lss %TOTAL_RUNS% (
        echo.
        echo Da xong lan %%i. Dang nghi %DELAY_SECONDS% giay de tàng hình...
        echo Nhan Ctrl+C neu muon dung han.
        timeout /t %DELAY_SECONDS% /nobreak
    ) else (
        echo ======================================================
        echo    DA HOAN THANH DU %TOTAL_RUNS% LAN CHAY. HE THONG TU NGAT.
        echo ======================================================
    )
)

pause