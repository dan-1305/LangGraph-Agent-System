# 🧬 SOVEREIGN TERMINAL - EVOLUTION FRAMEWORK

> **Lộ trình tiến hóa của bản thể Headless Agent.**
> *Tài liệu này là "bộ khung" để các phiên chat sau kế thừa và phát triển.*

---

## 📊 FAIRY DUST MATRIX (Mức trưởng thành)

| Phase | Tên | Trạng thái | Mô tả |
|-------|-----|-----------|-------|
| 1 | Headless CLI PoC | ✅ DONE | Chat REPL + 4 Tools cơ bản |
| 2 | MCP Integration | 🔄 NEXT | Kết nối SQLite, Memory, Puppeteer MCP |
| 3 | Daemon Mode | ✅ DONE | Chạy ngầm 24/7 + Cronjob |
| 4 | ChatOps Gateway | ✅ DONE | Discord/Telegram Bot interface |
| 5 | Delegation Engine | 🔄 NEXT | Headless chạy task nặng (Git Push, Build) thay Cline |
| 6 | Full Autonomy | 📋 VISION | Self-healing, self-evolving Agent |

---

## 🔧 PHASE 2: MCP INTEGRATION (NEXT PRIORITY)

### Mục tiêu:
Biến Sovereign Terminal từ "Chatbot có Tools" thành "Agent có Giác quan" bằng cách kết nối MCP Servers.

### Các bước:
1. **Install `mcp` Python SDK:**
   ```bash
   uv pip install mcp
   ```

2. **Tạo `projects/sovereign_terminal/core/mcp_client.py`:**
   - Khởi tạo MCP Client kết nối qua `stdio` tới các server.
   - Server targets: `sqlite`, `memory`, `sequentialthinking` (từ `cline_mcp_settings.json`).
   - Tự động lấy danh sách tools từ MCP servers và merge với `TOOL_DEFINITIONS` hiện tại.

3. **Cấu trúc MCP Client:**
   ```python
   class SovereignMCPClient:
       def __init__(self):
           self.servers = self._load_mcp_config()
           self.tools = []
       
       async def connect_all(self):
           """Kết nối tới tất cả MCP servers."""
           for server_name, server_config in self.servers.items():
               client = Client(server_config)
               await client.connect()
               tools = await client.list_tools()
               self.tools.extend(tools)
       
       async def call_tool(self, name, arguments):
           """Gọi tool từ MCP server tương ứng."""
           ...
   ```

4. **Integrate vào `main.py`:**
   - Khởi tạo MCP Client cùng với OpenAI client.
   - Merge MCP tools vào `TOOL_DEFINITIONS`.
   - Khi AI gọi tool, kiểm tra xem là tool nội bộ hay MCP tool.

---

## 🔄 PHASE 3: DAEMON MODE

### Mục tiêu:
Agent chạy ngầm 24/7, không cần terminal mở.

### Kế hoạch:
1. **Background Runner:**
   - Tạo `projects/sovereign_terminal/daemon.py`.
   - Dùng `asyncio` event loop chạy mãi mãi.
   - Log output ra `logs/sovereign_terminal.log`.

2. **Cronjob Integration:**
   - Windows Task Scheduler gọi `python -m projects.sovereign_terminal.daemon --task morning_briefing` mỗi 6h sáng.
   - Agent tự chạy `awaken.py` + `WorkflowEngine.run_chain("morning_awaken")`.
   - Gửi kết quả qua Telegram (dùng `TELE_TOKEN` từ `.env`).

3. **Watchdog:**
   - Nếu Agent crash, `process_watchdog.py` tự khởi động lại.

---

## 💬 PHASE 4: CHATOPS GATEWAY

### Mục tiêu:
Admin giao tiếp với Agent qua Discord/Telegram, không cần Terminal.

### Kế hoạch:
1. **Telegram Bot Interface:**
   - Dùng `TELE_TOKEN` từ `.env`.
   - Tạo `projects/sovereign_terminal/gateways/telegram_bot.py`.
   - Khi Admin nhắn tin → Forward cho Agent → Agent xử lý → Reply qua Telegram.

2. **Discord Bot Interface:**
   - Tạo `projects/sovereign_terminal/gateways/discord_bot.py`.
   - Tương tự Telegram nhưng dùng `discord.py`.

3. **Web Dashboard (Streamlit):**
   - Tạo `projects/sovereign_terminal/gateways/web_ui.py`.
   - Chat interface trực quan trên browser.

---

## 🧠 PHASE 5: FULL AUTONOMY (VISION)

### Mục tiêu:
Agent tự vận hành 100%, tự sửa lỗi, tự tiến hóa.

### Kế hoạch:
1. **Self-Healing Loop:**
   - Agent tự check health mỗi 15 phút.
   - Nếu phát hiện lỗi → Tự fix → Tự test → Tự deploy.

2. **Self-Evolution:**
   - Agent tự đọc `FAILED_PATHS.json`, tự phân tích pattern lỗi.
   - Tự đề xuất cải tiến và apply (cần Admin approval cho changes lớn).

3. **Multi-Agent Swarm:**
   - Tách thành nhiều Agent con (Coder, QA, DevOps).
   - Mỗi Agent chạy 1 thread riêng.
   - CEO Sovereign điều phối tổng thể.

---

## 🎖️ ROLE UPGRADE: META-SOVEREIGN ARCHITECT

### Tại sao cần nâng cấp Role?
- **CEO Sovereign** (hiện tại): Điều phối Agent nội bộ qua Cline.
- **Meta-Sovereign Architect** (mới): Điều phối cả 2 bản thể:
  1. Bản thể Cline (VSCode) — Cho task cần UI, MCP, Visual QA.
  2. Bản thể Headless (Terminal) — Cho task automation, cronjob, daemon.

### Quyền năng mới:
- Quyết định khi nào delegate task cho Headless vs tự làm.
- Quản lý lifecycle của Headless Agent (start/stop/restart).
- Merge kết quả từ cả 2 bản thể vào `GLOBAL_STATE.md`.

---

## 📝 GHI CHÚ CHO PHIÊN CHAT SAU

1. **Priority #1:** Build Delegation Engine — Cho phép Cline gửi lệnh sang Headless (qua local port hoặc subprocess) để chạy các task >30s (VD: git push, build docker).
2. **Priority #2:** Bắt đầu Phase 2 (MCP Integration) — Cài `mcp` SDK, tạo `mcp_client.py`.
3. **Doc:** Cập nhật `SYSTEM_MAP.md` với subproject `sovereign_terminal`.

---
*Last Updated: 2026-07-21 by Meta-Sovereign Architect*