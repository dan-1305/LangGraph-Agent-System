# 🚀 LangGraph Polymorphic Agent Monorepo

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![MkDocs Enterprise](https://img.shields.io/badge/docs-Enterprise--Grade-green)](http://localhost:8000)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange)](https://python.langchain.com/docs/langgraph)
[![Disaster Recovery](https://img.shields.io/badge/Recovery-Bulletproof-red)](core_utilities/backup_manager.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Chào mừng bạn đến với **LangGraph Polymorphic Agent Monorepo** - Một siêu hệ sinh thái tập trung điều phối và vận hành 12+ dự án trí tuệ nhân tạo chuyên biệt trên nền tảng LangGraph.

---

## 🏗️ Kiến trúc & Triết lý lõi
Dự án được xây dựng dựa trên 3 trụ cột Enterprise:
1. **Tính đa hình (Polymorphism):** Mọi Agent kế thừa từ `BaseAgent`, sở hữu chung cơ chế bảo mật, quản lý bộ nhớ và hệ thống công cụ (Tool Library).
2. **Local Proxy & Định tuyến API:** Trái tim điều phối I/O (Local Proxy Server) tích hợp **Groq**, **OpenRouter**, và Gemini, giúp tối ưu hóa chi phí và tốc độ (30k+ tps).
3. **Phòng thủ đa tầng (Defense-in-depth):** Tích hợp luật "The Death Rule" (Cấm API Key trực tiếp), tự động Backup Workspace vào kho lưu trữ ổ D, và cơ chế phục hồi mã nguồn từ cache VS Code (`recover_vsc.py`).

---

## 📦 Bản đồ Hệ sinh thái (27+ Projects)

### 📈 Nhóm Tài chính & Crypto
- **AI Trading Agent:** Phân tích kỹ thuật, tâm lý thị trường và quản lý rủi ro tự động.
- **Airdrop Guerrilla:** Săn kèo on-chain tự động (EVM, Monad, Soneium...).
- **Stock Forecasting:** Dự báo giá chứng khoán sử dụng mô hình LSTM & Deep Learning.

### 🧠 Nhóm Deep Learning & Research
- **Real Estate Prediction:** Dự báo giá bất động sản sử dụng XGBoost & Segmented Models.
- **Minecraft Eden Simulation:** Mô phỏng xã hội AI trong môi trường Minecraft.

### 🎬 Nhóm Content & Marketing
- **Auto Affiliate Video:** Quy trình tự động từ kịch bản đến edit video Tiktok/Youtube.
- **SillyTavern World Card:** Sáng tạo nhân vật và bối cảnh cho cộng đồng Roleplay.

### 🛠️ Nhóm Core & Auditor
- **Local Proxy Server:** Hệ thống Gateway điều phối API, tích hợp Groq/OpenRouter.
- **Roundtable Debate:** Hội đồng AI tự động tranh luận và thẩm định quyết định kiến trúc.
- **Real Execution Simulator:** Môi trường mô phỏng thực thi mã nguồn để bắt lỗi Logic.
- **Godot Translator:** Giải pháp dịch thuật tự động cho game engine Godot.
- **QA Chaos Agent:** Tự động hóa kiểm thử và "mổ xẻ" các lỗ hổng của LLM.

---

## 📖 Tài liệu hướng dẫn (Enterprise Docs)
Hệ thống sử dụng **MkDocs Material** tự động cào Docstrings từ mã nguồn Python.

### Cách xem tài liệu:
1. Setup môi trường: `uv pip install mkdocs-material mkdocstrings[python]`
2. Chạy server: `uv run mkdocs serve`
3. Xem tại: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## ⚡ Tech Stack
- **Languages:** Python 3.12 (Cốt lõi), JavaScript/TypeScript (MCP Servers), C (DRM Validator).
- **AI Frameworks:** LangGraph, LangChain, OpenAI, Gemini 1.5/3.1, Groq.
- **Data Tools:** Pandas, NumPy, XGBoost, Scikit-learn.
- **Infra:** Docker, GitHub Actions, UV (Package Manager), SQLite (WAL Mode), ChromaDB.

---

## 🛡️ Hướng dẫn Setup nhanh
```bash
# 1. Cài đặt toàn bộ dependencies trong nháy mắt
uv sync

# 2. Ingest dữ liệu vào não bộ hệ thống
uv run python tools/system/rag_ingest.py

# 3. Chạy Dashboard quản lý tập trung
uv run python web_dashboard.py
```

---

## 📝 Bản quyền & Giấy phép
Dự án được bảo hộ bởi giấy phép MIT. © 2026 Jarvis Auto.
