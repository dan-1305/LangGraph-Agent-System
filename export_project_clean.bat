@echo off
echo ========================================================
echo   LangGraph Agent System - CLEAN EXPORT SCRIPT
echo ========================================================
echo.
echo Script nay se tao ra mot file ZIP sieu nhe cua du an.
echo No se tu dong loai bo .venv, __pycache__, models/, va cac file rac
echo da duoc dinh nghia trong file .gitignore.
echo.

REM Kiem tra xem Git co duoc cai dat khong
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git khong duoc cai dat tren may nay! Vui long cai Git de chay script.
    pause
    exit /b
)

REM Ten file dau ra
set OUTPUT_FILE=LangGraph_Project_Clean.zip

echo [1/3] Dang don dep __pycache__ va cac thu muc rac con xot lai...
REM Dung git clean de xoa bot rac un-tracked neu can, nhung de an toan ta chi dung git archive.

echo [2/3] Dang dong goi du an vao %OUTPUT_FILE% bang thuat toan cua Git...
REM git archive tu dong bo qua cac file trong .gitignore
git archive --format=zip HEAD -o %OUTPUT_FILE%

if %errorlevel% neq 0 (
    echo [ERROR] Co loi xay ra khi dong goi. Hay chac chan ban da commit cac thay doi gan nhat.
    echo Meo: Chay lenh git add roi git commit truoc khi chay script nay.
    pause
    exit /b
)

echo [3/3] Dong goi hoan tat!
echo.
echo ========================================================
echo THANH CONG! File cua ban la: %OUTPUT_FILE%
echo Ban co the mang file ZIP nay chia se cho ban be hoac deploy.
echo ========================================================
pause
