import os
import sqlite3
import ast
import json
from datetime import datetime

def analyze_dependencies(project_path):
    """
    Phân tích các lệnh import để tìm sự phụ thuộc giữa các project.
    """
    dependencies = set()
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        tree = ast.parse(f.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    if "projects." in alias.name:
                                        dependencies.add(alias.name.split(".")[1])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module and "projects." in node.name:
                                    dependencies.add(node.module.split(".")[1])
                except Exception:
                    continue
    return list(dependencies)

def index_monorepo_v2():
    db_path = "reports/SYSTEM_MAP_METADATA.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Tables
    cursor.execute("DROP TABLE IF EXISTS projects")
    cursor.execute("DROP TABLE IF EXISTS project_dependencies")
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        path TEXT,
        status TEXT,
        maturity_level TEXT DEFAULT 'L1',
        owner_agent TEXT,
        is_priority INTEGER DEFAULT 0,
        last_indexed TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS project_dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        depends_on_project_id INTEGER,
        FOREIGN KEY (project_id) REFERENCES projects (id),
        FOREIGN KEY (depends_on_project_id) REFERENCES projects (id)
    )
    ''')

    project_root = "projects"
    project_dirs = [d for d in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, d))]

    # Phase 1: Index Projects & Owners
    for name in project_dirs:
        path = os.path.join(project_root, name)
        owner_file = os.path.join(path, "OWNERS.json")
        owner = "Unassigned"
        
        if os.path.exists(owner_file):
            try:
                with open(owner_file, "r") as f:
                    owner = json.load(f).get("primary_agent", "Unassigned")
            except: pass

        cursor.execute('''
        INSERT OR REPLACE INTO projects (name, path, status, owner_agent, is_priority, last_indexed)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, path, "ACTIVE", owner, 0, datetime.now().isoformat()))

    # Phase 2: Map Dependencies
    cursor.execute("SELECT id, name, path FROM projects")
    all_projs = cursor.fetchall()
    name_to_id = {name: pid for pid, name, _ in all_projs}

    for pid, name, path in all_projs:
        deps = analyze_dependencies(path)
        for dep_name in deps:
            if dep_name in name_to_id:
                cursor.execute('''
                INSERT OR IGNORE INTO project_dependencies (project_id, depends_on_project_id)
                VALUES (?, ?)
                ''', (pid, name_to_id[dep_name]))

    conn.commit()
    conn.close()
    print(f"Indexing V2 complete. Dependency Graph saved to {db_path}")

if __name__ == "__main__":
    index_monorepo_v2()
