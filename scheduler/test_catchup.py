import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from scheduler.main_scheduler import check_missed_jobs, load_state, logger
import json

# Force state to empty to trigger catch-up
state_file = os.path.join(BASE_DIR, "logs", "scheduler_state.json")
with open(state_file, "w") as f:
    json.dump({}, f)
    
print("--- RUNNING DRY-RUN CATCH-UP ---")
check_missed_jobs()
print("--- FINISHED DRY-RUN CATCH-UP ---")
