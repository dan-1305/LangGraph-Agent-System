@echo off
title 👑 SOVEREIGN VRIEU - SETUP WINDOWS STARTUP
chcp 65001 >nul
echo ============================================================
echo THIET LAP TU DONG KHOI CHAY SOVEREIGN TERMINAL
echo ============================================================
echo.

set "SCRIPT_PATH=%~dp0run_all.bat"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\Sovereign_Terminal_Master.lnk"

echo Dang tao loi tat (Shortcut) tai: 
echo %SHORTCUT_PATH%
echo.

:: Dung PowerShell de tao shortcut
powershell -Command "$wshell = New-Object -ComObject WScript.Shell; $shortcut = $wshell.CreateShortcut('%SHORTCUT_PATH%'); $shortcut.TargetPath = '%SCRIPT_PATH%'; $shortcut.WorkingDirectory = '%~dp0'; $shortcut.Description = 'Khoi dong Sovereign Enterprise System'; $shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo ✅ Thanh cong! He thong se tu dong chay khi Windows khoi dong.
) else (
    echo ❌ That bai! Vui long kiem tra quyen Admin.
)

echo.
pause
