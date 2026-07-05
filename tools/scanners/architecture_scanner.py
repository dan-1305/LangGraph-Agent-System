import os
import ast
import json

def analyze_file(filepath):
    violations = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
            
            # Check imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in ['httpx', 'requests', 'sqlalchemy', 'sqlite3', 'psycopg2', 'pymongo']:
                            violations.append(f"Import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    if node.module in ['httpx', 'requests', 'sqlalchemy', 'sqlite3', 'psycopg2', 'pymongo']:
                        violations.append(f"ImportFrom {node.module}")
    except Exception as e:
        # Ignore syntax errors or non-python files
        pass
    
    return violations

def main():
    target_dirs = ['src/factory/nodes', 'projects']
    report = {}
    
    for target in target_dirs:
        for root, dirs, files in os.walk(target):
            # Skip infra related folders to avoid false positives
            if 'infra' in root or 'database' in root or 'executor' in root:
                continue
                
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    
                    # We are only interested in files that represent Application Logic
                    # Typically node_*.py, agent.py, logic.py
                    if 'node' in file.lower() or 'agent' in file.lower() or 'logic' in file.lower():
                        v = analyze_file(filepath)
                        if v:
                            report[filepath] = v
                            
    # Save report
    os.makedirs('reports', exist_ok=True)
    with open('reports/architecture_violations.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=4)
        
        print(f"[SUCCESS] Da quet xong. Phat hien {len(report)} file vi pham.")
        for k, v in report.items():
            print(f" - {k}: {v}")

if __name__ == '__main__':
    main()
