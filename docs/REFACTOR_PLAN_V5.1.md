# 🛠️ KẾ HOẠCH TÁI CẤU TRÚC (REFACTOR PLAN) - V5.1

## Mục tiêu
Dọn dẹp "Mì Ý" (Spaghetti Code), loại bỏ các anti-pattern nguy hiểm, và xây dựng một nền móng vững chắc cấp độ Enterprise cho LangGraph Agent System.

## Danh sách công việc (Checklist)

### Giai đoạn 1: Chuẩn hóa Môi trường (Dependency Management)
- [ ] 1.1. Xóa bỏ cảnh báo rác từ `uv` (Sửa `tool.uv.dev-dependencies` thành `dependency-groups.dev` trong các file `pyproject.toml` của các project con).
- [ ] 1.2. Hợp nhất cấu hình môi trường, đảm bảo dự án chạy ổn định với `uv`.

### Giai đoạn 2: Triệt tiêu Anti-Pattern `sys.path.insert`
- [ ] 2.1. Quét toàn bộ source code (đặc biệt thư mục `projects/ai_trading_agent`, `scheduler`).
- [ ] 2.2. Xóa bỏ các đoạn code lạm dụng `sys.path.insert(0, ...)`.
- [ ] 2.3. Sửa lại cú pháp import sử dụng Absolute Imports chuẩn của Python (VD: `from projects.ai_trading_agent.src.database import SystemDB`).

### Giai đoạn 3: Nâng cấp SQLite (Chống Locking)
- [ ] 3.1. Rà soát các file khởi tạo Database (`projects/ai_trading_agent/src/database.py`, `src/database.py`...).
- [ ] 3.2. Đảm bảo Bổ sung `PRAGMA journal_mode=WAL;` và `timeout=20.0` cho MỌI kết nối SQLite để chống crash đa luồng.

### Giai đoạn 4: Thiết lập Centralized Logger
- [ ] 4.1. Tạo module `core_utilities/logger.py` sử dụng thư viện `logging` chuẩn của Python, cấu hình Rotate Log.
- [ ] 4.2. Cập nhật các file core (như `drip_feed_worker.py`, `live_advisor.py`) để chuyển từ `print()` sang `logger.info()`, `logger.error()`.
