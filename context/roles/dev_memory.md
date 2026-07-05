# 💻 DEV MEMORY - Tech Debt & Standards

## 🛠️ Ongoing Refactors
- **sys.path removal:** Completed 100%. System now uses `uv` workspace standards.
- **Async I/O:** Need to transition more tools from `requests` to `httpx`.

## 📜 Coding Standards
- Google-style Docstrings (MANDATORY).
- Pydantic for data validation.
- Minimal logic in `main.py`, favor modular project structures.

## 🧠 Learned Lessons
- Always run `uv run python tools/system/auto_mapper.py` after creating new sub-folders.
- Use `start /b` to run proxy servers in the background on Windows.
- **Trading Refactor (2026-07-05):** Refactored `ai_trading_agent` to inherit from `BaseAgent`. This ensures automatic retries, standardized labeling (tier-1/tier-2), and circuit breaker protection.
- **Godot 4 Binary Repack (2026-07-07):** Sửa lỗi `Expected '['` bằng cách ép conversion `.tscn` -> `.scn`. Nhận diện và sửa lỗi GDRE Tools tự tạo folder trùng tên file.

---
*Dev is the builder of the system.*
