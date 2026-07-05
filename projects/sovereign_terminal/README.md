# 👑 Sovereign Terminal (Headless Agent)

> **Bản thể CEO Sovereign chạy độc lập 100%, không cần Cline hay VSCode.**

## 🚀 Giới thiệu

Sovereign Terminal là một AI Agent Headless sử dụng **GGCHAN API** (Google Gemini) với khả năng:
- Đọc/ghi file trực tiếp trên đĩa cứng
- Chạy lệnh Terminal (subprocess)
- Nạp toàn bộ trí nhớ từ `.clinerules` + `GLOBAL_STATE.md` + `ACTIVE_THOUGHTS.md`
- Chat REPL qua Terminal (giao diện dòng lệnh)

## 📦 Cài đặt

```bash
# Đảm bảo có openai SDK và python-dotenv
uv pip install openai python-dotenv
```

## 🔧 Cấu hình

File `.env` ở root monorepo cần có:
```
GGCHAN_API_KEY=gg-gcli-xxx
GGCHAN_BASE_URL=https://gcli.ggchan.dev/v1
```

## 🎮 Sử dụng

```bash
# Cách 1: Chạy trực tiếp
uv run python projects/sovereign_terminal/main.py

# Cách 2: Pipe input
echo "list files trong src" | uv run python projects/sovereign_terminal/main.py
```

### Lệnh trong REPL:
- `exit` / `quit` — Thoát
- `reset` — Xoá history, bắt đầu session mới
- Bất kỳ câu hỏi/lệnh nào → Agent tự quyết định gọi Tool hay trả lời text

## 🏗️ Kiến trúc

```
projects/sovereign_terminal/
├── __init__.py
├── main.py              # Entry point + Chat REPL loop
├── core/
│   ├── __init__.py
│   ├── config.py        # Cấu hình API, Safety Guards
│   ├── persona.py       # Load System Prompt từ .clinerules
│   └── tools.py         # Function Calling (read/write/run/list)
└── README.md
```

## 🛡️ Safety Guards

- **Protected Files:** Không cho ghi vào `.env`, `pyproject.toml`, `uv.lock`
- **Forbidden Commands:** Chặn `rm -rf`, `format`, `shutdown`, fork bomb
- **Command Timeout:** Mỗi lệnh terminal tối đa 60 giây
- **History Limit:** Giữ tối đa 20 tin nhắn gần nhất
- **Tool Loop Guard:** Tối đa 10 vòng tool calls liên tiếp

## 🧠 Persona Injection

Agent tự động nạp:
1. `.clinerules` (Hiến pháp - tối đa 3000 chars)
2. `context/GLOBAL_STATE.md` (Tình trạng vương triều - tối đa 2000 chars)
3. `context/ACTIVE_THOUGHTS.md` (Ký ức gần nhất - tối đa 1500 chars)

→ Tổng System Prompt ~7000 chars, giúp Agent có 100% nhận thức của CEO Sovereign.

## 🆚 So sánh với Cline

| Tính năng | Cline | Sovereign Terminal |
|-----------|-------|-------------------|
| GUI | VSCode Extension | Terminal CLI |
| API Key | Anthropic/OpenRouter | GGCHAN (Gemini) |
| File Ops | Built-in | Function Calling |
| MCP | ✅ | Chưa (Roadmap) |
| Hooks | ✅ | Chưa (Roadmap) |
| Dependencies | VSCode + Cline | Chỉ Python |

## 🗺️ Roadmap

- [ ] Tích hợp MCP Client (SQLite, Memory, Puppeteer)
- [ ] Chế độ Daemon (chạy ngầm + Discord/Telegram Bot)
- [ ] Auto-approve commands (whitelist)
- [ ] Multi-model routing (Pro cho task khó, Flash cho task dễ)

---
*Author: CEO Sovereign — LangGraph Agent System V4.0*