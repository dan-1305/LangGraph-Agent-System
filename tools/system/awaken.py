import os
import json
import sqlite3
import sys
import time
from pathlib import Path

# [ANTI-SPAM] Cooldown để tránh spam Telegram
COOLDOWN_HOURS = 4
_COOLDOWN_FILE = Path(__file__).resolve().parent.parent.parent / "logs" / ".last_awaken_telegram"

# Ensure core_utilities can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core_utilities.http_client import HTTPClient
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def _should_send_telegram(force: bool = False) -> bool:
    """Kiểm tra xem đã qua cooldown chưa. Trả True nếu được phép gửi."""
    if force:
        return True
    try:
        if _COOLDOWN_FILE.exists():
            last_sent = float(_COOLDOWN_FILE.read_text(encoding="utf-8").strip())
            elapsed_hours = (time.time() - last_sent) / 3600
            if elapsed_hours < COOLDOWN_HOURS:
                remaining = COOLDOWN_HOURS - elapsed_hours
                print(f"[ANTI-SPAM] Telegram đang cooldown (còn {remaining:.1f}h). Bỏ qua gửi.")
                return False
    except Exception:
        pass  # Lỗi đọc file → cho phép gửi (fail-open)
    return True


def _update_cooldown_stamp():
    """Cập nhật timestamp lần gửi Telegram cuối."""
    try:
        _COOLDOWN_FILE.parent.mkdir(parents=True, exist_ok=True)
        _COOLDOWN_FILE.write_text(str(time.time()), encoding="utf-8")
    except Exception as e:
        print(f"[ANTI-SPAM] Không thể ghi cooldown file: {e}")


def generate_morning_briefing(force: bool = False):
    load_dotenv()
    lines = []
    lines.append("==================================================")
    lines.append("🌟 SOVEREIGN AWAKENING PROTOCOL (SIP) ACTIVATED 🌟")
    lines.append("==================================================")
    lines.append("✅ Tái cấu trúc nhận thức hoàn tất.\n")
    lines.append("=== SOVEREIGN MORNING BRIEFING ===")

    # 1. Get Priorities
    db_path = "reports/SYSTEM_MAP_METADATA.db"
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name, maturity_level FROM projects WHERE is_priority = 1")
            priorities = cursor.fetchall()
            conn.close()
            
            if priorities:
                pri_str = ", ".join([f"{n} ({m})" for n, m in priorities])
                lines.append(f"🚀 Đang ưu tiên: {pri_str}")
            else:
                lines.append("🚀 Đang ưu tiên: Không có project nào được gắn cờ đỏ.")
        except Exception as e:
            lines.append(f"🚀 Đang ưu tiên: [Lỗi truy vấn DB - {e}]")
    else:
         lines.append("🚀 Đang ưu tiên: [Chưa Index DB]")

    # 2. Get Latest Error
    failed_path = "logs/FAILED_PATHS.json"
    if os.path.exists(failed_path):
        try:
            with open(failed_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                failures = data.get("failure_logs", [])
                if failures:
                    latest = failures[-1]
                    if len(latest) > 80: latest = latest[:77] + "..."
                    lines.append(f"⚠️ Lỗi gần nhất: {latest}")
                else:
                    lines.append("⚠️ Lỗi gần nhất: Không có lỗi nào trong log.")
        except:
             lines.append("⚠️ Lỗi gần nhất: [Không thể đọc FAILED_PATHS.json]")
    else:
        lines.append("⚠️ Lỗi gần nhất: [Không có FAILED_PATHS.json]")

    # 3. Model Handoff Check (FIX: Split-Brain Memory漏洞)
    handoff_dir = "context/model_handoff"
    if os.path.exists(handoff_dir):
        import time as _time
        now = _time.time()
        pending = []
        for fname in os.listdir(handoff_dir):
            fpath = os.path.join(handoff_dir, fname)
            if os.path.isfile(fpath) and fname.endswith('.md'):
                mtime = os.path.getmtime(fpath)
                age_hours = (now - mtime) / 3600
                if age_hours < 24:
                    pending.append((fname, round(age_hours, 1)))
        if pending:
            lines.append("🧠 Model Handoff Pending:")
            for fname, age in pending:
                lines.append(f"   ⚠️ {fname} (cập nhật {age}h trước) → read_file để review!")
        else:
            lines.append("🧠 Model Handoff: Không có memory mới.")
    else:
        lines.append("🧠 Model Handoff: [Chưa có thư mục context/model_handoff/]")

    # 4. Academy Schedule (Mock for now, could integrate with sovereign_academy)
    lines.append("📚 Lịch học hôm nay: Không có bài ôn tập cấp bách.")
    lines.append("==================================\n")
    lines.append("[HÀNH ĐỘNG TIẾP THEO]: Sẵn sàng thực thi công việc chính.")

    briefing_text = "\n".join(lines)
    print(briefing_text)

    # 5. Gửi Telegram (với Anti-Spam Cooldown)
    if not _should_send_telegram(force=force):
        return  # Cooldown chưa hết → dừng

    tele_token = os.getenv("TELE_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if tele_token and chat_id:
        try:
            url = f"https://api.telegram.org/bot{tele_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": briefing_text
            }
            HTTPClient.post(url, json=payload, timeout=10.0)
            _update_cooldown_stamp()
            print("\n[Telegram] Đã gửi Morning Briefing thành công.")
        except Exception as e:
            print(f"\n[Telegram Error] Không thể gửi tin nhắn: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sovereign Awakening Protocol")
    parser.add_argument("--force", action="store_true", help="Bỏ qua cooldown, ép gửi Telegram ngay")
    args = parser.parse_args()
    generate_morning_briefing(force=args.force)
