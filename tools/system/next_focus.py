#!/usr/bin/env python3
"""
Next Focus Generator - Self-Continuation Prompt cho Auto-Pilot trong 1 session.

Thay thế new_task loop: Đọc ROADMAP + ACTIVE_THOUGHTS + session counter
→ Xuất prompt compact (~5 dòng) để AI tự tiếp tục trong cùng chat.

Safety Guards:
  - Max 5 task/session (configurable)
  - Convergence check (không còn task → STOP)
  - Session counter tracking qua file logs/session_state.json

Usage:
    uv run python tools/system/next_focus.py [--max-tasks N] [--reset]

Author: CEO Sovereign
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# === UTF-8 ENFORCEMENT (Windows Console Fix) ===
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

# === CONSTANTS ===
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ROADMAP_PATH = ROOT_DIR / "context" / "ROADMAP.md"
THOUGHTS_PATH = ROOT_DIR / "context" / "ACTIVE_THOUGHTS.md"
SESSION_STATE_PATH = ROOT_DIR / "logs" / "session_state.json"
DEFAULT_MAX_TASKS = 5


def load_session_state() -> dict:
    """Load session counter từ file JSON."""
    if SESSION_STATE_PATH.exists():
        try:
            with open(SESSION_STATE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "tasks_completed": 0,
        "task_history": [],
        "started_at": datetime.now().isoformat(),
    }


def save_session_state(state: dict) -> None:
    """Persist session counter."""
    SESSION_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SESSION_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def extract_pending_tasks(filepath: Path) -> list:
    """
    Trích xuất task chưa hoàn thành từ file markdown.
    Tìm các dòng có '- [ ]' (unchecked checkbox).
    """
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Match unchecked items
    pattern = r"- \[ \] (.+)"
    matches = re.findall(pattern, content)
    # Filter: bỏ các task đã đánh dấu [ON HOLD] hoặc ARCHIVE
    filtered = [m.strip() for m in matches if "ARCHIVE" not in m.upper()]
    return filtered


def extract_next_steps_from_thoughts(filepath: Path) -> list:
    """
    Trích xuất section 'NEXT STEPS' từ ACTIVE_THOUGHTS.md.
    """
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Tìm section NEXT STEPS
    pattern = r"## 🚀 CÔNG VIỆC CHÍNH ĐANG DANG DỞ.*?\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return []
    block = match.group(1)
    # Extract numbered items
    items = re.findall(r"\d+\.\s*\*\*([^:]+):\*\*(.+)", block)
    return [(title.strip(), desc.strip()) for title, desc in items]


def generate_focus_prompt(
    roadmap_tasks: list,
    thought_tasks: list,
    task_count: int,
    max_tasks: int,
) -> str:
    """
    Generate compact prompt (~5 dòng) cho next task.
    """
    lines = []
    lines.append("=" * 60)
    lines.append(f"📋 NEXT FOCUS (Task {task_count + 1}/{max_tasks})")
    lines.append("=" * 60)

    # Ưu tiên: NEXT STEPS từ ACTIVE_THOUGHTS > ROADMAP unchecked
    if thought_tasks:
        title, desc = thought_tasks[0]
        lines.append(f"🎯 Mục tiêu: {title}")
        lines.append(f"📝 Chi tiết: {desc}")
        lines.append(f"📊 Nguồn: ACTIVE_THOUGHTS.md (Priority)")
    elif roadmap_tasks:
        task = roadmap_tasks[0]
        lines.append(f"🎯 Mục tiêu: {task}")
        lines.append(f"📊 Nguồn: ROADMAP.md (Q3-Q4)")
    else:
        lines.append("✅ TẤT CẢ TASK ĐÃ HOÀN THÀNH!")
        lines.append("🛑 [STOP] Không còn task pending. Hãy review tổng thể.")
        return "\n".join(lines)

    lines.append(f"⚠️ Giới hạn: Chỉ sửa tối đa 2 file. Test sau mỗi thay đổi.")
    lines.append(f"🛑 Dừng nếu: Lỗi import, 3 lần retry thất bại, hoặc context > 50%.")
    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Next Focus Generator")
    parser.add_argument(
        "--max-tasks",
        type=int,
        default=DEFAULT_MAX_TASKS,
        help=f"Max tasks per session (default: {DEFAULT_MAX_TASKS})",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset session counter (bắt đầu session mới)",
    )
    parser.add_argument(
        "--complete",
        type=str,
        default=None,
        help="Đánh dấu 1 task hoàn thành và tăng counter. VD: --complete 'Multi-Model Routing'",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Chỉ hiển thị trạng thái session hiện tại",
    )
    args = parser.parse_args()

    # Load or reset session state
    if args.reset:
        state = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "tasks_completed": 0,
            "task_history": [],
            "started_at": datetime.now().isoformat(),
        }
        save_session_state(state)
        print("[RESET] Session counter da reset.")
        return

    state = load_session_state()

    # === STATUS MODE ===
    if args.status:
        print("=" * 60)
        print(f"[STATUS] Session: {state.get('session_id', 'N/A')}")
        print(f"   Tasks completed: {state.get('tasks_completed', 0)}/{args.max_tasks}")
        print(f"   Started: {state.get('started_at', 'N/A')}")
        history = state.get("task_history", [])
        if history:
            print(f"   History: {len(history)} task(s)")
            for i, h in enumerate(history, 1):
                print(f"     {i}. {h}")
        print("=" * 60)
        return

    # === COMPLETE MODE: Tăng counter ===
    if args.complete:
        task_name = args.complete
        state["tasks_completed"] = state.get("tasks_completed", 0) + 1
        state.setdefault("task_history", []).append(
            f"{task_name} ({datetime.now().strftime('%H:%M:%S')})"
        )
        save_session_state(state)
        print(
            f"[DONE] Task '{task_name}' completed. "
            f"Counter: {state['tasks_completed']}/{args.max_tasks}"
        )
        return

    task_count = state.get("tasks_completed", 0)

    # === SAFETY GUARD 1: Max tasks ===
    if task_count >= args.max_tasks:
        print("=" * 60)
        print(f"🛑 [STOP] Đã đạt giới hạn {args.max_tasks} tasks/session.")
        print(f"   Đã hoàn thành: {task_count} tasks")
        print(f"   Hãy review tổng thể trước khi tiếp tục.")
        print("   Để reset: uv run python tools/system/next_focus.py --reset")
        print("=" * 60)
        return

    # === Gather pending tasks ===
    roadmap_tasks = extract_pending_tasks(ROADMAP_PATH)
    thought_tasks = extract_next_steps_from_thoughts(THOUGHTS_PATH)

    # === SAFETY GUARD 2: Convergence check ===
    if not roadmap_tasks and not thought_tasks:
        print("=" * 60)
        print("✅ [CONVERGENCE] Không còn task pending nào.")
        print("   ROADMAP và ACTIVE_THOUGHTS đều sạch.")
        print("   Hãy định nghĩa task mới hoặc kết thúc session.")
        print("=" * 60)
        return

    # === Generate prompt ===
    prompt = generate_focus_prompt(
        roadmap_tasks, thought_tasks, task_count, args.max_tasks
    )
    print(prompt)

    # === Show queue preview ===
    total_remaining = len(thought_tasks) + len(roadmap_tasks)
    print(f"\n📂 Queue còn lại: {total_remaining} tasks")
    if thought_tasks:
        print(f"   - Từ ACTIVE_THOUGHTS: {len(thought_tasks)}")
    if roadmap_tasks:
        print(f"   - Từ ROADMAP: {len(roadmap_tasks)}")
    remaining_slots = args.max_tasks - task_count - 1
    print(f"   - Slots còn lại session này: {remaining_slots}")


if __name__ == "__main__":
    main()