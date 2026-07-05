# Contributing to LangGraph Agent System

Welcome to the **LangGraph Agent System**! We appreciate your interest in contributing to this AI Software Factory. Because this system operates as a complex Monorepo with integrated, autonomous AI agents, all contributions must adhere to a strict set of rules to maintain workflow integrity.

## 1. Core Mindset (Zero-Guessing & Logic First)
- **Zero-Guessing:** Never assume or guess. If a logic flow is ambiguous, report it or ask for clarification before proceeding.
- **Logic First:** Always sketch out the architecture or logic (using Mermaid diagrams or pseudo-code) before writing actual code.
- **Efficient Tool Usage:** Do not abuse sequential thinking tools for simple logic steps. Make precise, surgical edits.

## 2. Import Mastery (Strict Monorepo Rules)
Relative imports and dynamic path injections are the #1 enemy of this Monorepo structure.
- **MANDATORY:** Always use **Absolute Imports** starting from the project root.
  - *Example:* `from projects.ai_trading_agent.src.config import Config`
  - *Forbidden:* `from . import config` or `sys.path.append(...)`
- **Paths:** Never hardcode absolute file paths (e.g., `C:\...`). Always use `os.path` or `pathlib` (`Path(__file__).resolve()`) to calculate paths relative to the root directory. All databases must point to `data/system_logs.db` or their respective `data/` directories.

## 3. Resource & Hardware Management (Smart Parallelism)
The system runs on a defined workstation environment (Xeon E5 2676v3, 16GB RAM, RX 580 8GB).
- **Never activate `n_jobs=-1`** (100% CPU usage) for any task.
- Apply **Smart Parallelism**: Limit `n_jobs` or threads to 4-8 to allow the OS room to breathe.
- For Playwright or browser automation, limit parallel execution to a maximum of 2-3 tabs to prevent RAM exhaustion.

## 4. API Guard & Security Matrix
- **Absolute Security:** Never hardcode API Keys, Tokens, or Passwords in the source code. Always use environment variables via the `.env` file.
- **Fallback Mechanism:** When declaring an LLM, do not use a raw `ChatOpenAI` instance. You must integrate the "API Matrix" and the `create_fallback_chain` sequence so the system can automatically switch providers when hitting a 429 Quota error.
- **Safe JSON Wrapping:** To avoid 400 Bad Request errors from proxies, the output of LangGraph Tool Calling must always be wrapped in a valid JSON format: `json.dumps({"result": output})`.

## 5. Factory Workflow Integrity
- When coding new logic for an Agent, **do not break the existing architecture** in `src/factory/graph.py`.
- All flows must pass through the standard pipeline: `Planner -> Coder -> Tester -> QA Reviewer -> Triage Director -> Auto-Fixer`.
- The data passed within the LangGraph State is **sacred**. It is strictly forbidden to randomly overwrite important State keys (such as `product_requirements_document`).

Thank you for helping us build a robust, autonomous AI ecosystem!