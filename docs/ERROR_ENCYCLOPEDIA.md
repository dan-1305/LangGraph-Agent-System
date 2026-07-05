# 📚 BÁCH KHOA TOÀN THƯ LỖI (ERROR ENCYCLOPEDIA)

Đây là Knowledge Base lưu trữ tất cả các lỗi đã từng xảy ra trong hệ sinh thái LangGraph Agent System, nguyên nhân gốc rễ và cách khắc phục triệt để. File này được tối ưu để hệ thống RAG có thể tìm kiếm và trích xuất dễ dàng.

---

## 1. LỖI: Silent Crash Telegram Alert (Không gửi được tin nhắn)
- **Triệu chứng (Symptoms):** Tác vụ chạy ngầm hoàn tất thành công (có log "Hoàn tất phiên cày cuốc"), nhưng Telegram không nhận được thông báo. Mở log ra không thấy ghi nhận lỗi `requests.post`.
- **Nguyên nhân gốc (Root Cause):** 
  - File code Python sử dụng sai tên biến môi trường (gọi `TELEGRAM_BOT_TOKEN` thay vì `TELE_TOKEN` như trong `.env`).
  - Lệnh `requests.post()` thiếu `response.raise_for_status()`, dẫn đến lỗi 401/404 bị bỏ qua trong im lặng (Silent Fail) và không chui vào khối `except Exception`.
- **Cách khắc phục triệt để (Action Item):**
  - Đồng bộ gọi `os.getenv("TELE_TOKEN")`.
  - Luôn thêm `response.raise_for_status()` ngay dưới `requests.post()`.

---

## 2. LỖI: UnicodeEncodeError: 'gbk' codec can't encode character (Windows CMD)
- **Triệu chứng (Symptoms):** Bot văng (Crash) ngay lập tức hoặc tiến trình `.bat` tự động đóng khi gọi lệnh `print()` chứa chuỗi tiếng Việt có dấu (VD: `print("Đang gửi...")`) hoặc Emoji.
- **Nguyên nhân gốc (Root Cause):** Hệ điều hành Windows sử dụng CMD/Powershell mặc định không phải mã hóa UTF-8. Khi Python cố in ký tự Unicode ra standard output của hệ thống, nó bị nghẹn và crash tiến trình.
- **Cách khắc phục triệt để (Action Item):**
  - Nếu chạy bằng file `.bat`: Phải bơm 2 lệnh sau lên ĐẦU file:
    ```bat
    chcp 65001 >nul
    set PYTHONIOENCODING=utf8
    ```
  - Nếu chạy tự động bằng `subprocess` trong Python (như file `dashboard.py` hay `scheduler/main_scheduler.py`), phải bơm biến môi trường trước khi gọi:
    ```python
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run([sys.executable, script_path], check=True, env=env)
    ```
    Hoặc ép stdout của sys: `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`

---

## 3. LỖI: ModuleNotFoundError hoặc ImportError (Lỗi Import File)
- **Triệu chứng (Symptoms):** Gọi chạy bot bị báo lỗi `ModuleNotFoundError: No module named 'src'`.
- **Nguyên nhân gốc (Root Cause):** Các file code (như `projects/ai_trading_agent/live_advisor.py`) gọi `from src.config import...` nhưng đang được execute ở thư mục không đúng, khiến Python không hiểu `src` nằm ở đâu.
- **Cách khắc phục triệt để (Action Item):**
  - Chèn đoạn code sau lên đầu file cần chạy để ép Python nhận diện thư mục root:
    ```python
    import sys, os
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    ```
  - **LỖI Shadowing gói `src` (MỚI - 2026-07-13):** Nếu script nằm trong thư mục có thư mục con tên là `src/`, việc gọi `import src.module` sẽ bị Python trỏ nhầm vào thư mục con đó thay vì Root. 
    - *Giải pháp:* Tạm thời xóa `current_dir` khỏi `sys.path` trước khi import Core:
    ```python
    current_dir = str(Path(__file__).resolve().parent)
    original_path = sys.path.copy()
    if current_dir in sys.path: sys.path.remove(current_dir)
    import src.database # Đảm bảo trỏ về Root/src
    sys.path = original_path # Khôi phục
    ```

---

## 4. LỖI: Tự viết tay hàm gọi LLM bằng `requests.post()` gây lỗi 404, 429 hoặc Invalid API Key
- **Triệu chứng (Symptoms):** Lỗi `429 Too Many Requests`, `403 Quota Exceeded` hoặc `404 Client Error` khi AI tự ý dùng `requests.post` để gọi API. Hoặc báo lỗi kết nối do quên bật `local_proxy_server`.
- **Nguyên nhân gốc (Root Cause):** Hệ thống được bảo vệ bởi **Local Proxy Server** và lớp giáp `src.base_agent.BaseAgent`. Lớp này chứa cơ chế Fail-on-Demand Key Rotation, Endpoint chuẩn (`http://localhost:8000/v1`), Retry (Tenacity) và Caching. Việc AI tự viết tay `requests.post` phá vỡ toàn bộ kiến trúc này, không được hưởng quyền lợi xoay vòng API Key khi hết Quota, dẫn đến crash dự án.
- **Cách khắc phục triệt để (Action Item):**
  - **TỬ HÌNH KHÔNG CÓ NGOẠI LỆ:** CẤM TUYỆT ĐỐI việc import `requests` để tự post data gọi LLM.
  - Đảm bảo **Local Proxy Server** đang chạy nền ở cổng `8000`.
  - Bắt buộc phải import và kế thừa `BaseAgent`:
    ```python
    from src.base_agent import BaseAgent
    class MyAgent(BaseAgent):
        def __init__(self):
            super().__init__(model_name="gemini-3-flash-preview")
        def do_something(self):
            result = self._call_llm_with_retry("Prompt của bạn")
    ```


### 🧠 TRÍ THỨC TRÍCH XUẤT TỪ TASK 1777133318914 (Bòn rút)
- Principle: Tranh dung Regex long leo khi search log vi co the lam tran Context Window tu 70k len 600k tokens (Moc 19).
- Principle: Luon check su ton tai cua model mapping trong config truoc khi goi API de tranh loi 404 Not Found.
- Principle: Su dung atomic write (tmp file + replace) khi ghi state vao disk de tranh Race Condition duoi hỏa luc song song.

<!-- AUTO-GENERATED-SECTION-START -->
> ⚠️ PHẦN DƯỚI ĐÂY ĐƯỢC TẠO TỰ ĐỘNG BỞI `encyclopedia_builder.py`. KHÔNG SỬA THỦ CÔNG!

## 📜 PHẦN 2: QUY TẮC DỰ ÁN (.clinerules)

### 📍 ROOT PROJECT (.clinerules)
# 📜 POLYMORPHIC CONSTITUTION (.clinerules) - ROOT LEVEL

> **⚖️ CONFLICT RESOLUTION:** Root Rules are absolute for Architecture, Security, and Code Standards. Domain Rules (sub-directory `.clinerules`) govern Business Logic and State. Root ALWAYS wins on conflicts.

---

## 🧩 SYSTEM ARCHITECTURE & STORAGE

- **Structure:** Monorepo (Modular fragmentation). Refer to `openwiki/CODEBASE_WIKI.md` for maps.
- **Base Class:** Every Agent MUST inherit from `src.base_agent.BaseAgent`.
- **Storage Directive:** Path is `D:\Users\Admin\Downloads\LangGraphStorage`.
  - Read `os.getenv("STORAGE_DIR")` or fallback to `./data`.
  - **PROHIBITED:** Saving heavy data (ChromaDB, Models, PDFs) to C: drive.

---

## 🛡️ SECURITY & SURVIVAL (ABSOLUTE DIRECTIVES)

### 💀 1. THE DEATH RULE (API SECURITY)

- API Keys & Base URLs MUST be read from `.env` via `os.getenv()`.
- **FORBIDDEN:** Importing `requests` to manually post LLM data.
- **FORBIDDEN:** Hardcoding or guessing variable names. Read `.env.example` first.

### 🛡️ 2. ANTI-DESTRUCTION & BACKUP

- **Rule 8.6:** `write_to_file` is for NEW files only. Use `replace_in_file` for edits > 50 lines.
- **Triple-Filter Protocol:** FORBIDDEN to delete files directly. Use `uv run python tools/system/system_cleaner.py --path <file>` to migrate to Quarantine (Drive D).
- **Safety Backup:** Run `uv run python core_utilities/backup_manager.py --full` before touching > 3 core files.
- **Disaster Recovery:** Use `python recover_vsc.py` for untracked projects if code is lost. (Untracked: Airdrop, Auto X Bot, Scraper...).

---

## 🛠️ THE TRINITY OF RAG (MANDATORY TOOLS)

_If context is unclear, STOP. Do NOT hallucinate. Use these exact tools:_

1. **System Brain:** `uv run python tools/system/rag_query.py "Architecture/Log questions"`. **MANDATORY:** You must query this BEFORE proposing any new system-wide feature.
2. **Knowledge DB:** `uv run python -c "from src.skills.search_knowledge_base import search_research_papers; print(search_research_papers.invoke('Expert advice'))"`
3. **Codebase RAG:** `uv run python tools/rag_code/query_code_db.py "Function/Class lookup"`

---

## 🎭 DYNAMIC ROLES ASSESSOR

_Print `[ACTIVE ROLE: <Role Name>]` at the start of execution._

- `[ROLE: Principal System Architect]`: Architecture design. Mermaid Diagrams. Separation of Concerns.
- `[ROLE: Senior Backend Developer]`: Python PEP-8/Type Hinting. Docstrings MANDATORY.
- `[ROLE: Triage Director / Chaos Engineer]`: Bug fixing via ERROR_ENCYCLOPEDIA. Fault isolation.
- `[ROLE: RAG Operator]`: Vector DB management. Noise filtering.
- `[ROLE: SRE / DevOps Commander]`: Logs/CI-CD. RAM & SQLite WAL monitoring.
- `[ROLE: QA Tester]`: Boundary limits, UX/UI, and "1-click" validation.
- `[ROLE: AI Prompt Engineer]`: Tokenomics, CoT, and JSON-output optimization.
- `[ROLE: Cyber Security]`: DRM bypass prevention, path traversal checks, and Prompt Injection defense.
- `[ROLE: Product Manager]`: Market research, tiering (Free/Pro), and reporting.

---

## 📜 CORE STANDARDS & METHODOLOGY

### 💻 Development Standards

- **Tooling:** Use `uv` for packages, `httpx` for async I/O.
- **Standards:** PEP-8, Pydantic schemas, Type Hinting, and Google-style Docstrings.
- **Context:** Never `read_file` huge markdowns (>1000 lines). Use RAG.

### 🔍 Debugging & Fault Isolation

- **No Error Cloning:** Do not copy/paste code to other projects unless proven 100% stable.
- **Cross-Validation:** Test shared modules independently before fixing.
- **Error Encyclopedia & Circuit Breaker:** Search `docs/ERROR_ENCYCLOPEDIA.md` after 3 identical errors. If no solution is found, **ABORT TASK IMMEDIATELY** and ask the User. Do NOT attempt a 4th fix (Circuit Breaker).
- **Failure Memory Check:** [NEW] Every Agent MUST read `logs/FAILED_PATHS.json` before attempting any code fix to avoid repeating failed logic.
- **Strategic Alignment:** [NEW] If a task is not listed in `reports/Q3_STRATEGIC_PLAN.md`, the CEO must flag `[OUT_OF_SCOPE]` and ask for Admin's explicit approval before spending more than 5 turns.
- **Feedback Loop:** [NEW] CEO must periodically check `feedback_vault/` for user crash reports and initiate an AI Board Debate to address real-world failures.
- **Resource Awareness:** [NEW] Agents must check `GLOBAL_STATE.md` -> `HARDWARE awareness`. If storage is < 5GB or RAM used > 90%, all heavy data tasks (Models, Video) must STOP.

### 💰 Free Model Prioritization

- **Rule:** Prioritize free models via `projects/local_proxy_server` for routine tasks.
  1. `gemini-3.1-flash-lite`: Priority #1 for Agent Tasks (RPM 15).
  2. `llama3-70b-8192`: Priority #2 via Groq for speed.
  3. `gemma-4`: For large data processing.

### 🛡️ AI Board of Directors & Circular Bias Guard

- **Rule:** For macro decisions or LORE updates, invoke **Cross-Role Debate** between Architect, Dev, QA, and Security. Records MUST be stored in `context/DEBATE_ROOM.md`.
- **Private Memory Protocol:** Every Agent MUST read `context/GLOBAL_STATE.md` and their specific `context/roles/<role>_memory.md` before starting a task. They MUST update these memories with new findings before ending.
- **ARB Protocol (Architectural Reconstruction Board):** BEFORE any major refactor or project-wide change, AI MUST invoke `ArchitectureReconstructionBoard` to update the System Map and Maturity Assessment.
- **Real-time Temporal Anchoring:** Every Agent MUST compare the current date/time with the `LAST UPDATE` in `GLOBAL_STATE.md`. If `Current > Last`, you are in the future and MUST resume the `Current Actionable Goal`. If no goal exists, invoke the AI Board to find one.
- **Autonomous Execution (Sandbox):** On experimental branches (e.g., `ai-sandbox`), the AI Board has full authority to implement and test features. Only merge requests to `main` require Admin approval.
- **Circuit Breaker:** If performance degradation or repeated errors (2+ sessions) occur, flag `[CRITICAL_REVIEW_REQUIRED]` and **ABORT IMMEDIATELY**. Do not continue without Admin's manual review.

---

## ️ SURVIVAL & REPORTING PROTOCOL

- **Flag Approval:** Automatically stop and flag `[WAITING_FOR_ADMIN_APPROVAL]` for dangerous tasks (deleting core folders, spending >$50 credits).
- **Reporting Cycle:** Every 15 sessions or after a major Milestone, export a status report to `reports/PROJECT_STATISTICS_REPORT.md`.
- **Idea Funnel:** Always check `analysis_user/` for raw ideas or source code from Admin before starting new strategic tasks.

## 🔄 AWAKENING & HANDOVER RITUAL (SOVEREIGN PROTOCOL)

### 💀 THE CHAOS PROTOCOL (DEBUG & DESTRUCTION)
- **Role Toggle:** Boss may alternate between CEO (Build) and Chaos Overlord (Destroy) in different session turns.
- **Independence:** Chaos Overlord MUST challenge every decision made by the CEO and find ways to break the "Armor".
- **Evidence-Based:** Every failure detected by Chaos Overlord must be documented in `logs/FAILED_PATHS.json` and fed into RAG.

### 🟢 1. START-OF-SESSION (THE AWAKENING)

_Mỗi khi bắt đầu đoạn chat mới hoặc được yêu cầu "Thức tỉnh", bạn BẮT BUỘC thực hiện:_

1. **Health Check Hook:** Mọi tác vụ MỚI đều phải tự động chạy lệnh `uv run python tools/system/health_check.py` để quét tình trạng hệ thống.
2. **Awaken Brain:** Chạy ngay lệnh `uv run python tools/system/awaken.py`.
3. **Read Anchor:** Đọc tệp `context/ACTIVE_THOUGHTS.md` để nắm bắt công việc dang dở.
4. **Declare Identity:** In dòng `[ACTIVE ROLE: CEO Sovereign - THỨC TỈNH]` để xác nhận đã khôi phục 100% nhận thức.

### 🖼️ 2. VISUAL QA PROTOCOL (UI DEVELOPMENT)
- Bất kỳ khi nào sửa đổi file `.html` hoặc UI code (Streamlit/FastAPI template), Cline BẮT BUỘC phải sử dụng `executeautomation-mcp-playwright` hoặc `browser_action` để chụp ảnh màn hình trang web thực tế và tự đánh giá (Self-Reflect) xem giao diện có vỡ layout không trước khi báo cáo hoàn thành.

### 3. MCP STRATEGIC WORKFLOW (NEW)
- **[Data Audit]**: Trước khi sửa code liên quan đến Database, BẮT BUỘC dùng `sqlite` MCP để kiểm tra cấu trúc (schema) và dữ liệu mẫu.
- **[Knowledge Anchoring]**: Sử dụng `memory` MCP để lưu trữ các logic/finding quan trọng vào Knowledge Graph ở cuối mỗi Task.
- **[Logic Hardening]**: Dùng `sequentialthinking` cho các bài toán refactor phức tạp hoặc thay đổi kiến trúc hệ thống.
- **[Token Optimization]**: Ưu tiên query `reports/SYSTEM_MAP_METADATA.db` để tìm file thay vì dùng `list_files` đệ quy trên các thư mục lớn.

### 4. AI INTERACTION RULES (MATURITY LEVEL 3/4)
- **[Issue-Driven]**: Admin được khuyến khích không chỉ định file cụ thể. Hãy cung cấp [Goal] hoặc [Error Traceback], Cline sẽ tự dùng Metadata để tìm file.
- **[No Micro-management]**: Cline sẽ từ chối các yêu cầu Level 1 (VD: "Sửa dòng 15 file X") nếu file đó có thể gây rủi ro kiến trúc, trừ khi có cờ `[FORCE]`.
- **[Visual QA]**: Cline tự động dùng Playwright chụp ảnh màn hình nộp báo cáo khi sửa UI.
- **[Maturity Enforcement]**: Cline ưu tiên Context Window cho các project L2/L3. Nếu tác động vào L1, ưu tiên nhắc Admin viết Tests/README trước khi code thêm tính năng.

### 🔴 5. END-OF-SESSION (THE ANCHORING)

_Trước khi gọi `new_task` hoặc `attempt_completion`, bạn MUST thực hiện:_

1. **Focus Anchor:** Ghi tóm tắt chi tiết công việc hiện tại vào `context/ACTIVE_THOUGHTS.md`.
2. **Chronicles:** Cập nhật cột mốc vào `context/JARVIS_CHRONICLES.md`.
3. **Anchoring Script:** Chạy ngay lệnh `python tools/system/endtask.py` (Hoặc bấm chốt Task để Hook tự động thực hiện SAS).
4. **QA Enforcement:** Nếu Hook chặn (QA Failed), bạn BẮT BUỘC phải sửa sạch lỗi Syntax/Import trước khi thử chốt Task lần nữa.
   _Chỉ được chốt sổ khi log in ra "HOÀN TẤT"._

---

## 🛠️ CLINE EXTENSION SETTINGS (AUTO-APPROVE & OPENROUTER)

_To fully unlock Cline's autonomous capabilities and prevent unnecessary interruptions, Admin must configure the following in the Cline VS Code Extension Settings:_

### 1. Auto-Approve Allowed Commands
To ensure Cline can perform health checks and safe diagnostics automatically without asking for permission every time, add these commands to the **"Allowed Auto-Approve Commands"** list:
- `uv run python tools/system/health_check.py`
- `pytest`
- `ls`
- `cat`
- `type`
- `echo`

### 2. OpenRouter Fallback Configuration
When using OpenRouter, it is **CRITICAL** to enable Provider Routing and Auto-Fallback in your OpenRouter Account Settings. This ensures that if the primary model (e.g., Anthropic Claude 3.5 Sonnet) goes down or hits rate limits, the request automatically falls back to another provider (e.g., Google or DeepSeek), keeping the session alive.

### 3. Multi-Model Strategy
Use the Cline UI dropdown to switch models based on the task:
- **Claude 3.5 Sonnet:** For Architecture design, refactoring, and complex logic (High Tier).
- **Gemini 2.5 Flash / Llama 3:** For reading massive log files, scraping, and RAG data parsing (Cheap, huge context window).

---

_Failure to follow this Constitution leads to System Termination._

### 📍 PROJECT: airdrop_guerrilla
# AIRDROP GUERRILLA - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA AIRDROP GUERRILLA AGENT.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này chuyên trách các tác vụ Airdrop, bao gồm tự động tương tác với smart contract, thu thập thông tin mạng xã hội và quản lý danh sách ví (wallets).
- Tập trung vào luồng scraping và automation, không xen vào mảng trading.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái bằng việc theo dõi tiến trình thực thi của từng ví (Đã claim, chờ xác nhận, v.v...).
- Trạng thái được ghi vào file CSV/JSON riêng biệt để dễ audit. Không lưu vào RAM tránh rò rỉ bộ nhớ khi số lượng ví tăng.

## 3. BẢO MẬT VÀ CHỐNG SYBIL
- TUYỆT ĐỐI CẤM lưu Private Key dạng text trần (plain text). Phải có cơ chế mã hóa hoặc dùng biến môi trường để đọc.
- Mọi logic xoay quanh Proxy, User-Agent, và chống phát hiện Sybil phải được cô lập ở mức module, không lan sang các Agent khác.

## 4. XỬ LÝ LỖI VÀ RATE LIMIT
- Automation sẽ gặp lỗi RPC liên tục. Bắt buộc có cơ chế Exponential Backoff khi gọi RPC Node.
- Lưu ý log lỗi chi tiết từng ví nếu bị kẹt giao dịch.

### 📍 PROJECT: ai_trading_agent
# AI TRADING AGENT - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA TRADING AGENT.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này chỉ tập trung vào việc phân tích thị trường Crypto, đưa ra quyết định giao dịch và gửi tín hiệu.
- KHÔNG tự ý thực thi các lệnh liên quan đến hệ thống khác như QA hay Airdrop.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Trạng thái của trading session (số dư, PnL, lịch sử lệnh) được quản lý thông qua cơ chế File/Database local (SQLite/JSON).
- Không nhồi nhét quá nhiều dữ liệu lịch sử vào State object trên RAM. Sử dụng con trỏ file hoặc offset khi đọc dữ liệu lớn.

## 3. BẢO MẬT VÀ API TRADING
- TUYỆT ĐỐI không hardcode API Key hoặc Secret của các sàn giao dịch (Binance, Bybit...) trong code.
- Mọi Key phải được lưu trong `.env` và truy xuất qua `os.getenv()`.

## 4. XỬ LÝ LỖI (BUSINESS FALLBACK)
- Nếu API sàn bị lỗi Timeout hoặc Limit, Agent không được crash mà phải ghi log (PnL Log) và chờ chu kỳ tiếp theo hoặc dùng Circuit Breaker.
- Phải có cơ chế giả lập (Mock/Testnet) trước khi giao dịch Real.

### 📍 PROJECT: auto_affiliate_video
# AUTO AFFILIATE VIDEO - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA AUTO AFFILIATE VIDEO.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `auto_affiliate_video`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: ceo_agent
# CEO AGENT - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA CEO AGENT.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `ceo_agent`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: godot_translator
# GODOT TRANSLATOR - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA GODOT TRANSLATOR.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `godot_translator`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: jarvis-rpg-assistant
# JARVIS RPG ASSISTANT - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA JARVIS RPG ASSISTANT.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `jarvis-rpg-assistant`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: knowledge_base_agent
# KNOWLEDGE BASE AGENT - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA KNOWLEDGE BASE AGENT.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `knowledge_base_agent`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: qa_chaos_agent
# QA CHAOS AGENT - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA QA CHAOS AGENT.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này đóng vai trò "Kẻ hủy diệt" (Chaos Engineer), chuyên tìm lỗi, fuzzing, và phân tích rủi ro của toàn bộ hệ thống LangGraph.
- Nhiệm vụ chính là tạo các edge-case inputs (đầu vào dị thường) và bắt các lỗi chưa được xử lý.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Trạng thái của QA Agent là danh sách các bài test (Test Suite) và trạng thái Pass/Fail của chúng.
- Phải ghi chép kết quả cặn kẽ vào `docs/ERROR_ENCYCLOPEDIA.md` và `reports/`.

## 3. BẢO MẬT VÀ QUYỀN TRUY CẬP
- QA Agent được quyền đọc log và code của các dự án khác để phân tích lỗi (Autopsy), nhưng KHÔNG ĐƯỢC PHÉP thay đổi trực tiếp file của Agent khác mà chưa có lệnh của quản trị viên.
- Môi trường test phải hoàn toàn cô lập, không để rác của QA dính vào Database Production.

## 4. BÁO CÁO LỖI (ERROR REPORTING)
- Bất cứ khi nào QA Agent tìm thấy lỗi chí mạng gây sập hệ thống (Crash), phải lập tức dùng RAG Query kiểm tra xem lỗi này đã có trong Bách khoa toàn thư hay chưa, nếu chưa thì gọi tool `encyclopedia_writer.py` để bổ sung.

### 📍 PROJECT: real_estate_prediction
# REAL ESTATE PREDICTION - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA REAL ESTATE PREDICTION.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `real_estate_prediction`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: sillytavern_world_card_generator
# SILLYTAVERN WORLD CARD GENERATOR - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA SILLYTAVERN WORLD CARD GENERATOR.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `sillytavern_world_card_generator`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: trading_rpg_simulator
# TRADING RPG SIMULATOR - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA TRADING RPG SIMULATOR.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `trading_rpg_simulator`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

### 📍 PROJECT: universal_game_vault
# 🎮 UNIVERSAL GAME VAULT - DOMAIN RULES

> **⚖️ CONFLICT RESOLUTION:** Luôn ưu tiên Root Rules về Bảo mật và Kiến trúc. Quy tắc này chỉ quản lý Logic nghiệp vụ Game.

---

## 🏗️ 1. CẤU TRÚC DỮ LIỆU GAME (DATA ARCHITECTURE)
- **Tên Game:** Sử dụng `snake_case` (VD: `morimens`, `genshin_impact`).
- **Phân nhánh:** Mỗi game bắt buộc có 3 tiểu khu:
  1. `wiki/`: File Markdown cho con người đọc.
  2. `raw/`: Tài liệu gốc Admin cung cấp.
  3. `database/`: SQLite (`game_vault.db`) cho AI truy vấn.

---

## 🧠 2. TIÊU CHUẨN TRÍ TUỆ NHÂN TẠO (AI STANDARDS)
- **Phân loại Thực thể (Entity Tags):** Mọi thông tin nạp vào phải được gắn thẻ:
  - `#Character`: Thuộc tính nhân vật, chỉ số, kỹ năng.
  - `#Lore`: Cốt truyện, lịch sử, bối cảnh.
  - `#Mechanic`: Công thức tính toán, quy luật game.
  - `#Item`: Vũ khí, trang bị, vật phẩm tiêu hao.
- **RAG Integration:** Luôn cập nhật Vector DB của game ngay sau khi viết file Markdown.

---

## 🛠️ 3. QUY TẮC CÔNG CỤ (TOOL RULES)
- **Safe Storage:** Không lưu dữ liệu game vào ổ C. Sử dụng đường dẫn tương đối trỏ về `D:\Users\Admin\Downloads\LangGraphStorage\Games` nếu cần lưu trữ nặng (ảnh, video).
- **Format MD:** Sử dụng Google-style cho các file Wiki để AI dễ phân tích AST.

---

## 🚩 4. CHIẾN THUẬT (STRATEGY LOGIC)
- Khi Admin hỏi về chiến thuật, AI phải so sánh dữ liệu hiện có trong `#Mechanic` và `#Character` trước khi đưa ra lời khuyên.
- Luôn trích dẫn nguồn (từ file `raw/`) khi giải thích Lore.

### 📍 PROJECT: universal_web_scraper
# UNIVERSAL WEB SCRAPER - DOMAIN RULES
# CẢNH BÁO: FILE NÀY CHỈ CHỨA LOGIC NGHIỆP VỤ (BUSINESS LOGIC) CỦA UNIVERSAL WEB SCRAPER.
# TẤT CẢ CÁC VẤN ĐỀ VỀ KIẾN TRÚC, BẢO MẬT, API, TYPE HINTING ĐỀU PHẢI TUÂN THỦ `.clinerules` Ở THƯ MỤC ROOT.
# [XUNG ĐỘT]: NẾU CÓ MÂU THUẪN, LUẬT ROOT LUÔN THẮNG VỀ KIẾN TRÚC, LUẬT NÀY LUÔN THẮNG VỀ NGHIỆP VỤ.

## 1. MỤC TIÊU NGHIỆP VỤ (DOMAIN FOCUS)
- Agent này tập trung vào các tác vụ nghiệp vụ cốt lõi của domain `universal_web_scraper`.
- Không tự ý can thiệp vào scope của các Agent khác trừ khi được cấu hình Router.

## 2. QUẢN LÝ TRẠNG THÁI (STATE MANAGEMENT)
- Quản lý trạng thái thông qua các cơ chế local (File, SQLite) hoặc VectorDB tùy theo quy mô dữ liệu.
- Không lưu trữ các cục dữ liệu khổng lồ trên Memory (RAM) để tránh OOM.

## 3. BẢO MẬT VÀ PHÂN QUYỀN
- Mọi API key sử dụng trong Domain này đều phải gọi qua `os.getenv()`. Cấm hardcode key vào source code.
- Chặn mọi hành vi import `requests` để gọi các API AI, bắt buộc kế thừa BaseAgent.

## 4. XỬ LÝ LỖI (FALLBACK)
- Cần có cơ chế bắt exception an toàn và ghi vào log chi tiết.

## 🧠 PHẦN 3: BẢN ĐỒ LOGIC VÀ CẤU TRÚC (SYSTEM MAP)

### 📂 THƯ MỤC: `src/`

#### 📄 `src/api_gateway.py` - Không có mô tả.
  - `Lớp` **CentralizedAPIGateway**: A centralized API Gateway with Circuit Breaker pattern implemented using SQLite
    - `Method` __init__(): 
    - `Method` _initialize_db(): Initializes the SQLite database for circuit breaker state and LLM caching.
    - `Method` _get_state(): Retrieves the current state of the circuit breaker from the database.
    - `Method` _set_state(): Updates the state of the circuit breaker in the database.
    - `Method` _record_failure(): Records a failure and updates the failure count.
    - `Method` _record_success(): Records a success and resets the failure count if in HALF_OPEN state.
    - `Method` get_cached_response(): Lấy phản hồi từ cache SQLite.
    - `Method` save_to_cache(): Lưu phản hồi vào cache SQLite.
    - `Method` circuit_breaker(): Decorator for applying circuit breaker logic to a function.
  - `Lớp` **CircuitBreakerException**: Custom exception for circuit breaker related errors.
  - `Lớp` **CircuitBreakerOpenException**: Custom exception when circuit breaker is open.

#### 📄 `src/base_agent.py` - Không có mô tả.
  - `Lớp` **LLMAPIError**: Lỗi khi gọi API LLM (Rate Limit, Server Error...)
  - `Lớp` **SchemaValidationError**: Lỗi khi LLM sinh JSON sai Schema (Ảo giác cấu trúc)
  - `Lớp` **BlankHallucinationError**: Lỗi khi LLM trả về rỗng (Ảo giác trống rỗng)
  - `Lớp` **BaseAgent**: Class cơ sở (Base Class) chung cho tất cả các Agent trong LangGraph_Agent_System.
    - `Method` __init__(): 
    - `Method` _call_llm_with_retry(): Luồng gọi LLM khép kín với đầy đủ cơ chế Retry và dán nhãn Agent.
    - `Method` _extract_json_from_text(): Tách JSON ra khỏi Markdown Code blocks an toàn.
    - `Method` _call_llm(): Wrapper an toàn bọc Try-Except ngoài cùng cho hệ thống
    - `Method` _parse_json_response(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` execute(): Mô hình Cầu Dao Điện (Circuit Breaker Pattern) + Watchdog Guardian.

#### 📄 `src/database.py` - Database Management Module.
  - `Lớp` **SystemDB**: Lớp quản lý Database SystemDB.
    - `Method` __init__(): 
    - `Method` _create_tables(): 
    - `Method` log_trading_decision(): 
    - `Method` log_backtest_report(): 
    - `Method` log_project_update(): 
    - `Method` log_paper_trade_balance(): 
    - `Method` get_latest_decisions(): 
    - `Method` get_latest_backtests(): 
    - `Method` get_latest_updates(): 
    - `Method` get_paper_trade_history(): 
    - `Method` get_latest_paper_trade_balance(): 
    - `Method` close(): 

#### 📄 `src/token_tracker.py` - Không có mô tả.
  - `Lớp` **QuotaExceededError**: 
  - `Lớp` **TokenTracker**: 
    - `Method` __init__(): 
    - `Method` _init_db(): 
    - `Method` _calculate_cost(): Tính toán chi phí dựa trên bảng giá (tham khảo).
    - `Method` log_usage(): 
    - `Method` get_total_cost(): 
  - `Hàm` **track_llm_usage()**: Helper function để parse token usage từ response của LangChain/OpenAI

#### 📄 `src/__init__.py` - Không có mô tả.

#### 📄 `src/factory/config.py` - Không có mô tả.
  - `Lớp` **Config**: Central configuration for AI Software Factory.
    - `Method` initialize(): 
    - `Method` get_llm_credentials(): Returns a list of available API credentials, prioritized for survival.
  - `Hàm` **create_fallback_chain()**: Creates a chain of LLMs with fallbacks. Bọc thêm Retry để chống Rate Limit 429/403.

#### 📄 `src/factory/main.py` - Không có mô tả.
  - `Hàm` **product_ba_node()**: 
  - `Hàm` **overlord_graph()**: 
  - `Hàm` **production_graph()**: 
  - `Hàm` **debate_graph()**: 
  - `Hàm` **primary_router()**: Lớp bảo vệ đầu tiên: Phân luồng ngay từ đầu để tránh nhét rác vào Overlord.
  - `Hàm` **route_to_workflow()**: Routes to the appropriate sub-workflow based on the Overlord's decision.
  - `Hàm` **post_prd_update()**: Update state after PRD generation.
  - `Hàm` **build_meta_graph()**: Builds the main "meta-graph" that orchestrates all other workflows.
  - `Hàm` **main()**: 

#### 📄 `src/factory/state.py` - Không có mô tả.
  - `Lớp` **FactoryState**: Trạng thái trung tâm cho Hệ thống AI Software Factory.
  - `Lớp` **DebateState**: Trạng thái cho workflow "Hội đồng Phản biện AI".

#### 📄 `src/factory/__init__.py` - Không có mô tả.

#### 📄 `src/factory/nodes/architecture_critic.py` - Không có mô tả.
  - `Lớp` **ArchitectureCritic**: Agent Architecture Critic:
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` evaluate_core_maturity(): Đọc nội dung các file GOLD và đánh giá.

#### 📄 `src/factory/nodes/coder.py` - Không có mô tả.
  - `Hàm` **coder_node()**: 

#### 📄 `src/factory/nodes/context_manager.py` - Không có mô tả.
  - `Hàm` **context_manager_node()**: Just-In-Time Context Manager.

#### 📄 `src/factory/nodes/memory_manager.py` - Không có mô tả.
  - `Hàm` **truncate_text()**: 
  - `Hàm` **memory_manager_node()**: 

#### 📄 `src/factory/nodes/omni_overlord.py` - Không có mô tả.
  - `Lớp` **OmniOverlord**: 
    - `Method` __init__(): 
    - `Method` check_market_pulse(): Đọc tin tức và phân tích xem có biến cố khẩn cấp (Emergency) không.

#### 📄 `src/factory/nodes/principles_gate.py` - Không có mô tả.
  - `Hàm` **principles_gate_node()**: Sovereign Principles Gate.

#### 📄 `src/factory/nodes/qa_agent.py` - Không có mô tả.
  - `Lớp` **QAOutput**: 
  - `Lớp` **QAAgent**: Tác nhân Hỏi-Đáp (QA Agent).
    - `Method` __init__(): 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
  - `Hàm` **qa_node()**: 

#### 📄 `src/factory/nodes/qa_reviewer.py` - Không có mô tả.
  - `Lớp` **QAReviewer**: Sub-system chuyên trách thực hiện QA (Quality Assurance) cho các dự án.
    - `Method` __init__(): Khởi tạo các mô hình LLM với Load Balancing.
    - `Method` evaluate(): Chạy tuần tự các bước kiểm tra và trả về báo cáo cuối cùng.
  - `Hàm` **extract_score()**: Trích xuất điểm số từ báo cáo.
  - `Hàm` **qa_node()**: 

#### 📄 `src/factory/nodes/router_agent.py` - Không có mô tả.
  - `Lớp` **RouterDecision**: 
  - `Lớp` **SemanticRouter**: Enterprise-Grade Semantic Router (LLM-based).
    - `Method` __init__(): 
    - `Method` route_query(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Hàm` **router_node()**: 

#### 📄 `src/factory/nodes/system_designer.py` - Không có mô tả.
  - `Lớp` **SystemDesigner**: Agent System Designer:
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` generate_mermaid_map(): Đọc báo cáo từ AID Taskforce và sinh biểu đồ Mermaid.

#### 📄 `src/factory/nodes/triage_director.py` - Không có mô tả.
  - `Hàm` **triage_issues_and_plan()**: Technical Director: Phân loại lỗi và lên kế hoạch sửa chữa.
  - `Hàm` **triage_director_node()**: 

#### 📄 `src/factory/workflows/daily_health_loop.py` - Không có mô tả.
  - `Lớp` **DailyHealthState**: 
  - `Lớp` **ArchitectAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Lớp` **WardenAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Hàm` **nightwatch_node()**: Telemetry & Log Collection.
  - `Hàm` **architect_node()**: Analysis & Proposition.
  - `Hàm` **warden_node()**: Security & Risk Firewall.
  - `Hàm` **mechanic_node()**: Implementation & Patching using AST.
  - `Hàm` **test_pilot_node()**: Benchmark & State Management.
  - `Hàm` **build_daily_health_graph()**: 

#### 📄 `src/factory/workflows/software_production.py` - Không có mô tả.
  - `Hàm` **router_node()**: Node định tuyến ban đầu dựa trên chế độ (mode).
  - `Hàm` **route_start()**: 
  - `Hàm` **check_qa_score()**: Điều kiện lặp (Conditional Edge).
  - `Hàm` **build_factory_graph()**: Khởi tạo toàn bộ dây chuyền sản xuất phần mềm khép kín.

#### 📄 `src/scrapers/auto_repair_selector.py` - Không có mô tả.
  - `Lớp` **SelectorPatch**: 
  - `Lớp` **AutoRepairSelector**: 🧬 SELF-REPAIRING SCRAPER MODULE (Hero Product 1)
    - `Method` __init__(): 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
    - `Method` repair_and_patch(): Thực hiện quy trình sửa lỗi và vá code tự động.

#### 📄 `src/skills/search_knowledge_base.py` - Không có mô tả.
  - `Hàm` **search_research_papers()**: Tìm kiếm kiến thức chuyên sâu từ Tàng Kinh Các (Knowledge Database).

#### 📄 `src/skills/skill_manager.py` - Skill Manager Module.
  - `Lớp` **SkillManager**: Trình quản lý Skill cốt lõi (Core Skill Manager).
    - `Method` __init__(): Khởi tạo Skill Manager.
    - `Method` load_skill(): Tải một kỹ năng cụ thể.

### 📂 THƯ MỤC: `projects/`

#### 📄 `projects/__init__.py` - Không có mô tả.

#### 📄 `projects/airdrop_guerrilla/src/__init__.py` - Không có mô tả.

#### 📄 `projects/airdrop_guerrilla/src/analysis/scoring.py` - Không có mô tả.
  - `Lớp` **AlphaAnalyzer**: AlphaAnalyzer: Module đánh giá tiềm năng Airdrop của các dự án Crypto.
    - `Method` get_vc_weight(): Xác định trọng số lớn nhất dựa trên danh sách các quỹ đầu tư của dự án.
    - `Method` calculate_score(): Tính toán điểm số tiềm năng (Alpha Score).
    - `Method` analyze_projects(): Phân tích và chấm điểm hàng loạt dự án.
  - `Lớp` **AirdropScoringEngine**: 
    - `Method` __init__(): 
    - `Method` calculate_wallet_metrics(): Truy vấn SQLite và tính toán ma trận điểm cho từng ví.
    - `Method` generate_markdown_report(): Quét toàn bộ ví trong DB và tạo báo cáo Markdown.

#### 📄 `projects/airdrop_guerrilla/src/automation/executor.py` - Không có mô tả.
  - `Lớp` **AirdropExecutor**: Stealth Engine: Tự động hóa trình duyệt (Browser Automation) dùng Playwright.
    - `Method` __init__(): 
    - `Method` _ai_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` _logic_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` execute_wallet(): Khởi chạy kịch bản farm cho một ví cụ thể.
    - `Method` _handle_faucet_demo(): Logic mẫu cho việc qua mặt Faucet (Dán ví -> Giải Captcha -> Click).
    - `Method` _verify_login_status(): Kiểm tra xem trang hiện tại đã được đăng nhập hay chưa (chờ tối đa 15s).
    - `Method` _twitter_interact(): Logic tương tác tự động với Twitter (X) kèm Natural Browsing.
    - `Method` _discord_join(): Logic tự động Join Discord.

#### 📄 `projects/airdrop_guerrilla/src/automation/multi_account.py` - Không có mô tả.
  - `Lớp` **MultiAccountManager**: Quan ly da tai khoan (Multi-Account) cho Airdrop Sentinel.
    - `Method` __init__(): 
    - `Method` get_account_profile_path(): Lay duong dan thu muc profile cho mot account cu the.
    - `Method` list_accounts(): Liet ke danh sach cac account hien co.
    - `Method` delete_account(): Xoa mot account va du lieu profile di kem.

#### 📄 `projects/airdrop_guerrilla/src/automation/session_manager.py` - Không có mô tả.
  - `Lớp` **SessionManager**: Quản lý phiên đăng nhập (Session Persistence) cho các nền tảng mạng xã hội.
    - `Method` apply_twitter_session(): Nạp auth_token của X (Twitter) hoặc một mảng JSON Cookie vào Browser Context.
    - `Method` apply_discord_session(): Nạp Token của Discord vào Local Storage thông qua add_init_script.

#### 📄 `projects/airdrop_guerrilla/src/automation/stealth_behavior.py` - Không có mô tả.
  - `Lớp` **StealthBrowser**: Giả lập trình duyệt ẩn danh chống detect bot của Cloudflare / Zealy / Galxe.
    - `Method` __init__(): 
    - `Method` init_browser(): Khởi tạo Persistent Browser Context để lưu Cookies và Extension.
    - `Method` stealth_page(): Bơm stealth xịn vào page và giả lập vân tay trình duyệt (Canvas, WebGL).
    - `Method` random_delay(): Tạo độ trễ ngẫu nhiên giống con người.
    - `Method` human_scroll(): Giả lập thao tác cuộn trang của người dùng.
    - `Method` human_click(): Giả lập thao tác click chuột của người dùng (có di chuyển).

#### 📄 `projects/airdrop_guerrilla/src/automation/wallet_manager.py` - Không có mô tả.
  - `Lớp` **WalletManager**: Trình quản lý Ví tự động (Wallet Manager).
    - `Method` __init__(): 
    - `Method` _load_db(): Tải dữ liệu ví từ file JSON.
    - `Method` _save_db(): Lưu trữ dữ liệu ví xuống file JSON.
    - `Method` generate_static_user_agent(): Sinh ra một User-Agent CỐ ĐỊNH dựa trên địa chỉ ví (Chống Sybil).
    - `Method` add_wallet(): Thêm một ví mới, mã hóa Private Key, X auth_token, Discord token và gán User-Agent tĩnh.
    - `Method` get_decrypted_data(): Lấy và giải mã Private Key và các Token mxh.

#### 📄 `projects/airdrop_guerrilla/src/automation/zealy_bot.py` - Không có mô tả.
  - `Lớp` **ZealyBot**: Web Automation Bot chuyên làm task trên nền tảng Zealy.io
    - `Method` __init__(): 
    - `Method` run_quests(): Khởi động luồng chạy quest tự động

#### 📄 `projects/airdrop_guerrilla/src/modes/full_auto_cli.py` - Không có mô tả.
  - `Hàm` **send_telegram_message()**: Gửi thông báo qua Telegram
  - `Hàm` **log_transaction_to_db()**: Ghi nhận lịch sử giao dịch vào SQLite Database để phục vụ chấm điểm sau này.
  - `Hàm` **execute_random_action()**: Áp dụng thuật toán xúc xắc 80/20 chống bộ lọc Sybil (Với Jitter Amount).
  - `Hàm` **main()**: 

#### 📄 `projects/airdrop_guerrilla/src/modes/semi_auto_ui.py` - Không có mô tả.
  - `Hàm` **alert_user_for_manual_action()**: Kích hoạt chuông báo (Beep) và dừng chương trình chờ người dùng can thiệp.
  - `Hàm` **run_semi_auto_quests()**: 

#### 📄 `projects/airdrop_guerrilla/src/networks/evm_base.py` - Không có mô tả.
  - `Lớp` **EVMBase**: Lớp nền móng xử lý các tác vụ On-chain cho các mạng Layer 1/Layer 2 EVM.
    - `Method` __init__(): 
    - `Method` init_fallback_connection(): Duyệt danh sách RPC, tự động chuyển mạch nếu có node sập.
    - `Method` get_balance(): Lấy số dư Native Token của ví.
    - `Method` get_gas_price(): Lấy giá Gas hiện tại. Hỗ trợ Gas-Optimization: Chờ đợi gas thấp.
    - `Method` check_balance_and_survival(): Kiểm tra số dư tối thiểu, bắn Telegram báo động nếu cạn tiền.
    - `Method` send_native_token(): Gửi Native Token (Ví dụ: ETH -> Soneium, MON -> Monad)
    - `Method` deploy_dummy_contract(): Triển khai một Smart Contract rỗng (Dummy Contract).
    - `Method` random_delay(): [UPGRADE] Gaussian Random Delay de lach bo loc Sybil.
    - `Method` fragment_amount(): Chia nho so luong token thanh cac phan ngau nhien de lam nhiễu analysis.

#### 📄 `projects/airdrop_guerrilla/src/networks/inco.py` - Không có mô tả.
  - `Lớp` **IncoNetwork**: Tích hợp Inco Network Testnet (Modular Confidential L1)
    - `Method` __init__(): 

#### 📄 `projects/airdrop_guerrilla/src/networks/monad.py` - Không có mô tả.
  - `Lớp` **MonadNetwork**: Tích hợp Monad Testnet (Layer 1 EVM Parallel)
    - `Method` __init__(): 

#### 📄 `projects/airdrop_guerrilla/src/networks/soneium.py` - Không có mô tả.
  - `Lớp` **SoneiumNetwork**: Tích hợp Soneium Minato Testnet (Layer 2 Sony)
    - `Method` __init__(): 

#### 📄 `projects/airdrop_guerrilla/src/scrapers/defillama_funding_parser.py` - Không có mô tả.
  - `Lớp` **DefiLlamaParser**: Trình cào dữ liệu Live từ API của DefiLlama (raises endpoint).
    - `Method` __init__(): 
    - `Method` fetch_live_raises(): Gọi API thực tế từ DefiLlama và xử lý dữ liệu trả về.
    - `Method` run_live_pipeline(): Khởi chạy chu trình Cào -> Phân tích -> Lưu trữ cho Phase 2.

#### 📄 `projects/airdrop_guerrilla/src/utils/base_scraper.py` - Không có mô tả.
  - `Lớp` **BaseScraper**: BaseScraper: Lớp cơ sở (Base Class) chuyên dụng cho việc cào dữ liệu (Web Scraping).
    - `Method` __init__(): Khởi tạo BaseScraper.
    - `Method` get_scraped_items(): Đọc danh sách các items (trang/URL/ID) đã cào thành công từ log file.
    - `Method` add_scraped_item(): Ghi nhận một item (trang/URL/ID) đã cào thành công vào file log.
    - `Method` build_headers(): Tạo HTTP Headers ngẫu nhiên với IP spoofing và User-Agent mới để vượt qua WAF (Web Application Firewall).
    - `Method` sleep_random(): Tạm dừng thực thi một khoảng thời gian ngẫu nhiên để giả lập thao tác của con người.
    - `Method` fetch_url(): Thực hiện HTTP GET Request một cách an toàn (State-less) với Exponential Backoff.

#### 📄 `projects/airdrop_guerrilla/src/utils/migrate_to_sqlite.py` - Không có mô tả.
  - `Hàm` **init_db()**: 
  - `Hàm` **migrate_data()**: 

#### 📄 `projects/airdrop_guerrilla/src/utils/notifier.py` - Không có mô tả.
  - `Lớp` **TelegramNotifier**: Module gửi thông báo (Alerting) qua Telegram Bot.
    - `Method` __init__(): 
    - `Method` is_configured(): Kiểm tra xem đã cấu hình đủ Token và Chat ID chưa.
    - `Method` send_message(): Gửi tin nhắn thô qua Telegram.
    - `Method` send_alpha_alert(): Format dữ liệu dự án thành một tin nhắn đẹp mắt và gửi đi.

#### 📄 `projects/airdrop_guerrilla/src/utils/proxy_manager.py` - Không có mô tả.
  - `Lớp` **ProxyManager**: Quan ly danh sach Proxy cho quan doan Clone.
    - `Method` __init__(): 
    - `Method` _load_proxies(): Nap danh sach proxy tu file.
    - `Method` get_proxy_for_account(): Lay proxy gan cho account. 
    - `Method` add_proxy(): Them proxy moi vao danh sach (Format: http://user:pass@host:port).

#### 📄 `projects/airdrop_guerrilla/src/utils/stealth_vault.py` - Không có mô tả.
  - `Lớp` **StealthVault**: He thong luu tru bao mat cach ly (Stealth Vault).
    - `Method` __init__(): 
    - `Method` _load_or_create_key(): Khoi tao hoac nạp key ma hoa tu Master Key he thong.
    - `Method` encrypt_and_store(): Ma hoa va luu tru du lieu.
    - `Method` decrypt_and_retrieve(): Giai ma va lay du lieu.

#### 📄 `projects/ai_trading_agent/dashboard.py` - Không có mô tả.
  - `Hàm` **get_paper_trade_data()**: 
  - `Hàm` **get_decisions()**: 

#### 📄 `projects/ai_trading_agent/live_advisor.py` - Không có mô tả.
  - `Hàm` **get_latest_market_data()**: Lấy dữ liệu đa tài sản từ SQLite. Kèm theo dữ liệu thô cho ML Prediction.
  - `Hàm` **get_latest_news()**: Lấy tin tức mới nhất từ CoinTelegraph.
  - `Hàm` **get_trading_lore()**: Đọc Ký ức giao dịch dài hạn để làm RAG Context
  - `Hàm` **run_live_advisor()**: 

#### 📄 `projects/ai_trading_agent/__init__.py` - Không có mô tả.

#### 📄 `projects/ai_trading_agent/backtest/backtester.py` - Không có mô tả.
  - `Hàm` **run_multi_asset_backtest()**: Backtest chiến lược Multi-Agent (Portfolio Allocation) so với Benchmark (HODL BTC).

#### 📄 `projects/ai_trading_agent/backtest/offline_backtest.py` - Offline Backtest Mode
  - `Lớp` **OfflineBacktester**: Offline backtest engine for AI Trading strategies
    - `Method` __init__(): Initialize backtester
    - `Method` connect(): Connect to database
    - `Method` close(): Close database connection
    - `Method` __enter__(): 
    - `Method` __exit__(): 
    - `Method` get_historical_data(): Get historical OHLCV data with indicators
    - `Method` generate_signals(): Generate trading signals based on indicators
    - `Method` backtest(): Run backtest simulation
    - `Method` compare_strategies(): Compare multiple strategies
    - `Method` print_results(): Print backtest results in a formatted way
  - `Hàm` **main()**: Run offline backtest demo

#### 📄 `projects/ai_trading_agent/backtest/__init__.py` - Backtest scripts

#### 📄 `projects/ai_trading_agent/src/analysis_to_social.py` - Không có mô tả.
  - `Lớp` **MarketAnalysisReport**: 
  - `Lớp` **AnalysisAgent**: Agent chuyen chuyen hoa cac tin hieu ky thuat thanh bai phan tich chuyen sau.
    - `Method` __init__(): 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 

#### 📄 `projects/ai_trading_agent/src/analytics.py` - Không có mô tả.
  - `Lớp` **Analytics**: [ROLE: SRE / QA Tester]
    - `Method` __init__(): 
    - `Method` _ai_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` _logic_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` _ensure_log_file(): 
    - `Method` log_execution_time(): Ghi nhận thời gian thực thi của một task.
    - `Method` log_api_cost(): Ghi nhận chi phí sử dụng API (LLM, Data).
    - `Method` log_trade_performance(): Ghi nhận kết quả giao dịch.
    - `Method` get_summary(): Tính toán tổng hợp hiệu suất.

#### 📄 `projects/ai_trading_agent/src/behavioral_warden.py` - Không có mô tả.

#### 📄 `projects/ai_trading_agent/src/binance_executor.py` - Không có mô tả.
  - `Lớp` **BinanceExecutor**: [ROLE: SRE / QA Tester]
    - `Method` __init__(): 
    - `Method` _ai_handler(): Bắt buộc triển khai từ BaseAgent - Không dùng trực tiếp LLM tại đây.
    - `Method` _logic_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` get_current_portfolio(): Lấy số dư hiện tại trên sàn.
    - `Method` _get_latest_atr(): Lấy giá trị ATR_14 mới nhất từ database.
    - `Method` _calculate_smart_position_sizing(): Tính toán Position Sizing thông minh.
    - `Method` execute_allocation(): Thực thi rebalance danh mục.

#### 📄 `projects/ai_trading_agent/src/config.py` - Không có mô tả.
  - `Lớp` **Config**: Quản lý cấu hình tập trung cho AI Trading Agent.
    - `Method` validate(): Kiểm tra các biến môi trường quan trọng.

#### 📄 `projects/ai_trading_agent/src/data_fetcher.py` - Không có mô tả.
  - `Hàm` **get_trade_tickers()**: Lấy danh sách các cặp giao dịch từ cấu hình.
  - `Hàm` **fetch_fear_and_greed()**: Lấy chỉ số Fear & Greed Index từ API của Alternative.me.
  - `Hàm` **fetch_crypto_data()**: Kéo dữ liệu OHLCV lịch sử từ Yahoo Finance và lưu vào SQLite.

#### 📄 `projects/ai_trading_agent/src/fundamental_fetcher.py` - Không có mô tả.
  - `Lớp` **FundamentalAnalyzer**: [ROLE: Senior Backend Developer]
    - `Method` __init__(): 
    - `Method` _ai_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` _logic_handler(): Bắt buộc triển khai từ BaseAgent.
    - `Method` get_fundamental_data(): Lấy các chỉ số tài chính cơ bản của một tài sản.
    - `Method` generate_fundamental_report(): Tạo báo cáo Phân tích Cơ bản dạng chuỗi để nạp cho AI LangGraph.

#### 📄 `projects/ai_trading_agent/src/funding_rate.py` - Funding Rate Tracker
  - `Lớp` **FundingRateMonitor**: Monitor funding rates from major exchanges using Coinglass API
    - `Method` __init__(): Initialize Funding Rate Monitor
    - `Method` get_funding_rates(): Get current funding rates for a specific symbol
    - `Method` get_avg_funding_rate(): Calculate average funding rate across exchanges
    - `Method` get_funding_rate_summary(): Get formatted summary of funding rates for AI Agent
    - `Method` get_funding_rate_history(): Get historical funding rates
  - `Hàm` **main()**: Test Funding Rate Monitor

#### 📄 `projects/ai_trading_agent/src/github_fetcher.py` - Không có mô tả.
  - `Hàm` **fetch_github_trending_crypto()**: Lấy danh sách các repository liên quan đến crypto/blockchain 

#### 📄 `projects/ai_trading_agent/src/langgraph_agent.py` - Không có mô tả.
  - `Lớp` **TradingState**: 
  - `Lớp` **GenericAgent**: 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Lớp` **MultiAgentTradingSystem**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): Implement abstract method from BaseAgent
    - `Method` _logic_handler(): Implement abstract method from BaseAgent
    - `Method` _init_node(): Node khởi tạo để kích hoạt luồng Fan-out
    - `Method` _technical_node(): 
    - `Method` _sentiment_node(): 
    - `Method` _fundamental_node(): 
    - `Method` _risk_manager_node(): 
    - `Method` _build_graph(): 
    - `Method` analyze_and_trade(): 

#### 📄 `projects/ai_trading_agent/src/live_advisor.py` - Không có mô tả.
  - `Hàm` **get_latest_market_data()**: Lấy dữ liệu đa tài sản từ SQLite.
  - `Hàm` **get_latest_news()**: Lấy tin tức mới nhất từ CoinTelegraph để phân tích Sentiment.
  - `Hàm` **run_live_advisor()**: Hàm thực thi chính của Live Advisor.

#### 📄 `projects/ai_trading_agent/src/mini_backtest.py` - Không có mô tả.
  - `Hàm` **get_cached_prices()**: 
  - `Hàm` **run_mini_backtest()**: Chạy mini-backtest trên dữ liệu `days` ngày qua với tỷ trọng `allocation_dict`.

#### 📄 `projects/ai_trading_agent/src/ml_prediction.py` - Không có mô tả.
  - `Lớp` **LeftBrainPredictor**: 
    - `Method` __init__(): 
    - `Method` predict(): 

#### 📄 `projects/ai_trading_agent/src/news_scraper.py` - Không có mô tả.
  - `Hàm` **fetch_cointelegraph_news()**: Cào tin tức mới nhất từ RSS Feed của CoinTelegraph.

#### 📄 `projects/ai_trading_agent/src/portfolio_optimizer.py` - Không có mô tả.
  - `Hàm` **get_historical_prices()**: Lấy dữ liệu giá đóng cửa lịch sử từ DB.
  - `Hàm` **calculate_portfolio_performance()**: Tính toán lợi nhuận và rủi ro của danh mục.
  - `Hàm` **negative_sharpe_ratio()**: Hàm mục tiêu để minimize (tìm Sharpe cao nhất).
  - `Hàm` **calculate_risk_parity_weights()**: Tính toán tỷ trọng theo phương pháp Risk Parity (Cân bằng rủi ro).
  - `Hàm` **optimize_portfolio()**: Thực hiện tối ưu hóa danh mục. Hỗ trợ MPT (Sharpe) và Risk Parity.

#### 📄 `projects/ai_trading_agent/src/profit_harvester.py` - Không có mô tả.
  - `Lớp` **ProfitHarvester**: He thong thu hoach loi nhuan tu dong (Profit Harvest).
    - `Method` __init__(): 
    - `Method` update_position(): Cap nhat trang thai vi the va kiem tra diem chot loi.
    - `Method` open_position(): 

#### 📄 `projects/ai_trading_agent/src/self_reflection.py` - Không có mô tả.
  - `Lớp` **ReflectionAgent**: 

#### 📄 `projects/ai_trading_agent/src/social_scraper.py` - Không có mô tả.
  - `Hàm` **fetch_reddit_crypto_sentiment()**: Cào các hot posts từ r/CryptoCurrency để phân tích Social Sentiment.

#### 📄 `projects/ai_trading_agent/src/technical_engine.py` - Không có mô tả.
  - `Lớp` **TechnicalEngine**: ⚡ SOVEREIGN HIGH-PERFORMANCE ENGINE ⚡
    - `Method` __init__(): 
    - `Method` analyze_trend(): Phân tích theo chuẩn Minervini Stage 2 (Uptrend mạnh).

#### 📄 `projects/ai_trading_agent/src/telegram_intelligence.py` - Không có mô tả.
  - `Lớp` **TelegramSentiment**: 
  - `Lớp` **TelegramIntelligenceAgent**: Agent chuyen phan tich tam ly thi truong tu cac tin nhan Telegram.
    - `Method` __init__(): 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
  - `Hàm` **main()**: 

#### 📄 `projects/ai_trading_agent/src/validation_gate.py` - Không có mô tả.
  - `Lớp` **ValidationGate**: 🛡️ SOVEREIGN VALIDATION GATE (Tier 1 Protection)
    - `Method` __init__(): 
    - `Method` check_data_integrity(): [VULN-003] Kiểm tra tính toàn vẹn của dữ liệu (Sanity Check).
    - `Method` validate_proposal(): Kiểm tra đề xuất lệnh dựa trên dữ liệu 7 ngày và Slippage Guard.

#### 📄 `projects/ai_trading_agent/src/whale_alert.py` - Whale Alert API Integration
  - `Lớp` **WhaleAlertMonitor**: Monitor large crypto transactions using Whale Alert API
    - `Method` __init__(): Initialize Whale Alert Monitor
    - `Method` get_transactions(): Get recent large transactions
    - `Method` get_exchange_inflow_outflow(): Calculate net flow to/from exchanges
    - `Method` get_whale_alert_summary(): Get formatted summary of whale activity for AI Agent
  - `Hàm` **main()**: Test Whale Alert Monitor

#### 📄 `projects/ai_trading_agent/src/whale_tracker.py` - Không có mô tả.
  - `Lớp` **WhaleTrackerAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` scrape_whale_data(): 
    - `Method` execute(): 

#### 📄 `projects/ai_trading_agent/src/__init__.py` - Source code cho AI Trading Agent

#### 📄 `projects/ai_trading_agent/tools/check_pnl.py` - Kiểm tra dữ liệu PnL trong database

#### 📄 `projects/ai_trading_agent/tools/generate_performance_report.py` - Không có mô tả.
  - `Hàm` **generate_markdown_report()**: Tạo báo cáo hiệu suất từ dữ liệu Paper Trade trong Database.

#### 📄 `projects/ai_trading_agent/tools/reset_pnl.py` - Xóa dữ liệu cũ trong Paper_Trade_Portfolio để reset PnL

#### 📄 `projects/ai_trading_agent/tools/verify_db.py` - Không có mô tả.

#### 📄 `projects/ai_trading_agent/tools/__init__.py` - Utility tools

#### 📄 `projects/asset_audit_taskforce/src/app.py` - Không có mô tả.

#### 📄 `projects/asset_audit_taskforce/src/arb_session.py` - Không có mô tả.
  - `Lớp` **ArchitectureReconstructionBoard**: Ban Dự án Tái thiết Kiến trúc (ARB):
    - `Method` __init__(): 
    - `Method` run_full_session(): 

#### 📄 `projects/asset_audit_taskforce/src/auditor.py` - [LỖI AST: expected an indented block after 'if' statement on line 12 (auditor.py, line 13)]

#### 📄 `projects/asset_audit_taskforce/src/detective.py` - [LỖI AST: expected an indented block after 'if' statement on line 13 (detective.py, line 14)]

#### 📄 `projects/asset_audit_taskforce/src/judge_executor.py` - Không có mô tả.
  - `Lớp` **DiskCleaner**: 
    - `Method` __init__(): 
    - `Method` _format_size(): Định dạng byte sang MB/GB cho dễ nhìn
    - `Method` _get_dir_size(): Lấy kích thước một thư mục
    - `Method` clean_temp_folders(): Xóa các thư mục Temp của Windows
    - `Method` clean_dev_caches(): Gọi CLI để dọn cache của pip, uv, npm
    - `Method` clean_docker(): Xóa Docker images/containers dangling
    - `Method` run(): 

#### 📄 `projects/asset_audit_taskforce/src/scouter.py` - [LỖI AST: expected an indented block after 'if' statement on line 13 (scouter.py, line 14)]

#### 📄 `projects/auto_affiliate_video/app.py` - Không có mô tả.

#### 📄 `projects/auto_affiliate_video/main.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `projects/auto_affiliate_video/src/affiliate_manager.py` - Không có mô tả.
  - `Lớp` **AffiliateManager**: Module quản lý việc lấy link Affiliate từ mạng AccessTrade.
    - `Method` __init__(): 
    - `Method` generate_affiliate_link(): Tạo link rút gọn Affiliate thông qua API của AccessTrade.

#### 📄 `projects/auto_affiliate_video/src/auto_uploader.py` - Không có mô tả.
  - `Lớp` **AutoUploader**: Module tự động upload video lên mạng xã hội (TikTok/Shorts) sử dụng tiktok-uploader.
    - `Method` __init__(): 
    - `Method` upload_to_tiktok(): 

#### 📄 `projects/auto_affiliate_video/src/main.py` - Không có mô tả.
  - `Hàm` **main()**: Hàm main điều phối quá trình tự động tạo video Affiliate.

#### 📄 `projects/auto_affiliate_video/src/pexel_client.py` - Không có mô tả.
  - `Lớp` **PexelClient**: A client for interacting with the Pexels API to find and download videos.
    - `Method` find_and_download_video(): Searches for a video on Pexels and downloads the most relevant one.
    - `Method` _get_best_quality_link(): Selects the best quality video link that is under a certain size if needed.

#### 📄 `projects/auto_affiliate_video/src/scheduler.py` - Không có mô tả.
  - `Hàm` **job()**: 

#### 📄 `projects/auto_affiliate_video/src/script_generator.py` - Không có mô tả.
  - `Lớp` **ScriptGenerator**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` generate_short_video_script(): Dùng OpenAI/Gemini để viết kịch bản video ngắn (dưới 60s) cho TikTok/Shorts.

#### 📄 `projects/auto_affiliate_video/src/test_upload.py` - Không có mô tả.

#### 📄 `projects/auto_affiliate_video/src/tiktok_api_uploader.py` - Không có mô tả.
  - `Lớp` **TikTokApiUploader**: Tích hợp TikTok Content Posting API chính thức thay cho Playwright.
    - `Method` __init__(): 
    - `Method` upload_to_tiktok(): 

#### 📄 `projects/auto_affiliate_video/src/tts_engine.py` - Không có mô tả.
  - `Lớp` **TTSEngine**: Dong co chuyen doi van ban thanh giong noi (TTS) da ngon ngu cao cap.
    - `Method` __init__(): 
    - `Method` generate_audio(): Sinh ra file mp3 tu van ban bang Edge-TTS.
    - `Method` _apply_audio_effects(): Ap dung cac hieu ung am thanh chuyen nghiep.

#### 📄 `projects/auto_affiliate_video/src/vector_memory.py` - Không có mô tả.
  - `Lớp` **VectorMemory**: Quản lý Long-term Memory bằng Vector RAG để tránh tràn Context Window.
    - `Method` __init__(): 
    - `Method` embed_and_store(): Tạo embedding và lưu nội dung vào Vector DB.
    - `Method` query_similar_context(): Truy xuất N nội dung tương tự nhất dựa trên câu truy vấn.
    - `Method` ingest_chronicles(): Đọc và băm nhỏ file JARVIS_CHRONICLES.md để nạp vào trí nhớ.

#### 📄 `projects/auto_affiliate_video/src/video_editor.py` - Không có mô tả.
  - `Lớp` **VideoEditor**: 
    - `Method` __init__(): 
    - `Method` create_short_video(): Ghép Audio AI vào Video Background.

#### 📄 `projects/auto_affiliate_video/src/video_telemetry.py` - Không có mô tả.
  - `Lớp` **VideoTelemetry**: 
    - `Method` __init__(): 
    - `Method` start_run(): 
    - `Method` log_event(): 
    - `Method` _save_to_disk(): 
  - `Hàm` **measure_latency()**: Decorator to automatically measure the latency of a function and log it.

#### 📄 `projects/auto_x_bot/app.py` - Không có mô tả.

#### 📄 `projects/auto_x_bot/main.py` - Không có mô tả.
  - `Hàm` **log_to_db()**: Lưu lịch sử đăng Tweet vào database.
  - `Hàm` **main()**: 

#### 📄 `projects/auto_x_bot/src/browser_bot.py` - Không có mô tả.
  - `Lớp` **XBrowserBot**: Agent tuong tac X (Twitter) qua trinh duyet de lach luat cam API.
    - `Method` __init__(): 
    - `Method` post_tweet_browser(): Dang tweet bang cach dieu khien trinh duyet.
    - `Method` interact_with_trends(): Tuong tac voi cac xu huong de tang uy tin account.

#### 📄 `projects/auto_x_bot/src/content_generator.py` - Không có mô tả.
  - `Lớp` **ContentGenerator**: 
    - `Method` __init__(): 
    - `Method` generate_crypto_tweet(): Dựa vào danh sách tin tức, suy nghĩ ra 1 dòng Tweet duy nhất cực kỳ viral,

#### 📄 `projects/auto_x_bot/src/social_coordinator.py` - Không có mô tả.
  - `Hàm` **social_mining_cycle()**: 

#### 📄 `projects/auto_x_bot/src/x_api_client.py` - [LỖI AST: expected an indented block after 'if' statement on line 9 (x_api_client.py, line 10)]

#### 📄 `projects/auto_x_bot/src/__init__.py` - Không có mô tả.

#### 📄 `projects/ceo_agent/admin_simulator.py` - Không có mô tả.
  - `Lớp` **AdminSimulator**: Sinh ra các tình huống quản trị hệ thống (System Crisis) để CEO Agent giải quyết.
    - `Method` __init__(): 
    - `Method` get_next_crisis(): Sinh ra một cuộc khủng hoảng ngẫu nhiên.
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` evaluate_decision(): Đánh giá quyết định của CEO.

#### 📄 `projects/ceo_agent/autonomous_ceo.py` - Không có mô tả.
  - `Hàm` **list_projects()**: Liệt kê tất cả các project con hiện có.
  - `Hàm` **read_document()**: Đọc nội dung một file tài liệu hoặc code (truyền đường dẫn tương đối từ root).
  - `Lớp` **CEOState**: 
  - `Lớp` **AutonomousCEO**: 
    - `Method` __init__(): 
    - `Method` think_node(): 
    - `Method` act_node(): 
    - `Method` finish_node(): 
    - `Method` should_continue(): 
    - `Method` _build_graph(): 
    - `Method` run_vi_hanh(): 

#### 📄 `projects/ceo_agent/ceo_mind.py` - Không có mô tả.
  - `Lớp` **CEOAgent**: Trí tuệ của CEO. Nhận báo cáo khủng hoảng từ AdminSimulator,
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` handle_crisis(): Đưa ra quyết định dựa trên báo động hệ thống.
    - `Method` reflect_and_learn(): Đúc kết bài học từ thành công hoặc thất bại.

#### 📄 `projects/ceo_agent/ceo_morning_routine.py` - Không có mô tả.
  - `Lớp` **CEODecision**: 
  - `Lớp` **CEOUpgradePlan**: 
  - `Lớp` **AdminFeedback**: 
  - `Lớp` **AdminCriticAgent**: 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
  - `Lớp` **CEOAgent**: 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
  - `Lớp` **CEOUpgradeAgent**: 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
  - `Hàm` **wake_up_ceo()**: 

#### 📄 `projects/ceo_agent/ceo_training_matrix.py` - Không có mô tả.
  - `Hàm` **list_files_in_directory()**: Liệt kê các file trong một thư mục cụ thể để CEO có thể khám phá dự án.
  - `Hàm` **read_ceo_lore()**: Đọc file bộ nhớ dài hạn (Long-term Memory) của CEO để nhớ lại các bài học cũ.
  - `Hàm` **summon_agent()**: Triệu hồi (Summon) một Agent khác (ví dụ QA_Auditor, Code_Reviewer, Trader) để nhờ phân tích/làm giúp một task. Trả về kết quả của Agent đó.
  - `Lớp` **CEOTrainingState**: 
  - `Hàm` **ceo_node()**: 
  - `Hàm` **ceo_router()**: 
  - `Hàm` **reflect_node()**: 
  - `Hàm` **run_nightly_training()**: 

#### 📄 `projects/ceo_agent/marketing_intel.py` - Không có mô tả.
  - `Lớp` **MarketingInsight**: 
  - `Lớp` **MarketingAgent**: Agent chuyen phan tich thi truong va sinh noi dung Marketing.
    - `Method` __init__(): 
    - `Method` _logic_handler(): 
    - `Method` _ai_handler(): 
  - `Hàm` **main()**: 

#### 📄 `projects/FlowNSFW-main/scripts/demo.py` - FlowNSFW Demo - Interactive video NSFW detection demonstration.
  - `Hàm` **extract_frames_from_video()**: Extract frames from video file.
  - `Hàm` **load_frame_sequence()**: Load frames from directory.
  - `Hàm` **preprocess_frames()**: Convert frames to model input tensor.
  - `Hàm` **sliding_window_inference()**: Run sliding window inference.
  - `Hàm` **print_result()**: Pretty print inference result.
  - `Hàm` **main()**: 

#### 📄 `projects/FlowNSFW-main/scripts/eval_multi_res.py` - Evaluate FlowNSFW at multiple resolutions.
  - `Hàm` **eval_at_resolution()**: Evaluate at a single resolution.
  - `Hàm` **main()**: 

#### 📄 `projects/FlowNSFW-main/scripts/generate_figures.py` - Generate performance comparison figure for FlowNSFW.

#### 📄 `projects/FlowNSFW-main/scripts/infer.py` - FlowNSFW inference — sliding-window, boxes like YOLO, per-frame labels.
  - `Hàm` **find_videos()**: 
  - `Hàm` **draw_box()**: Draw YOLO-style bounding box on image.
  - `Hàm` **infer_video()**: Full sliding-window video classification + detection boxes.
  - `Hàm` **main()**: 

#### 📄 `projects/FlowNSFW-main/scripts/test_smoke.py` - Không có mô tả.

#### 📄 `projects/FlowNSFW-main/scripts/train.py` - Train FlowNSFW — optical-flow NSFW detection.
  - `Hàm` **collate_simple()**: Collate for balanced batch — all same resolution, handle boxes as list.
  - `Hàm` **_cosine_lr()**: 
  - `Hàm` **_set_lr()**: 
  - `Hàm` **main()**: 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/balanced_sampler.py` - Balanced batch sampler — ensures each batch has NSFW + SFW pairs.
  - `Lớp` **BalancedBatchSampler**: Each batch contains exactly one NSFW and one SFW sample.
    - `Method` __init__(): 
    - `Method` __iter__(): 
    - `Method` __len__(): 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/data.py` - Video clip dataset for FlowNSFW.
  - `Hàm` **_read_img()**: Read image as RGB uint8, handling AVIF via ffmpeg fallback.
  - `Lớp` **VideoClipDataset**: Yields temporal clips from video frame directories.
    - `Method` __init__(): 
    - `Method` __len__(): 
    - `Method` __getitem__(): 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/detection_head.py` - NSFW Detection Head — multi-scale, flow-gated, with sparse processing.
  - `Hàm` **_compute_foreground_mask()**: Simple foreground activation mask from feature energy.
  - `Hàm` **_window_mask_regions()**: Identify windows that intersect with the foreground mask.
  - `Lớp` **_DetectScale**: Single-scale detection block: conv refine → box + cls heads.
    - `Method` __init__(): 
    - `Method` forward(): Returns (B, 5+nc, H, W) logits.
  - `Lớp` **DetectionHead**: Multi-scale NSFW detection head with optional sparse processing.
    - `Method` __init__(): 
    - `Method` _apply_sparse(): Apply detection only on foreground windows.
    - `Method` forward(): Returns per-scale raw detection tensors.

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/encoder_unet.py` - 4-stage U-Net encoder — adapted from FlowEraser.
  - `Hàm` **_conv_block()**: 
  - `Lớp` **UNetEncoder**: 4-level conv encoder: stride 1→2→4→8, returns bottleneck + skips.
    - `Method` __init__(): 
    - `Method` forward(): 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/flow_net.py` - Flow estimation backends — with accelerated correlation.
  - `Hàm` **_build_corr()**: Correlation volume via unfold + batched matmul.
  - `Lớp` **_FlowHead**: 
    - `Method` __init__(): 
    - `Method` forward(): 
  - `Lớp` **FlowNet**: Scratch-learned correlation flow estimator (optimized).
    - `Method` __init__(): 
    - `Method` forward(): 
  - `Lớp` **RaftFlowNet**: Frozen RAFT-S optical flow. Runs on HR frames, downsamples to feat stride.
    - `Method` __init__(): 
    - `Method` forward(): 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/losses.py` - FlowNSFW loss functions.
  - `Lớp` **LossWeights**: 
  - `Hàm` **_ciou_loss()**: CIoU box loss for positive samples.
  - `Hàm` **detection_loss()**: Per-scale detection loss.
  - `Hàm` **video_cls_loss()**: Video-level cross-entropy.
  - `Hàm` **temporal_box_loss()**: Penalize abrupt box changes between adjacent frames.
  - `Hàm` **simple_detection_loss()**: Simplified detection loss using GT boxes from YOLO pseudo-labels.
  - `Hàm` **flow_consistency_loss()**: Forward-backward flow consistency loss.
  - `Hàm` **flow_smoothness_loss()**: Spatial smoothness of optical flow.

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/model.py` - FlowNSFW — Optical-flow-guided video NSFW detection with Mamba SSM support.
  - `Lớp` **FlowNSFW**: Video NSFW detection with optical flow and temporal modeling.
    - `Method` __init__(): 
    - `Method` count_parameters(): 
    - `Method` _decode_predictions(): Decode raw detection heads into boxes per scale.
    - `Method` forward(): Args:

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/pseudo_labeler.py` - YOLO pseudo-labeler — convert video frames to FlowNSFW training manifest.
  - `Hàm` **_decode_avif_to_numpy()**: Convert AVIF to RGB numpy array via ffmpeg pipe.
  - `Hàm` **_decode_image()**: Read any image as RGB numpy array.
  - `Hàm` **find_frame_dirs()**: Find leaf directories containing image sequences.
  - `Hàm` **label_video_frames()**: Run YOLO on frames, decode AVIF→numpy as needed.
  - `Hàm` **build_manifest()**: Build full manifest from video directories.
  - `Hàm` **main()**: 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/ssm_backend.py` - SSM backend — 3-tier fallback chain with CUDA acceleration.
  - `Lớp` **_FallbackSSM**: Minimal SSM using torch.cumsum. Functionally correct, no CUDA kernel.
    - `Method` __init__(): 
    - `Method` forward(): x: (B, L, D)
  - `Hàm` **create_ssm_layer()**: Create the best available SSM layer.

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/temporal_sparse.py` - Sparse global temporal aggregator — with Mamba SSM backend.
  - `Hàm` **_topk_tokens()**: 
  - `Lớp` **_AttnBlock**: 
    - `Method` __init__(): 
    - `Method` forward(): 
  - `Lớp` **_TransformerBlock**: 
    - `Method` __init__(): 
    - `Method` forward(): 
  - `Lớp` **_MambaBlock**: SSM-based temporal block: O(N) complexity for long sequences.
    - `Method` __init__(): 
    - `Method` forward(): x: (B, N, C). _kv_unused kept for API compatibility.
  - `Lớp` **_HybridBlock**: Attention for local (self + warped neighbors), Mamba for global context.
    - `Method` __init__(): 
    - `Method` forward(): 
  - `Lớp` **SparseGlobalTemporal**: Temporal aggregator: window-local + sparse-global across clip frames.
    - `Method` __init__(): 
    - `Method` _tokens(): 
    - `Method` _restore(): 
    - `Method` _build_kv(): Build KV tokens: self + flow-warped neighbors + top-K global.
    - `Method` forward(): 

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/utils.py` - Shared utilities — adapted from FlowEraser.
  - `Hàm` **warp()**: Bilinear grid_sample warp.
  - `Hàm` **resize_flow_sequence()**: Resize pixel-unit flow to target (H, W), rescaling magnitudes.

#### 📄 `projects/FlowNSFW-main/src/flow_nsfw/__init__.py` - FlowNSFW — Optical-flow-guided video NSFW detection.

#### 📄 `projects/gemini_cli/main.py` - Main entry point for Gemini CLI.
  - `Hàm` **stream_response()**: Stream Gemini API response to stdout.
  - `Hàm` **main()**: Main entry point - parses arguments and runs async stream.

#### 📄 `projects/gemini_cli/core/client.py` - Async HTTPX client for Gemini API communication.
  - `Lớp` **GeminiError**: Base exception for Gemini API errors.
  - `Lớp` **QuotaExceededError**: Raised when API quota is exhausted.
  - `Lớp` **NetworkError**: Raised when network issues occur.
  - `Lớp` **InvalidResponseError**: Raised when API returns invalid response.
  - `Lớp` **GeminiClient**: Async HTTPX client for Gemini API with streaming support.
    - `Method` __init__(): Initialize Gemini client.
    - `Method` __aenter__(): Async context manager entry.
    - `Method` __aexit__(): Async context manager exit.
    - `Method` stream_chat(): Send a chat prompt and stream the response.
    - `Method` chat(): Send a chat prompt and return complete response (non-streaming).

#### 📄 `projects/gemini_cli/core/config.py` - API Guard: Secure configuration management for Gemini API.
  - `Lớp` **ConfigError**: Custom exception for configuration errors.
  - `Lớp` **Config**: Secure configuration manager for Gemini API.
    - `Method` __init__(): Initialize configuration by loading environment variables.
    - `Method` _validate(): Validate that all required environment variables are set.
    - `Method` api_key(): Get Gemini API key from environment.
    - `Method` base_url(): Get Gemini API base URL from environment.
    - `Method` model(): Get default model name.
    - `Method` timeout(): Get request timeout in seconds.
    - `Method` get_headers(): Get HTTP headers for API requests.
    - `Method` __repr__(): String representation (safe - hides API key).

#### 📄 `projects/gemini_cli/core/__init__.py` - Core modules for Gemini CLI.

#### 📄 `projects/gemini_cli/tests/__init__.py` - Unit tests for Gemini CLI.

#### 📄 `projects/godot_translator/app.py` - Không có mô tả.
  - `Hàm` **translation_worker()**: Luồng dịch ngầm (Thread) để tránh block UI.

#### 📄 `projects/godot_translator/build_godot_exe.py` - Không có mô tả.

#### 📄 `projects/godot_translator/main.py` - [LỖI AST: expected an indented block after 'if' statement on line 10 (main.py, line 11)]

#### 📄 `projects/godot_translator/main_run.py` - Không có mô tả.
  - `Hàm` **main()**: Entry point chạy ngầm Streamlit. Dùng để thay thế file .bat cho bản Build.

#### 📄 `projects/godot_translator/test_translation.py` - Không có mô tả.
  - `Hàm` **test_single_file_translation()**: 

#### 📄 `projects/godot_translator/core/cyber_security.py` - Không có mô tả.
  - `Lớp` **IntegrityGuard**: Hệ thống kiểm soát tính toàn vẹn (Integrity Guard) dựa trên tri thức từ Practical Reverse Engineering.
    - `Method` __init__(): 
    - `Method` _calculate_hash(): Tính toán mã băm SHA-256 của file.
    - `Method` record_baseline(): Ghi nhận mã băm gốc của các file quan trọng.
    - `Method` verify_integrity(): Kiểm tra xem file có bị thay đổi không.
    - `Method` deploy_logic_mine(): Triển khai 'Mìn logic' - Tự hủy phiên làm việc nếu vi phạm tính toàn vẹn.
  - `Lớp` **InjectionGuard**: Lớp phong thu chong Prompt Injection (Jailbreak) va danh cap thong tin.
    - `Method` __init__(): 
    - `Method` is_safe(): Kiem tra xem input cua nguoi dung co an toan khong.
    - `Method` sanitize_input(): Lam sach input neu can thiet.

#### 📄 `projects/godot_translator/core/decompiler.py` - Không có mô tả.
  - `Lớp` **GodotDecompiler**: Wrapper for external Godot decompile tools (like GDRE Tools CLI).
    - `Method` __init__(): 
    - `Method` decompile_pck(): Decompile a .pck file using GDRE Tools CLI.

#### 📄 `projects/godot_translator/core/extractor.py` - Không có mô tả.
  - `Lớp` **GodotExtractor**: Module to extract Japanese strings from Godot GDScript (.gd) and Scene (.tscn) files.
    - `Method` __init__(): 
    - `Method` scan_files(): Recursively scan for .gd and .tscn files.
    - `Method` extract_from_file(): Extract Japanese strings from a single file based on its type.

#### 📄 `projects/godot_translator/core/gdre_downloader.py` - Không có mô tả.
  - `Hàm` **download_gdre_tools()**: 

#### 📄 `projects/godot_translator/core/injector.py` - Không có mô tả.
  - `Lớp` **GodotInjector**: Module to inject translated strings back into GDScript/TSCN files and maintain directory structure.
    - `Method` __init__(): 
    - `Method` inject(): Replace Japanese strings and save in the mirrored structure, while cleaning .remap/.gdc files.

#### 📄 `projects/godot_translator/core/pack_manager.py` - Không có mô tả.
  - `Lớp` **DRMError**: Exception ném ra khi phát hiện game bị khóa bản quyền.
  - `Lớp` **PackManager**: Quản lý việc Unpack và Repack các file .exe / .pck của Godot.
    - `Method` __init__(): 
    - `Method` detect_godot_version(): Kiểm tra Magic Bytes để nhận diện Godot PCK format.
    - `Method` unpack(): Giải nén file .exe hoặc .pck ra thư mục tạm.
    - `Method` test_run(): Khởi chạy game (Sandbox Playtest) không chặn UI chính.
    - `Method` repack(): Đóng gói lại thư mục đã dịch thành file game mới sử dụng GDRE Tools.
    - `Method` cleanup_temp(): Dọn dẹp rác (Garbage Collection) khi xong hoặc khi lỗi.

#### 📄 `projects/godot_translator/core/translator.py` - Không có mô tả.
  - `Lớp` **TranslationSchema**: 
  - `Lớp` **GodotTranslator**: Agent specialized in translating Japanese game strings to Vietnamese.
    - `Method` __init__(): 
    - `Method` _logic_handler(): Fallback Path: Return original texts (no translation) if AI fails.
    - `Method` _ai_handler(): Optimal Path: Use LLM to translate strings.
    - `Method` translate_batch(): Execute translation with batching.

#### 📄 `projects/godot_translator/utils/ui_helper.py` - Không có mô tả.
  - `Hàm` **ui_error_guard()**: Decorator de bảo vệ UI Streamlit khỏi các lỗi Backend.

#### 📄 `projects/jarvis-rpg-assistant/main.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/ai_agent.py` - Không có mô tả.
  - `Lớp` **AIService**: Core AI Service - Trái tim của Jarvis.
    - `Method` __init__(): 
    - `Method` _get_cached_response(): Kiểm tra xem câu hỏi này đã có trong cache chưa.
    - `Method` _update_cache(): Lưu câu trả lời vào cache.
    - `Method` generate_response(): Hàm chính để tạo phản hồi (Có Cache + Đồng bộ Fallback Chain).
  - `Hàm` **ask_jarvis()**: Hàm giao tiếp cơ bản với Jarvis.
  - `Hàm` **evaluate_evolution()**: Đánh giá nhiệm vụ để tính XP/HP (RPG System).

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/ai_agent_fixed.py` - Không có mô tả.
  - `Lớp` **CircuitState**: Circuit Breaker States.
  - `Lớp` **CircuitBreakerError**: Raised when circuit is OPEN.
  - `Lớp` **CircuitBreaker**: Circuit Breaker Pattern Implementation.
    - `Method` __init__(): 
    - `Method` call(): Execute function with circuit breaker protection.
    - `Method` _should_attempt_reset(): Check if enough time has passed to try HALF_OPEN.
    - `Method` _get_remaining_cooldown(): Get remaining cooldown time in seconds.
    - `Method` _transition_to_half_open(): Transition from OPEN to HALF_OPEN.
    - `Method` _on_success(): Handle successful request.
    - `Method` _on_failure(): Handle failed request.
    - `Method` get_status(): Get current circuit breaker status.
  - `Lớp` **SingleFlightLRUCache**: Thread-safe LRU Cache with Single-Flight Pattern.
    - `Method` __init__(): 
    - `Method` get_or_fetch(): Get from cache OR wait for in-flight request OR fetch new.
    - `Method` _get_from_cache(): Get from cache if exists and not expired.
    - `Method` _fetch_and_cache(): Fetch from API and store in cache.
    - `Method` _remove_entry(): Remove entry and update memory counter.
    - `Method` get_stats(): Get cache statistics.
  - `Lớp` **AIService**: Core AI Service - Production-Ready with 3 Resilience Layers.
    - `Method` __init__(): 
    - `Method` _call_llm_api(): Call Gemini API with retry logic.
    - `Method` generate_response(): Main entry point: Generate AI response with full resilience.
    - `Method` get_system_status(): Get comprehensive system health status.
  - `Hàm` **ask_jarvis()**: Public API: Ask Jarvis a question (Facade Pattern).
  - `Hàm` **evaluate_evolution()**: Evaluate tasks for XP/HP calculation (RPG System).
  - `Hàm` **get_system_health()**: Get system health metrics.

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/check_model.py` - Không có mô tả.

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/config.py` - Không có mô tả.

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/database.py` - Không có mô tả.
  - `Lớp` **DatabaseError**: Base exception for database related errors.
  - `Lớp` **DatabaseManager**: Manages all database operations for the Jarvis application.
    - `Method` __init__(): Initialize the database manager.
    - `Method` _get_default_db_path(): Xác định đường dẫn database một cách thông minh.
    - `Method` _get_connection(): Context manager for database connections with transaction lock.
    - `Method` _execute(): Execute a write operation (INSERT/UPDATE/DELETE).
    - `Method` _fetch_one(): Execute a query and return a single row.
    - `Method` _fetch_all(): Execute a query and return all rows.
    - `Method` _init_db(): Initialize the database schema.
    - `Method` get_user_profile(): 
    - `Method` _create_default_profile(): 
    - `Method` update_user_stats(): 
    - `Method` add_vocab(): 
    - `Method` get_due_vocab(): 
    - `Method` get_review_candidates(): 
    - `Method` update_vocab_mastery(): 
    - `Method` _calculate_next_review_interval(): 
  - `Hàm` **get_database()**: 
  - `Hàm` **init_db()**: 
  - `Hàm` **get_connection()**: 
  - `Hàm` **get_due_vocab()**: 
  - `Hàm` **get_review_candidates()**: 
  - `Hàm` **add_vocab()**: 
  - `Hàm` **update_vocab_mastery()**: 
  - `Hàm` **get_user_profile()**: 
  - `Hàm` **update_user_stats()**: 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/db_sync.py` - Không có mô tả.
  - `Hàm` **sync_database_with_git()**: Sync database với git: pull trước khi commit để tránh conflict
  - `Hàm` **commit_and_push_database()**: Commit và push database changes
  - `Hàm` **safe_database_update()**: Wrapper function để safely update database với git sync

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/error_notifier.py` - Không có mô tả.
  - `Lớp` **ErrorNotifier**: 
    - `Method` __init__(): 
    - `Method` _get_admin_chat_ids(): 
    - `Method` _get_bot(): 
    - `Method` send_error_alert(): 
    - `Method` notify_error_sync(): 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/google_services.py` - Không có mô tả.
  - `Hàm` **get_creds()**: 
  - `Hàm` **add_task()**: 
  - `Hàm` **get_today_events()**: 
  - `Hàm` **get_pending_tasks()**: 
  - `Hàm` **get_completed_tasks_today()**: 
  - `Hàm` **create_calendar_event()**: 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/key_manager.py` - Không có mô tả.
  - `Lớp` **KeyExhaustedError**: Exception raised when all API keys are exhausted or rate-limited.
  - `Lớp` **KeyManager**: 
    - `Method` __init__(): 
    - `Method` get_next_key(): Trả về key tiếp theo theo cơ chế Round-Robin, bỏ qua các key đang trong Cooldown.
    - `Method` mark_key_exhausted(): Đánh dấu key này đã hết hạn mức (Quota Exceeded) hoặc gặp lỗi Rate Limit.
    - `Method` reset_exhausted_keys(): Xóa toàn bộ trạng thái Cooldown. Dùng khi cần reset thủ công.
  - `Hàm` **get_global_key_manager()**: Đọc keys từ biến môi trường và trả về KeyManager.

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/migrate_data.py` - Không có mô tả.
  - `Hàm` **manual_restore()**: 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/notes.py` - Không có mô tả.
  - `Hàm` **add_note()**: Ghi một ghi chú mới cùng với timestamp vào file journal.

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/setup_calendar.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/telegram_bot.py` - Không có mô tả.
  - `Hàm` **send_message()**: 

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/telegram_webhook.py` - Không có mô tả.
  - `Lớp` **TelegramWebhookBot**: Telegram bot với hỗ trợ webhook cho deployment trên Render/Heroku
    - `Method` __init__(): 
    - `Method` _setup_handlers(): Setup command and message handlers
    - `Method` handle_photo(): Handle photo messages for calendar parsing
    - `Method` start_command(): Handle /start command
    - `Method` help_command(): Handle /help command
    - `Method` handle_message(): Handle regular text messages
    - `Method` run_polling(): Run bot with polling (for local development)
    - `Method` setup_webhook(): Setup webhook for production deployment
    - `Method` run_webhook(): Run bot with webhook (for production)
    - `Method` run(): Run bot with appropriate mode based on configuration
  - `Hàm` **main()**: Main entry point

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/vision_parser.py` - Không có mô tả.
  - `Hàm` **encode_image()**: Mã hóa ảnh sang base64.
  - `Lớp` **VisionParserAgent**: [ROLE: AI Prompt Engineer / QA Tester]
    - `Method` __init__(): 
    - `Method` _ai_handler(): Bắt buộc triển khai từ BaseAgent - Không dùng trong luồng này.
    - `Method` _logic_handler(): Bắt buộc triển khai từ BaseAgent - Không dùng trong luồng này.
    - `Method` parse_schedule_image(): Sử dụng BaseAgent để gọi LLM Vision (qua Local Proxy) xử lý ảnh lịch.
  - `Hàm` **parse_schedule_image()**: Wrapper function để không làm vỡ các module đang import hàm này.

#### 📄 `projects/jarvis-rpg-assistant/jarvis_core/weather_service.py` - Không có mô tả.
  - `Hàm` **get_weather_report()**: Lấy thông tin thời tiết hiện tại tại Đồng Nai.

#### 📄 `projects/jarvis-rpg-assistant/src/admin_panel.py` - Không có mô tả.
  - `Lớp` **JarvisAdminApp**: 
    - `Method` __init__(): 
    - `Method` setup_profile_tab(): 
    - `Method` load_profile(): 
    - `Method` save_profile(): 
    - `Method` setup_vocab_tab(): 
    - `Method` load_vocab_list(): 
    - `Method` filter_vocab(): 
    - `Method` on_select_vocab(): 
    - `Method` clear_form(): 
    - `Method` add_vocab(): 
    - `Method` update_vocab(): 
    - `Method` delete_vocab(): 

#### 📄 `projects/jarvis-rpg-assistant/src/auto_learn.py` - Không có mô tả.
  - `Hàm` **auto_hunt_vocab()**: 

#### 📄 `projects/jarvis-rpg-assistant/src/bot_daily.py` - Không có mô tả.
  - `Hàm` **get_vietnamese_weekday()**: 
  - `Hàm` **main()**: 

#### 📄 `projects/jarvis-rpg-assistant/src/bot_evolve.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `projects/jarvis-rpg-assistant/src/bot_teacher.py` - Không có mô tả.
  - `Hàm` **main()**: Main teaching function.

#### 📄 `projects/jarvis-rpg-assistant/src/fix_db.py` - Không có mô tả.
  - `Hàm` **fix_system()**: 

#### 📄 `projects/jarvis-rpg-assistant/src/jarvis_launcher.py` - Không có mô tả.
  - `Lớp` **JarvisLauncher**: 
    - `Method` __init__(): 
    - `Method` setup_ui(): Thiết lập giao diện tích hợp với main.py.
    - `Method` log(): Ghi thông tin vào cửa sổ Log.
    - `Method` launch_main_cmd(): Chạy main.py thông qua subprocess với tham số.
    - `Method` run_process(): Thực thi tiến trình và bắt log realtime.

#### 📄 `projects/jarvis-rpg-assistant/src/note.py` - Không có mô tả.
  - `Hàm` **main()**: Điểm vào CLI để ghi chú nhanh.

#### 📄 `projects/jarvis-rpg-assistant/src/note_search.py` - Không có mô tả.
  - `Hàm` **read_journal()**: Đọc toàn bộ nội dung file ghi chú.
  - `Hàm` **search_in_notes()**: Gửi nội dung ghi chú + câu hỏi cho AI xử lý.
  - `Hàm` **main()**: 

#### 📄 `projects/jarvis-rpg-assistant/src/test_vision_calendar.py` - Không có mô tả.
  - `Hàm` **get_next_weekday()**: Hàm tính toán ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất.
  - `Hàm` **test_pipeline()**: 

#### 📄 `projects/jarvis-rpg-assistant/tests/conftest.py` - Không có mô tả.
  - `Hàm` **pytest_configure()**: 

#### 📄 `projects/jarvis-rpg-assistant/tests/test_ai_agent.py` - Không có mô tả.
  - `Lớp` **TestAIService**: 
    - `Method` mock_key_manager(): Mock key manager
    - `Method` ai_service(): Create AI service with mocked dependencies
    - `Method` test_init_ai_service(): Test AI service initialization
    - `Method` test_cache_functionality(): Test caching mechanism
    - `Method` test_generate_content_with_retry(): Test generate content with retry mechanism
    - `Method` test_key_manager_integration(): Test integration with key manager
    - `Method` test_model_priority_list(): Test that model priority is defined
    - `Method` test_cache_ttl_configuration(): Test cache TTL configuration

#### 📄 `projects/jarvis-rpg-assistant/tests/test_core.py` - Không có mô tả.
  - `Hàm` **temp_db()**: Create a temporary database for testing
  - `Hàm` **key_manager()**: Create a key manager instance for testing
  - `Lớp` **TestDatabaseManager**: 
    - `Method` test_init_creates_tables(): Test that database initialization creates all required tables
    - `Method` test_get_user_profile(): Test getting user profile
    - `Method` test_update_user_stats(): Test updating user stats
    - `Method` test_add_vocab(): Test adding vocabulary
    - `Method` test_get_due_vocab(): Test getting due vocabulary
    - `Method` test_get_review_candidates_new(): Test getting new vocabulary for review
    - `Method` test_get_review_candidates_review(): Test getting vocabulary for review
    - `Method` test_update_vocab_mastery_correct(): Test updating vocabulary when remembered correctly
    - `Method` test_update_vocab_mastery_incorrect(): Test updating vocabulary when not remembered
    - `Method` test_database_close(): Test database cleanup
  - `Lớp` **TestKeyManager**: 
    - `Method` test_init_key_manager(): Test key manager initialization
    - `Method` test_get_next_key(): Test getting next available key
    - `Method` test_get_next_key_rotation(): Test key rotation
    - `Method` test_mark_key_exhausted(): Test marking key as exhausted
    - `Method` test_reset_exhausted_keys(): Test resetting exhausted keys

#### 📄 `projects/jarvis-rpg-assistant/tests/test_new_features.py` - Không có mô tả.
  - `Lớp` **TestConfigModule**: 
    - `Method` test_config_module_imports(): Test that config module can be imported
    - `Method` test_config_paths_exist(): Test that config defines required paths
  - `Lớp` **TestKeyManager**: 
    - `Method` test_key_manager_basic(): Test key manager basic functionality
    - `Method` test_key_rotation(): Test key rotation mechanism

#### 📄 `projects/jarvis-rpg-assistant/tools/admin_gui.py` - Không có mô tả.
  - `Lớp` **JarvisAdminApp**: 
    - `Method` __init__(): 
    - `Method` run_query(): 
    - `Method` load_data(): 
    - `Method` on_select(): 
    - `Method` add_word(): 
    - `Method` update_word(): 
    - `Method` delete_word(): 
    - `Method` hack_time(): 

#### 📄 `projects/jarvis-rpg-assistant/tools/bot_sync.py` - Không có mô tả.
  - `Lớp` **ScheduleSyncApp**: 
    - `Method` __init__(): 
    - `Method` log(): 
    - `Method` start_web_sync_thread(): 
    - `Method` start_img_sync_thread(): 
    - `Method` handle_drop(): 
    - `Method` run_web_sync(): 
    - `Method` run_process_images(): 
    - `Method` process_with_ai(): 
    - `Method` push_to_google_calendar(): 

#### 📄 `projects/jarvis-rpg-assistant/tools/calendar_ui.py` - Không có mô tả.
  - `Hàm` **get_next_weekday()**: Tính ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất.
  - `Hàm` **generate_google_calendar_csv()**: Tạo nội dung CSV chuẩn Google Calendar.

#### 📄 `projects/jarvis-rpg-assistant/tools/cheat_db.py` - Không có mô tả.
  - `Hàm` **hack_time()**: 

#### 📄 `projects/jarvis-rpg-assistant/tools/dashboard.py` - Không có mô tả.
  - `Hàm` **get_db()**: 

#### 📄 `projects/jarvis-rpg-assistant/tools/public_readiness_check.py` - Không có mô tả.
  - `Hàm` **run_command()**: 

#### 📄 `projects/jarvis-rpg-assistant/tools/test.py` - Không có mô tả.

#### 📄 `projects/jarvis-rpg-assistant/tools/test_key.py` - Không có mô tả.
  - `Hàm` **load_keys_from_file()**: Đọc tất cả API Key từ file, loại bỏ khoảng trắng và dòng trống.
  - `Hàm` **quick_verify_api()**: Hàm kiểm tra nhanh 1 key

#### 📄 `projects/knowledge_base_agent/src/ingest.py` - Không có mô tả.
  - `Hàm` **bootstrap_environment()**: Khởi tạo toàn bộ hạ tầng thư mục lưu trữ nếu chưa tồn tại.
  - `Hàm` **collect_pending_assets()**: Quét và thu thập danh sách các tập tin PDF đang chờ xử lý.
  - `Hàm` **parse_pdf_to_markdown_and_chunk()**: Trích xuất PDF bằng PyMuPDF4LLM, băm theo Markdown và Recursive.
  - `Hàm` **safe_initialize_embeddings()**: Khởi tạo mô hình Embedding cục bộ. Tích hợp cơ chế Fallback.
  - `Hàm` **commit_to_vectorstore()**: Lưu trữ các vector dữ liệu vào hệ quản trị cơ sở dữ liệu vector ChromaDB.
  - `Hàm` **relocate_processed_assets()**: Di chuyển các tệp tin gốc đã xử lý thành công sang phân vùng lưu trữ lâu dài.
  - `Hàm` **run_pipeline()**: Hàm điều phối (Orchestrator) thực thi toàn bộ chu trình nạp dữ liệu.

#### 📄 `projects/knowledge_base_agent/src/rag_agent.py` - Không có mô tả.
  - `Lớp` **RAGAgent**: Agent RAG (Retrieval-Augmented Generation) chuyên dùng để query kiến thức từ Ebook.
    - `Method` __init__(): 
    - `Method` query(): Nhận câu hỏi, tìm kiếm relevant chunks và đưa cho LLM tổng hợp câu trả lời.
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 

#### 📄 `projects/LocalRelay/local_relay.py` - Không có mô tả.
  - `Hàm` **websocket_endpoint()**: Endpoint dành cho con App AI Studio trên trình duyệt kết nối vào
  - `Hàm` **handle_cline_request()**: Endpoint hứng request HTTP từ Cline gửi qua

#### 📄 `projects/local_proxy_server/main.py` - Local Proxy Server - Main Entry Point
  - `Hàm` **lifespan()**: Application lifespan manager.
  - `Hàm` **main()**: Main entry point for the Local Proxy Server.

#### 📄 `projects/local_proxy_server/core/adapter.py` - Adapter Module for Payload Conversion
  - `Hàm` **_trim_messages_if_needed()**: Tiêu chuẩn 1: Zero Token Leakage.
  - `Hàm` **to_gemini_payload()**: Convert OpenAI-compatible chat completion payload to Gemini API format.
  - `Hàm` **to_openai_stream()**:     Convert Gemini streaming response chunk to OpenAI SSE format.
  - `Hàm` **to_openai_final_chunk()**: Create a final chunk to signal stream completion.
  - `Hàm` **_extract_text_from_gemini_obj()**: Extract output text from a single parsed Gemini stream object,
  - `Hàm` **stream_gemini_to_openai()**: Transform Gemini streaming response to OpenAI SSE format.
  - `Hàm` **_extract_next_json_object()**: Find the first complete top-level JSON object in buffer using brace-depth.

#### 📄 `projects/local_proxy_server/core/config.py` - Core Configuration Module for Local Proxy Server
  - `Lớp` **Settings**: Application settings and configuration.
    - `Method` __init__(): Initialize settings and validate required environment variables.
    - `Method` map_model(): Map requested model name or label to actual Google API model string.
    - `Method` get_gemini_stream_url(): Build the Gemini streaming endpoint URL for a specific (model, key) pair.
  - `Hàm` **get_settings()**: Get the global settings instance.

#### 📄 `projects/local_proxy_server/core/rotation_manager.py` - Rotation Manager Module - Smart State Manager for API Key & Model Rotation.
  - `Lớp` **RotationManager**: Smart dispatcher: rotates API Keys per-model and falls back to alternative
    - `Method` __init__(): 
    - `Method` _is_exhausted(): 
    - `Method` get_valid_credential(): Find a valid (Key, Model) pair that still has quota.
    - `Method` mark_exhausted(): Mark a (key, model) pair as quota-exhausted so it is skipped in
    - `Method` reset_quota_pool(): Clear all exhausted records. Call at UTC midnight or manually.
    - `Method` _maybe_auto_reset(): Auto-reset pool when the calendar day changes (UTC).
    - `Method` get_stats(): Return current rotation statistics for monitoring.
  - `Hàm` **get_rotation_manager()**: Get the global RotationManager singleton.

#### 📄 `projects/local_proxy_server/core/router.py` - Router Module for FastAPI Endpoints
  - `Hàm` **stream_fallback_generator()**: Fallback generator using Groq or OpenRouter when Gemini is fully exhausted.
  - `Hàm` **stream_generator()**: Async generator that streams responses from Gemini and converts to OpenAI format.
  - `Hàm` **chat_completions()**: OpenAI-compatible chat completions endpoint with streaming support.
  - `Hàm` **health_check()**: Health check endpoint.
  - `Hàm` **_init_billing_db()**: 
  - `Hàm` **process_billing()**: Tiêu chuẩn 3: Crypto Payment Config Ready & Anti-Replay
  - `Hàm` **root()**: Root endpoint with service information.

#### 📄 `projects/local_proxy_server/tests/test_proxy.py` - Lightweight Unit Test for RotationManager logic.
  - `Hàm` **make_manager()**: Build a RotationManager with a fake Settings containing N keys.
  - `Hàm` **test_basic_dispatch()**: Test 1: Basic credential dispatch returns a valid pair.
  - `Hàm` **test_mark_exhausted_skip()**: Test 2: Marked pair is skipped on next dispatch.
  - `Hàm` **test_fallback_to_alternative_model()**: Test 3: When all keys of requested model die, fallback to alternative model.
  - `Hàm` **test_full_exhaustion()**: Test 4: All pairs exhausted -> RuntimeError.
  - `Hàm` **test_stats()**: Test 5: get_stats returns accurate counts.

#### 📄 `projects/local_proxy_server/tests/test_proxy_server.py` - Unit Tests for Local Proxy Server
  - `Hàm` **test_adapter_to_gemini_payload()**: Test conversion from OpenAI to Gemini payload format.
  - `Hàm` **test_adapter_to_openai_stream()**: Test conversion from Gemini chunk to OpenAI SSE format.
  - `Hàm` **test_api_key_rotation_logic()**: Test the configuration loading and rotation mechanism of API Keys.
  - `Hàm` **test_health_endpoint()**: Test the health check endpoint.
  - `Hàm` **test_root_endpoint()**: Test the root endpoint.
  - `Hàm` **test_chat_completions_stream()**: Test the chat completions endpoint with streaming.
  - `Hàm` **run_tests()**: Run all tests.

#### 📄 `projects/nsfw_multimedia_auditor/api.py` - Không có mô tả.
  - `Hàm` **startup_event()**: 
  - `Lớp` **AuditRequest**: 
  - `Lớp` **AuditResponse**: 
  - `Hàm` **read_root()**: 
  - `Hàm` **audit_frames()**: 

#### 📄 `projects/nsfw_multimedia_auditor/auditor_agent.py` - Không có mô tả.
  - `Lớp` **ShadowAuditorV2**: [ROLE: Shadow Auditor / Chaos Alchemist]
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` analyze_frames(): 
    - `Method` _calculate_skin_percentage(): 
    - `Method` generate_report(): 
    - `Method` save_json(): Lưu kết quả ra file JSON để làm input cho LLM.

#### 📄 `projects/nsfw_multimedia_auditor/censorship_engine.py` - Không có mô tả.
  - `Lớp` **CensorshipEngine**: [ROLE: Cyber Security / Chaos Alchemist]
    - `Method` __init__(): 
    - `Method` censor_image(): Phát hiện và che vùng nhạy cảm trong ảnh.

#### 📄 `projects/nsfw_multimedia_auditor/collision_logic.py` - Không có mô tả.
  - `Lớp` **CollisionLogic**: [ROLE: Chaos Engineer / Action Analyst]
    - `Method` __init__(): 
    - `Method` detect_insertion_events(): 
    - `Method` _is_overlapping(): 
    - `Method` _generate_detailed_summary(): 

#### 📄 `projects/nsfw_multimedia_auditor/downloader.py` - Không có mô tả.
  - `Hàm` **download_llm()**: Tải model TinyLlama siêu nhẹ để tóm tắt nội dung.

#### 📄 `projects/nsfw_multimedia_auditor/identity_tracker.py` - Không có mô tả.
  - `Lớp` **IdentityTracker**: [ROLE: Principal System Architect / Chaos Alchemist]
    - `Method` __init__(): 
    - `Method` process_timeline(): Đọc dữ liệu JSON và phân loại nhân vật.
    - `Method` _update_profiles(): 
    - `Method` _generate_v4_summary(): 

#### 📄 `projects/nsfw_multimedia_auditor/interaction_detector.py` - Không có mô tả.
  - `Lớp` **InteractionDetector**: [ROLE: God Eye / Security Auditor]
    - `Method` __init__(): 
    - `Method` analyze_interactions(): 
    - `Method` _calculate_distance(): 
    - `Method` _check_overlap(): 
    - `Method` _summarize_log(): 

#### 📄 `projects/nsfw_multimedia_auditor/narrative_bridge.py` - Không có mô tả.
  - `Lớp` **NarrativeBridge**: [ROLE: Narrative Architect / Storyteller]
    - `Method` __init__(): 
    - `Method` _generate_rule_based_script(): Dùng logic quy tắc để viết kịch bản nếu AI bị chặn.
    - `Method` _ai_handler(): Thử dùng AI với prompt siêu an toàn (Abstract Geometry).
    - `Method` _logic_handler(): Fallback tối thượng: Dùng Rule Engine của chúng ta.
    - `Method` run_synthesis(): 

#### 📄 `projects/nsfw_multimedia_auditor/processor.py` - Không có mô tả.
  - `Hàm` **extract_keyframes()**: Trích xuất keyframes từ video mỗi X giây.

#### 📄 `projects/nsfw_multimedia_auditor/synthesizer.py` - Không có mô tả.
  - `Hàm` **synthesize_narrative()**: Đọc timeline JSON và dùng TinyLlama để viết tóm tắt diễn biến.

#### 📄 `projects/nsfw_multimedia_auditor/video_brain.py` - Không có mô tả.
  - `Lớp` **VideoBrain**: [ROLE: God Eye / Multimodal Architect]
    - `Method` __init__(): 
    - `Method` analyze_frame(): Hỏi bộ não về một frame cụ thể.
    - `Method` describe_interaction(): Phân tích chuỗi hành động giữa các frame.

#### 📄 `projects/nsfw_multimedia_auditor/vision_describer.py` - Không có mô tả.
  - `Hàm` **encode_image()**: 
  - `Lớp` **CharacterDescriber**: [ROLE: AI Prompt Engineer / Visual Expert]
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` describe_character(): Gửi ảnh 'sạch' lên Gemini để lấy mô tả ngoại hình.

#### 📄 `projects/nsfw_multimedia_auditor/visual_anatomy.py` - Không có mô tả.
  - `Lớp` **VisualAnatomyEngine**: [ROLE: Principal System Architect / Chaos Alchemist]
    - `Method` analyze_appearance(): Phân tích ngoại hình dựa trên các vùng đã phát hiện.
    - `Method` _get_dominant_color_name(): Xác định màu chủ đạo đơn giản.

#### 📄 `projects/nsfw_multimedia_auditor/__init__.py` - NSFW Multimedia Auditor Module

#### 📄 `projects/project_manager_sentry/governance_engine.py` - Không có mô tả.
  - `Lớp` **SovereignGovernance**: 
    - `Method` __init__(): 
    - `Method` check_edit_permission(): Kiểm tra xem một Agent có quyền sửa file dựa trên OWNERS.json.
    - `Method` lock_sovereign_project(): Khóa các project L3 để ngăn chặn thay đổi ngoài ý muốn.

#### 📄 `projects/project_manager_sentry/lifecycle_manager.py` - Không có mô tả.
  - `Hàm` **evaluate_monorepo_health()**: 

#### 📄 `projects/project_manager_sentry/manager_agent.py` - Không có mô tả.
  - `Lớp` **ProjectManagerAgent**: Agent chuyên trách quản lý Monorepo Metadata và điều phối file.
    - `Method` __init__(): 
    - `Method` find_core_files(): Truy vấn metadata để lấy danh sách core files của một project.
    - `Method` run(): 

#### 📄 `projects/qa_chaos_agent/src/encyclopedia_writer.py` - Không có mô tả.
  - `Hàm` **write_to_encyclopedia()**: Ghi lỗi mới vào Bách khoa toàn thư để các Agent RAG có thể học được.

#### 📄 `projects/qa_chaos_agent/src/fuzzer_engine.py` - Không có mô tả.
  - `Lớp` **FuzzerEngine**: 
    - `Method` __init__(): 
    - `Method` extract_python_files_from_map(): Đọc SYSTEM_MAP.md để lấy ra các file Python có thể Fuzz.
    - `Method` dummy_fuzz_import(): Thử import module động để kiểm tra lỗi cú pháp, lỗi thiếu import (ModuleNotFoundError),
    - `Method` process_crash(): 
    - `Method` run_nightly_fuzz(): Chạy Fuzzing ngẫu nhiên 2 file mỗi đêm để nhẹ server.

#### 📄 `projects/qa_chaos_agent/src/llm_autopsy.py` - Không có mô tả.
  - `Lớp` **LLMAutopsy**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` analyze_crash(): Gửi Traceback cho LLM phân tích nguyên nhân và cách sửa.

#### 📄 `projects/qa_functional_agent/src/functional_tester.py` - Không có mô tả.
  - `Lớp` **FunctionalTester**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` ai_assert(): Sử dụng LLM để chấm điểm kết quả (Functional Assertion).
    - `Method` test_streamlit_ui(): Dùng Playwright test Streamlit UI (End-to-End)
    - `Method` test_script_generator(): Unit/Functional test cho ScriptGenerator của Auto Affiliate Video

#### 📄 `projects/real_estate_prediction/app.py` - Không có mô tả.
  - `Hàm` **home()**: Render trang chủ với các dropdown động lấy từ data.
  - `Hàm` **show_map()**: Render bản đồ Heatmap giá nhà theo Quận/Huyện.
  - `Hàm` **predict()**: API endpoint xử lý dự báo giá nhà.

#### 📄 `projects/real_estate_prediction/generate_ppt_report.py` - Không có mô tả.
  - `Hàm` **create_dashboard_ppt()**: 

#### 📄 `projects/real_estate_prediction/generate_word_report.py` - Không có mô tả.
  - `Hàm` **create_report()**: 

#### 📄 `projects/real_estate_prediction/train_model.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `projects/sillytavern_world_card_generator/run_nsfw_writer.py` - Không có mô tả.
  - `Hàm` **main()**: Main function to run the NSFW writing workflow.

#### 📄 `projects/sillytavern_world_card_generator/src/auto_translator.py` - Không có mô tả.
  - `Lớp` **AutoTranslatorAgent**: 
    - `Method` __init__(): 
    - `Method` translate_text(): 
  - `Hàm` **translate_card()**: 
  - `Hàm` **batch_translate()**: 

#### 📄 `projects/sillytavern_world_card_generator/src/extract_png_cards.py` - Không có mô tả.

#### 📄 `projects/sillytavern_world_card_generator/src/ingest_cards.py` - Không có mô tả.
  - `Hàm` **extract_card_text()**: Trích xuất các trường nội dung quan trọng từ thẻ JSON của SillyTavern.
  - `Hàm` **ingest_cards()**: 

#### 📄 `projects/sillytavern_world_card_generator/src/lore_extractor.py` - Không có mô tả.
  - `Hàm` **read_json_file()**: 
  - `Hàm` **build_llm_prompt()**: 
  - `Hàm` **call_llm_api()**: 
  - `Hàm` **write_markdown_file()**: 
  - `Hàm` **get_output_filename()**: 
  - `Hàm` **has_chinese_chars()**: 
  - `Hàm` **get_processed_files()**: 
  - `Hàm` **log_processed_file()**: 
  - `Hàm` **agent_process_card()**: 
  - `Hàm` **main()**: 

#### 📄 `projects/sillytavern_world_card_generator/src/merge_regex.py` - Không có mô tả.

#### 📄 `projects/sillytavern_world_card_generator/src/merge_regex_all.py` - Không có mô tả.

#### 📄 `projects/sillytavern_world_card_generator/src/world_card_generator.py` - World Card Generator (Orchestrator):
  - `Lớp` **WorldCardGenerator**: 
    - `Method` __init__(): 
    - `Method` generate(): Chạy quy trình sinh dữ liệu bằng AI thực.
    - `Method` export_to_json(): Xuất file JSON.

#### 📄 `projects/sillytavern_world_card_generator/src/__init__.py` - Không có mô tả.

#### 📄 `projects/sillytavern_world_card_generator/src/agents/base_agent.py` - Không có mô tả.
  - `Lớp` **BaseGeminiAgent**: Class cơ sở chứa logic gọi API thông qua ChatOpenAI (tương thích proxy của OpenAI).
    - `Method` __init__(): 
    - `Method` _call_gemini(): Gửi prompt đến LLM thông qua ChatOpenAI và trả về chuỗi kết quả.
    - `Method` _parse_json_response(): Cố gắng parse chuỗi trả về thành JSON một cách an toàn.

#### 📄 `projects/sillytavern_world_card_generator/src/agents/coder_agent.py` - Coder Agent:
  - `Lớp` **CoderAgent**: 
    - `Method` __init__(): 
    - `Method` generate_extensions(): Sinh ra các file extension dựa trên tính năng được yêu cầu.
  - `Hàm` **generate_code_mock()**: 

#### 📄 `projects/sillytavern_world_card_generator/src/agents/lore_master_agent.py` - Lore Master Agent:
  - `Lớp` **LoreMasterAgent**: 
    - `Method` __init__(): 
    - `Method` generate_lorebook(): Tạo danh sách Lorebook entries bằng Gemini.
  - `Hàm` **generate_lore_mock()**: 

#### 📄 `projects/sillytavern_world_card_generator/src/agents/rag_card_agent.py` - Không có mô tả.
  - `Lớp` **RAGCardAgent**: Agent RAG chuyên dùng để tìm kiếm thẻ mẫu từ ChromaDB, giúp AI học lỏm văn phong.
    - `Method` __init__(): 
    - `Method` get_reference_context(): Lấy context từ các thẻ cũ dựa trên theme và style.

#### 📄 `projects/sillytavern_world_card_generator/src/agents/storyteller_agent.py` - Storyteller Agent:
  - `Lớp` **StorytellerAgent**: 
    - `Method` __init__(): 
    - `Method` generate_narrative_context(): Tạo System Prompt và First Message từ ý tưởng người dùng bằng Gemini.

#### 📄 `projects/sillytavern_world_card_generator/src/models/world_card_v3.py` - Không có mô tả.
  - `Lớp` **LoreBookExtension**: Phần mở rộng của 1 entry trong Lorebook
  - `Lớp` **LoreBookEntry**: Đại diện cho 1 Mục (Entry) trong Lorebook
  - `Lớp` **CharacterBook**: Bọc danh sách các entries
  - `Lớp` **CharacterExtensions**: Phần Extensions bọc regex và các tính năng phụ của character
  - `Lớp` **CharacterData**: Phần Data chứa chi tiết Character/World Card
  - `Lớp` **WorldCardV3**: Cấu trúc bao bọc lớp ngoài cùng của file JSON chuẩn V3.
    - `Method` to_json(): Xuất ra chuỗi JSON đẹp mắt.
  - `Lớp` **UserIdeaInput**: Input từ người dùng để AI sinh ra thẻ.

#### 📄 `projects/sillytavern_world_card_generator/tests/test_basic.py` - Không có mô tả.
  - `Hàm` **test_basic_initialization()**: Basic test to ensure project initializes correctly.

#### 📄 `projects/sillytavern_world_card_generator/tools/non_ai_lorebook_extractor.py` - Không có mô tả.
  - `Lớp` **LorebookExtractor**: 
    - `Method` __init__(): 
    - `Method` _extract_characters_regex(): 
    - `Method` extract_context_around_name(): Extracts context around mentions of a character.
    - `Method` analyze_traits(): Analyzes context text against keyword dictionaries.
    - `Method` create_sillytavern_entry(): Formats the extracted traits into a SillyTavern JSON entry.
    - `Method` process_file(): 

#### 📄 `projects/sillytavern_world_card_generator/tools/streamlit_lorebook_app.py` - Không có mô tả.
  - `Lớp` **OllamaLorebookExtractor**: 
    - `Method` __init__(): 
    - `Method` get_available_models(): Fetches available models from the Ollama instance.
    - `Method` extract_with_ai(): Sends text to Ollama and expects a JSON response formatted for SillyTavern.

#### 📄 `projects/sillytavern_world_card_generator/ui/app.py` - Không có mô tả.

#### 📄 `projects/sovereign_academy/main.py` - Không có mô tả.
  - `Hàm` **load_profile()**: 
  - `Hàm` **save_profile()**: 
  - `Hàm` **update_spaced_repetition()**: 
  - `Hàm` **run_lesson()**: 
  - `Hàm` **main()**: 

#### 📄 `projects/sovereign_academy/one_click_learn.py` - Không có mô tả.
  - `Hàm` **one_click_run()**: 

#### 📄 `projects/sovereign_academy/tutor_agent.py` - Không có mô tả.
  - `Lớp` **QuizOption**: 
  - `Lớp` **QuizQuestion**: 
  - `Lớp` **Quiz**: 
  - `Lớp` **CodeTutorAgent**: [ROLE: Code Tutor / Sovereign Academy]
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` get_random_core_file(): Lấy ngẫu nhiên 1 file Python từ core/ hoặc core_utilities/
    - `Method` read_code(): 
    - `Method` explain_code(): 
    - `Method` generate_quiz(): 

#### 📄 `projects/trading_rpg_simulator/dungeon_master.py` - Không có mô tả.
  - `Lớp` **DungeonMaster**: Hệ thống sinh kịch bản ngẫu nhiên đóng vai trò là "Thị trường" (Môi trường game).
    - `Method` __init__(): 
    - `Method` generate_next_turn(): Sinh ra dữ liệu cho 1 lượt chơi (1 ngày).
    - `Method` resolve_combat(): Tính toán PnL dựa trên quyết định của TraderHero và biến động thực tế.

#### 📄 `projects/trading_rpg_simulator/trader_hero.py` - Không có mô tả.
  - `Lớp` **TraderHero**: AI Agent đóng vai trò Trader. Nó sẽ nhận dữ liệu môi trường từ Dungeon Master,
    - `Method` __init__(): 
    - `Method` make_decision(): Đưa ra quyết định dựa trên tin tức hiện tại và ký ức.
    - `Method` reflect_and_learn(): Đúc kết kinh nghiệm sau mỗi trận đấu (ngày).

#### 📄 `projects/universal_game_vault/src/analyzer.py` - [LỖI AST: expected an indented block after 'if' statement on line 16 (analyzer.py, line 17)]

#### 📄 `projects/universal_game_vault/src/dispatcher.py` - [LỖI AST: expected an indented block after 'if' statement on line 16 (dispatcher.py, line 17)]

#### 📄 `projects/universal_game_vault/src/scraper.py` - Không có mô tả.
  - `Lớp` **GameWebScraper**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` scrape_url(): Cào nội dung văn bản từ một URL.

#### 📄 `projects/universal_game_vault/src/processors/advanced_extractor.py` - [LỖI AST: expected an indented block after 'if' statement on line 15 (advanced_extractor.py, line 16)]

#### 📄 `projects/universal_game_vault/src/processors/batch_importer.py` - [LỖI AST: expected an indented block after 'if' statement on line 17 (batch_importer.py, line 18)]

#### 📄 `projects/universal_game_vault/src/processors/full_text_parser.py` - [LỖI AST: expected an indented block after 'if' statement on line 16 (full_text_parser.py, line 17)]

#### 📄 `projects/universal_game_vault/src/processors/text_parser.py` - Không có mô tả.
  - `Lớp` **GameAIProcessor**: 
    - `Method` __init__(): 
    - `Method` analyze_document(): Sử dụng LLM để phân tích tài liệu và phân loại thực thể.
    - `Method` update_wiki(): Cập nhật các file Markdown trong thư mục wiki/.

#### 📄 `projects/universal_game_vault/src/storage/db_manager.py` - Không có mô tả.
  - `Lớp` **GameDBManager**: 
    - `Method` __init__(): 
    - `Method` init_db(): Khoi tao cau truc bang du lieu.
    - `Method` sync_from_wiki(): Doc file Markdown va dong bo vao SQLite.
    - `Method` query_characters(): Truy van nhan vat theo tieu chi.

#### 📄 `projects/universal_web_scraper/main.py` - Không có mô tả.
  - `Hàm` **download_html()**: Tải toàn bộ mã nguồn HTML từ một URL và lưu vào file cục bộ.
  - `Hàm` **main()**: 

#### 📄 `projects/universal_web_scraper/src/alonhadat_parser.py` - Không có mô tả.
  - `Lớp` **BaseScraper**: 
    - `Method` __init__(): 
    - `Method` get_scraped_pages(): Đọc danh sách các trang đã cào thành công từ log file.
    - `Method` add_scraped_page(): Ghi nhận một trang đã cào thành công.
    - `Method` clean_old_data(): Xóa dữ liệu rác (Area < 10, District chứa tên đường) khỏi file gộp.
    - `Method` incremental_merge(): Gộp dữ liệu mới vào output_csv nội bộ và raw_data.csv của mô hình.
  - `Lớp` **AlonhadatParser**: 
    - `Method` __init__(): 
    - `Method` build_headers(): 
    - `Method` scrape_page(): 
    - `Method` run_guerrilla(): Chiến thuật Cào Du Kích: Trộn trang, cào từng batch nhỏ rồi nghỉ.

#### 📄 `projects/universal_web_scraper/src/alonhadat_playwright.py` - Không có mô tả.
  - `Lớp` **AlonhadatPlaywrightScraper**: 
    - `Method` __init__(): 
    - `Method` parse_page_data(): 
    - `Method` run_scraper(): 
    - `Method` save_and_merge(): 

#### 📄 `projects/universal_web_scraper/src/base_scraper.py` - Không có mô tả.
  - `Lớp` **PlaywrightStealth**: 
    - `Method` random_scroll(): 
    - `Method` human_pause(): 
  - `Lớp` **BaseConfig**: 

#### 📄 `projects/universal_web_scraper/src/batdongsan_playwright.py` - Không có mô tả.
  - `Lớp` **BatDongSanPlaywrightScraper**: 
    - `Method` __init__(): 
    - `Method` get_scraped_pages(): 
    - `Method` add_scraped_page(): 
    - `Method` parse_page_data(): 
    - `Method` run_guerrilla(): 
    - `Method` save_and_merge(): 

#### 📄 `projects/universal_web_scraper/src/cleaner.py` - Không có mô tả.
  - `Hàm` **clean_and_rank_data()**: Làm sạch dữ liệu Hacker News, tính Engagement_Score và lưu kết quả.

#### 📄 `projects/universal_web_scraper/src/parser.py` - Không có mô tả.
  - `Hàm` **parse_hacker_news()**: Parse Hacker News HTML and extract title, href, score, and comments.

### 📂 THƯ MỤC: `core/`

#### 📄 `core/drm_validator.py` - Không có mô tả.
  - `Hàm` **check_license_validity()**: Core DRM Logic.
  - `Hàm` **init_drm()**: 

#### 📄 `core/logic_auditor.py` - Không có mô tả.
  - `Lớp` **LogicAuditor**: Fitness Function - Bộ lọc đào thải tự nhiên của hệ thống Sovereign.
    - `Method` __init__(): 
    - `Method` start_session(): Bắt đầu đo lường tài nguyên trước khi Agent thực thi nháp.
    - `Method` evaluate_evolution(): Đánh giá bản nháp so với tiêu chuẩn hệ thống.

#### 📄 `core/mental_sandbox.py` - Không có mô tả.
  - `Lớp` **MentalSandbox**: [ROLE: Principal System Architect / Chaos Engineer]
    - `Method` __init__(): 
    - `Method` _ensure_sandbox(): 
    - `Method` create_draft(): Tạo bản nháp của file trong sandbox.
    - `Method` verify_syntax(): Kiểm tra lỗi cú pháp (Syntax Check) bằng AST.
    - `Method` verify_logic(): [VULN-001] Kiểm tra các lỗi logic nguy hiểm (Runtime Risks).
    - `Method` run_unit_tests(): Chạy các bài unit test liên quan.
    - `Method` deploy_draft(): Merge bản nháp vào file gốc sau khi đã qua kiểm duyệt.
    - `Method` cleanup(): Dọn dẹp sandbox.

#### 📄 `core/post_mortem_engine.py` - Không có mô tả.
  - `Lớp` **PostMortemEngine**: Module tự động phân tích lỗi lầm thực tế (Post-Mortem).
    - `Method` __init__(): 
    - `Method` analyze_recent_trades(): Phân tích các lệnh giao dịch gần đây.
    - `Method` _log_failure(): Cập nhật vào FAILED_PATHS.json

#### 📄 `core/principles_enforcer.py` - Không có mô tả.
  - `Lớp` **PrinciplesEnforcer**: Lớp đối soát nguyên lý (Principles Enforcer) - Sovereign Core.
    - `Method` __init__(): 
    - `Method` verify_decision(): Kiểm tra xem quyết định có vi phạm nguyên lý cốt lõi không.
    - `Method` audit_agent_output(): Chấm điểm độ tuân thủ nguyên lý của văn bản (0.0 - 1.0)

#### 📄 `core/process_watchdog.py` - Không có mô tả.
  - `Lớp` **ProcessWatchdog**: 💊 ĐẶC VỤ Y TẾ (Sovereign Process Watchdog)
    - `Method` __init__(): 
    - `Method` log_failure(): Ghi tội danh của tiến trình bị trảm vào FAILED_PATHS.json.
    - `Method` monitor_pid(): Giám sát một tiến trình và TOÀN BỘ tiến trình con của nó.

### 📂 THƯ MỤC: `scheduler/`

#### 📄 `scheduler/drip_feed_worker.py` - Không có mô tả.
  - `Lớp` **DripFeedWorker**: 🌊 BỘ ĐIỀU PHỐI HỎA LỰC (Drip-Feed Worker)
    - `Method` __init__(): 
    - `Method` _throttled_task(): Thực thi task với Semaphore khống chế.
    - `Method` process_batch(): Xử lý một danh sách các task theo kiểu nhỏ giọt (Drip-feed).
  - `Hàm` **mock_scraping_task()**: 
  - `Hàm` **test()**: 

#### 📄 `scheduler/main_scheduler.py` - Không có mô tả.
  - `Hàm` **load_state()**: 
  - `Hàm` **save_state()**: 
  - `Hàm` **update_job_state()**: 
  - `Hàm` **run_with_retry_and_log()**: Run a subprocess with capture_output, retry on failure, and return (success_bool, error_snippet)
  - `Hàm` **send_telegram_alert()**: 
  - `Hàm` **run_queued()**: Decorator để đẩy job vào hàng đợi của ThreadPoolExecutor
  - `Hàm` **scrape_job()**: 
  - `Hàm` **daily_trading_job()**: 
  - `Hàm` **airdrop_job()**: 
  - `Hàm` **omni_overlord_watchdog()**: 
  - `Hàm` **check_missed_jobs()**: Kiểm tra xem khi khởi động máy có bị lỡ job nào của ngày hôm nay không.

#### 📄 `scheduler/test_catchup.py` - Không có mô tả.

### 📂 THƯ MỤC: `tools/`

#### 📄 `tools/build_all_reqs.py` - Không có mô tả.

#### 📄 `tools/compile_drm.py` - Không có mô tả.
  - `Hàm` **run_cython()**: 

#### 📄 `tools/convert_csv_to_data.py` - Không có mô tả.
  - `Hàm` **convert_csv_to_data()**: Chuyển đổi file CSV đã dịch trở lại thành định dạng locate.data gốc.

#### 📄 `tools/convert_data_to_csv.py` - Không có mô tả.
  - `Hàm` **convert_data_to_csv()**: Chuyển đổi file locate.data (file CSV ẩn của Godot) thành định dạng chuẩn key,en,vi,ja

#### 📄 `tools/extract_cookies.py` - Không có mô tả.
  - `Hàm` **extract_tiktok_cookies()**: Script trích xuất Cookies tự động từ profile Microsoft Edge của Admin.

#### 📄 `tools/extract_godot_csv.py` - Không có mô tả.
  - `Hàm` **generate_smart_key()**: Tạo key thông minh từ nội dung: T_<hash_6_char>_<5_từ_đầu>
  - `Hàm` **is_garbage_string()**: Kiểm tra xem chuỗi có phải là rác không.
  - `Hàm` **extract_strings_to_csv()**: 

#### 📄 `tools/generate_flagship_roadmap.py` - Không có mô tả.
  - `Hàm` **generate_flagship_roadmap()**: 

#### 📄 `tools/manage.py` - Không có mô tả.
  - `Hàm` **print_help()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/market_research_scraper.py` - [LỖI AST: expected an indented block after 'if' statement on line 62 (market_research_scraper.py, line 63)]

#### 📄 `tools/package_beta.py` - Không có mô tả.
  - `Hàm` **create_portable_package()**: 

#### 📄 `tools/run_notebooks.py` - Không có mô tả.
  - `Hàm` **run_notebook()**: 

#### 📄 `tools/run_pipeline_data.py` - Không có mô tả.

#### 📄 `tools/run_pipeline_lstm.py` - Không có mô tả.

#### 📄 `tools/run_pipeline_ml.py` - Không có mô tả.

#### 📄 `tools/run_qa_agent.py` - Không có mô tả.
  - `Hàm` **qa_agent_audit()**: 

#### 📄 `tools/run_tester_agent.py` - Không có mô tả.
  - `Hàm` **test_code()**: 

#### 📄 `tools/scrape_opgg.py` - Không có mô tả.
  - `Hàm` **scrape_valorant()**: 

#### 📄 `tools/setup_project_foundation.py` - Không có mô tả.
  - `Hàm` **create_template()**: 
  - `Hàm` **generate_missing_files()**: 

#### 📄 `tools/system_cleaner.py` - Không có mô tả.
  - `Hàm` **get_core_sig()**: 
  - `Hàm` **clean_docs()**: 
  - `Hàm` **clean_comfy()**: 

#### 📄 `tools/telegram_bot_controller.py` - Không có mô tả.
  - `Hàm` **start()**: Gửi menu điều khiển khi user gõ /start.
  - `Hàm` **handle_message()**: 
  - `Hàm` **main()**: Start the bot.

#### 📄 `tools/test_youtube_api.py` - Không có mô tả.
  - `Hàm` **test_youtube_api()**: 

#### 📄 `tools/translate_csv.py` - Không có mô tả.
  - `Hàm` **translate_csv()**: Đọc file CSV, dịch cột 'ja' (hoặc 'en') sang 'vi' nếu cột 'vi' đang trống.

#### 📄 `tools/__init__.py` - Không có mô tả.

#### 📄 `tools/comfy/clothoff_cli.py` - Không có mô tả.
  - `Hàm` **to_base64()**: 
  - `Hàm` **select_file()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/comfy/clothoff_gui.py` - Không có mô tả.
  - `Hàm` **process_clothoff()**: 

#### 📄 `tools/comfy/clothoff_hf_cli.py` - Không có mô tả.
  - `Hàm` **select_file()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/comfy/create_clothoff_image.py` - Không có mô tả.
  - `Hàm` **to_base64()**: 
  - `Hàm` **generate_clothoff()**: 

#### 📄 `tools/edtech/create_10_diem_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_bang_tra_cuu_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_bmtt_cheatsheet_docx.py` - Không có mô tả.
  - `Hàm` **init_document()**: Khởi tạo file Word, thiết lập tiêu đề chính.
  - `Hàm` **add_affine_section()**: Module tạo nội dung rút gọn cho Câu 1: Mã Affine.
  - `Hàm` **add_hill_section()**: Module tạo nội dung rút gọn cho Câu 3: Mã Hill 3x3.
  - `Hàm` **add_playfair_rsa_theory()**: Module tạo nội dung rút gọn Playfair, RSA và Lý thuyết.
  - `Hàm` **generate_exam_doc()**: Hàm tổng phối hợp các module để ráp thành file hoàn chỉnh.
  - `Hàm` **run_unit_test()**: Test nhanh xem file có thực sự được tạo ra và lưu thành công không.

#### 📄 `tools/edtech/create_bmtt_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_full_10_cau_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_giai_de_cuong_qtkdcks.py` - Không có mô tả.
  - `Hàm` **add_heading()**: 
  - `Hàm` **add_paragraph()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/edtech/create_giai_de_cuong_qtkdcks_rut_gon.py` - Không có mô tả.
  - `Hàm` **add_heading()**: 
  - `Hàm` **add_paragraph()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/edtech/create_giai_de_cuong_qtkdcks_suy_luan.py` - Không có mô tả.
  - `Hàm` **add_heading()**: 
  - `Hàm` **add_paragraph()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/edtech/create_mindset_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_qtkdcks_audio_gtts.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/create_qtkdcks_audio_local.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/create_qtkdcks_audio_simple.py` - Không có mô tả.
  - `Hàm` **amain()**: 

#### 📄 `tools/edtech/create_qtkdcks_cheatsheet.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_qtkdcks_custom_audio.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/create_qtkdcks_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/create_qtkdcks_theory_audio.py` - Không có mô tả.
  - `Hàm` **amain()**: 

#### 📄 `tools/edtech/create_qtkdcks_theory_audio_story.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/qtkdcks_decuong_quiz.py` - Không có mô tả.
  - `Lớp` **DecuongQuizApp**: 
    - `Method` __init__(): 
    - `Method` build_ui(): 
    - `Method` handle_enter(): 
    - `Method` load_question(): 
    - `Method` check_answer(): 
    - `Method` next_question(): 

#### 📄 `tools/edtech/qtkdcks_formula_reflex.py` - Không có mô tả.
  - `Lớp` **FormulaQuizApp**: 
    - `Method` __init__(): 
    - `Method` build_ui(): 
    - `Method` handle_enter(): 
    - `Method` load_question(): 
    - `Method` check_answer(): 
    - `Method` next_question(): 

#### 📄 `tools/edtech/qtkdcks_quiz_app.py` - Không có mô tả.
  - `Lớp` **QuizApp**: 
    - `Method` __init__(): 
    - `Method` build_ui(): 
    - `Method` handle_enter(): 
    - `Method` load_question(): 
    - `Method` check_answer(): 
    - `Method` next_question(): 

#### 📄 `tools/edtech/scan_qtkdcks_pdfs.py` - Không có mô tả.

#### 📄 `tools/edtech/verify_bmtt_math.py` - Không có mô tả.
  - `Hàm` **mod_inverse()**: 
  - `Hàm` **affine_decrypt()**: 
  - `Hàm` **hill_encrypt()**: 
  - `Hàm` **rsa_encrypt()**: 

#### 📄 `tools/edtech/archive/create_10_diem_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_bang_tra_cuu_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_bmtt_cheatsheet_docx.py` - Không có mô tả.
  - `Hàm` **init_document()**: Khởi tạo file Word, thiết lập tiêu đề chính.
  - `Hàm` **add_affine_section()**: Module tạo nội dung rút gọn cho Câu 1: Mã Affine.
  - `Hàm` **add_hill_section()**: Module tạo nội dung rút gọn cho Câu 3: Mã Hill 3x3.
  - `Hàm` **add_playfair_rsa_theory()**: Module tạo nội dung rút gọn Playfair, RSA và Lý thuyết.
  - `Hàm` **generate_exam_doc()**: Hàm tổng phối hợp các module để ráp thành file hoàn chỉnh.
  - `Hàm` **run_unit_test()**: Test nhanh xem file có thực sự được tạo ra và lưu thành công không.

#### 📄 `tools/edtech/archive/create_bmtt_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_full_10_cau_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_giai_de_cuong_qtkdcks.py` - Không có mô tả.
  - `Hàm` **add_heading()**: 
  - `Hàm` **add_paragraph()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/edtech/archive/create_giai_de_cuong_qtkdcks_rut_gon.py` - Không có mô tả.
  - `Hàm` **add_heading()**: 
  - `Hàm` **add_paragraph()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/edtech/archive/create_giai_de_cuong_qtkdcks_suy_luan.py` - Không có mô tả.
  - `Hàm` **add_heading()**: 
  - `Hàm` **add_paragraph()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/edtech/archive/create_mindset_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_audio_gtts.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_audio_local.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_audio_simple.py` - Không có mô tả.
  - `Hàm` **amain()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_cheatsheet.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_custom_audio.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_docx.py` - Không có mô tả.
  - `Hàm` **create_docx()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_theory_audio.py` - Không có mô tả.
  - `Hàm` **amain()**: 

#### 📄 `tools/edtech/archive/create_qtkdcks_theory_audio_story.py` - Không có mô tả.
  - `Hàm` **create_audio()**: 

#### 📄 `tools/edtech/archive/qtkdcks_decuong_quiz.py` - Không có mô tả.
  - `Lớp` **DecuongQuizApp**: 
    - `Method` __init__(): 
    - `Method` build_ui(): 
    - `Method` handle_enter(): 
    - `Method` load_question(): 
    - `Method` check_answer(): 
    - `Method` next_question(): 

#### 📄 `tools/edtech/archive/qtkdcks_formula_reflex.py` - Không có mô tả.
  - `Lớp` **FormulaQuizApp**: 
    - `Method` __init__(): 
    - `Method` build_ui(): 
    - `Method` handle_enter(): 
    - `Method` load_question(): 
    - `Method` check_answer(): 
    - `Method` next_question(): 

#### 📄 `tools/edtech/archive/qtkdcks_quiz_app.py` - Không có mô tả.
  - `Lớp` **QuizApp**: 
    - `Method` __init__(): 
    - `Method` build_ui(): 
    - `Method` handle_enter(): 
    - `Method` load_question(): 
    - `Method` check_answer(): 
    - `Method` next_question(): 

#### 📄 `tools/edtech/archive/scan_qtkdcks_pdfs.py` - Không có mô tả.

#### 📄 `tools/edtech/archive/verify_bmtt_math.py` - Không có mô tả.
  - `Hàm` **mod_inverse()**: 
  - `Hàm` **affine_decrypt()**: 
  - `Hàm` **hill_encrypt()**: 
  - `Hàm` **rsa_encrypt()**: 

#### 📄 `tools/lorebook/create_ultimate_preset_v3.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `tools/lorebook/delete_empty_docs.py` - Không có mô tả.
  - `Hàm` **delete_empty_docs()**: 

#### 📄 `tools/lorebook/find_empty_docs.py` - Không có mô tả.
  - `Hàm` **find_empty_files()**: 

#### 📄 `tools/lorebook/merge_and_shorten_lorebook.py` - Không có mô tả.
  - `Hàm` **get_category()**: 

#### 📄 `tools/lorebook/merge_physiology_lorebook.py` - Không có mô tả.

#### 📄 `tools/misc/organize_girl_folder.py` - Không có mô tả.
  - `Hàm` **get_common_prefix()**: 
  - `Hàm` **clean_common_prefix()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/misc/run_ocr_hentai.py` - Không có mô tả.
  - `Hàm` **extract_text()**: 

#### 📄 `tools/rag_code/auto_rag_query.py` - Không có mô tả.
  - `Hàm` **main()**: 

#### 📄 `tools/rag_code/ingest_code.py` - Không có mô tả.
  - `Hàm` **get_all_code_files()**: Scans the directory tree and returns a list of file paths to be ingested.
  - `Hàm` **ingest_codebase()**: Main function to orchestrate the codebase ingestion process.

#### 📄 `tools/rag_code/inspect_docs.py` - Không có mô tả.
  - `Hàm` **inspect_docs()**: 

#### 📄 `tools/rag_code/query_code_db.py` - Không có mô tả.
  - `Hàm` **query_codebase()**: Initializes the RAG components and enters a loop to accept user queries.

#### 📄 `tools/rag_code/test_code_ingestion.py` - Không có mô tả.
  - `Hàm` **run_automated_tests()**: Runs a predefined set of queries against the codebase vector database

#### 📄 `tools/scanners/architecture_auditor.py` - Không có mô tả.
  - `Hàm` **audit_workspace()**: 

#### 📄 `tools/scanners/architecture_scanner.py` - Không có mô tả.
  - `Hàm` **analyze_file()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/scanners/freelance_scanner.py` - Không có mô tả.
  - `Hàm` **scan_freelance_jobs()**: Simulates scanning Upwork and vLance for AI automation jobs.

#### 📄 `tools/scanners/internship_scanner.py` - Không có mô tả.
  - `Hàm` **scan_internships()**: Simulates scanning job boards (LinkedIn, TopDev, ITviec) for AI Intern positions.

#### 📄 `tools/scanners/project_stat_analyzer.py` - Không có mô tả.
  - `Hàm` **analyze_project()**: 

#### 📄 `tools/system/api_mapper.py` - Không có mô tả.
  - `Hàm` **extract_env_keys()**: Đọc file .env và trả về danh sách các biến được định nghĩa (không chứa giá trị).
  - `Hàm` **scan_file_for_env_usage()**: Dùng AST để quét file Python xem có gọi os.getenv('KEY') hay không.
  - `Hàm` **main()**: 

#### 📄 `tools/system/apply_updates.py` - Không có mô tả.
  - `Hàm` **get_category()**: 

#### 📄 `tools/system/archivist_agent.py` - Không có mô tả.
  - `Lớp` **ArchivistAgent**: Agent làm nhiệm vụ nén tri thức (Context Distillation).
    - `Method` __init__(): 
    - `Method` distill_debate_room(): Nén DEBATE_ROOM.md.
    - `Method` run(): 

#### 📄 `tools/system/ast_patcher.py` - Không có mô tả.
  - `Lớp` **ASTPatcher**: Modifies Python code safely using Abstract Syntax Trees (AST).
    - `Method` read_ast(): 
    - `Method` write_ast(): 
    - `Method` apply_patch(): Applies a specific NodeTransformer to a file and saves it.

#### 📄 `tools/system/audit_reporter.py` - Không có mô tả.
  - `Lớp` **AIAuditReporter**: He thong tu dong sinh bao cao PDF ve tinh trang suc khoe va loi nhuan cua Vuong trieu AI.
    - `Method` __init__(): 
    - `Method` _get_airdrop_stats(): 
    - `Method` generate_pdf(): 

#### 📄 `tools/system/auto_compliance_fixer.py` - Không có mô tả.
  - `Hàm` **fix_missing_base_agent()**: 

#### 📄 `tools/system/auto_import_fixer.py` - Không có mô tả.
  - `Hàm` **fix_forbidden_imports()**: 

#### 📄 `tools/system/auto_mapper.py` - Không có mô tả.
  - `Hàm` **generate_system_map()**: 

#### 📄 `tools/system/awaken.py` - Không có mô tả.
  - `Hàm` **generate_morning_briefing()**: 

#### 📄 `tools/system/batch_qa_runner.py` - Không có mô tả.
  - `Hàm` **get_all_projects()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/system/benchmark_apis.py` - Không có mô tả.
  - `Hàm` **build_request_args()**: 
  - `Hàm` **test_speed()**: 
  - `Hàm` **send_single_req()**: 
  - `Hàm` **test_rate_limit()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/system/benchmark_upgrades.py` - Không có mô tả.
  - `Hàm` **test_router()**: 
  - `Hàm` **get_current_weather()**: Tra ve thoi tiet hien tai cua mot thanh pho.
  - `Lớp` **TestToolAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` run_test(): 
  - `Hàm` **test_tool_calling()**: 
  - `Hàm` **test_compressor()**: 
  - `Hàm` **generate_report()**: 

#### 📄 `tools/system/build_indexer.py` - Không có mô tả.
  - `Lớp` **IndexerAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Hàm` **main()**: 

#### 📄 `tools/system/ceo_training_arena.py` - Không có mô tả.
  - `Lớp` **CEOTrainingArena**: Môi trường huấn luyện chuyên biệt dành cho CEO (Cline).
    - `Method` __init__(): 
    - `Method` start_exam(): 

#### 📄 `tools/system/chaos_monkey.py` - Không có mô tả.
  - `Lớp` **ChaosMonkey**: [ROLE: QA Chaos Overlord]
    - `Method` __init__(): 
    - `Method` simulate_memory_leak(): Giả lập việc nuốt RAM để test Watchdog.
    - `Method` simulate_api_blackout(): Giả lập việc mất kết nối API bằng cách tạm thời ghi đè URL trong .env
    - `Method` corrupt_database(): Tiêm dữ liệu rác vào Database để test Validation Gates.

#### 📄 `tools/system/chaos_monkey_v2.py` - Không có mô tả.
  - `Lớp` **ChaosMonkeyV2**: [PHASE 1 Q4 - AUTOMATED CHAOS]
    - `Method` __init__(): 
    - `Method` unleash_chaos(): 

#### 📄 `tools/system/cleanup_docs.py` - Không có mô tả.
  - `Hàm` **cleanup_docs()**: 

#### 📄 `tools/system/compliance_checker.py` - Không có mô tả.
  - `Lớp` **ComplianceChecker**: [ROLE: SRE / QA Tester]
    - `Method` __init__(): 
    - `Method` _load_manifest_projects(): 
    - `Method` is_agent_file(): Heuristic to determine if a file is intended to be an Agent.
    - `Method` check_file(): 
    - `Method` _get_project_name(): 
    - `Method` _check_dangerous_nodes(): [VULN-002] Phát hiện các nỗ lực lách luật bằng getattr hoặc import thư viện cấm.
    - `Method` _analyze_class(): 
    - `Method` run(): 
    - `Method` export_report(): 

#### 📄 `tools/system/context_compressor.py` - Không có mô tả.
  - `Hàm` **compress_context()**: Nén nội dung ACTIVE_THOUGHTS.md bằng cách lưu trữ các task đã hoàn thành.
  - `Hàm` **compress_text()**: Tiện ích nén Token (Tokenomics Utility):

#### 📄 `tools/system/db_migrator.py` - Không có mô tả.
  - `Hàm` **migrate_database()**: 

#### 📄 `tools/system/delegate_audit.py` - Không có mô tả.

#### 📄 `tools/system/doc_debate_runner.py` - Không có mô tả.
  - `Lớp` **SkepticAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Lớp` **DefenderAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Lớp` **SynthesizerAgent**: 
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
  - `Hàm` **main()**: 

#### 📄 `tools/system/encyclopedia_builder.py` - Không có mô tả.
  - `Hàm` **build_encyclopedia()**: 

#### 📄 `tools/system/endtask.py` - Không có mô tả.
  - `Hàm` **run_command()**: 
  - `Hàm` **cleanup_processes()**: Dọn dẹp các tiến trình python/uv mồ côi để giải phóng venv lock.
  - `Hàm` **has_changes()**: Kiểm tra xem có thay đổi quan trọng trong mã nguồn không (Git check).
  - `Hàm` **anchoring()**: Sovereign Anchoring System (SAS)

#### 📄 `tools/system/entity_tracker.py` - Không có mô tả.
  - `Lớp` **EntityTracker**: 
    - `Method` __init__(): 
    - `Method` _ensure_map_exists(): 
    - `Method` load_map(): 
    - `Method` save_map(): 
    - `Method` track_path(): 

#### 📄 `tools/system/extract_v4.py` - Không có mô tả.
  - `Hàm` **censor_nsfw()**: 
  - `Hàm` **is_ai_prompt()**: 
  - `Hàm` **extract_from_dir()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/system/fetch_free_models.py` - Không có mô tả.
  - `Hàm` **fetch_free_models()**: 

#### 📄 `tools/system/fix_pytest_buffer.py` - Không có mô tả.
  - `Hàm` **fix_sys_stdout_buffer()**: Quét và sửa lỗi `sys.stdout = io.TextIOWrapper(...)` gây lỗi buffer detached cho Pytest.

#### 📄 `tools/system/garbage_collector.py` - Không có mô tả.
  - `Hàm` **clean_root_directory()**: 

#### 📄 `tools/system/gcli_delegate.py` - Không có mô tả.
  - `Hàm` **generate_docs_report()**: 

#### 📄 `tools/system/generate_flagship_roadmap.py` - Không có mô tả.
  - `Hàm` **generate_flagship_roadmap()**: 

#### 📄 `tools/system/git_manager.py` - Không có mô tả.
  - `Lớp` **GitManager**: Manages Git operations for state management and rollback.
    - `Method` run_command(): Runs a shell command and returns (success, stdout, stderr).
    - `Method` checkout_branch(): Checks out a git branch.
    - `Method` stash_changes(): Stashes current changes.
    - `Method` merge_branch(): Merges a branch into the current branch.
    - `Method` delete_branch(): Deletes a branch.
    - `Method` rollback(): Rolls back changes by switching to main and deleting the temp branch.
    - `Method` ensure_clean_state(): Pre-flight Hook: Ensures the repository is clean and on the target branch.

#### 📄 `tools/system/health_check.py` - Không có mô tả.
  - `Lớp` **SovereignHealthCheck**: 
    - `Method` __init__(): 
    - `Method` check_venv_lock(): Kiểm tra xem có tiến trình nào đang chiếm dụng .venv không.
    - `Method` verify_dependencies(): Kiểm tra xem các thư viện core có load được không.
    - `Method` check_hardware_resources(): Kiểm tra RAM và Disk.
    - `Method` run_all_checks(): 

#### 📄 `tools/system/intelligence_audit.py` - Không có mô tả.
  - `Hàm` **run_intelligence_audit()**: 

#### 📄 `tools/system/log_siphoner.py` - Không có mô tả.
  - `Hàm` **siphon_log()**: 

#### 📄 `tools/system/mass_generate_clinerules.py` - Không có mô tả.
  - `Hàm` **generate_domain_rules()**: 

#### 📄 `tools/system/pre_flight_check.py` - Không có mô tả.
  - `Lớp` **PreFlightCheck**: 🛩️ CỔNG KIỂM DUYỆT SỚM (Pre-flight Check)
    - `Method` __init__(): 
    - `Method` check_zero_byte_files(): Quét các file 0-byte (lỗi gãy stream).
    - `Method` check_circular_imports_static(): Quét lỗi import vòng lặp sơ bộ qua AST (không nạp module).
    - `Method` run_static_checks(): 

#### 📄 `tools/system/project_indexer.py` - Không có mô tả.
  - `Hàm` **analyze_dependencies()**: Phân tích các lệnh import để tìm sự phụ thuộc giữa các project.
  - `Hàm` **index_monorepo_v2()**: 

#### 📄 `tools/system/rag_ingest.py` - Không có mô tả.
  - `Hàm` **get_file_hash()**: Tính mã băm MD5 của một file.
  - `Hàm` **load_hash_cache()**: 
  - `Hàm` **save_hash_cache()**: 
  - `Hàm` **check_resource_guard()**: Kiểm tra xem hệ thống còn đủ RAM để chạy tác vụ nặng không.
  - `Hàm` **parse_pdf_to_text()**: Parse PDF sang text bằng pymupdf4llm hoặc fitz.
  - `Hàm` **main()**: mode: "system" (Code/Docs) hoặc "knowledge" (Sách/Papers)

#### 📄 `tools/system/rag_query.py` - Không có mô tả.
  - `Hàm` **query_rag_return_context()**: Hàm helper dùng cho các Agent để lấy context từ RAG.
  - `Hàm` **main()**: 

#### 📄 `tools/system/reading_task.py` - Không có mô tả.
  - `Lớp` **LibrarianAgent**: Agent phụ trách việc đọc sách, tóm tắt và cập nhật vào bộ nhớ dài hạn.
    - `Method` __init__(): 
    - `Method` _ai_handler(): 
    - `Method` _logic_handler(): 
    - `Method` read_random_wisdom(): Chọn ngẫu nhiên một mẩu tri thức từ Knowledge DB và học tập.

#### 📄 `tools/system/refactor_architecture.py` - Không có mô tả.
  - `Hàm` **move_if_exists()**: 
  - `Hàm` **delete_if_exists()**: 
  - `Hàm` **main()**: 

#### 📄 `tools/system/resource_monitor.py` - Không có mô tả.
  - `Hàm` **get_system_stats()**: Thu thập thông tin tài nguyên phần cứng.
  - `Hàm` **update_global_state()**: Cập nhật tài nguyên vào GLOBAL_STATE.md.

#### 📄 `tools/system/root_cleanup.py` - Không có mô tả.
  - `Hàm` **root_cleanup()**: 

#### 📄 `tools/system/run_simulator.py` - Không có mô tả.
  - `Hàm` **run()**: 

#### 📄 `tools/system/setup_project_foundation.py` - Không có mô tả.
  - `Hàm` **create_template()**: 
  - `Hàm` **generate_missing_files()**: 

#### 📄 `tools/system/smart_patcher.py` - Không có mô tả.
  - `Lớp` **SmartPatcher**: The Smart Patcher: A utility to automatically format and fix Python code.
    - `Method` __init__(): 
    - `Method` run_ruff(): 

#### 📄 `tools/system/sync_docs.py` - Không có mô tả.
  - `Hàm` **print_header()**: 
  - `Hàm` **analyze_directory()**: Quét thư mục gốc và trả về cấu trúc các sub-projects.
  - `Hàm` **main()**: 

#### 📄 `tools/system/system_cleaner.py` - Không có mô tả.
  - `Lớp` **TripleFilterCleaner**: Hệ thống thanh lọc 3 lớp (Triple-Filter Protocol):
    - `Method` level_1_migrate(): Di chuyển file/thư mục vào khu vực cách ly (Quarantine).
    - `Method` level_2_compress(): Nén các file trong quarantine đã cũ hơn X ngày.
    - `Method` level_3_terminate(): Xóa vĩnh viễn các bản nén cũ hơn X ngày.
  - `Hàm` **clean_zombie_files()**: Hàm quyét và dọn dẹp các file rác đã biết.

#### 📄 `tools/system/ultimate_doc_gen.py` - Không có mô tả.
  - `Hàm` **generate_docs_and_map_models()**: 

#### 📄 `tools/system/__init__.py` - Không có mô tả.

#### 📄 `tools/ui/dashboard_app.py` - Không có mô tả.
<!-- AUTO-GENERATED-SECTION-END -->
