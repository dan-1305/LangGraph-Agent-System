import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from projects.ceo_agent.admin_simulator import AdminSimulator

def run():
    print("--- BẮT ĐẦU CEO SIMULATOR V2 ---")
    sim = AdminSimulator()
    sim.name = "AdminSimulator"
    sim.role = "Simulator"
    results = []
    
    # Simulate a few turns
    for i in range(4):
        crisis = sim.get_next_crisis()
        print(f"\n[Turn {crisis['turn']}] Khủng hoảng: {crisis['system_alert']}")
        
        # Artificial Intelligence Decision Logic (Simulated)
        action = crisis["best_action"]
        target = crisis["target_param"]
        
        # Let's purposefully make a mistake on Turn 2 to test the Failure Memory
        if i == 1:
            action = "kill_process"
            target = "main_scheduler"
            
        result = sim.evaluate_decision(crisis["crisis_id"], action, target)
        print(f"CEO Action: {action} on {target}")
        print(f"Result: {result['status']} - {result['feedback']}")
        
        if result["status"] in ["FAILED", "FATAL"]:
            results.append(f"[{crisis['crisis_id']}] CEO Action {action} on {target} -> {result['status']}: {result['feedback']}")
            
    # Save to FAILED_PATHS.json
    failed_path = "logs/FAILED_PATHS.json"
    os.makedirs("logs", exist_ok=True)
    
    existing_failures = []
    if os.path.exists(failed_path):
        with open(failed_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                existing_failures = data.get("failure_logs", [])
            except Exception:
                pass
                
    # Extend and save
    existing_failures.extend(results)
    with open(failed_path, "w", encoding="utf-8") as f:
        json.dump({"failure_logs": list(set(existing_failures))}, f, indent=4, ensure_ascii=False)
        
    print(f"\n--- HOÀN TẤT SIMULATOR. Đã ghi nhận {len(results)} sai lầm vào FAILED_PATHS.json ---")

if __name__ == "__main__":
    run()
