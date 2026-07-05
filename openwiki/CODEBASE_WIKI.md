# 📖 LangGraph Agent System - Codebase Wiki

## 🗺️ High-Level Architecture
This system is a **Modular Monorepo** designed for high-performance AI orchestration.

### 1. Core Engines
- **`src/base_agent.py`**: Foundation for all agents (Inheritance MANDATORY).
- **`src/api_gateway.py`**: Intelligent routing between LLM providers (Gemini, Groq, OpenRouter).
- **`src/database.py`**: SQLite backend with PRAGMA WAL for high concurrency.
- **`core_utilities/`**: Backup Manager, Logger, and System Watchdog.

### 2. Specialized Agent Projects (`/projects`)
- **`local_proxy_server`**: OpenAI-compatible bridge for rotating free Gemini keys.
- **`ai_trading_agent`**: Financial data fetching and automated trade execution.
- **`airdrop_guerrilla`**: Web automation for on-chain crypto tasks.
- **`ceo_agent`**: Central brain for task delegation.

### 3. Developer Tools (`/tools`)
- **System RAG**: Document ingestion and semantic search for codebase context.
- **Auto-Mapper**: Scans codebase to generate `SYSTEM_MAP.md`.

## 🛠️ Essential Workflows
- **Update Brain:** `uv run python tools/system/rag_ingest.py --force`
- **Full Backup:** `uv run python core_utilities/backup_manager.py --full`
- **Free Proxy:** `uv run python -m projects.local_proxy_server.main`

## 🤖 AI Agent Guidelines
- **Context:** Always refer to `docs/SYSTEM_MAP.md` before coding.
- **Rules:** Follow **`.clinerules`** (The Constitution) for security and standards.
- **Circuit Breaker:** Abort task after 3 identical errors.

---
*Created by Cline Architect - Powered by System Map Analysis*
