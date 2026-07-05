import os
import sys
import json
import time
import psutil
from pathlib import Path

class ProcessWatchdog:
    """
    💊 ĐẶC VỤ Y TẾ (Sovereign Process Watchdog)
    Nhiệm vụ: Giám sát, bảo vệ tài nguyên Xeon.
    Quy tắc:
    - RAM > 2GB (2048MB) -> KILL.
    - Treo > 60s -> KILL.
    - Ghi tội danh vào `logs/FAILED_PATHS.json`.
    """
    def __init__(self, max_ram_mb: float = 2048.0, max_timeout_s: float = 60.0):
        self.max_ram_mb = max_ram_mb
        self.max_timeout_s = max_timeout_s
        self.root_dir = Path(__file__).resolve().parent.parent
        self.failed_paths_file = self.root_dir / "logs" / "FAILED_PATHS.json"
        self.failed_paths_file.parent.mkdir(parents=True, exist_ok=True)

    def log_failure(self, reason: str):
        """Ghi tội danh của tiến trình bị trảm vào FAILED_PATHS.json."""
        log_data = {"failure_logs": []}
        if self.failed_paths_file.exists():
            try:
                with open(self.failed_paths_file, "r", encoding="utf-8") as f:
                    log_data = json.load(f)
            except Exception:
                pass
        
        log_data["failure_logs"].append(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {reason}")
        
        # Đảm bảo lưu an toàn
        temp_file = self.failed_paths_file.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=4, ensure_ascii=False)
        os.replace(temp_file, self.failed_paths_file)
        print(f"📝 [Watchdog] Đã ghi nhận thất bại vào FAILED_PATHS.json")

    def monitor_pid(self, pid: int) -> bool:
        """
        Giám sát một tiến trình và TOÀN BỘ tiến trình con của nó.
        Trả về True nếu an toàn, False nếu có tiến trình bị KILL.
        """
        try:
            main_process = psutil.Process(pid)
            start_time = time.time()
            
            while main_process.is_running():
                # Danh sách các tiến trình cần kiểm tra (cha + con)
                try:
                    processes_to_check = [main_process] + main_process.children(recursive=True)
                except Exception:
                    processes_to_check = [main_process]

                for proc in processes_to_check:
                    try:
                        # Check Timeout (Dựa trên thời gian bắt đầu của Watchdog)
                        elapsed_time = time.time() - start_time
                        if elapsed_time > self.max_timeout_s:
                            msg = f"Tiến trình {proc.pid} ({proc.name()}) thuộc cụm {pid} bị TREO quá {self.max_timeout_s}s."
                            print(f"🚨 [Watchdog] KILL: {msg}")
                            proc.kill()
                            self.log_failure(msg)
                            return False
                        
                        # Check RAM
                        mem_info = proc.memory_info()
                        ram_mb = mem_info.rss / 1024 / 1024
                        if ram_mb > self.max_ram_mb:
                            msg = f"Tiến trình {proc.pid} ({proc.name()}) NUỐT QUÁ GIỚI HẠN RAM ({ram_mb:.2f}MB > {self.max_ram_mb}MB)."
                            print(f"🚨 [Watchdog] KILL: {msg}")
                            proc.kill()
                            self.log_failure(msg)
                            return False
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                time.sleep(1.0)
                
            return True
            
        except psutil.NoSuchProcess:
            return True
        except Exception as e:
            print(f"⚠️ [Watchdog] Lỗi khi giám sát {pid}: {e}")
            return True

watchdog = ProcessWatchdog()
