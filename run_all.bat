@echo off
title SOVEREIGN VRIEU - MASTER STARTUP
chcp 65001 >nul
set PYTHONIOENCODING=utf8

echo ============================================================
echo 👑 SOVEREIGN ENTERPRISE SYSTEM - STARTING UP...
echo ============================================================

:: 1. Start Local Proxy Server in background
echo [+] Khoi dong Local Proxy Server (Port 8001)...
start /B uv run python -m projects.local_proxy_server.main

:: 2. Wait for Proxy to be ready
timeout /t 5 >nul

:: 3. Start Enterprise Dashboard V2
echo [+] Khoi dong Enterprise Dashboard...
start /B uv run streamlit run web_dashboard_v2.py --server.port 8501

:: 4. Start Master Scheduler
echo [+] Khoi dong He thong Lap lich (Scheduler)...
start /B uv run python scheduler/main_scheduler.py

:: 5. Start Sovereign Terminal (Telegram Bot & Daemon)
echo [+] Khoi dong Sovereign Terminal (ChatOps and Daemon)...
start "Sovereign Telegram Bot" uv run python projects/sovereign_terminal/gateways/telegram_bot.py
start "Sovereign Daemon" uv run python projects/sovereign_terminal/daemon.py

:: 6. Start Sovereign Daily Routine (Auto-evolve on boot)
echo [+] Khoi dong Daily Routine (Kaizen Evolution & Auto-Maintenance)...
start /B uv run python scripts/run_daily_routine.py

echo ============================================================
echo ✅ VUONG TRIEU DA SAN SANG!
echo 📊 Dashboard: http://localhost:8501
echo 🔌 Proxy: http://localhost:8001
echo 💊 Watchdog: ACTIVE
echo ============================================================
echo Bam bat ky phim nao de dong cua so nay (He thong van chay ngam).
pause >nul
