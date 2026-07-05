#!/usr/bin/env python3
"""
Sovereign Daily Routine - Kịch bản chạy hàng ngày (vd: 06:00 AM)
Đóng gói các tác vụ sinh tồn, làm sạch hệ thống, đồng bộ tri thức và xuất báo cáo.
Có thể chạy độc lập qua CLI hoặc gọi từ Telegram Bot.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# UTF-8 fix for Windows (anti-crash on emoji/vietnamese)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

# Add root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# [ANTI-BOMB] Redirect verbose subprocess output to log file instead of stdout
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
ROUTINE_LOG = LOG_DIR / "daily_routine.log"


def _write_log(content: str):
    """Ghi output vào log file, không in ra stdout để tránh Token Amplification."""
    with open(ROUTINE_LOG, "a", encoding="utf-8") as f:
        f.write(content + "\n")


def print_step(title):
    print(f"\n{'='*50}\n[STEP] {title}\n{'='*50}")
    _write_log(f"\n{'='*50}\n[STEP] {title}\n{'='*50}")


def run_command(cmd, cwd=None):
    """Chạy lệnh subprocess, redirect toàn bộ output sang log file.
    Chỉ in summary (pass/fail + tail) ra stdout."""
    cmd_str = " ".join(str(c) for c in cmd)
    try:
        result = subprocess.run(
            cmd, cwd=cwd or ROOT_DIR,
            capture_output=True, text=True, check=True,
            encoding="utf-8", errors="replace"
        )
        _write_log(f"[CMD] {cmd_str}\n{result.stdout}")
        # [ANTI-BOMB] Chỉ in 3 dòng cuối làm summary
        tail = result.stdout.strip().splitlines()[-3:] if result.stdout.strip() else []
        print(f"  ✅ OK | Tail: {' | '.join(tail)}")
        return True
    except subprocess.CalledProcessError as e:
        _write_log(f"[CMD-FAIL] {cmd_str}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
        tail = (e.stderr or e.stdout or "").strip().splitlines()[-3:]
        print(f"  ❌ FAIL | Tail: {' | '.join(tail)}")
        return False

def main():
    print(f"[SOVEREIGN] BAT DAU DAILY ROUTINE [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

    # 1. Health & Security Scan
    print_step("Health & Security Scan")
    run_command([sys.executable, "tools/system/health_check.py"])
    run_command([sys.executable, "tools/system/workflow_engine.py", "--chain", "deep_audit"])
    run_command([sys.executable, "tools/system/workflow_engine.py", "--run", "compliance_check"])

    # 2. Code Health Scan (Static Analysis)
    print_step("Code Health Scan (Static Analysis 5-Layer)")
    run_command([sys.executable, "tools/system/code_health_sentinel.py", "--fix"])

    # 3. Intelligence Sync & Context Optimize
    print_step("Intelligence Sync (RAG) & Context Optimize")
    run_command([sys.executable, "tools/system/workflow_engine.py", "--run", "rag_ingest"])
    run_command([sys.executable, "tools/system/workflow_engine.py", "--run", "context_optimize"])

    # 4. Data Ingestion (Universal Game Vault)
    print_step("Data Ingestion (Universal Game Vault - OCR/Crawl)")
    try:
        from projects.universal_game_vault.src.processors.lore_ingest_pipeline import LoreIngestionAgent
        agent = LoreIngestionAgent()
        target_dir = ROOT_DIR / "data" / "morimens" / "raw" / "screenshots"
        if target_dir.exists():
            agent.ingest_from_images(str(target_dir))
        else:
            print("Khong tim thay du lieu anh moi de Ingest.")
    except Exception as e:
        print(f"Loi khi chay Lore Ingest: {e}")

    # 5. System Cleanup
    print_step("System Cleanup (Don rac log/cache)")
    cleanup_script = ROOT_DIR / "tools" / "system" / "system_cleaner.py"
    if cleanup_script.exists():
         run_command([sys.executable, "tools/system/system_cleaner.py", "--run"])
    else:
        print("Bo qua System Cleaner (chua kich hoat mode tu dong).")

    # 6. Kaizen Evolution (Tien hoa 1%)
    print_step("Kaizen Evolution (Tu sinh Unit Test & Cam nhan AI)")
    run_command([sys.executable, "tools/system/workflow_engine.py", "--run", "kaizen_evolution"])

    # 7. Financial & Morning Briefing
    print_step("Morning Briefing & Telegram Report")
    run_command([sys.executable, "tools/system/awaken.py"])

    print(f"\n[SOVEREIGN] HOAN TAT DAILY ROUTINE [{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")

if __name__ == "__main__":
    main()