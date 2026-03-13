@echo off
REM ======================================================================
REM WINDOWS TASK SCHEDULER SETUP FOR AI TRADING AGENT
REM ======================================================================
REM 
REM This script sets up automated tasks for 24/7 trading operations
REM Run as Administrator
REM ======================================================================

echo.
echo ============================================================
echo   SETUP WINDOWS TASK SCHEDULER - AI TRADING AGENT
echo ============================================================
echo.

REM Get current directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=python"

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run this script as Administrator!
    echo        Right-click the file and select "Run as administrator"
    pause
    exit /b 1
)

echo [1/5] Setting up Data Fetcher Task (Every 1 hour)...
schtasks /create /tn "AI_Trading_Data_Fetcher" ^
    /tr "%PYTHON_EXE% \"%SCRIPT_DIR%data_fetcher.py\"" ^
    /sc hourly ^
    /st 00:00 ^
    /ru SYSTEM ^
    /f

if %errorLevel% equ 0 (
    echo     [OK] Data Fetcher task created successfully
) else (
    echo     [ERROR] Failed to create Data Fetcher task
)

echo.
echo [2/5] Setting up Live Advisor Task (Every 4 hours)...
schtasks /create /tn "AI_Trading_Live_Advisor" ^
    /tr "%PYTHON_EXE% \"%SCRIPT_DIR%live_advisor.py\"" ^
    /sc hourly ^
    /mo 4 ^
    /st 00:00 ^
    /ru SYSTEM ^
    /f

if %errorLevel% equ 0 (
    echo     [OK] Live Advisor task created successfully
) else (
    echo     [ERROR] Failed to create Live Advisor task
)

echo.
echo [3/5] Setting up News Scraper Task (Every 2 hours)...
schtasks /create /tn "AI_Trading_News_Scraper" ^
    /tr "%PYTHON_EXE% \"%SCRIPT_DIR%news_scraper.py\"" ^
    /sc hourly ^
    /mo 2 ^
    /st 00:00 ^
    /ru SYSTEM ^
    /f

if %errorLevel% equ 0 (
    echo     [OK] News Scraper task created successfully
) else (
    echo     [ERROR] Failed to create News Scraper task
)

echo.
echo [4/5] Setting up Backtest Task (Daily at 02:00)...
schtasks /create /tn "AI_Trading_Daily_Backtest" ^
    /tr "%PYTHON_EXE% \"%SCRIPT_DIR%backtester.py\"" ^
    /sc daily ^
    /st 02:00 ^
    /ru SYSTEM ^
    /f

if %errorLevel% equ 0 (
    echo     [OK] Daily Backtest task created successfully
) else (
    echo     [ERROR] Failed to create Backtest task
)

echo.
echo [5/5] Setting up System Update Log Task (Daily at 06:00)...
schtasks /create /tn "AI_Trading_System_Log" ^
    /tr "\"%SCRIPT_DIR%..\..\dashboard.py\" 10" ^
    /sc daily ^
    /st 06:00 ^
    /ru SYSTEM ^
    /f

if %errorLevel% equ 0 (
    echo     [OK] System Log task created successfully
) else (
    echo     [ERROR] Failed to create System Log task
)

echo.
echo ============================================================
echo   TASK SCHEDULER SETUP COMPLETE!
echo ============================================================
echo.
echo Scheduled Tasks:
echo   - AI_Trading_Data_Fetcher      : Every 1 hour (Data update)
echo   - AI_Trading_Live_Advisor      : Every 4 hours (Trading signals)
echo   - AI_Trading_News_Scraper      : Every 2 hours (News update)
echo   - AI_Trading_Daily_Backtest    : Daily 02:00 (Backtest)
echo   - AI_Trading_System_Log        : Daily 06:00 (System log)
echo.
echo To view tasks: Open Task Scheduler (taskschd.msc)
echo To remove tasks: Run remove_scheduler.bat
echo.
pause