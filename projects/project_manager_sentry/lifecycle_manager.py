import os
import sqlite3
from datetime import datetime, timedelta

def evaluate_monorepo_health():
    db_path = "reports/SYSTEM_MAP_METADATA.db"
    if not os.path.exists(db_path):
        print("Metadata DB not found. Run indexer first.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Add maturity_level column if not exists
    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN maturity_level TEXT DEFAULT 'L1'")
    except sqlite3.OperationalError:
        pass # Already exists
        
    try:
        cursor.execute("ALTER TABLE projects ADD COLUMN health_score REAL DEFAULT 0")
    except sqlite3.OperationalError:
        pass # Already exists

    cursor.execute("SELECT id, name, path FROM projects")
    projects = cursor.fetchall()

    audit_report = ["# 🩺 MONOREPO HEALTH AUDIT REPORT", f"> Date: {datetime.now().isoformat()}", ""]
    audit_report.append("| Project Name | Maturity | Score | Status | Issues |")
    audit_report.append("| :--- | :--- | :--- | :--- | :--- |")

    for p_id, name, path in projects:
        if not os.path.exists(path):
            continue
            
        score = 0
        issues = []
        
        # Criterion 1: BaseAgent inheritance
        has_base_agent = False
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        if "BaseAgent" in f.read():
                            has_base_agent = True
                            break
            if has_base_agent: break
        
        if has_base_agent:
            score += 40
        else:
            issues.append("Missing BaseAgent")

        # Criterion 2: README existence
        if os.path.exists(os.path.join(path, "README.md")):
            score += 20
        else:
            issues.append("No README")

        # Criterion 3: Tests existence
        test_dir = os.path.join(path, "tests")
        if os.path.exists(test_dir) or any("test_" in f for f in os.listdir(path)):
            score += 20
        else:
            issues.append("No Tests")

        # Criterion 4: Dockerization (L3)
        if os.path.exists(os.path.join(path, "Dockerfile")):
            score += 20
        
        # Determine Level
        level = "L1"
        if score >= 80: level = "L3"
        elif score >= 60: level = "L2"
        
        status = "HEALTHY" if score >= 60 else "NEEDS ATTENTION"
        if score < 40: status = "CRITICAL / DORMANT"

        cursor.execute("UPDATE projects SET maturity_level = ?, health_score = ? WHERE id = ?", (level, score, p_id))
        
        audit_report.append(f"| {name} | {level} | {score} | {status} | {', '.join(issues) if issues else 'None'} |")

    conn.commit()
    conn.close()

    report_path = "reports/MONOREPO_HEALTH_AUDIT.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(audit_report))

    print(f"Health Audit complete. Report saved to {report_path}")

if __name__ == "__main__":
    evaluate_monorepo_health()
