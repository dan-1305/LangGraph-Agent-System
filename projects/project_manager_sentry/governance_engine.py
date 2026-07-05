import os
import sqlite3
import json

class SovereignGovernance:
    def __init__(self):
        self.db_path = "reports/SYSTEM_MAP_METADATA.db"

    def check_edit_permission(self, agent_name, file_path):
        """
        Kiểm tra xem một Agent có quyền sửa file dựa trên OWNERS.json.
        """
        # Find project name from path
        parts = file_path.split(os.sep)
        if "projects" not in parts:
            return True, "Core file - CEO only"
            
        project_name = parts[parts.index("projects") + 1]
        owner_file = os.path.join("projects", project_name, "OWNERS.json")
        
        if not os.path.exists(owner_file):
            return True, "No owner defined - Public domain"

        with open(owner_file, "r") as f:
            owners = json.load(f)
            primary = owners.get("primary_agent", "Unassigned")
            allowed = owners.get("allowed_agents", [])
            
            if agent_name == primary or agent_name in allowed or agent_name == "CEO":
                return True, f"Permission granted to {agent_name}"
            else:
                return False, f"Permission denied. Owner is {primary}"

    def lock_sovereign_project(self, project_name):
        """
        Khóa các project L3 để ngăn chặn thay đổi ngoài ý muốn.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE projects SET status = 'LOCKED' WHERE name = ? AND maturity_level = 'L3'", (project_name,))
        conn.commit()
        conn.close()
        return f"Project {project_name} (L3) is now LOCKED."

if __name__ == "__main__":
    gov = SovereignGovernance()
    print("--- GOVERNANCE ENGINE READY ---")
    # Example check
    # print(gov.check_edit_permission("Cline", "projects/ai_trading_agent/src/main.py"))
