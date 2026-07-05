import json
import time
from datetime import datetime
from pathlib import Path
from functools import wraps

class VideoTelemetry:
    def __init__(self, log_file: str = "logs/video_pipeline.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.current_run_id = None
        self.events = []

    def start_run(self, run_id: str = None):
        self.current_run_id = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.events = []
        return self.current_run_id

    def log_event(self, step_name: str, start_time: float, end_time: float):
        if not self.current_run_id:
            self.start_run()
            
        event = {
            "run_id": self.current_run_id,
            "step": step_name,
            "start_time": start_time,
            "end_time": end_time,
            "duration_seconds": round(end_time - start_time, 2),
            "timestamp": datetime.now().isoformat()
        }
        self.events.append(event)
        self._save_to_disk()

    def _save_to_disk(self):
        try:
            # Read existing logs if any
            existing_data = []
            if self.log_file.exists():
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    try:
                        existing_data = json.load(f)
                    except json.JSONDecodeError:
                        existing_data = []
                        
            # Append new events
            existing_data.extend(self.events)
            
            # Keep only the last 100 events to prevent massive file sizes
            existing_data = existing_data[-100:]
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4)
                
            # Clear local events after saving so we don't duplicate on next save
            self.events = []
        except Exception as e:
            print(f"[Telemetry Error] Failed to save log: {e}")

telemetry = VideoTelemetry()

def measure_latency(step_name: str):
    """
    Decorator to automatically measure the latency of a function and log it.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.time()
                telemetry.log_event(step_name, start_time, end_time)
        return wrapper
    return decorator
