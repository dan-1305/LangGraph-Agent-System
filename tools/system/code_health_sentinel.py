#!/usr/bin/env python3
"""
Code Health Sentinel - Static Analysis Engine cho Monorepo.
Quét 5 layer: Syntax, Structure, Imports, Complexity, Security.
Output: Console summary + JSON report.
"""
import os
import sys
import ast
import json
import py_compile
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field, asdict

# UTF-8 fix for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', 'monorepo_quarantine',
             '.clineignore', 'data', 'logs', 'reports', 'temp_workspace', 'dist',
             'archive', '_archive', 'mcp_servers'}
MAX_FUNC_LINES = 100
MAX_FILE_LINES = 500
MAX_NESTING = 5


@dataclass
class Issue:
    """Một vấn đề được phát hiện."""
    layer: str
    severity: str  # CRITICAL, WARNING, INFO
    file: str
    line: int
    message: str


@dataclass
class HealthReport:
    """Báo cáo sức khỏe code tổng thể."""
    timestamp: str = ""
    total_files: int = 0
    syntax_issues: List[Issue] = field(default_factory=list)
    structure_issues: List[Issue] = field(default_factory=list)
    import_issues: List[Issue] = field(default_factory=list)
    complexity_issues: List[Issue] = field(default_factory=list)
    security_issues: List[Issue] = field(default_factory=list)
    score: float = 0.0

    @property
    def total_issues(self) -> int:
        return (len(self.syntax_issues) + len(self.structure_issues) +
                len(self.import_issues) + len(self.complexity_issues) +
                len(self.security_issues))

    @property
    def critical_count(self) -> int:
        all_issues = (self.syntax_issues + self.structure_issues +
                      self.import_issues + self.complexity_issues +
                      self.security_issues)
        return sum(1 for i in all_issues if i.severity == "CRITICAL")


def collect_python_files(root: Path) -> List[Path]:
    """Thu thập tất cả file .py trong monorepo, bỏ qua SKIP_DIRS."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith('.py'):
                files.append(Path(dirpath) / f)
    return sorted(files)


def collect_package_dirs(root: Path) -> List[Path]:
    """Tìm các thư mục nên là package (chứa .py) nhưng thiếu __init__.py."""
    missing = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        has_py = any(f.endswith('.py') for f in filenames)
        has_init = '__init__.py' in filenames
        if has_py and not has_init:
            rel = Path(dirpath).relative_to(root)
            # Bỏ qua root và các thư mục không cần package
            if str(rel) != '.' and not any(skip in str(rel) for skip in ['temp_workspace', 'tests/chaos']):
                missing.append(Path(dirpath))
    return sorted(missing)


# ─── LAYER 1: SYNTAX ───────────────────────────────────────────

def scan_syntax(files: List[Path], root: Path) -> List[Issue]:
    """L1: Kiểm tra syntax error bằng py_compile."""
    issues = []
    for f in files:
        rel = str(f.relative_to(root))
        try:
            py_compile.compile(str(f), doraise=True)
        except py_compile.PyCompileError as e:
            issues.append(Issue("L1-Syntax", "CRITICAL", rel, 0, str(e)[:200]))
        except Exception as e:
            issues.append(Issue("L1-Syntax", "CRITICAL", rel, 0, f"Compile error: {e}"))
    return issues


# ─── LAYER 2: STRUCTURE ────────────────────────────────────────

def scan_structure(root: Path) -> List[Issue]:
    """L2: Kiểm tra missing __init__.py trong package dirs."""
    issues = []
    missing = collect_package_dirs(root)
    for d in missing:
        rel = str(d.relative_to(root))
        issues.append(Issue("L2-Structure", "WARNING", rel, 0, "Missing __init__.py"))
    return issues


# ─── LAYER 3: IMPORTS ──────────────────────────────────────────

def scan_imports(files: List[Path], root: Path) -> List[Issue]:
    """L3: Phát hiện unused imports và bare imports rủi ro."""
    issues = []
    for f in files:
        rel = str(f.relative_to(root))
        try:
            content = f.read_text(encoding='utf-8', errors='replace')
            tree = ast.parse(content, filename=str(f))

            # Collect all imports
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.asname or alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for alias in node.names:
                            imports.add(alias.asname or alias.name)

            # Check if imported names appear elsewhere in code (rough heuristic)
            # Remove import lines, then search for name usage
            lines = content.split('\n')
            code_lines = []
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if not (stripped.startswith('import ') or stripped.startswith('from ')):
                    code_lines.append(stripped)
            code_text = ' '.join(code_lines)

            for imp in imports:
                # Skip common always-used imports
                if imp in ('os', 'sys', 'json', 'Path', 'logging', 'time', 'datetime'):
                    continue
                # Word boundary search
                if imp and len(imp) > 2 and imp not in code_text:
                    issues.append(Issue("L3-Imports", "INFO", rel, 0, f"Unused import: '{imp}'"))
        except Exception:
            pass  # Skip files that can't be parsed
    return issues


# ─── LAYER 4: COMPLEXITY ───────────────────────────────────────

def _get_nesting_depth(node, depth=0):
    """Độ sâu lồng tối đa của một node."""
    max_depth = depth
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            max_depth = max(max_depth, _get_nesting_depth(child, depth + 1))
        else:
            max_depth = max(max_depth, _get_nesting_depth(child, depth))
    return max_depth


def scan_complexity(files: List[Path], root: Path) -> List[Issue]:
    """L4: Kiểm tra functions >100 dòng, files >500 dòng, nesting sâu."""
    issues = []
    for f in files:
        rel = str(f.relative_to(root))
        try:
            content = f.read_text(encoding='utf-8', errors='replace')
            lines = content.split('\n')

            # File too long
            if len(lines) > MAX_FILE_LINES:
                issues.append(Issue("L4-Complexity", "WARNING", rel, 1,
                                    f"File quá dài: {len(lines)}/{MAX_FILE_LINES} dòng"))

            tree = ast.parse(content, filename=str(f))

            # Check function length
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_lines = (getattr(node.end_lineno, '__int__', lambda: node.end_lineno)() -
                                  node.lineno) if hasattr(node, 'end_lineno') and node.end_lineno else 0
                    if func_lines > MAX_FUNC_LINES:
                        issues.append(Issue("L4-Complexity", "WARNING", rel, node.lineno,
                                            f"Function '{node.name}' quá dài: {func_lines}/{MAX_FUNC_LINES} dòng"))

                    # Check nesting depth
                    depth = _get_nesting_depth(node)
                    if depth > MAX_NESTING:
                        issues.append(Issue("L4-Complexity", "INFO", rel, node.lineno,
                                            f"Function '{node.name}' nesting sâu: {depth}/{MAX_NESTING}"))
        except Exception:
            pass
    return issues


# ─── LAYER 5: SECURITY ─────────────────────────────────────────

SECURITY_PATTERNS = [
    ('bare_except', r'^\s*except\s*:', "Bare except: nuốt tất cả exceptions"),
    ('eval_usage', r'\beval\s*\(', "eval() — RCE risk"),
    ('exec_usage', r'\bexec\s*\(', "exec() — RCE risk"),
    ('hardcoded_key', r'(api_key|secret|password)\s*=\s*["\'][^"\']{10,}', "Hardcoded secret detected"),
    ('shell_true', r'shell\s*=\s*True', "shell=True — command injection risk"),
]


def scan_security(files: List[Path], root: Path) -> List[Issue]:
    """L5: Pattern match các rủi ro security phổ biến."""
    import re
    issues = []
    for f in files:
        rel = str(f.relative_to(root))
        try:
            content = f.read_text(encoding='utf-8', errors='replace')
            lines = content.split('\n')

            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # Skip comments
                if stripped.startswith('#'):
                    continue

                for pattern_name, regex, message in SECURITY_PATTERNS:
                    if re.search(regex, stripped, re.IGNORECASE):
                        sev = "CRITICAL" if pattern_name in ('eval_usage', 'hardcoded_key') else "WARNING"
                        issues.append(Issue("L5-Security", sev, rel, i, message))
        except Exception:
            pass
    return issues


# ─── SCORING ───────────────────────────────────────────────────

def calculate_score(report: HealthReport) -> float:
    """Tính Health Score 0-10 (Weighted, normalized)."""
    # Syntax: CRITICAL — mỗi lỗi = 5% penalty (capped)
    syntax_penalty = min(len(report.syntax_issues) * 0.5, 3.0)
    # Structure: mỗi lỗi = 1% penalty (capped)
    structure_penalty = min(len(report.structure_issues) * 0.01, 1.0)
    # Imports: INFO level, cap at 1.0 (118 imports = ~1.0)
    import_penalty = min(len(report.import_issues) * 0.01, 1.0)
    # Complexity: cap at 1.5
    complexity_penalty = min(len(report.complexity_issues) * 0.02, 1.5)
    # Security: CRITICAL = 0.3 each (capped at 2.0), WARNING = 0.05 each (capped at 1.0)
    sec_critical = sum(1 for i in report.security_issues if i.severity == "CRITICAL")
    sec_warning = sum(1 for i in report.security_issues if i.severity == "WARNING")
    security_penalty = min(sec_critical * 0.3, 2.0) + min(sec_warning * 0.05, 1.0)

    total_penalty = syntax_penalty + structure_penalty + import_penalty + complexity_penalty + security_penalty
    score = 10.0 - total_penalty
    return max(0.0, round(score, 1))


# ─── AUTO-FIX ──────────────────────────────────────────────────

def auto_fix_structure(issues: List[Issue], root: Path) -> int:
    """Tự tạo __init__.py thiếu."""
    fixed = 0
    for issue in issues:
        if "Missing __init__.py" in issue.message:
            init_path = root / issue.file / "__init__.py"
            try:
                init_path.write_text(f'"""Auto-generated by Code Health Sentinel."""\n', encoding='utf-8')
                fixed += 1
            except Exception:
                pass
    return fixed


# ─── MAIN ──────────────────────────────────────────────────────

def run_scan(root: Path = None, auto_fix: bool = False) -> HealthReport:
    """Chạy toàn bộ 5-layer scan. Trả về HealthReport."""
    root = root or ROOT_DIR
    report = HealthReport(timestamp=datetime.now().isoformat())

    print("=" * 60)
    print("🔍 CODE HEALTH SENTINEL — STARTING SCAN")
    print("=" * 60)

    files = collect_python_files(root)
    report.total_files = len(files)
    print(f"📁 Đã quét {len(files)} file Python trong monorepo.\n")

    # L1: Syntax
    print("[L1] Đang quét Syntax...")
    report.syntax_issues = scan_syntax(files, root)
    syntax_ok = len(files) - len(report.syntax_issues)
    print(f"     ✅ {syntax_ok}/{len(files)} PASS | ❌ {len(report.syntax_issues)} lỗi\n")

    # L2: Structure
    print("[L2] Đang quét Structure (__init__.py)...")
    report.structure_issues = scan_structure(root)
    pkg_total = len([d for d in collect_package_dirs(root)]) + len(report.structure_issues)
    print(f"     📦 {pkg_total - len(report.structure_issues)}/{pkg_total} OK | ⚠️ {len(report.structure_issues)} thiếu\n")

    if auto_fix and report.structure_issues:
        fixed = auto_fix_structure(report.structure_issues, root)
        print(f"     🔧 Auto-fix: Đã tạo {fixed} __init__.py\n")

    # L3: Imports
    print("[L3] Đang quét Imports...")
    report.import_issues = scan_imports(files, root)
    print(f"     ℹ️ {len(report.import_issues)} unused imports phát hiện\n")

    # L4: Complexity
    print("[L4] Đang quét Complexity...")
    report.complexity_issues = scan_complexity(files, root)
    print(f"     📏 {len(report.complexity_issues)} vấn đề phức tạp\n")

    # L5: Security
    print("[L5] Đang quét Security...")
    report.security_issues = scan_security(files, root)
    print(f"     🔒 {len(report.security_issues)} rủi ro phát hiện\n")

    # Score
    report.score = calculate_score(report)

    # Summary
    print("=" * 60)
    print("📊 CODE HEALTH REPORT SUMMARY")
    print("=" * 60)
    print(f"📁 Files scanned:  {report.total_files}")
    print(f"✅ Syntax errors:  {len(report.syntax_issues)}")
    print(f"📦 Missing init:   {len(report.structure_issues)}")
    print(f"🔄 Import issues:  {len(report.import_issues)}")
    print(f"📏 Complexity:     {len(report.complexity_issues)}")
    print(f"🔒 Security risks: {len(report.security_issues)}")
    print(f"🚨 Critical:       {report.critical_count}")
    print("-" * 60)
    status = "🟢 HEALTHY" if report.score >= 8 else ("🟡 NEEDS REVIEW" if report.score >= 6 else "🔴 CRITICAL")
    print(f"📊 HEALTH SCORE:   {report.score}/10 {status}")
    print("=" * 60)

    # Save JSON report
    report_path = root / "reports" / "code_health_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_data = {
        "timestamp": report.timestamp,
        "total_files": report.total_files,
        "total_issues": report.total_issues,
        "critical_count": report.critical_count,
        "score": report.score,
        "syntax_issues": [asdict(i) for i in report.syntax_issues],
        "structure_issues": [asdict(i) for i in report.structure_issues],
        "import_issues": [asdict(i) for i in report.import_issues[:50]],  # Limit for file size
        "complexity_issues": [asdict(i) for i in report.complexity_issues],
        "security_issues": [asdict(i) for i in report.security_issues],
    }
    report_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n📄 Full report: {report_path}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Code Health Sentinel — Static Analysis Engine")
    parser.add_argument("--fix", action="store_true", help="Auto-fix safe issues (missing __init__.py)")
    parser.add_argument("--root", type=str, default=None, help="Root directory to scan")
    args = parser.parse_args()

    root = Path(args.root) if args.root else ROOT_DIR
    report = run_scan(root=root, auto_fix=args.fix)

    # Exit code: 0 = healthy, 1 = needs review, 2 = critical
    if report.critical_count > 0:
        sys.exit(2)
    elif report.score < 7.0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()