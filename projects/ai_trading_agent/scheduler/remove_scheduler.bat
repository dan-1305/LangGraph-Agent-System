@echo off
REM ======================================================================
REM REMOVE WINDOWS TASK SCHEDULER TASKS - AI TRADING AGENT
REM ======================================================================
REM 
REM This script removes all automated tasks created by setup_scheduler.bat
REM Run as Administrator
REM ======================================================================

echo.
echo ============================================================
echo   REMOVE WINDOWS TASK SCHEDULER - AI TRADING AGENT
echo ============================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run this script as Administrator!
    echo        Right-click the file and select "Run as administrator"
    pause
    exit /b 1
)

echo [1/5] Removing Data Fetcher Task...
schtasks /delete /tn "AI_Trading_Data_Fetcher" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo     [OK] Data Fetcher task removed
) else (
    echo     [SKIP] Data Fetcher task not found or already removed
)

echo [2/5] Removing Live Advisor Task...
schtasks /delete /tn "AI_Trading_Live_Advisor" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo     [OK] Live Advisor task removed
) else (
    echo     [SKIP] Live Advisor task not found or already removed
)

echo [3/5] Removing News Scraper Task...
schtasks /delete /tn "AI_Trading_News_Scraper" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo     [OK] News Scraper task removed
) else (
    echo     [SKIP] News Scraper task not found or already removed
)

echo [4/5] Removing Daily Backtest Task...
schtasks /delete /tn "AI_Trading_Daily_Backtest" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo     [OK] Daily Backtest task removed
) else (
    echo     [SKIP] Daily Backtest task not found or already removed
)

echo [5/5] Removing System Log Task...
schtasks /delete /tn "AI_Trading_System_Log" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo     [OK] System Log task removed
) else (
    echo     [SKIP] System Log task not found or already removed
)

echo.
echo ============================================================
echo   ALL TASKS REMOVED SUCCESSFULLY!
echo ============================================================
echo.
echo To recreate tasks: Run setup_scheduler.bat as Administrator
echo.
pause