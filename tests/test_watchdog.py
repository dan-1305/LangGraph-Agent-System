import pytest
import os
import json
import time
import subprocess
import sys
from pathlib import Path
from core.process_watchdog import watchdog

@pytest.mark.asyncio
async def test_watchdog_kill_memory_leak():
    """
    Test Case: Verify Watchdog kills a process that exceeds RAM limit (2GB).
    """
    # 1. Chuẩn bị script rác gây leak RAM
    leak_script = Path("tmp/leak_for_test.py")
    leak_script.parent.mkdir(parents=True, exist_ok=True)
    with open(leak_script, "w", encoding="utf-8") as f:
        f.write("import time\n")
        f.write("data = []\n")
        f.write("while True:\n")
        f.write("    data.append(' ' * (1024 * 1024 * 50)) # 50MB leak\n")
        f.write("    time.sleep(0.1)\n")

    # 2. Xóa log cũ để test chính xác
    failed_paths_file = Path("logs/FAILED_PATHS.json")
    initial_log_count = 0
    if failed_paths_file.exists():
        with open(failed_paths_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                initial_log_count = len(data.get("failure_logs", []))
            except:
                pass

    # 3. Khởi chạy tiến trình rác
    proc = subprocess.Popen([sys.executable, str(leak_script)])
    pid = proc.pid
    print(f"\n[Test] Started leak process with PID: {pid}")

    # 4. Chạy Watchdog giám sát PID này (Watchdog có max_ram_mb=2048)
    # Ta sẽ chạy monitor_pid và nó sẽ chặn (block) cho đến khi kill xong
    is_safe = watchdog.monitor_pid(pid)

    # 5. Kiểm chứng (Assertions)
    assert is_safe is False, "Watchdog should have killed the process"
    
    # Kiểm tra xem tiến trình đã thực sự chết chưa
    import psutil
    assert not psutil.pid_exists(pid), "Process should be terminated"

    # Kiểm tra log
    with open(failed_paths_file, "r", encoding="utf-8") as f:
        new_data = json.load(f)
        new_log_count = len(new_data.get("failure_logs", []))
        assert new_log_count > initial_log_count, "New failure log should be recorded"
        latest_log = new_data["failure_logs"][-1]
        assert "NUỐT QUÁ GIỚI HẠN RAM" in latest_log, "Log reason should be RAM leak"

    print("[Test] Watchdog Test PASSED perfectly.")
