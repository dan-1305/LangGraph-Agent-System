#!/usr/bin/env python3
"""
Workflow DB - SQLite layer cho Sovereign Workflow Engine.

Schema:
  - workflow_registry: Master table định nghĩa các cycles
  - workflow_executions: Log table lưu kết quả chạy

Usage:
    from tools.system.workflow_db import WorkflowDB
    db = WorkflowDB()
    db.init_schema()
    db.register_cycle("self_review", "Tu nhan xet code", ...)
    db.log_execution("self_review", score=8.5, findings=[...])
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "workflows.db"


class WorkflowDB:
    """SQLite CRUD layer cho Workflow Registry."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        """Khoi tao schema neu chua co."""
        with self._connect() as conn:
            conn.executescript(
                """
            CREATE TABLE IF NOT EXISTS workflow_registry (
                cycle_id TEXT PRIMARY KEY,
                cycle_name TEXT NOT NULL,
                description TEXT,
                script_path TEXT,
                trigger_condition TEXT,
                can_combine_with TEXT,
                estimated_tokens INTEGER DEFAULT 0,
                auto_trigger INTEGER DEFAULT 0,
                category TEXT DEFAULT 'analysis',
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS workflow_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cycle_id TEXT NOT NULL,
                session_id TEXT,
                trigger_reason TEXT,
                target_file TEXT,
                score REAL DEFAULT 0,
                findings TEXT,
                actions_taken TEXT,
                status TEXT DEFAULT 'pending',
                parent_execution_id INTEGER,
                created_at TEXT,
                FOREIGN KEY (cycle_id) REFERENCES workflow_registry(cycle_id)
            );

            CREATE INDEX IF NOT EXISTS idx_exec_cycle ON workflow_executions(cycle_id);
            CREATE INDEX IF NOT EXISTS idx_exec_status ON workflow_executions(status);
            """
            )

    def register_cycle(
        self,
        cycle_id: str,
        cycle_name: str,
        description: str = "",
        script_path: str = "",
        trigger_condition: str = "",
        can_combine_with: str = "",
        estimated_tokens: int = 0,
        auto_trigger: bool = False,
        category: str = "analysis",
    ) -> bool:
        """Dang ky hoac update 1 cycle."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO workflow_registry
                    (cycle_id, cycle_name, description, script_path,
                     trigger_condition, can_combine_with, estimated_tokens,
                     auto_trigger, category, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(cycle_id) DO UPDATE SET
                    cycle_name=excluded.cycle_name,
                    description=excluded.description,
                    script_path=excluded.script_path,
                    trigger_condition=excluded.trigger_condition,
                    can_combine_with=excluded.can_combine_with,
                    estimated_tokens=excluded.estimated_tokens,
                    auto_trigger=excluded.auto_trigger,
                    category=excluded.category
                """,
                (
                    cycle_id,
                    cycle_name,
                    description,
                    script_path,
                    trigger_condition,
                    can_combine_with,
                    estimated_tokens,
                    int(auto_trigger),
                    category,
                    datetime.now().isoformat(),
                ),
            )
            return True

    def get_cycle(self, cycle_id: str) -> Optional[Dict[str, Any]]:
        """Lay thong tin 1 cycle."""
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM workflow_registry WHERE cycle_id = ?", (cycle_id,)
            ).fetchone()
            return dict(row) if row else None

    def list_cycles(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lay danh sach cycles."""
        with self._connect() as conn:
            if category:
                rows = conn.execute(
                    "SELECT * FROM workflow_registry WHERE category = ? ORDER BY cycle_id",
                    (category,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM workflow_registry ORDER BY cycle_id"
                ).fetchall()
            return [dict(r) for r in rows]

    def log_execution(
        self,
        cycle_id: str,
        session_id: str = "",
        trigger_reason: str = "",
        target_file: str = "",
        score: float = 0.0,
        findings: Optional[list] = None,
        actions_taken: Optional[list] = None,
        status: str = "pending",
        parent_execution_id: Optional[int] = None,
    ) -> int:
        """Ghi log 1 execution. Return execution ID."""
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO workflow_executions
                    (cycle_id, session_id, trigger_reason, target_file,
                     score, findings, actions_taken, status,
                     parent_execution_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    cycle_id,
                    session_id,
                    trigger_reason,
                    target_file,
                    score,
                    json.dumps(findings or [], ensure_ascii=False),
                    json.dumps(actions_taken or [], ensure_ascii=False),
                    status,
                    parent_execution_id,
                    datetime.now().isoformat(),
                ),
            )
            return cursor.lastrowid

    def update_execution(
        self, exec_id: int, score: float = None, status: str = None,
        findings: list = None, actions_taken: list = None,
    ) -> bool:
        """Update execution sau khi chay xong."""
        updates = []
        params = []
        if score is not None:
            updates.append("score = ?")
            params.append(score)
        if status is not None:
            updates.append("status = ?")
            params.append(status)
        if findings is not None:
            updates.append("findings = ?")
            params.append(json.dumps(findings, ensure_ascii=False))
        if actions_taken is not None:
            updates.append("actions_taken = ?")
            params.append(json.dumps(actions_taken, ensure_ascii=False))
        if not updates:
            return False
        params.append(exec_id)
        with self._connect() as conn:
            conn.execute(
                f"UPDATE workflow_executions SET {', '.join(updates)} WHERE id = ?",
                params,
            )
            return True

    def get_execution_history(
        self, cycle_id: Optional[str] = None, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Lay lich su executions."""
        with self._connect() as conn:
            if cycle_id:
                rows = conn.execute(
                    "SELECT * FROM workflow_executions WHERE cycle_id = ? ORDER BY id DESC LIMIT ?",
                    (cycle_id, limit),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM workflow_executions ORDER BY id DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            return [dict(r) for r in rows]

    def get_stats(self) -> Dict[str, Any]:
        """Thong ke tong quan."""
        with self._connect() as conn:
            total = conn.execute(
                "SELECT COUNT(*) as c FROM workflow_executions"
            ).fetchone()["c"]
            passed = conn.execute(
                "SELECT COUNT(*) as c FROM workflow_executions WHERE status = 'passed'"
            ).fetchone()["c"]
            failed = conn.execute(
                "SELECT COUNT(*) as c FROM workflow_executions WHERE status = 'failed'"
            ).fetchone()["c"]
            avg_score = conn.execute(
                "SELECT AVG(score) as s FROM workflow_executions WHERE score > 0"
            ).fetchone()["s"]
            return {
                "total_executions": total,
                "passed": passed,
                "failed": failed,
                "avg_score": round(avg_score, 2) if avg_score else 0,
            }


def seed_default_cycles():
    """Seed DB voi 14 cycles mac dinh."""
    db = WorkflowDB()
    db.init_schema()

    cycles = [
        # Analysis
        ("self_review", "Tu nhan xet code",
         "AI doc lai code vua viet, cham diem, tim issue",
         "tools/system/cycles/self_review.py",
         "after_code_change", "regression_guard,compliance_check", 500,
         True, "analysis"),
        ("kaizen_evolution", "Tien hoa Kaizen 1%",
         "Tu dong sinh test, optimize code, va ghi chem Reflex",
         "tools/system/cycles/kaizen_evolution.py",
         "end_of_session", "token_audit", 1500,
         False, "analysis"),
        ("project_eval", "Danh gia project",
         "Check health 1 project cu the",
         "tools/system/cycles/project_eval.py",
         "on_demand", "codebase_audit", 1000,
         False, "analysis"),
        ("codebase_audit", "Audit kien truc",
         "Phan tich toan bo project, kien truc",
         "", "on_demand", "security_scan,failure_memory", 2000,
         False, "analysis"),
        # Guard
        ("regression_guard", "Chong hoi quy",
         "Chay test cu sau khi fix bug",
         "", "after_bug_fix", "self_review", 300,
         True, "guard"),
        ("compliance_check", "Kiem tra chuan",
         "Kiem tra BaseAgent, imports",
         "", "after_add_file", "security_scan", 200,
         True, "guard"),
        ("security_scan", "Quet bao mat",
         "Kiem tra API key leak, path traversal",
         "", "before_deploy", "compliance_check", 400,
         False, "guard"),
        ("failure_memory", "Nho loi cu",
         "Doc FAILED_PATHS.json truoc khi fix",
         "", "before_bug_fix", "", 100,
         True, "guard"),
        # Optimization
        ("context_optimize", "Nen context",
         "Goi context_compressor khi context > 50%",
         "", "context>50%", "", 0,
         True, "optimization"),
        ("token_audit", "Kiem token",
         "Dem token da tieu, warning neu vuot nguong",
         "", "end_of_task", "", 100,
         True, "optimization"),
        ("rag_ingest", "Nap tri thuc",
         "Ingest thay doi vao ChromaDB",
         "", "after_arch_change", "", 0,
         False, "optimization"),
        # Chain Presets
        ("safe_commit", "Commit an toan (Chain)",
         "self_review + regression_guard + compliance_check",
         "", "before_commit", "", 1000,
         False, "chain"),
        ("deep_audit", "Audit sau (Chain)",
         "codebase_audit + security_scan + failure_memory",
         "", "on_demand", "", 3000,
         False, "chain"),
        ("session_wrap", "Chot session (Chain)",
         "kaizen_evolution + token_audit + rag_ingest",
         "", "end_of_session", "", 1000,
         False, "chain"),
    ]

    for c in cycles:
        db.register_cycle(*c)

    print(f"[SEED] Da seed {len(cycles)} cycles vao workflows.db")
    return len(cycles)


if __name__ == "__main__":
    import sys
    if "--seed" in sys.argv:
        seed_default_cycles()
    elif "--stats" in sys.argv:
        db = WorkflowDB()
        db.init_schema()
        stats = db.get_stats()
        print(json.dumps(stats, indent=2))
    elif "--list" in sys.argv:
        db = WorkflowDB()
        db.init_schema()
        cycles = db.list_cycles()
        for c in cycles:
            auto = "[AUTO]" if c["auto_trigger"] else ""
            print(f"  {c['category']:12s} | {c['cycle_id']:20s} | {c['cycle_name']:30s} {auto}")
    else:
        print("Usage: python workflow_db.py [--seed | --stats | --list]")