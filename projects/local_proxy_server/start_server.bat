@echo off
REM ==============================================================================
REM Quick Start Script for Local Proxy Server
REM ==============================================================================

echo ==============================================================================
echo   Starting Local Proxy Server for Gemini API
echo ==============================================================================
echo.

REM Check if .env exists in parent directory
if exist "..\..\.env" (
    echo   Found .env file in parent directory
) else (
    echo   WARNING: .env file not found!
    echo   Please create a .env file with your GEMINI_API_KEY
    echo   Run: copy .env.example .env
    echo   Then edit .env to add your API key
    echo.
    pause
    exit /b 1
)

REM Start the server
echo   Starting server on http://0.0.0.0:8000
echo   Press Ctrl+C to stop
echo.
echo ==============================================================================
echo.

uv run main.py

pause