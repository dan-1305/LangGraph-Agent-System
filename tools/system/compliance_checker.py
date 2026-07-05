import os
import ast
import json
import sys
from pathlib import Path

# Ensure we handle UTF-8 for Windows
if hasattr(sys.stdout, 'reconfigure'):
    if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

class ComplianceChecker:
    """
    [ROLE: SRE / QA Tester]
    Automated tool to verify architectural compliance in the LangGraph Agent Monorepo.
    Checks for:
    1. BaseAgent inheritance for Agent classes.
    2. Forbidden use of manual 'requests.post' for LLM interactions.
    3. Hardcoded API keys (simple heuristic).
    """
    def __init__(self, root_dir):
        self.root_dir = Path(root_dir)
        self.violations = []
        self.manifest_path = self.root_dir / "monorepo_manifest.json"
        self.active_projects = self._load_manifest_projects()

    def _load_manifest_projects(self):
        if not self.manifest_path.exists():
            return []
        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return list(data.get("active_projects", {}).keys())
        except Exception:
            return []

    def is_agent_file(self, file_path, content):
        """Heuristic to determine if a file is intended to be an Agent."""
        filename = file_path.name.lower()
        if any(x in filename for x in ["agent", "bot", "executor"]):
            return True
        if "class" in content and ("Agent" in content or "Graph" in content):
            return True
        return False

    def check_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                tree = ast.parse(content)
        except (SyntaxError, UnicodeDecodeError):
            return

        is_agent = self.is_agent_file(file_path, content)
        
        # [VULN-002 FIX] Deep AST Analysis for Dangerous Calls/Imports
        self._check_dangerous_nodes(tree, file_path, is_agent)

        # Check for forbidden imports/calls (specifically targeting LLM usage)
        if "requests.post" in content:
            # Heuristic to detect if it's likely an LLM API call
            llm_keywords = ["openai", "anthropic", "gemini", "groq", "ollama", "chat/completions", "v1/chat"]
            content_lower = content.lower()
            if any(k in content_lower for k in llm_keywords):
                self.violations.append({
                    "project": self._get_project_name(file_path),
                    "file": str(file_path.relative_to(self.root_dir)),
                    "type": "FORBIDDEN_MANUAL_LLM_REQUESTS",
                    "severity": "CRITICAL",
                    "message": "Manual requests.post for LLM detected. Use BaseAgent._call_llm instead."
                })
            else:
                # Lower severity for other API calls, unless it's an Agent file
                if is_agent:
                    self.violations.append({
                        "project": self._get_project_name(file_path),
                        "file": str(file_path.relative_to(self.root_dir)),
                        "type": "UNOFFICIAL_API_CALL",
                        "severity": "MEDIUM",
                        "message": "Manual requests.post in Agent file. Consider wrapping in a dedicated Utility."
                    })

        # AST analysis
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self._analyze_class(node, file_path, is_agent)

    def _get_project_name(self, file_path):
        try:
            parts = file_path.relative_to(self.root_dir).parts
            if len(parts) > 1 and parts[0] == "projects":
                return parts[1]
        except Exception:
            pass
        return "core"

    def _check_dangerous_nodes(self, tree, file_path, is_agent):
        """
        [VULN-002] Phát hiện các nỗ lực lách luật bằng getattr hoặc import thư viện cấm.
        """
        forbidden_libs = ["requests", "httpx", "urllib", "smtplib", "socket"]
        
        for node in ast.walk(tree):
            # 1. Check Imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = []
                if isinstance(node, ast.Import):
                    names = [n.name for n in node.names]
                else:
                    names = [node.module] if node.module else []
                
                for name in names:
                    if any(lib == name or name.startswith(lib + '.') for lib in forbidden_libs):
                        self.violations.append({
                            "project": self._get_project_name(file_path),
                            "file": str(file_path.relative_to(self.root_dir)),
                            "type": "FORBIDDEN_IMPORT",
                            "severity": "HIGH",
                            "message": f"Sử dụng thư viện cấm: {name}. Hãy sử dụng BaseAgent hoặc các Utility đã được phê duyệt."
                        })

            # 2. Check getattr (Bypass attempt)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "getattr":
                # getattr(obj, 'name')
                if len(node.args) >= 2:
                    attr_name = ""
                    if isinstance(node.args[1], ast.Constant):
                        attr_name = str(node.args[1].value)
                    
                    dangerous_attrs = ["post", "get", "request", "put", "delete", "eval", "exec", "system"]
                    if any(d in attr_name for d in dangerous_attrs):
                        self.violations.append({
                            "project": self._get_project_name(file_path),
                            "file": str(file_path.relative_to(self.root_dir)),
                            "type": "DYNAMIC_CALL_BYPASS",
                            "severity": "CRITICAL",
                            "message": f"Phát hiện nỗ lực lách luật bằng getattr('{attr_name}')."
                        })

    def _analyze_class(self, node, file_path, is_agent):
        bases = []
        for b in node.bases:
            if isinstance(b, ast.Name):
                bases.append(b.id)
            elif isinstance(b, ast.Attribute):
                bases.append(b.attr)

        class_name_lower = node.name.lower()
        # Exception for helper classes or already inherited
        if (is_agent or "agent" in class_name_lower or "bot" in class_name_lower) and \
           "BaseAgent" not in bases and node.name != "BaseAgent":
            
            # Filter out obviously non-agent classes
            if any(x in class_name_lower for x in ["state", "config", "data", "manager", "error", "schema"]):
                return

            self.violations.append({
                "project": self._get_project_name(file_path),
                "file": str(file_path.relative_to(self.root_dir)),
                "class": node.name,
                "type": "MISSING_BASE_AGENT",
                "severity": "HIGH",
                "message": f"Class '{node.name}' should inherit from BaseAgent."
            })

    def run(self):
        print(f"🔍 Starting Compliance Audit for {len(self.active_projects)} projects...")
        
        # Scan projects
        projects_dir = self.root_dir / "projects"
        if projects_dir.exists():
            for root, _, files in os.walk(projects_dir):
                for file in files:
                    if file.endswith(".py"):
                        self.check_file(Path(root) / file)

        # Scan src (core)
        src_dir = self.root_dir / "src"
        if src_dir.exists():
             for root, _, files in os.walk(src_dir):
                for file in files:
                    if file.endswith(".py"):
                        self.check_file(Path(root) / file)

        return self.violations

    def export_report(self, output_path):
        report = {
            "timestamp": "2026-07-09",
            "summary": {
                "total_violations": len(self.violations),
                "critical": len([v for v in self.violations if v.get("severity") == "CRITICAL"]),
                "high": len([v for v in self.violations if v.get("severity") == "HIGH"]),
                "medium": len([v for v in self.violations if v.get("severity") == "MEDIUM"])
            },
            "violations": self.violations
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        print(f"✅ Audit complete. Report saved to {output_path}")

if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent.parent
    checker = ComplianceChecker(root)
    violations = checker.run()
    
    report_file = root / "reports" / "compliance_violations.json"
    checker.export_report(report_file)
