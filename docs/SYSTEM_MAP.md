# 🗺️ BẢN ĐỒ HỆ THỐNG VÀ CHỨC NĂNG (SYSTEM MAP - AUTO GENERATED)

Đây là Bản đồ định vị toàn bộ cấu trúc dự án. Được tạo tự động thông qua quét AST (Abstract Syntax Tree). Hệ thống RAG dùng file này để định vị vị trí các hàm và chức năng.

---

## THƯ MỤC: `src/`

### 📄 File: `src/api_gateway.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CentralizedAPIGateway`: A centralized API Gateway with Circuit Breaker pattern implemented using SQLite
- `CircuitBreakerException`: Custom exception for circuit breaker related errors.
- `CircuitBreakerOpenException`: Custom exception when circuit breaker is open.

**Các Hàm (Functions/Methods):**
- `CentralizedAPIGateway.__init__()`
- `CentralizedAPIGateway._initialize_db()`: Initializes the SQLite database for circuit breaker state.
- `CentralizedAPIGateway._get_state()`: Retrieves the current state of the circuit breaker from the database.
- `CentralizedAPIGateway._set_state()`: Updates the state of the circuit breaker in the database.
- `CentralizedAPIGateway._record_failure()`: Records a failure and updates the failure count.
- `CentralizedAPIGateway._record_success()`: Records a success and resets the failure count if in HALF_OPEN state.
- `CentralizedAPIGateway.circuit_breaker()`: Decorator for applying circuit breaker logic to a function.

### 📄 File: `src/base_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `LLMAPIError`: Lỗi khi gọi API LLM (Rate Limit, Server Error...)
- `SchemaValidationError`: Lỗi khi LLM sinh JSON sai Schema (Ảo giác cấu trúc)
- `BlankHallucinationError`: Lỗi khi LLM trả về rỗng (Ảo giác trống rỗng)
- `BaseAgent`: Class cơ sở (Base Class) chung cho tất cả các Agent trong LangGraph_Agent_System.

**Các Hàm (Functions/Methods):**
- `BaseAgent.__init__()`
- `BaseAgent._call_llm_with_retry()`: Luồng gọi LLM khép kín với đầy đủ cơ chế Retry và dán nhãn Agent.
- `BaseAgent._extract_json_from_text()`: Tách JSON ra khỏi Markdown Code blocks an toàn.
- `BaseAgent._call_llm()`: Wrapper an toàn bọc Try-Except ngoài cùng cho hệ thống
- `BaseAgent._parse_json_response()`
- `BaseAgent._ai_handler()`
- `BaseAgent._logic_handler()`
- `BaseAgent.execute()`: Mô hình Cầu Dao Điện (Circuit Breaker Pattern).

### 📄 File: `src/database.py`
- **Mô tả File:** Database Management Module.

**Các Lớp (Classes):**
- `SystemDB`: Lớp quản lý Database SystemDB.

**Các Hàm (Functions/Methods):**
- `SystemDB.__init__()`
- `SystemDB._create_tables()`
- `SystemDB.log_trading_decision()`
- `SystemDB.log_backtest_report()`
- `SystemDB.log_project_update()`
- `SystemDB.log_paper_trade_balance()`
- `SystemDB.get_latest_decisions()`
- `SystemDB.get_latest_backtests()`
- `SystemDB.get_latest_updates()`
- `SystemDB.get_paper_trade_history()`
- `SystemDB.get_latest_paper_trade_balance()`
- `SystemDB.close()`

### 📄 File: `src/token_tracker.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `QuotaExceededError`
- `TokenTracker`

**Các Hàm (Functions/Methods):**
- `TokenTracker.__init__()`
- `TokenTracker._init_db()`
- `TokenTracker._calculate_cost()`: Tính toán chi phí dựa trên bảng giá (tham khảo).
- `TokenTracker.log_usage()`
- `TokenTracker.get_total_cost()`
- `track_llm_usage()`: Helper function để parse token usage từ response của LangChain/OpenAI

### 📄 File: `src/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `src/factory/config.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `Config`: Central configuration for AI Software Factory.

**Các Hàm (Functions/Methods):**
- `Config.initialize()`
- `Config.get_llm_credentials()`: Returns a list of available API credentials, prioritized.
- `create_fallback_chain()`: Creates a chain of LLMs with fallbacks. Bọc thêm Retry để chống Rate Limit 429/403.

### 📄 File: `src/factory/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `product_ba_node()`
- `overlord_graph()`
- `production_graph()`
- `debate_graph()`
- `primary_router()`: Lớp bảo vệ đầu tiên: Phân luồng ngay từ đầu để tránh nhét rác vào Overlord.
- `route_to_workflow()`: Routes to the appropriate sub-workflow based on the Overlord's decision.
- `post_prd_update()`: Update state after PRD generation.
- `build_meta_graph()`: Builds the main "meta-graph" that orchestrates all other workflows.
- `main()`

### 📄 File: `src/factory/state.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `FactoryState`: Trạng thái trung tâm cho Hệ thống AI Software Factory.
- `DebateState`: Trạng thái cho workflow "Hội đồng Phản biện AI".

### 📄 File: `src/factory/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `src/factory/nodes/coder.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `coder_node()`

### 📄 File: `src/factory/nodes/context_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `context_manager_node()`: Just-In-Time Context Manager.

### 📄 File: `src/factory/nodes/memory_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `truncate_text()`
- `memory_manager_node()`

### 📄 File: `src/factory/nodes/omni_overlord.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `OmniOverlord`

**Các Hàm (Functions/Methods):**
- `OmniOverlord.__init__()`
- `OmniOverlord.check_market_pulse()`: Đọc tin tức và phân tích xem có biến cố khẩn cấp (Emergency) không.

### 📄 File: `src/factory/nodes/qa_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `QAOutput`
- `QAAgent`: Tác nhân Hỏi-Đáp (QA Agent).

**Các Hàm (Functions/Methods):**
- `QAAgent.__init__()`
- `QAAgent._logic_handler()`
- `QAAgent._ai_handler()`
- `qa_node()`

### 📄 File: `src/factory/nodes/qa_reviewer.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `QAReviewer`: Sub-system chuyên trách thực hiện QA (Quality Assurance) cho các dự án.

**Các Hàm (Functions/Methods):**
- `QAReviewer.__init__()`: Khởi tạo các mô hình LLM với Load Balancing.
- `QAReviewer.evaluate()`: Chạy tuần tự các bước kiểm tra và trả về báo cáo cuối cùng.
- `extract_score()`: Trích xuất điểm số từ báo cáo.
- `qa_node()`

### 📄 File: `src/factory/nodes/router_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SemanticRouter`: Enterprise-Grade Semantic Router.

**Các Hàm (Functions/Methods):**
- `SemanticRouter.__init__()`
- `SemanticRouter.route_query()`
- `router_node()`

### 📄 File: `src/factory/nodes/triage_director.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `triage_issues_and_plan()`: Technical Director: Phân loại lỗi và lên kế hoạch sửa chữa.
- `triage_director_node()`

### 📄 File: `src/factory/workflows/daily_health_loop.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DailyHealthState`
- `ArchitectAgent`
- `WardenAgent`

**Các Hàm (Functions/Methods):**
- `ArchitectAgent.__init__()`
- `ArchitectAgent._ai_handler()`
- `ArchitectAgent._logic_handler()`
- `WardenAgent.__init__()`
- `WardenAgent._ai_handler()`
- `WardenAgent._logic_handler()`
- `nightwatch_node()`: Telemetry & Log Collection.
- `architect_node()`: Analysis & Proposition.
- `warden_node()`: Security & Risk Firewall.
- `mechanic_node()`: Implementation & Patching using AST.
- `test_pilot_node()`: Benchmark & State Management.
- `build_daily_health_graph()`

### 📄 File: `src/factory/workflows/software_production.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `router_node()`: Node định tuyến ban đầu dựa trên chế độ (mode).
- `route_start()`
- `check_qa_score()`: Điều kiện lặp (Conditional Edge).
- `build_factory_graph()`: Khởi tạo toàn bộ dây chuyền sản xuất phần mềm khép kín.

### 📄 File: `src/skills/search_knowledge_base.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `search_research_papers()`: Tìm kiếm kiến thức chuyên sâu từ Tàng Kinh Các (Knowledge Database).

### 📄 File: `src/skills/skill_manager.py`
- **Mô tả File:** Skill Manager Module.

**Các Lớp (Classes):**
- `SkillManager`: Trình quản lý Skill cốt lõi (Core Skill Manager).

**Các Hàm (Functions/Methods):**
- `SkillManager.__init__()`: Khởi tạo Skill Manager.
- `SkillManager.load_skill()`: Tải một kỹ năng cụ thể.

### 📄 File: `src/skills/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `src/skills/file_management/file_archiver_skill.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `src/tools/safe_codec_handler.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `src/utils/safe_patcher.py`
- **Mô tả File:** Không có mô tả.

## THƯ MỤC: `projects/`

### 📄 File: `projects/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/airdrop_guerrilla/src/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/airdrop_guerrilla/src/analysis/scoring.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AlphaAnalyzer`: AlphaAnalyzer: Module đánh giá tiềm năng Airdrop của các dự án Crypto.
- `AirdropScoringEngine`

**Các Hàm (Functions/Methods):**
- `AlphaAnalyzer.get_vc_weight()`: Xác định trọng số lớn nhất dựa trên danh sách các quỹ đầu tư của dự án.
- `AlphaAnalyzer.calculate_score()`: Tính toán điểm số tiềm năng (Alpha Score).
- `AlphaAnalyzer.analyze_projects()`: Phân tích và chấm điểm hàng loạt dự án.
- `AirdropScoringEngine.__init__()`
- `AirdropScoringEngine.calculate_wallet_metrics()`: Truy vấn SQLite và tính toán ma trận điểm cho từng ví.
- `AirdropScoringEngine.generate_markdown_report()`: Quét toàn bộ ví trong DB và tạo báo cáo Markdown.

### 📄 File: `projects/airdrop_guerrilla/src/automation/executor.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AirdropExecutor`: Stealth Engine: Tự động hóa trình duyệt (Browser Automation) dùng Playwright.

**Các Hàm (Functions/Methods):**
- `AirdropExecutor.__init__()`
- `AirdropExecutor.execute_wallet()`: Khởi chạy kịch bản farm cho một ví cụ thể.
- `AirdropExecutor._handle_faucet_demo()`: Logic mẫu cho việc qua mặt Faucet (Dán ví -> Giải Captcha -> Click).
- `AirdropExecutor._verify_login_status()`: Kiểm tra xem trang hiện tại đã được đăng nhập hay chưa (chờ tối đa 15s).
- `AirdropExecutor._twitter_interact()`: Logic tương tác tự động với Twitter (X) kèm Natural Browsing.
- `AirdropExecutor._discord_join()`: Logic tự động Join Discord.

### 📄 File: `projects/airdrop_guerrilla/src/automation/session_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SessionManager`: Quản lý phiên đăng nhập (Session Persistence) cho các nền tảng mạng xã hội.

**Các Hàm (Functions/Methods):**
- `SessionManager.apply_twitter_session()`: Nạp auth_token của X (Twitter) hoặc một mảng JSON Cookie vào Browser Context.
- `SessionManager.apply_discord_session()`: Nạp Token của Discord vào Local Storage thông qua add_init_script.

### 📄 File: `projects/airdrop_guerrilla/src/automation/stealth_behavior.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `StealthBrowser`: Giả lập trình duyệt ẩn danh chống detect bot của Cloudflare / Zealy / Galxe.

**Các Hàm (Functions/Methods):**
- `StealthBrowser.__init__()`
- `StealthBrowser.init_browser()`: Khởi tạo Persistent Browser Context để lưu Cookies và Extension.
- `StealthBrowser.stealth_page()`: Bơm stealth xịn vào page
- `StealthBrowser.random_delay()`: Tạo độ trễ ngẫu nhiên giống con người.
- `StealthBrowser.human_scroll()`: Giả lập thao tác cuộn trang của người dùng.

### 📄 File: `projects/airdrop_guerrilla/src/automation/wallet_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `WalletManager`: Trình quản lý Ví tự động (Wallet Manager).

**Các Hàm (Functions/Methods):**
- `WalletManager.__init__()`
- `WalletManager._load_db()`: Tải dữ liệu ví từ file JSON.
- `WalletManager._save_db()`: Lưu trữ dữ liệu ví xuống file JSON.
- `WalletManager.generate_static_user_agent()`: Sinh ra một User-Agent CỐ ĐỊNH dựa trên địa chỉ ví (Chống Sybil).
- `WalletManager.add_wallet()`: Thêm một ví mới, mã hóa Private Key, X auth_token, Discord token và gán User-Agent tĩnh.
- `WalletManager.get_decrypted_data()`: Lấy và giải mã Private Key và các Token mxh.

### 📄 File: `projects/airdrop_guerrilla/src/automation/zealy_bot.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ZealyBot`: Web Automation Bot chuyên làm task trên nền tảng Zealy.io

**Các Hàm (Functions/Methods):**
- `ZealyBot.__init__()`
- `ZealyBot.run_quests()`: Khởi động luồng chạy quest tự động

### 📄 File: `projects/airdrop_guerrilla/src/modes/full_auto_cli.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `send_telegram_message()`: Gửi thông báo qua Telegram
- `log_transaction_to_db()`: Ghi nhận lịch sử giao dịch vào SQLite Database để phục vụ chấm điểm sau này.
- `execute_random_action()`: Áp dụng thuật toán xúc xắc 80/20 chống bộ lọc Sybil (Với Jitter Amount).
- `main()`

### 📄 File: `projects/airdrop_guerrilla/src/modes/semi_auto_ui.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `alert_user_for_manual_action()`: Kích hoạt chuông báo (Beep) và dừng chương trình chờ người dùng can thiệp.
- `run_semi_auto_quests()`

### 📄 File: `projects/airdrop_guerrilla/src/networks/evm_base.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `EVMBase`: Lớp nền móng xử lý các tác vụ On-chain cho các mạng Layer 1/Layer 2 EVM.

**Các Hàm (Functions/Methods):**
- `EVMBase.__init__()`
- `EVMBase.init_fallback_connection()`: Duyệt danh sách RPC, tự động chuyển mạch nếu có node sập.
- `EVMBase.get_balance()`: Lấy số dư Native Token của ví.
- `EVMBase.get_gas_price()`: Lấy giá Gas hiện tại, cộng thêm tí xíu để giao dịch đi nhanh hơn.
- `EVMBase.check_balance_and_survival()`: Kiểm tra số dư tối thiểu, bắn Telegram báo động nếu cạn tiền.
- `EVMBase.send_native_token()`: Gửi Native Token (Ví dụ: ETH -> Soneium, MON -> Monad)
- `EVMBase.deploy_dummy_contract()`: Triển khai một Smart Contract rỗng (Dummy Contract).
- `EVMBase.random_delay()`

### 📄 File: `projects/airdrop_guerrilla/src/networks/inco.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `IncoNetwork`: Tích hợp Inco Network Testnet (Modular Confidential L1)

**Các Hàm (Functions/Methods):**
- `IncoNetwork.__init__()`

### 📄 File: `projects/airdrop_guerrilla/src/networks/monad.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `MonadNetwork`: Tích hợp Monad Testnet (Layer 1 EVM Parallel)

**Các Hàm (Functions/Methods):**
- `MonadNetwork.__init__()`

### 📄 File: `projects/airdrop_guerrilla/src/networks/soneium.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SoneiumNetwork`: Tích hợp Soneium Minato Testnet (Layer 2 Sony)

**Các Hàm (Functions/Methods):**
- `SoneiumNetwork.__init__()`

### 📄 File: `projects/airdrop_guerrilla/src/scrapers/defillama_funding_parser.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DefiLlamaParser`: Trình cào dữ liệu Live từ API của DefiLlama (raises endpoint).

**Các Hàm (Functions/Methods):**
- `DefiLlamaParser.__init__()`
- `DefiLlamaParser.fetch_live_raises()`: Gọi API thực tế từ DefiLlama và xử lý dữ liệu trả về.
- `DefiLlamaParser.run_live_pipeline()`: Khởi chạy chu trình Cào -> Phân tích -> Lưu trữ cho Phase 2.

### 📄 File: `projects/airdrop_guerrilla/src/utils/base_scraper.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `BaseScraper`: BaseScraper: Lớp cơ sở (Base Class) chuyên dụng cho việc cào dữ liệu (Web Scraping).

**Các Hàm (Functions/Methods):**
- `BaseScraper.__init__()`: Khởi tạo BaseScraper.
- `BaseScraper.get_scraped_items()`: Đọc danh sách các items (trang/URL/ID) đã cào thành công từ log file.
- `BaseScraper.add_scraped_item()`: Ghi nhận một item (trang/URL/ID) đã cào thành công vào file log.
- `BaseScraper.build_headers()`: Tạo HTTP Headers ngẫu nhiên với IP spoofing và User-Agent mới để vượt qua WAF (Web Application Firewall).
- `BaseScraper.sleep_random()`: Tạm dừng thực thi một khoảng thời gian ngẫu nhiên để giả lập thao tác của con người.
- `BaseScraper.fetch_url()`: Thực hiện HTTP GET Request một cách an toàn (State-less) với Exponential Backoff.

### 📄 File: `projects/airdrop_guerrilla/src/utils/migrate_to_sqlite.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `init_db()`
- `migrate_data()`

### 📄 File: `projects/airdrop_guerrilla/src/utils/notifier.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TelegramNotifier`: Module gửi thông báo (Alerting) qua Telegram Bot.

**Các Hàm (Functions/Methods):**
- `TelegramNotifier.__init__()`
- `TelegramNotifier.is_configured()`: Kiểm tra xem đã cấu hình đủ Token và Chat ID chưa.
- `TelegramNotifier.send_message()`: Gửi tin nhắn thô qua Telegram.
- `TelegramNotifier.send_alpha_alert()`: Format dữ liệu dự án thành một tin nhắn đẹp mắt và gửi đi.

### 📄 File: `projects/ai_trading_agent/dashboard.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_paper_trade_data()`
- `get_decisions()`

### 📄 File: `projects/ai_trading_agent/live_advisor.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_latest_market_data()`: Lấy dữ liệu đa tài sản từ SQLite. Kèm theo dữ liệu thô cho ML Prediction.
- `get_latest_news()`: Lấy tin tức mới nhất từ CoinTelegraph.
- `get_trading_lore()`: Đọc Ký ức giao dịch dài hạn để làm RAG Context
- `run_live_advisor()`

### 📄 File: `projects/ai_trading_agent/backtest/backtester.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `run_multi_asset_backtest()`: Backtest chiến lược Multi-Agent (Portfolio Allocation) so với Benchmark (HODL BTC).

### 📄 File: `projects/ai_trading_agent/backtest/offline_backtest.py`
- **Mô tả File:** Offline Backtest Mode

**Các Lớp (Classes):**
- `OfflineBacktester`: Offline backtest engine for AI Trading strategies

**Các Hàm (Functions/Methods):**
- `OfflineBacktester.__init__()`: Initialize backtester
- `OfflineBacktester.connect()`: Connect to database
- `OfflineBacktester.close()`: Close database connection
- `OfflineBacktester.__enter__()`
- `OfflineBacktester.__exit__()`
- `OfflineBacktester.get_historical_data()`: Get historical OHLCV data with indicators
- `OfflineBacktester.generate_signals()`: Generate trading signals based on indicators
- `OfflineBacktester.backtest()`: Run backtest simulation
- `OfflineBacktester.compare_strategies()`: Compare multiple strategies
- `OfflineBacktester.print_results()`: Print backtest results in a formatted way
- `main()`: Run offline backtest demo

### 📄 File: `projects/ai_trading_agent/backtest/__init__.py`
- **Mô tả File:** Backtest scripts

### 📄 File: `projects/ai_trading_agent/src/analytics.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `Analytics`: Module đo lường và ghi nhận hiệu suất của AI Trading Agent.

**Các Hàm (Functions/Methods):**
- `Analytics.__init__()`
- `Analytics._ensure_log_file()`
- `Analytics.log_execution_time()`: Ghi nhận thời gian thực thi của một task.
- `Analytics.log_api_cost()`: Ghi nhận chi phí sử dụng API (LLM, Data).
- `Analytics.log_trade_performance()`: Ghi nhận kết quả giao dịch.
- `Analytics.get_summary()`: Tính toán tổng hợp hiệu suất.

### 📄 File: `projects/ai_trading_agent/src/behavioral_warden.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `BehavioralWarden`: Cầu Dao Tâm Lý (The Behavioral Warden).

**Các Hàm (Functions/Methods):**
- `BehavioralWarden.__init__()`
- `BehavioralWarden.evaluate_position()`: Đánh giá trạng thái lệnh hiện tại (Long position).
- `BehavioralWarden.check_overtrading()`: Khóa tài khoản nếu thua lỗ 3 lệnh liên tiếp.

### 📄 File: `projects/ai_trading_agent/src/binance_executor.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `BinanceExecutor`: Thực thi lệnh giao dịch trên Binance Testnet dựa trên tỷ trọng phân bổ vốn từ AI.

**Các Hàm (Functions/Methods):**
- `BinanceExecutor.__init__()`
- `BinanceExecutor.get_current_portfolio()`: Lấy số dư hiện tại trên sàn.
- `BinanceExecutor.print_testnet_balance()`: Hàm dùng riêng cho Dashboard hiển thị số dư thực tế
- `BinanceExecutor._get_latest_atr()`: Lấy giá trị ATR_14 mới nhất của một coin từ database.
- `BinanceExecutor._calculate_smart_position_sizing()`: Tính toán Position Sizing thông minh dựa trên:
- `BinanceExecutor.send_telegram_alert()`: Gửi thông báo qua Telegram.
- `BinanceExecutor.execute_allocation()`: Thực thi lệnh để đưa danh mục về đúng tỷ trọng allocation_dict.

### 📄 File: `projects/ai_trading_agent/src/config.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `Config`: Quản lý cấu hình tập trung cho AI Trading Agent.

**Các Hàm (Functions/Methods):**
- `Config.validate()`: Kiểm tra các biến môi trường quan trọng.

### 📄 File: `projects/ai_trading_agent/src/data_fetcher.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_trade_tickers()`: Lấy danh sách các cặp giao dịch từ cấu hình.
- `fetch_fear_and_greed()`: Lấy chỉ số Fear & Greed Index từ API của Alternative.me.
- `fetch_crypto_data()`: Kéo dữ liệu OHLCV lịch sử từ Yahoo Finance và lưu vào SQLite.

### 📄 File: `projects/ai_trading_agent/src/fundamental_fetcher.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `FundamentalAnalyzer`: Phân tích cơ bản (Fundamental Analysis) dựa trên lý thuyết của Benjamin Graham

**Các Hàm (Functions/Methods):**
- `FundamentalAnalyzer.__init__()`
- `FundamentalAnalyzer.get_fundamental_data()`: Lấy các chỉ số tài chính cơ bản của một tài sản.
- `FundamentalAnalyzer.generate_fundamental_report()`: Tạo báo cáo Phân tích Cơ bản dạng chuỗi để nạp cho AI LangGraph.

### 📄 File: `projects/ai_trading_agent/src/funding_rate.py`
- **Mô tả File:** Funding Rate Tracker

**Các Lớp (Classes):**
- `FundingRateMonitor`: Monitor funding rates from major exchanges using Coinglass API

**Các Hàm (Functions/Methods):**
- `FundingRateMonitor.__init__()`: Initialize Funding Rate Monitor
- `FundingRateMonitor.get_funding_rates()`: Get current funding rates for a specific symbol
- `FundingRateMonitor.get_avg_funding_rate()`: Calculate average funding rate across exchanges
- `FundingRateMonitor.get_funding_rate_summary()`: Get formatted summary of funding rates for AI Agent
- `FundingRateMonitor.get_funding_rate_history()`: Get historical funding rates
- `main()`: Test Funding Rate Monitor

### 📄 File: `projects/ai_trading_agent/src/github_fetcher.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `fetch_github_trending_crypto()`: Lấy danh sách các repository liên quan đến crypto/blockchain 

### 📄 File: `projects/ai_trading_agent/src/langgraph_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TradingState`
- `MultiAgentTradingSystem`

**Các Hàm (Functions/Methods):**
- `MultiAgentTradingSystem.__init__()`
- `MultiAgentTradingSystem._invoke_with_retry()`
- `MultiAgentTradingSystem._technical_node()`
- `MultiAgentTradingSystem._sentiment_node()`
- `MultiAgentTradingSystem._fundamental_node()`
- `MultiAgentTradingSystem._risk_manager_node()`
- `MultiAgentTradingSystem._build_graph()`
- `MultiAgentTradingSystem.analyze_and_trade()`

### 📄 File: `projects/ai_trading_agent/src/live_advisor.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_latest_market_data()`: Lấy dữ liệu đa tài sản từ SQLite.
- `get_latest_news()`: Lấy tin tức mới nhất từ CoinTelegraph để phân tích Sentiment.
- `run_live_advisor()`: Hàm thực thi chính của Live Advisor.

### 📄 File: `projects/ai_trading_agent/src/mini_backtest.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_cached_prices()`
- `run_mini_backtest()`: Chạy mini-backtest trên dữ liệu `days` ngày qua với tỷ trọng `allocation_dict`.

### 📄 File: `projects/ai_trading_agent/src/ml_prediction.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `LeftBrainPredictor`

**Các Hàm (Functions/Methods):**
- `LeftBrainPredictor.__init__()`
- `LeftBrainPredictor.predict()`

### 📄 File: `projects/ai_trading_agent/src/news_scraper.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `fetch_cointelegraph_news()`: Cào tin tức mới nhất từ RSS Feed của CoinTelegraph.

### 📄 File: `projects/ai_trading_agent/src/portfolio_optimizer.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_historical_prices()`: Lấy dữ liệu giá đóng cửa lịch sử từ DB.
- `calculate_portfolio_performance()`: Tính toán lợi nhuận và rủi ro của danh mục.
- `negative_sharpe_ratio()`: Hàm mục tiêu để minimize (tìm Sharpe cao nhất).
- `optimize_portfolio()`: Thực hiện Mean-Variance Optimization để tìm tỷ trọng tối ưu.

### 📄 File: `projects/ai_trading_agent/src/self_reflection.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ReflectionAgent`

### 📄 File: `projects/ai_trading_agent/src/social_scraper.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `fetch_reddit_crypto_sentiment()`: Cào các hot posts từ r/CryptoCurrency để phân tích Social Sentiment.

### 📄 File: `projects/ai_trading_agent/src/technical_engine.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TechnicalEngine`: Động Cơ Giao Dịch (The Technical Engine) dựa trên Steven B. Achelis.

**Các Hàm (Functions/Methods):**
- `TechnicalEngine.__init__()`
- `TechnicalEngine.analyze_trend()`: Phân tích biểu đồ giá (df cần có cột 'close', 'high', 'low', 'volume')

### 📄 File: `projects/ai_trading_agent/src/whale_alert.py`
- **Mô tả File:** Whale Alert API Integration

**Các Lớp (Classes):**
- `WhaleAlertMonitor`: Monitor large crypto transactions using Whale Alert API

**Các Hàm (Functions/Methods):**
- `WhaleAlertMonitor.__init__()`: Initialize Whale Alert Monitor
- `WhaleAlertMonitor.get_transactions()`: Get recent large transactions
- `WhaleAlertMonitor.get_exchange_inflow_outflow()`: Calculate net flow to/from exchanges
- `WhaleAlertMonitor.get_whale_alert_summary()`: Get formatted summary of whale activity for AI Agent
- `main()`: Test Whale Alert Monitor

### 📄 File: `projects/ai_trading_agent/src/whale_tracker.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `WhaleTrackerAgent`

**Các Hàm (Functions/Methods):**
- `WhaleTrackerAgent.__init__()`
- `WhaleTrackerAgent._ai_handler()`
- `WhaleTrackerAgent._logic_handler()`
- `WhaleTrackerAgent.scrape_whale_data()`
- `WhaleTrackerAgent.execute()`

### 📄 File: `projects/ai_trading_agent/src/__init__.py`
- **Mô tả File:** Source code cho AI Trading Agent

### 📄 File: `projects/ai_trading_agent/tools/check_pnl.py`
- **Mô tả File:** Kiểm tra dữ liệu PnL trong database

### 📄 File: `projects/ai_trading_agent/tools/generate_performance_report.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_markdown_report()`: Tạo báo cáo hiệu suất từ dữ liệu Paper Trade trong Database.

### 📄 File: `projects/ai_trading_agent/tools/reset_pnl.py`
- **Mô tả File:** Xóa dữ liệu cũ trong Paper_Trade_Portfolio để reset PnL

### 📄 File: `projects/ai_trading_agent/tools/verify_db.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ai_trading_agent/tools/__init__.py`
- **Mô tả File:** Utility tools

### 📄 File: `projects/auto_affiliate_video/app.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/auto_affiliate_video/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/auto_affiliate_video/src/affiliate_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AffiliateManager`: Module quản lý việc lấy link Affiliate từ mạng AccessTrade.

**Các Hàm (Functions/Methods):**
- `AffiliateManager.__init__()`
- `AffiliateManager.generate_affiliate_link()`: Tạo link rút gọn Affiliate thông qua API của AccessTrade.

### 📄 File: `projects/auto_affiliate_video/src/auto_uploader.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AutoUploader`: Module tự động upload video lên mạng xã hội (TikTok/Shorts) sử dụng tiktok-uploader.

**Các Hàm (Functions/Methods):**
- `AutoUploader.__init__()`
- `AutoUploader.upload_to_tiktok()`

### 📄 File: `projects/auto_affiliate_video/src/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`: Hàm main điều phối quá trình tự động tạo video Affiliate.

### 📄 File: `projects/auto_affiliate_video/src/pexel_client.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `PexelClient`: A client for interacting with the Pexels API to find and download videos.

**Các Hàm (Functions/Methods):**
- `PexelClient.find_and_download_video()`: Searches for a video on Pexels and downloads the most relevant one.
- `PexelClient._get_best_quality_link()`: Selects the best quality video link that is under a certain size if needed.

### 📄 File: `projects/auto_affiliate_video/src/scheduler.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `job()`

### 📄 File: `projects/auto_affiliate_video/src/script_generator.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ScriptGenerator`

**Các Hàm (Functions/Methods):**
- `ScriptGenerator.__init__()`
- `ScriptGenerator._ai_handler()`
- `ScriptGenerator._logic_handler()`
- `ScriptGenerator.generate_short_video_script()`: Dùng OpenAI/Gemini để viết kịch bản video ngắn (dưới 60s) cho TikTok/Shorts.

### 📄 File: `projects/auto_affiliate_video/src/test_upload.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/auto_affiliate_video/src/tiktok_api_uploader.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TikTokApiUploader`: Tích hợp TikTok Content Posting API chính thức thay cho Playwright.

**Các Hàm (Functions/Methods):**
- `TikTokApiUploader.__init__()`
- `TikTokApiUploader.upload_to_tiktok()`

### 📄 File: `projects/auto_affiliate_video/src/tts_engine.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TTSEngine`: Động cơ chuyển đổi văn bản thành giọng nói (Text-to-Speech).

**Các Hàm (Functions/Methods):**
- `TTSEngine.__init__()`: Sử dụng Google TTS (gTTS) mặc định để tránh lỗi mạng của edge-tts.
- `TTSEngine.generate_audio()`: Sinh ra file mp3 từ văn bản và trả về đường dẫn cùng số ký tự.

### 📄 File: `projects/auto_affiliate_video/src/vector_memory.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `VectorMemory`: Quản lý Long-term Memory bằng Vector RAG để tránh tràn Context Window.

**Các Hàm (Functions/Methods):**
- `VectorMemory.__init__()`
- `VectorMemory.embed_and_store()`: Tạo embedding và lưu nội dung vào Vector DB.
- `VectorMemory.query_similar_context()`: Truy xuất N nội dung tương tự nhất dựa trên câu truy vấn.
- `VectorMemory.ingest_chronicles()`: Đọc và băm nhỏ file JARVIS_CHRONICLES.md để nạp vào trí nhớ.

### 📄 File: `projects/auto_affiliate_video/src/video_editor.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `VideoEditor`

**Các Hàm (Functions/Methods):**
- `VideoEditor.__init__()`
- `VideoEditor.create_short_video()`: Ghép Audio AI vào Video Background.

### 📄 File: `projects/auto_affiliate_video/src/video_telemetry.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `VideoTelemetry`

**Các Hàm (Functions/Methods):**
- `VideoTelemetry.__init__()`
- `VideoTelemetry.start_run()`
- `VideoTelemetry.log_event()`
- `VideoTelemetry._save_to_disk()`
- `measure_latency()`: Decorator to automatically measure the latency of a function and log it.

### 📄 File: `projects/auto_x_bot/app.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/auto_x_bot/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `log_to_db()`: Lưu lịch sử đăng Tweet vào database.
- `main()`

### 📄 File: `projects/auto_x_bot/src/content_generator.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ContentGenerator`

**Các Hàm (Functions/Methods):**
- `ContentGenerator.__init__()`
- `ContentGenerator.generate_crypto_tweet()`: Dựa vào danh sách tin tức, suy nghĩ ra 1 dòng Tweet duy nhất cực kỳ viral,

### 📄 File: `projects/auto_x_bot/src/x_api_client.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `XApiClient`: Client gọi Twitter API v2 để cày Social Point.

**Các Hàm (Functions/Methods):**
- `XApiClient.__init__()`
- `XApiClient.get_me()`: Lấy thông tin tài khoản đang login
- `XApiClient.post_tweet()`: Đăng 1 dòng Tweet mới
- `XApiClient.like_tweet()`: Like 1 tweet
- `XApiClient.retweet()`: Retweet (Repost)

### 📄 File: `projects/auto_x_bot/src/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/BepInEx/gemini_batch_translator.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `translate_batch()`
- `main()`

### 📄 File: `projects/ceo_agent/admin_simulator.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AdminSimulator`: Sinh ra các tình huống quản trị hệ thống (System Crisis) để CEO Agent giải quyết.

**Các Hàm (Functions/Methods):**
- `AdminSimulator.__init__()`
- `AdminSimulator.get_next_crisis()`: Sinh ra một cuộc khủng hoảng ngẫu nhiên.
- `AdminSimulator.evaluate_decision()`: Đánh giá quyết định của CEO.

### 📄 File: `projects/ceo_agent/autonomous_ceo.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CEOState`
- `AutonomousCEO`

**Các Hàm (Functions/Methods):**
- `list_projects()`: Liệt kê tất cả các project con hiện có.
- `read_document()`: Đọc nội dung một file tài liệu hoặc code (truyền đường dẫn tương đối từ root).
- `AutonomousCEO.__init__()`
- `AutonomousCEO.think_node()`
- `AutonomousCEO.act_node()`
- `AutonomousCEO.finish_node()`
- `AutonomousCEO.should_continue()`
- `AutonomousCEO._build_graph()`
- `AutonomousCEO.run_vi_hanh()`

### 📄 File: `projects/ceo_agent/ceo_mind.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CEOAgent`: Trí tuệ của CEO. Nhận báo cáo khủng hoảng từ AdminSimulator,

**Các Hàm (Functions/Methods):**
- `CEOAgent.__init__()`
- `CEOAgent.handle_crisis()`: Đưa ra quyết định dựa trên báo động hệ thống.
- `CEOAgent.reflect_and_learn()`: Đúc kết bài học từ thành công hoặc thất bại.

### 📄 File: `projects/ceo_agent/ceo_morning_routine.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CEODecision`
- `CEOUpgradePlan`
- `AdminFeedback`
- `AdminCriticAgent`
- `CEOAgent`
- `CEOUpgradeAgent`

**Các Hàm (Functions/Methods):**
- `AdminCriticAgent._logic_handler()`
- `AdminCriticAgent._ai_handler()`
- `CEOAgent._logic_handler()`
- `CEOAgent._ai_handler()`
- `CEOUpgradeAgent._logic_handler()`
- `CEOUpgradeAgent._ai_handler()`
- `wake_up_ceo()`

### 📄 File: `projects/ceo_agent/ceo_training_matrix.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CEOTrainingState`

**Các Hàm (Functions/Methods):**
- `list_files_in_directory()`: Liệt kê các file trong một thư mục cụ thể để CEO có thể khám phá dự án.
- `read_ceo_lore()`: Đọc file bộ nhớ dài hạn (Long-term Memory) của CEO để nhớ lại các bài học cũ.
- `summon_agent()`: Triệu hồi (Summon) một Agent khác (ví dụ QA_Auditor, Code_Reviewer, Trader) để nhờ phân tích/làm giúp một task. Trả về kết quả của Agent đó.
- `ceo_node()`
- `ceo_router()`
- `reflect_node()`
- `run_nightly_training()`

### 📄 File: `projects/chinese-character-recognition/chinese_character_recognition_bn.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DataIterator`

**Các Hàm (Functions/Methods):**
- `DataIterator.__init__()`
- `DataIterator.size()`
- `DataIterator.data_augmentation()`
- `DataIterator.input_pipeline()`
- `build_graph()`
- `train()`
- `validation()`
- `inference()`
- `main()`

### 📄 File: `projects/chinese-character-recognition/chinese_keras_modern.py`
- **Mô tả File:** Modern Keras implementation of Chinese Character Recognition with CNN and Batch Normalization.

**Các Hàm (Functions/Methods):**
- `build_model()`: Builds a modern CNN model equivalent to the original TF1 slim model.
- `create_dataset_pipeline()`: Uses modern tf.data API instead of old QueueRunners.
- `main()`

### 📄 File: `projects/disk_cleaner/deep_scanner.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DeepScanner`

**Các Hàm (Functions/Methods):**
- `format_size()`: Format bytes to human readable format
- `DeepScanner.__init__()`
- `DeepScanner.scan()`
- `DeepScanner.report_top_files()`
- `DeepScanner.report_top_dirs()`
- `clean_project_archives()`: Don dep cac file zip rac trong thu muc archives cua project

### 📄 File: `projects/disk_cleaner/run_cleaner.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DiskCleaner`

**Các Hàm (Functions/Methods):**
- `DiskCleaner.__init__()`
- `DiskCleaner._format_size()`: Định dạng byte sang MB/GB cho dễ nhìn
- `DiskCleaner._get_dir_size()`: Lấy kích thước một thư mục
- `DiskCleaner.clean_temp_folders()`: Xóa các thư mục Temp của Windows
- `DiskCleaner.clean_dev_caches()`: Gọi CLI để dọn cache của pip, uv, npm
- `DiskCleaner.clean_docker()`: Xóa Docker images/containers dangling
- `DiskCleaner.run()`

### 📄 File: `projects/ExtractDoanChat/extract_story.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ExtractDoanChat/GiaoDien_ChuyenDoi_Truyen.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/gemini_cli/main.py`
- **Mô tả File:** Main entry point for Gemini CLI.

**Các Hàm (Functions/Methods):**
- `stream_response()`: Stream Gemini API response to stdout.
- `main()`: Main entry point - parses arguments and runs async stream.

### 📄 File: `projects/gemini_cli/core/client.py`
- **Mô tả File:** Async HTTPX client for Gemini API communication.

**Các Lớp (Classes):**
- `GeminiError`: Base exception for Gemini API errors.
- `QuotaExceededError`: Raised when API quota is exhausted.
- `NetworkError`: Raised when network issues occur.
- `InvalidResponseError`: Raised when API returns invalid response.
- `GeminiClient`: Async HTTPX client for Gemini API with streaming support.

**Các Hàm (Functions/Methods):**
- `GeminiClient.__init__()`: Initialize Gemini client.
- `GeminiClient.__aenter__()`: Async context manager entry.
- `GeminiClient.__aexit__()`: Async context manager exit.
- `GeminiClient.stream_chat()`: Send a chat prompt and stream the response.
- `GeminiClient.chat()`: Send a chat prompt and return complete response (non-streaming).

### 📄 File: `projects/gemini_cli/core/config.py`
- **Mô tả File:** API Guard: Secure configuration management for Gemini API.

**Các Lớp (Classes):**
- `ConfigError`: Custom exception for configuration errors.
- `Config`: Secure configuration manager for Gemini API.

**Các Hàm (Functions/Methods):**
- `Config.__init__()`: Initialize configuration by loading environment variables.
- `Config._validate()`: Validate that all required environment variables are set.
- `Config.api_key()`: Get Gemini API key from environment.
- `Config.base_url()`: Get Gemini API base URL from environment.
- `Config.model()`: Get default model name.
- `Config.timeout()`: Get request timeout in seconds.
- `Config.get_headers()`: Get HTTP headers for API requests.
- `Config.__repr__()`: String representation (safe - hides API key).

### 📄 File: `projects/gemini_cli/core/__init__.py`
- **Mô tả File:** Core modules for Gemini CLI.

### 📄 File: `projects/gemini_cli/tests/__init__.py`
- **Mô tả File:** Unit tests for Gemini CLI.

### 📄 File: `projects/godot_translator/app.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/godot_translator/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/godot_translator/core/decompiler.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `GodotDecompiler`: Wrapper for external Godot decompile tools (like GDRE Tools CLI).

**Các Hàm (Functions/Methods):**
- `GodotDecompiler.__init__()`
- `GodotDecompiler.decompile_pck()`: Decompile a .pck file using GDRE Tools CLI.

### 📄 File: `projects/godot_translator/core/extractor.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `GodotExtractor`: Module to extract Japanese strings from Godot GDScript (.gd) and Scene (.tscn) files.

**Các Hàm (Functions/Methods):**
- `GodotExtractor.__init__()`
- `GodotExtractor.scan_files()`: Recursively scan for .gd and .tscn files.
- `GodotExtractor.extract_from_file()`: Extract Japanese strings from a single file based on its type.

### 📄 File: `projects/godot_translator/core/injector.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `GodotInjector`: Module to inject translated strings back into GDScript/TSCN files and maintain directory structure.

**Các Hàm (Functions/Methods):**
- `GodotInjector.__init__()`
- `GodotInjector.inject()`: Replace Japanese strings and save in the mirrored structure, while cleaning .remap/.gdc files.

### 📄 File: `projects/godot_translator/core/translator.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TranslationSchema`
- `GodotTranslator`: Agent specialized in translating Japanese game strings to Vietnamese.

**Các Hàm (Functions/Methods):**
- `GodotTranslator.__init__()`
- `GodotTranslator._logic_handler()`: Fallback Path: Return original texts (no translation) if AI fails.
- `GodotTranslator._ai_handler()`: Optimal Path: Use LLM to translate strings.
- `GodotTranslator.translate_batch()`: Execute translation with batching.

### 📄 File: `projects/History_Cline/analysis_user/mark_ai_prompts.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `mark_ai_prompts()`

### 📄 File: `projects/History_Cline/analysis_user/prompt_classifier.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `classify_prompts()`

### 📄 File: `projects/jarvis-rpg-assistant/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/jarvis-rpg-assistant/config/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/docs/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/docs/image/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/ai_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AIService`: Core AI Service - Trái tim của Jarvis.

**Các Hàm (Functions/Methods):**
- `AIService.__init__()`
- `AIService._get_cached_response()`: Kiểm tra xem câu hỏi này đã có trong cache chưa.
- `AIService._update_cache()`: Lưu câu trả lời vào cache.
- `AIService.generate_response()`: Hàm chính để tạo phản hồi (Có Cache + Đồng bộ Fallback Chain).
- `ask_jarvis()`: Hàm giao tiếp cơ bản với Jarvis.
- `evaluate_evolution()`: Đánh giá nhiệm vụ để tính XP/HP (RPG System).

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/ai_agent_fixed.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CircuitState`: Circuit Breaker States.
- `CircuitBreakerError`: Raised when circuit is OPEN.
- `CircuitBreaker`: Circuit Breaker Pattern Implementation.
- `SingleFlightLRUCache`: Thread-safe LRU Cache with Single-Flight Pattern.
- `AIService`: Core AI Service - Production-Ready with 3 Resilience Layers.

**Các Hàm (Functions/Methods):**
- `CircuitBreaker.__init__()`
- `CircuitBreaker.call()`: Execute function with circuit breaker protection.
- `CircuitBreaker._should_attempt_reset()`: Check if enough time has passed to try HALF_OPEN.
- `CircuitBreaker._get_remaining_cooldown()`: Get remaining cooldown time in seconds.
- `CircuitBreaker._transition_to_half_open()`: Transition from OPEN to HALF_OPEN.
- `CircuitBreaker._on_success()`: Handle successful request.
- `CircuitBreaker._on_failure()`: Handle failed request.
- `CircuitBreaker.get_status()`: Get current circuit breaker status.
- `SingleFlightLRUCache.__init__()`
- `SingleFlightLRUCache.get_or_fetch()`: Get from cache OR wait for in-flight request OR fetch new.
- `SingleFlightLRUCache._get_from_cache()`: Get from cache if exists and not expired.
- `SingleFlightLRUCache._fetch_and_cache()`: Fetch from API and store in cache.
- `SingleFlightLRUCache._remove_entry()`: Remove entry and update memory counter.
- `SingleFlightLRUCache.get_stats()`: Get cache statistics.
- `AIService.__init__()`
- `AIService._call_llm_api()`: Call Gemini API with retry logic.
- `AIService.generate_response()`: Main entry point: Generate AI response with full resilience.
- `AIService.get_system_status()`: Get comprehensive system health status.
- `ask_jarvis()`: Public API: Ask Jarvis a question (Facade Pattern).
- `evaluate_evolution()`: Evaluate tasks for XP/HP calculation (RPG System).
- `get_system_health()`: Get system health metrics.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/check_model.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/config.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/database.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DatabaseError`: Base exception for database related errors.
- `DatabaseManager`: Manages all database operations for the Jarvis application.

**Các Hàm (Functions/Methods):**
- `DatabaseManager.__init__()`: Initialize the database manager.
- `DatabaseManager._get_default_db_path()`: Xác định đường dẫn database một cách thông minh.
- `DatabaseManager._get_connection()`: Context manager for database connections with transaction lock.
- `DatabaseManager._execute()`: Execute a write operation (INSERT/UPDATE/DELETE).
- `DatabaseManager._fetch_one()`: Execute a query and return a single row.
- `DatabaseManager._fetch_all()`: Execute a query and return all rows.
- `DatabaseManager._init_db()`: Initialize the database schema.
- `DatabaseManager.get_user_profile()`
- `DatabaseManager._create_default_profile()`
- `DatabaseManager.update_user_stats()`
- `DatabaseManager.add_vocab()`
- `DatabaseManager.get_due_vocab()`
- `DatabaseManager.get_review_candidates()`
- `DatabaseManager.update_vocab_mastery()`
- `DatabaseManager._calculate_next_review_interval()`
- `get_database()`
- `init_db()`
- `get_connection()`
- `get_due_vocab()`
- `get_review_candidates()`
- `add_vocab()`
- `update_vocab_mastery()`
- `get_user_profile()`
- `update_user_stats()`

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/db_sync.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `sync_database_with_git()`: Sync database với git: pull trước khi commit để tránh conflict
- `commit_and_push_database()`: Commit và push database changes
- `safe_database_update()`: Wrapper function để safely update database với git sync

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/error_notifier.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ErrorNotifier`

**Các Hàm (Functions/Methods):**
- `ErrorNotifier.__init__()`
- `ErrorNotifier._get_admin_chat_ids()`
- `ErrorNotifier._get_bot()`
- `ErrorNotifier.send_error_alert()`
- `ErrorNotifier.notify_error_sync()`

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/google_services.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_creds()`
- `add_task()`
- `get_today_events()`
- `get_pending_tasks()`
- `get_completed_tasks_today()`
- `create_calendar_event()`

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/key_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `KeyExhaustedError`: Exception raised when all API keys are exhausted or rate-limited.
- `KeyManager`

**Các Hàm (Functions/Methods):**
- `KeyManager.__init__()`
- `KeyManager.get_next_key()`: Trả về key tiếp theo theo cơ chế Round-Robin, bỏ qua các key đang trong Cooldown.
- `KeyManager.mark_key_exhausted()`: Đánh dấu key này đã hết hạn mức (Quota Exceeded) hoặc gặp lỗi Rate Limit.
- `KeyManager.reset_exhausted_keys()`: Xóa toàn bộ trạng thái Cooldown. Dùng khi cần reset thủ công.
- `get_global_key_manager()`: Đọc keys từ biến môi trường và trả về KeyManager.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/migrate_data.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `manual_restore()`

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/notes.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_note()`: Ghi một ghi chú mới cùng với timestamp vào file journal.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/setup_calendar.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/telegram_bot.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `send_message()`

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/telegram_webhook.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TelegramWebhookBot`: Telegram bot với hỗ trợ webhook cho deployment trên Render/Heroku

**Các Hàm (Functions/Methods):**
- `TelegramWebhookBot.__init__()`
- `TelegramWebhookBot._setup_handlers()`: Setup command and message handlers
- `TelegramWebhookBot.handle_photo()`: Handle photo messages for calendar parsing
- `TelegramWebhookBot.start_command()`: Handle /start command
- `TelegramWebhookBot.help_command()`: Handle /help command
- `TelegramWebhookBot.handle_message()`: Handle regular text messages
- `TelegramWebhookBot.run_polling()`: Run bot with polling (for local development)
- `TelegramWebhookBot.setup_webhook()`: Setup webhook for production deployment
- `TelegramWebhookBot.run_webhook()`: Run bot with webhook (for production)
- `TelegramWebhookBot.run()`: Run bot with appropriate mode based on configuration
- `main()`: Main entry point

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/vision_parser.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `encode_image()`
- `parse_schedule_image()`: Sử dụng GCLI API Key (chuẩn OpenAI Vision) để đọc ảnh lịch và trả về danh sách event JSON.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/weather_service.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_weather_report()`: Lấy thông tin thời tiết hiện tại tại Đồng Nai.

### 📄 File: `projects/jarvis-rpg-assistant/jarvis_core/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/src/admin_panel.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `JarvisAdminApp`

**Các Hàm (Functions/Methods):**
- `JarvisAdminApp.__init__()`
- `JarvisAdminApp.setup_profile_tab()`
- `JarvisAdminApp.load_profile()`
- `JarvisAdminApp.save_profile()`
- `JarvisAdminApp.setup_vocab_tab()`
- `JarvisAdminApp.load_vocab_list()`
- `JarvisAdminApp.filter_vocab()`
- `JarvisAdminApp.on_select_vocab()`
- `JarvisAdminApp.clear_form()`
- `JarvisAdminApp.add_vocab()`
- `JarvisAdminApp.update_vocab()`
- `JarvisAdminApp.delete_vocab()`

### 📄 File: `projects/jarvis-rpg-assistant/src/auto_learn.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `auto_hunt_vocab()`

### 📄 File: `projects/jarvis-rpg-assistant/src/bot_daily.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_vietnamese_weekday()`
- `main()`

### 📄 File: `projects/jarvis-rpg-assistant/src/bot_evolve.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/jarvis-rpg-assistant/src/bot_teacher.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`: Main teaching function.

### 📄 File: `projects/jarvis-rpg-assistant/src/fix_db.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `fix_system()`

### 📄 File: `projects/jarvis-rpg-assistant/src/jarvis_launcher.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `JarvisLauncher`

**Các Hàm (Functions/Methods):**
- `JarvisLauncher.__init__()`
- `JarvisLauncher.setup_ui()`: Thiết lập giao diện tích hợp với main.py.
- `JarvisLauncher.log()`: Ghi thông tin vào cửa sổ Log.
- `JarvisLauncher.launch_main_cmd()`: Chạy main.py thông qua subprocess với tham số.
- `JarvisLauncher.run_process()`: Thực thi tiến trình và bắt log realtime.

### 📄 File: `projects/jarvis-rpg-assistant/src/note.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`: Điểm vào CLI để ghi chú nhanh.

### 📄 File: `projects/jarvis-rpg-assistant/src/note_search.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `read_journal()`: Đọc toàn bộ nội dung file ghi chú.
- `search_in_notes()`: Gửi nội dung ghi chú + câu hỏi cho AI xử lý.
- `main()`

### 📄 File: `projects/jarvis-rpg-assistant/src/test_vision_calendar.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_next_weekday()`: Hàm tính toán ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất.
- `test_pipeline()`

### 📄 File: `projects/jarvis-rpg-assistant/src/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/tests/conftest.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `pytest_configure()`

### 📄 File: `projects/jarvis-rpg-assistant/tests/test_ai_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TestAIService`

**Các Hàm (Functions/Methods):**
- `TestAIService.mock_key_manager()`: Mock key manager
- `TestAIService.ai_service()`: Create AI service with mocked dependencies
- `TestAIService.test_init_ai_service()`: Test AI service initialization
- `TestAIService.test_cache_functionality()`: Test caching mechanism
- `TestAIService.test_generate_content_with_retry()`: Test generate content with retry mechanism
- `TestAIService.test_key_manager_integration()`: Test integration with key manager
- `TestAIService.test_model_priority_list()`: Test that model priority is defined
- `TestAIService.test_cache_ttl_configuration()`: Test cache TTL configuration

### 📄 File: `projects/jarvis-rpg-assistant/tests/test_core.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TestDatabaseManager`
- `TestKeyManager`

**Các Hàm (Functions/Methods):**
- `temp_db()`: Create a temporary database for testing
- `key_manager()`: Create a key manager instance for testing
- `TestDatabaseManager.test_init_creates_tables()`: Test that database initialization creates all required tables
- `TestDatabaseManager.test_get_user_profile()`: Test getting user profile
- `TestDatabaseManager.test_update_user_stats()`: Test updating user stats
- `TestDatabaseManager.test_add_vocab()`: Test adding vocabulary
- `TestDatabaseManager.test_get_due_vocab()`: Test getting due vocabulary
- `TestDatabaseManager.test_get_review_candidates_new()`: Test getting new vocabulary for review
- `TestDatabaseManager.test_get_review_candidates_review()`: Test getting vocabulary for review
- `TestDatabaseManager.test_update_vocab_mastery_correct()`: Test updating vocabulary when remembered correctly
- `TestDatabaseManager.test_update_vocab_mastery_incorrect()`: Test updating vocabulary when not remembered
- `TestDatabaseManager.test_database_close()`: Test database cleanup
- `TestKeyManager.test_init_key_manager()`: Test key manager initialization
- `TestKeyManager.test_get_next_key()`: Test getting next available key
- `TestKeyManager.test_get_next_key_rotation()`: Test key rotation
- `TestKeyManager.test_mark_key_exhausted()`: Test marking key as exhausted
- `TestKeyManager.test_reset_exhausted_keys()`: Test resetting exhausted keys

### 📄 File: `projects/jarvis-rpg-assistant/tests/test_new_features.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TestConfigModule`
- `TestKeyManager`

**Các Hàm (Functions/Methods):**
- `TestConfigModule.test_config_module_imports()`: Test that config module can be imported
- `TestConfigModule.test_config_paths_exist()`: Test that config defines required paths
- `TestKeyManager.test_key_manager_basic()`: Test key manager basic functionality
- `TestKeyManager.test_key_rotation()`: Test key rotation mechanism

### 📄 File: `projects/jarvis-rpg-assistant/tools/admin_gui.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `JarvisAdminApp`

**Các Hàm (Functions/Methods):**
- `JarvisAdminApp.__init__()`
- `JarvisAdminApp.run_query()`
- `JarvisAdminApp.load_data()`
- `JarvisAdminApp.on_select()`
- `JarvisAdminApp.add_word()`
- `JarvisAdminApp.update_word()`
- `JarvisAdminApp.delete_word()`
- `JarvisAdminApp.hack_time()`

### 📄 File: `projects/jarvis-rpg-assistant/tools/bot_sync.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ScheduleSyncApp`

**Các Hàm (Functions/Methods):**
- `ScheduleSyncApp.__init__()`
- `ScheduleSyncApp.log()`
- `ScheduleSyncApp.start_web_sync_thread()`
- `ScheduleSyncApp.start_img_sync_thread()`
- `ScheduleSyncApp.handle_drop()`
- `ScheduleSyncApp.run_web_sync()`
- `ScheduleSyncApp.run_process_images()`
- `ScheduleSyncApp.process_with_ai()`
- `ScheduleSyncApp.push_to_google_calendar()`

### 📄 File: `projects/jarvis-rpg-assistant/tools/calendar_ui.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_next_weekday()`: Tính ngày tháng (YYYY-MM-DD) cho ngày trong tuần gần nhất.
- `generate_google_calendar_csv()`: Tạo nội dung CSV chuẩn Google Calendar.

### 📄 File: `projects/jarvis-rpg-assistant/tools/cheat_db.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `hack_time()`

### 📄 File: `projects/jarvis-rpg-assistant/tools/dashboard.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_db()`

### 📄 File: `projects/jarvis-rpg-assistant/tools/public_readiness_check.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `run_command()`

### 📄 File: `projects/jarvis-rpg-assistant/tools/test.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/jarvis-rpg-assistant/tools/test_key.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `load_keys_from_file()`: Đọc tất cả API Key từ file, loại bỏ khoảng trắng và dòng trống.
- `quick_verify_api()`: Hàm kiểm tra nhanh 1 key

### 📄 File: `projects/jarvis-rpg-assistant/tools/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/knowledge_base_agent/src/ingest.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `bootstrap_environment()`: Khởi tạo toàn bộ hạ tầng thư mục lưu trữ nếu chưa tồn tại.
- `collect_pending_assets()`: Quét và thu thập danh sách các tập tin PDF đang chờ xử lý.
- `parse_pdf_to_markdown_and_chunk()`: Trích xuất PDF bằng PyMuPDF4LLM, băm theo Markdown và Recursive.
- `safe_initialize_embeddings()`: Khởi tạo mô hình Embedding cục bộ. Tích hợp cơ chế Fallback.
- `commit_to_vectorstore()`: Lưu trữ các vector dữ liệu vào hệ quản trị cơ sở dữ liệu vector ChromaDB.
- `relocate_processed_assets()`: Di chuyển các tệp tin gốc đã xử lý thành công sang phân vùng lưu trữ lâu dài.
- `run_pipeline()`: Hàm điều phối (Orchestrator) thực thi toàn bộ chu trình nạp dữ liệu.

### 📄 File: `projects/knowledge_base_agent/src/rag_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `RAGAgent`: Agent RAG (Retrieval-Augmented Generation) chuyên dùng để query kiến thức từ Ebook.

**Các Hàm (Functions/Methods):**
- `RAGAgent.__init__()`
- `RAGAgent.query()`: Nhận câu hỏi, tìm kiếm relevant chunks và đưa cho LLM tổng hợp câu trả lời.
- `RAGAgent._ai_handler()`
- `RAGAgent._logic_handler()`

### 📄 File: `projects/LocalRelay/local_relay.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `websocket_endpoint()`: Endpoint dành cho con App AI Studio trên trình duyệt kết nối vào
- `handle_cline_request()`: Endpoint hứng request HTTP từ Cline gửi qua

### 📄 File: `projects/local_proxy_server/main.py`
- **Mô tả File:** Local Proxy Server - Main Entry Point

**Các Hàm (Functions/Methods):**
- `lifespan()`: Application lifespan manager.
- `main()`: Main entry point for the Local Proxy Server.

### 📄 File: `projects/local_proxy_server/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/local_proxy_server/core/adapter.py`
- **Mô tả File:** Adapter Module for Payload Conversion

**Các Hàm (Functions/Methods):**
- `_trim_messages_if_needed()`: Tiêu chuẩn 1: Zero Token Leakage.
- `to_gemini_payload()`: Convert OpenAI-compatible chat completion payload to Gemini API format.
- `to_openai_stream()`:     Convert Gemini streaming response chunk to OpenAI SSE format.
- `to_openai_final_chunk()`: Create a final chunk to signal stream completion.
- `_extract_text_from_gemini_obj()`: Extract output text from a single parsed Gemini stream object,
- `stream_gemini_to_openai()`: Transform Gemini streaming response to OpenAI SSE format.
- `_extract_next_json_object()`: Find the first complete top-level JSON object in buffer using brace-depth.

### 📄 File: `projects/local_proxy_server/core/config.py`
- **Mô tả File:** Core Configuration Module for Local Proxy Server

**Các Lớp (Classes):**
- `Settings`: Application settings and configuration.

**Các Hàm (Functions/Methods):**
- `Settings.__init__()`: Initialize settings and validate required environment variables.
- `Settings.map_model()`: Map requested model name or label to actual Google API model string.
- `Settings.get_gemini_stream_url()`: Build the Gemini streaming endpoint URL for a specific (model, key) pair.
- `get_settings()`: Get the global settings instance.

### 📄 File: `projects/local_proxy_server/core/rotation_manager.py`
- **Mô tả File:** Rotation Manager Module - Smart State Manager for API Key & Model Rotation.

**Các Lớp (Classes):**
- `RotationManager`: Smart dispatcher: rotates API Keys per-model and falls back to alternative

**Các Hàm (Functions/Methods):**
- `RotationManager.__init__()`
- `RotationManager._is_exhausted()`
- `RotationManager.get_valid_credential()`: Find a valid (Key, Model) pair that still has quota.
- `RotationManager.mark_exhausted()`: Mark a (key, model) pair as quota-exhausted so it is skipped in
- `RotationManager.reset_quota_pool()`: Clear all exhausted records. Call at UTC midnight or manually.
- `RotationManager._maybe_auto_reset()`: Auto-reset pool when the calendar day changes (UTC).
- `RotationManager.get_stats()`: Return current rotation statistics for monitoring.
- `get_rotation_manager()`: Get the global RotationManager singleton.

### 📄 File: `projects/local_proxy_server/core/router.py`
- **Mô tả File:** Router Module for FastAPI Endpoints

**Các Hàm (Functions/Methods):**
- `stream_fallback_generator()`: Fallback generator using Groq or OpenRouter when Gemini is fully exhausted.
- `stream_generator()`: Async generator that streams responses from Gemini and converts to OpenAI format.
- `chat_completions()`: OpenAI-compatible chat completions endpoint with streaming support.
- `health_check()`: Health check endpoint.
- `_init_billing_db()`
- `process_billing()`: Tiêu chuẩn 3: Crypto Payment Config Ready & Anti-Replay
- `root()`: Root endpoint with service information.

### 📄 File: `projects/local_proxy_server/tests/test_proxy.py`
- **Mô tả File:** Lightweight Unit Test for RotationManager logic.

**Các Hàm (Functions/Methods):**
- `make_manager()`: Build a RotationManager with a fake Settings containing N keys.
- `test_basic_dispatch()`: Test 1: Basic credential dispatch returns a valid pair.
- `test_mark_exhausted_skip()`: Test 2: Marked pair is skipped on next dispatch.
- `test_fallback_to_alternative_model()`: Test 3: When all keys of requested model die, fallback to alternative model.
- `test_full_exhaustion()`: Test 4: All pairs exhausted -> RuntimeError.
- `test_stats()`: Test 5: get_stats returns accurate counts.

### 📄 File: `projects/local_proxy_server/tests/test_proxy_server.py`
- **Mô tả File:** Unit Tests for Local Proxy Server

**Các Hàm (Functions/Methods):**
- `test_adapter_to_gemini_payload()`: Test conversion from OpenAI to Gemini payload format.
- `test_adapter_to_openai_stream()`: Test conversion from Gemini chunk to OpenAI SSE format.
- `test_api_key_rotation_logic()`: Test the configuration loading and rotation mechanism of API Keys.
- `test_health_endpoint()`: Test the health check endpoint.
- `test_root_endpoint()`: Test the root endpoint.
- `test_chat_completions_stream()`: Test the chat completions endpoint with streaming.
- `run_tests()`: Run all tests.

### 📄 File: `projects/minecraft_eden_simulation/src/simulation_runner.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SimulationRunner`

**Các Hàm (Functions/Methods):**
- `SimulationRunner.__init__()`
- `SimulationRunner.clear_screen()`
- `SimulationRunner.draw_tui()`
- `SimulationRunner._log()`
- `SimulationRunner.execute_action()`
- `SimulationRunner.step()`
- `SimulationRunner.run()`

### 📄 File: `projects/minecraft_eden_simulation/src/telemetry.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `EdenTelemetry`

**Các Hàm (Functions/Methods):**
- `EdenTelemetry.__init__()`
- `EdenTelemetry.record_tick()`
- `EdenTelemetry.record_action()`
- `EdenTelemetry.record_damage()`
- `EdenTelemetry.record_reflection()`
- `EdenTelemetry.record_api_call()`
- `EdenTelemetry.finalize_report()`

### 📄 File: `projects/minecraft_eden_simulation/src/agents/eden_player.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `PlayerActionSchema`
- `EdenPlayer`

**Các Hàm (Functions/Methods):**
- `EdenPlayer.__init__()`
- `EdenPlayer._ai_handler()`: Luồng suy nghĩ của Agent
- `EdenPlayer._logic_handler()`: Fallback Sinh Tồn nếu AI sập: Tự động đi hái lượm

### 📄 File: `projects/minecraft_eden_simulation/src/agents/memory_module.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `MemoryModule`: Hệ thống nén ký ức và Vector Store cho Project Eden

**Các Hàm (Functions/Methods):**
- `MemoryModule.__init__()`
- `MemoryModule.add_lesson()`: Đánh giá Importance Score của bài học bằng LLM và thêm vào bộ nhớ ngắn hạn.
- `MemoryModule.should_compress()`: Kích hoạt Deep Reflection khi tổng điểm quan trọng vượt ngưỡng 100.
- `MemoryModule.compress_memory()`: Nén các bài học ngắn hạn thành 1-2 nguyên lý cốt lõi và lưu vào ChromaDB.
- `MemoryModule._garbage_collection()`: Xóa các ký ức không quan trọng theo Ebbinghaus Forgetting Curve.
- `MemoryModule.retrieve_memory()`: Truy xuất ký ức sử dụng thuật toán HyDE (Hypothetical Document Embeddings).

### 📄 File: `projects/minecraft_eden_simulation/src/world_engine/grid_map.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `Tile`
- `GridMap`

**Các Hàm (Functions/Methods):**
- `Tile.__init__()`
- `Tile.__repr__()`
- `GridMap.__init__()`
- `GridMap._generate_world()`: Sinh thế giới đơn giản với tỉ lệ xuất hiện nhất định.
- `GridMap.get_tile()`: Lấy thông tin của một ô tại tọa độ x, y.
- `GridMap.set_tile()`: Cập nhật một ô (vd: khi AI đập cây, ô thành đất trống).
- `GridMap.update()`: Cập nhật thế giới mỗi tick. Trả về lượng sát thương Player phải chịu.
- `GridMap.render()`: Trả về chuỗi hiển thị bản đồ.

### 📄 File: `projects/minecraft_eden_simulation/src/world_engine/tech_tree.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TechTree`: Cây công nghệ định nghĩa các công thức Crafting (Chế tạo) cho AI.

**Các Hàm (Functions/Methods):**
- `TechTree.__init__()`
- `TechTree.craft()`: Kiểm tra xem AI có đủ nguyên liệu để chế tạo target_item không.

### 📄 File: `projects/minhchung_pdf_generator/generate_minhchung_pdf.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_caption_from_filename()`
- `create_pdf()`

### 📄 File: `projects/mnist-handwritten-digit-recognition/mnist_keras_modern.py`
- **Mô tả File:** Modern Keras implementation of MNIST handwritten digit recognition.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/mnist-handwritten-digit-recognition/mnist_softmax.py`
- **Mô tả File:** A very simple MNIST classifier.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/qa_chaos_agent/src/encyclopedia_writer.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `write_to_encyclopedia()`: Ghi lỗi mới vào Bách khoa toàn thư để các Agent RAG có thể học được.

### 📄 File: `projects/qa_chaos_agent/src/fuzzer_engine.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `FuzzerEngine`

**Các Hàm (Functions/Methods):**
- `FuzzerEngine.__init__()`
- `FuzzerEngine.extract_python_files_from_map()`: Đọc SYSTEM_MAP.md để lấy ra các file Python có thể Fuzz.
- `FuzzerEngine.dummy_fuzz_import()`: Thử import module động để kiểm tra lỗi cú pháp, lỗi thiếu import (ModuleNotFoundError),
- `FuzzerEngine.process_crash()`
- `FuzzerEngine.run_nightly_fuzz()`: Chạy Fuzzing ngẫu nhiên 2 file mỗi đêm để nhẹ server.

### 📄 File: `projects/qa_chaos_agent/src/llm_autopsy.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `LLMAutopsy`

**Các Hàm (Functions/Methods):**
- `LLMAutopsy.__init__()`
- `LLMAutopsy._ai_handler()`
- `LLMAutopsy._logic_handler()`
- `LLMAutopsy.analyze_crash()`: Gửi Traceback cho LLM phân tích nguyên nhân và cách sửa.

### 📄 File: `projects/qa_functional_agent/src/functional_tester.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `FunctionalTester`

**Các Hàm (Functions/Methods):**
- `FunctionalTester.__init__()`
- `FunctionalTester._ai_handler()`
- `FunctionalTester._logic_handler()`
- `FunctionalTester.ai_assert()`: Sử dụng LLM để chấm điểm kết quả (Functional Assertion).
- `FunctionalTester.test_streamlit_ui()`: Dùng Playwright test Streamlit UI (End-to-End)
- `FunctionalTester.test_script_generator()`: Unit/Functional test cho ScriptGenerator của Auto Affiliate Video

### 📄 File: `projects/real_estate_prediction/app.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `home()`: Render trang chủ với các dropdown động lấy từ data.
- `show_map()`: Render bản đồ Heatmap giá nhà theo Quận/Huyện.
- `predict()`: API endpoint xử lý dự báo giá nhà.

### 📄 File: `projects/real_estate_prediction/generate_ppt_report.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_dashboard_ppt()`

### 📄 File: `projects/real_estate_prediction/generate_word_report.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_report()`

### 📄 File: `projects/real_estate_prediction/train_model.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `projects/real_execution_simulator/agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SimulatorState`

**Các Hàm (Functions/Methods):**
- `agent_node()`
- `should_continue()`
- `reflect_node()`
- `run_simulator()`

### 📄 File: `projects/real_execution_simulator/buggy_script.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `calculate_square_root()`

### 📄 File: `projects/real_execution_simulator/main.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/real_execution_simulator/tools.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `execute_terminal_command()`: Thực thi một lệnh terminal trên hệ điều hành Windows và trả về kết quả.
- `read_file_content()`: Đọc nội dung của một file code.
- `rewrite_entire_file()`: Ghi đè toàn bộ nội dung mới vào một file. (Có cơ chế Backup tự động)
- `list_markdown_files()`: Quét một thư mục và trả về danh sách các file Markdown (.md).
- `restore_backup()`: Phục hồi file từ bản backup (.bak). Dùng khi test file sau khi sửa bị lỗi nặng hơn.

### 📄 File: `projects/roundtable_debate/architecture_meeting.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ArchMeetingState`
- `ArchitectureRoundtable`

**Các Hàm (Functions/Methods):**
- `ArchitectureRoundtable.__init__()`
- `ArchitectureRoundtable.architect_node()`
- `ArchitectureRoundtable.qa_node()`
- `ArchitectureRoundtable.ceo_node()`
- `ArchitectureRoundtable.should_continue()`
- `ArchitectureRoundtable._build_graph()`
- `ArchitectureRoundtable.start_meeting()`

### 📄 File: `projects/roundtable_debate/autonomous_auditor.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AuditorState`
- `AutonomousAuditor`

**Các Hàm (Functions/Methods):**
- `AutonomousAuditor.__init__()`
- `AutonomousAuditor.get_file_content()`
- `AutonomousAuditor.file_reader_node()`
- `AutonomousAuditor.coder_node()`
- `AutonomousAuditor.qa_node()`
- `AutonomousAuditor.techlead_node()`
- `AutonomousAuditor.master_architect_node()`
- `AutonomousAuditor.should_continue_debate()`
- `AutonomousAuditor.has_more_files()`
- `AutonomousAuditor._build_graph()`
- `AutonomousAuditor.run_audit()`

### 📄 File: `projects/roundtable_debate/code_review_council.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ReviewState`
- `CodeReviewCouncil`

**Các Hàm (Functions/Methods):**
- `CodeReviewCouncil.__init__()`
- `CodeReviewCouncil.coder_node()`
- `CodeReviewCouncil.qa_node()`
- `CodeReviewCouncil.techlead_node()`
- `CodeReviewCouncil.should_continue()`
- `CodeReviewCouncil._build_graph()`
- `CodeReviewCouncil.run_review()`

### 📄 File: `projects/roundtable_debate/deployment_council.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DeployState`
- `DeploymentCouncil`

**Các Hàm (Functions/Methods):**
- `DeploymentCouncil.__init__()`
- `DeploymentCouncil.get_git_status()`: Lấy thông tin git status và những file bị thay đổi (giả lập hoặc chạy thật).
- `DeploymentCouncil.techlead_node()`
- `DeploymentCouncil.devops_node()`
- `DeploymentCouncil.ceo_node()`
- `DeploymentCouncil._build_graph()`
- `DeploymentCouncil.run_deployment()`

### 📄 File: `projects/roundtable_debate/grand_council.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `CouncilState`
- `GrandCouncil`

**Các Hàm (Functions/Methods):**
- `GrandCouncil.__init__()`
- `GrandCouncil.trading_node()`
- `GrandCouncil.growth_node()`
- `GrandCouncil.sysadmin_node()`
- `GrandCouncil.ceo_node()`
- `GrandCouncil._build_graph()`
- `GrandCouncil.hold_meeting()`

### 📄 File: `projects/roundtable_debate/meeting_room.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `MeetingState`
- `AIRoundtable`

**Các Hàm (Functions/Methods):**
- `AIRoundtable.__init__()`
- `AIRoundtable.trader_node()`
- `AIRoundtable.skeptic_node()`
- `AIRoundtable.ceo_node()`
- `AIRoundtable.should_continue()`
- `AIRoundtable._build_graph()`
- `AIRoundtable.start_meeting()`

### 📄 File: `projects/sillytavern_world_card_generator/run_nsfw_writer.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`: Main function to run the NSFW writing workflow.

### 📄 File: `projects/sillytavern_world_card_generator/src/auto_translator.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AutoTranslatorAgent`

**Các Hàm (Functions/Methods):**
- `AutoTranslatorAgent.__init__()`
- `AutoTranslatorAgent.translate_text()`
- `translate_card()`
- `batch_translate()`

### 📄 File: `projects/sillytavern_world_card_generator/src/extract_png_cards.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/sillytavern_world_card_generator/src/ingest_cards.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `extract_card_text()`: Trích xuất các trường nội dung quan trọng từ thẻ JSON của SillyTavern.
- `ingest_cards()`

### 📄 File: `projects/sillytavern_world_card_generator/src/lore_extractor.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `read_json_file()`
- `build_llm_prompt()`
- `call_llm_api()`
- `write_markdown_file()`
- `get_output_filename()`
- `has_chinese_chars()`
- `get_processed_files()`
- `log_processed_file()`
- `agent_process_card()`
- `main()`

### 📄 File: `projects/sillytavern_world_card_generator/src/merge_regex.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/sillytavern_world_card_generator/src/merge_regex_all.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/sillytavern_world_card_generator/src/world_card_generator.py`
- **Mô tả File:** World Card Generator (Orchestrator):

**Các Lớp (Classes):**
- `WorldCardGenerator`

**Các Hàm (Functions/Methods):**
- `WorldCardGenerator.__init__()`
- `WorldCardGenerator.generate()`: Chạy quy trình sinh dữ liệu bằng AI thực.
- `WorldCardGenerator.export_to_json()`: Xuất file JSON.

### 📄 File: `projects/sillytavern_world_card_generator/src/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/sillytavern_world_card_generator/src/agents/base_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `BaseGeminiAgent`: Class cơ sở chứa logic gọi API thông qua ChatOpenAI (tương thích proxy của OpenAI).

**Các Hàm (Functions/Methods):**
- `BaseGeminiAgent.__init__()`
- `BaseGeminiAgent._call_gemini()`: Gửi prompt đến LLM thông qua ChatOpenAI và trả về chuỗi kết quả.
- `BaseGeminiAgent._parse_json_response()`: Cố gắng parse chuỗi trả về thành JSON một cách an toàn.

### 📄 File: `projects/sillytavern_world_card_generator/src/agents/coder_agent.py`
- **Mô tả File:** Coder Agent:

**Các Lớp (Classes):**
- `CoderAgent`

**Các Hàm (Functions/Methods):**
- `CoderAgent.__init__()`
- `CoderAgent.generate_extensions()`: Sinh ra các file extension dựa trên tính năng được yêu cầu.
- `generate_code_mock()`

### 📄 File: `projects/sillytavern_world_card_generator/src/agents/lore_master_agent.py`
- **Mô tả File:** Lore Master Agent:

**Các Lớp (Classes):**
- `LoreMasterAgent`

**Các Hàm (Functions/Methods):**
- `LoreMasterAgent.__init__()`
- `LoreMasterAgent.generate_lorebook()`: Tạo danh sách Lorebook entries bằng Gemini.
- `generate_lore_mock()`

### 📄 File: `projects/sillytavern_world_card_generator/src/agents/rag_card_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `RAGCardAgent`: Agent RAG chuyên dùng để tìm kiếm thẻ mẫu từ ChromaDB, giúp AI học lỏm văn phong.

**Các Hàm (Functions/Methods):**
- `RAGCardAgent.__init__()`
- `RAGCardAgent.get_reference_context()`: Lấy context từ các thẻ cũ dựa trên theme và style.

### 📄 File: `projects/sillytavern_world_card_generator/src/agents/storyteller_agent.py`
- **Mô tả File:** Storyteller Agent:

**Các Lớp (Classes):**
- `StorytellerAgent`

**Các Hàm (Functions/Methods):**
- `StorytellerAgent.__init__()`
- `StorytellerAgent.generate_narrative_context()`: Tạo System Prompt và First Message từ ý tưởng người dùng bằng Gemini.

### 📄 File: `projects/sillytavern_world_card_generator/src/models/world_card_v3.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `LoreBookExtension`: Phần mở rộng của 1 entry trong Lorebook
- `LoreBookEntry`: Đại diện cho 1 Mục (Entry) trong Lorebook
- `CharacterBook`: Bọc danh sách các entries
- `CharacterExtensions`: Phần Extensions bọc regex và các tính năng phụ của character
- `CharacterData`: Phần Data chứa chi tiết Character/World Card
- `WorldCardV3`: Cấu trúc bao bọc lớp ngoài cùng của file JSON chuẩn V3.
- `UserIdeaInput`: Input từ người dùng để AI sinh ra thẻ.

**Các Hàm (Functions/Methods):**
- `WorldCardV3.to_json()`: Xuất ra chuỗi JSON đẹp mắt.

### 📄 File: `projects/sillytavern_world_card_generator/tests/test_basic.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `test_basic_initialization()`: Basic test to ensure project initializes correctly.

### 📄 File: `projects/sillytavern_world_card_generator/tools/non_ai_lorebook_extractor.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `LorebookExtractor`

**Các Hàm (Functions/Methods):**
- `LorebookExtractor.__init__()`
- `LorebookExtractor._extract_characters_regex()`
- `LorebookExtractor.extract_context_around_name()`: Extracts context around mentions of a character.
- `LorebookExtractor.analyze_traits()`: Analyzes context text against keyword dictionaries.
- `LorebookExtractor.create_sillytavern_entry()`: Formats the extracted traits into a SillyTavern JSON entry.
- `LorebookExtractor.process_file()`

### 📄 File: `projects/sillytavern_world_card_generator/tools/streamlit_lorebook_app.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `OllamaLorebookExtractor`

**Các Hàm (Functions/Methods):**
- `OllamaLorebookExtractor.__init__()`
- `OllamaLorebookExtractor.get_available_models()`: Fetches available models from the Ollama instance.
- `OllamaLorebookExtractor.extract_with_ai()`: Sends text to Ollama and expects a JSON response formatted for SillyTavern.

### 📄 File: `projects/sillytavern_world_card_generator/ui/app.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/trading_rpg_simulator/dungeon_master.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DungeonMaster`: Hệ thống sinh kịch bản ngẫu nhiên đóng vai trò là "Thị trường" (Môi trường game).

**Các Hàm (Functions/Methods):**
- `DungeonMaster.__init__()`
- `DungeonMaster.generate_next_turn()`: Sinh ra dữ liệu cho 1 lượt chơi (1 ngày).
- `DungeonMaster.resolve_combat()`: Tính toán PnL dựa trên quyết định của TraderHero và biến động thực tế.

### 📄 File: `projects/trading_rpg_simulator/trader_hero.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TraderHero`: AI Agent đóng vai trò Trader. Nó sẽ nhận dữ liệu môi trường từ Dungeon Master,

**Các Hàm (Functions/Methods):**
- `TraderHero.__init__()`
- `TraderHero.make_decision()`: Đưa ra quyết định dựa trên tin tức hiện tại và ký ức.
- `TraderHero.reflect_and_learn()`: Đúc kết kinh nghiệm sau mỗi trận đấu (ngày).

### 📄 File: `projects/universal_web_scraper/main.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `download_html()`: Tải toàn bộ mã nguồn HTML từ một URL và lưu vào file cục bộ.
- `main()`

### 📄 File: `projects/universal_web_scraper/src/alonhadat_parser.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `BaseScraper`
- `AlonhadatParser`

**Các Hàm (Functions/Methods):**
- `BaseScraper.__init__()`
- `BaseScraper.get_scraped_pages()`: Đọc danh sách các trang đã cào thành công từ log file.
- `BaseScraper.add_scraped_page()`: Ghi nhận một trang đã cào thành công.
- `BaseScraper.clean_old_data()`: Xóa dữ liệu rác (Area < 10, District chứa tên đường) khỏi file gộp.
- `BaseScraper.incremental_merge()`: Gộp dữ liệu mới vào output_csv nội bộ và raw_data.csv của mô hình.
- `AlonhadatParser.__init__()`
- `AlonhadatParser.build_headers()`
- `AlonhadatParser.scrape_page()`
- `AlonhadatParser.run_guerrilla()`: Chiến thuật Cào Du Kích: Trộn trang, cào từng batch nhỏ rồi nghỉ.

### 📄 File: `projects/universal_web_scraper/src/alonhadat_playwright.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `AlonhadatPlaywrightScraper`

**Các Hàm (Functions/Methods):**
- `AlonhadatPlaywrightScraper.__init__()`
- `AlonhadatPlaywrightScraper.parse_page_data()`
- `AlonhadatPlaywrightScraper.run_scraper()`
- `AlonhadatPlaywrightScraper.save_and_merge()`

### 📄 File: `projects/universal_web_scraper/src/base_scraper.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `PlaywrightStealth`
- `BaseConfig`

**Các Hàm (Functions/Methods):**
- `PlaywrightStealth.random_scroll()`
- `PlaywrightStealth.human_pause()`

### 📄 File: `projects/universal_web_scraper/src/batdongsan_playwright.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `BatDongSanPlaywrightScraper`

**Các Hàm (Functions/Methods):**
- `BatDongSanPlaywrightScraper.__init__()`
- `BatDongSanPlaywrightScraper.get_scraped_pages()`
- `BatDongSanPlaywrightScraper.add_scraped_page()`
- `BatDongSanPlaywrightScraper.parse_page_data()`
- `BatDongSanPlaywrightScraper.run_guerrilla()`
- `BatDongSanPlaywrightScraper.save_and_merge()`

### 📄 File: `projects/universal_web_scraper/src/cleaner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `clean_and_rank_data()`: Làm sạch dữ liệu Hacker News, tính Engagement_Score và lưu kết quả.

### 📄 File: `projects/universal_web_scraper/src/parser.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `parse_hacker_news()`: Parse Hacker News HTML and extract title, href, score, and comments.

### 📄 File: `projects/_template/config/settings.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/_template/src/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/_template/tests/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/apply_headings.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `apply_styles()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/create_colab_notebook.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_colab_notebook()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/final_deep_clean.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `delete_element()`
- `replace_text_in_p()`
- `regex_replace_text_in_p()`
- `clean_common()`
- `clean_ml()`
- `clean_dl()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/fix_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `delete_paragraph()`
- `fix_ml_doc()`
- `fix_dl_doc()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/merge_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `delete_paragraphs_after()`
- `copy_paragraph()`
- `process_ml()`
- `process_dl()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/micro_clean.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `regex_replace_text_in_p()`
- `replace_text_in_p()`
- `fix_ml()`
- `fix_dl()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/split_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `delete_paragraph()`
- `split_doc()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/super_clean_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `delete_element()`
- `clean_tables()`
- `clean_toc_and_indexes()`
- `replace_text_in_p()`
- `clean_dl_doc()`
- `clean_ml_doc()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/app.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/create_colab_notebook.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_colab_notebook()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/backtest_engine.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/data_ingestion.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/feature_engineering.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/model_architecture.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `TimeAttentionLayer`
- `DataFusionModel`

**Các Hàm (Functions/Methods):**
- `TimeAttentionLayer.__init__()`
- `TimeAttentionLayer.build()`
- `TimeAttentionLayer.call()`
- `TimeAttentionLayer.get_config()`
- `DataFusionModel.__init__()`
- `DataFusionModel.build_model()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/nlp_processor.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/upgrade_train.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `plot_training_history()`
- `plot_predictions()`
- `main()`

### 📄 File: `projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy/Stock_Forecasting_Project/04_Source_Code/Tien_Machine_Learning/05_Tien_Streamlit_App.py`
- **Mô tả File:** Không có mô tả.

## THƯ MỤC: `core/`

### 📄 File: `core/drm_validator.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `check_license_validity()`: Core DRM Logic.
- `init_drm()`

### 📄 File: `core/file_handler.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `core/fundamental_fetcher.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `core/skill_manager.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `core/obfuscated/drm_validator.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `core/obfuscated/pyarmor_runtime_000000/__init__.py`
- **Mô tả File:** Không có mô tả.

## THƯ MỤC: `scheduler/`

### 📄 File: `scheduler/drip_feed_worker.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `load_stats()`
- `save_stats()`
- `run_drip_feed()`

### 📄 File: `scheduler/main_scheduler.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `load_state()`
- `save_state()`
- `update_job_state()`
- `run_with_retry_and_log()`: Run a subprocess with capture_output, retry on failure, and return (success_bool, error_snippet)
- `send_telegram_alert()`
- `run_queued()`: Decorator để đẩy job vào hàng đợi của ThreadPoolExecutor
- `scrape_job()`
- `daily_trading_job()`
- `airdrop_job()`
- `omni_overlord_watchdog()`
- `check_missed_jobs()`: Kiểm tra xem khi khởi động máy có bị lỡ job nào của ngày hôm nay không.

### 📄 File: `scheduler/test_catchup.py`
- **Mô tả File:** Không có mô tả.

## THƯ MỤC: `tools/`

### 📄 File: `tools/build_all_reqs.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/compile_drm.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/convert_csv_to_data.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `convert_csv_to_data()`: Chuyển đổi file CSV đã dịch trở lại thành định dạng locate.data gốc.

### 📄 File: `tools/convert_data_to_csv.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `convert_data_to_csv()`: Chuyển đổi file locate.data (file CSV ẩn của Godot) thành định dạng chuẩn key,en,vi,ja

### 📄 File: `tools/extract_cookies.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `extract_tiktok_cookies()`: Script trích xuất Cookies tự động từ profile Microsoft Edge của Admin.

### 📄 File: `tools/extract_godot_csv.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_smart_key()`: Tạo key thông minh từ nội dung: T_<hash_6_char>_<5_từ_đầu>
- `is_garbage_string()`: Kiểm tra xem chuỗi có phải là rác không.
- `extract_strings_to_csv()`

### 📄 File: `tools/generate_flagship_roadmap.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_flagship_roadmap()`

### 📄 File: `tools/manage.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `print_help()`
- `main()`

### 📄 File: `tools/market_research_scraper.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `scrape_reddit()`
- `main()`

### 📄 File: `tools/package_beta.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_beta_zip()`

### 📄 File: `tools/resource_scout.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/run_notebooks.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `run_notebook()`

### 📄 File: `tools/run_pipeline_data.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/run_pipeline_lstm.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/run_pipeline_ml.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/run_qa_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `qa_agent_audit()`

### 📄 File: `tools/run_tester_agent.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `test_code()`

### 📄 File: `tools/scrape_opgg.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `scrape_valorant()`

### 📄 File: `tools/setup_project_foundation.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_template()`
- `generate_missing_files()`

### 📄 File: `tools/system_cleaner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_core_sig()`
- `clean_docs()`
- `clean_comfy()`

### 📄 File: `tools/telegram_bot_controller.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `start()`: Gửi menu điều khiển khi user gõ /start.
- `handle_message()`
- `main()`: Start the bot.

### 📄 File: `tools/test_youtube_api.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `test_youtube_api()`

### 📄 File: `tools/translate_csv.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `translate_csv()`: Đọc file CSV, dịch cột 'ja' (hoặc 'en') sang 'vi' nếu cột 'vi' đang trống.

### 📄 File: `tools/worldcard_converter.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/comfy/clothoff_cli.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `to_base64()`
- `select_file()`
- `main()`

### 📄 File: `tools/comfy/clothoff_gui.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `process_clothoff()`

### 📄 File: `tools/comfy/clothoff_hf_cli.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `select_file()`
- `main()`

### 📄 File: `tools/comfy/create_clothoff_image.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `to_base64()`
- `generate_clothoff()`

### 📄 File: `tools/edtech/create_10_diem_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_bang_tra_cuu_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_bmtt_cheatsheet_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `init_document()`: Khởi tạo file Word, thiết lập tiêu đề chính.
- `add_affine_section()`: Module tạo nội dung rút gọn cho Câu 1: Mã Affine.
- `add_hill_section()`: Module tạo nội dung rút gọn cho Câu 3: Mã Hill 3x3.
- `add_playfair_rsa_theory()`: Module tạo nội dung rút gọn Playfair, RSA và Lý thuyết.
- `generate_exam_doc()`: Hàm tổng phối hợp các module để ráp thành file hoàn chỉnh.
- `run_unit_test()`: Test nhanh xem file có thực sự được tạo ra và lưu thành công không.

### 📄 File: `tools/edtech/create_bmtt_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_full_10_cau_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_giai_de_cuong_qtkdcks.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_heading()`
- `add_paragraph()`
- `main()`

### 📄 File: `tools/edtech/create_giai_de_cuong_qtkdcks_rut_gon.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_heading()`
- `add_paragraph()`
- `main()`

### 📄 File: `tools/edtech/create_giai_de_cuong_qtkdcks_suy_luan.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_heading()`
- `add_paragraph()`
- `main()`

### 📄 File: `tools/edtech/create_mindset_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_qtkdcks_audio_gtts.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/create_qtkdcks_audio_local.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/create_qtkdcks_audio_simple.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `amain()`

### 📄 File: `tools/edtech/create_qtkdcks_cheatsheet.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_qtkdcks_custom_audio.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/create_qtkdcks_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/create_qtkdcks_theory_audio.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `amain()`

### 📄 File: `tools/edtech/create_qtkdcks_theory_audio_story.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/qtkdcks_decuong_quiz.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DecuongQuizApp`

**Các Hàm (Functions/Methods):**
- `DecuongQuizApp.__init__()`
- `DecuongQuizApp.build_ui()`
- `DecuongQuizApp.handle_enter()`
- `DecuongQuizApp.load_question()`
- `DecuongQuizApp.check_answer()`
- `DecuongQuizApp.next_question()`

### 📄 File: `tools/edtech/qtkdcks_formula_reflex.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `FormulaQuizApp`

**Các Hàm (Functions/Methods):**
- `FormulaQuizApp.__init__()`
- `FormulaQuizApp.build_ui()`
- `FormulaQuizApp.handle_enter()`
- `FormulaQuizApp.load_question()`
- `FormulaQuizApp.check_answer()`
- `FormulaQuizApp.next_question()`

### 📄 File: `tools/edtech/qtkdcks_quiz_app.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `QuizApp`

**Các Hàm (Functions/Methods):**
- `QuizApp.__init__()`
- `QuizApp.build_ui()`
- `QuizApp.handle_enter()`
- `QuizApp.load_question()`
- `QuizApp.check_answer()`
- `QuizApp.next_question()`

### 📄 File: `tools/edtech/scan_qtkdcks_pdfs.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/edtech/verify_bmtt_math.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `mod_inverse()`
- `affine_decrypt()`
- `hill_encrypt()`
- `rsa_encrypt()`

### 📄 File: `tools/edtech/archive/create_10_diem_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_bang_tra_cuu_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_bmtt_cheatsheet_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `init_document()`: Khởi tạo file Word, thiết lập tiêu đề chính.
- `add_affine_section()`: Module tạo nội dung rút gọn cho Câu 1: Mã Affine.
- `add_hill_section()`: Module tạo nội dung rút gọn cho Câu 3: Mã Hill 3x3.
- `add_playfair_rsa_theory()`: Module tạo nội dung rút gọn Playfair, RSA và Lý thuyết.
- `generate_exam_doc()`: Hàm tổng phối hợp các module để ráp thành file hoàn chỉnh.
- `run_unit_test()`: Test nhanh xem file có thực sự được tạo ra và lưu thành công không.

### 📄 File: `tools/edtech/archive/create_bmtt_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_full_10_cau_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_giai_de_cuong_qtkdcks.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_heading()`
- `add_paragraph()`
- `main()`

### 📄 File: `tools/edtech/archive/create_giai_de_cuong_qtkdcks_rut_gon.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_heading()`
- `add_paragraph()`
- `main()`

### 📄 File: `tools/edtech/archive/create_giai_de_cuong_qtkdcks_suy_luan.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `add_heading()`
- `add_paragraph()`
- `main()`

### 📄 File: `tools/edtech/archive/create_mindset_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_audio_gtts.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_audio_local.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_audio_simple.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `amain()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_cheatsheet.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_custom_audio.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_docx.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_docx()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_theory_audio.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `amain()`

### 📄 File: `tools/edtech/archive/create_qtkdcks_theory_audio_story.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_audio()`

### 📄 File: `tools/edtech/archive/qtkdcks_decuong_quiz.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `DecuongQuizApp`

**Các Hàm (Functions/Methods):**
- `DecuongQuizApp.__init__()`
- `DecuongQuizApp.build_ui()`
- `DecuongQuizApp.handle_enter()`
- `DecuongQuizApp.load_question()`
- `DecuongQuizApp.check_answer()`
- `DecuongQuizApp.next_question()`

### 📄 File: `tools/edtech/archive/qtkdcks_formula_reflex.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `FormulaQuizApp`

**Các Hàm (Functions/Methods):**
- `FormulaQuizApp.__init__()`
- `FormulaQuizApp.build_ui()`
- `FormulaQuizApp.handle_enter()`
- `FormulaQuizApp.load_question()`
- `FormulaQuizApp.check_answer()`
- `FormulaQuizApp.next_question()`

### 📄 File: `tools/edtech/archive/qtkdcks_quiz_app.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `QuizApp`

**Các Hàm (Functions/Methods):**
- `QuizApp.__init__()`
- `QuizApp.build_ui()`
- `QuizApp.handle_enter()`
- `QuizApp.load_question()`
- `QuizApp.check_answer()`
- `QuizApp.next_question()`

### 📄 File: `tools/edtech/archive/scan_qtkdcks_pdfs.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/edtech/archive/verify_bmtt_math.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `mod_inverse()`
- `affine_decrypt()`
- `hill_encrypt()`
- `rsa_encrypt()`

### 📄 File: `tools/lorebook/create_ultimate_preset_v3.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `tools/lorebook/delete_empty_docs.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `delete_empty_docs()`

### 📄 File: `tools/lorebook/find_empty_docs.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `find_empty_files()`

### 📄 File: `tools/lorebook/merge_and_shorten_lorebook.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_category()`

### 📄 File: `tools/lorebook/merge_physiology_lorebook.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/misc/organize_girl_folder.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_common_prefix()`
- `clean_common_prefix()`
- `main()`

### 📄 File: `tools/misc/run_ocr_hentai.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `extract_text()`

### 📄 File: `tools/rag_code/auto_rag_query.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `tools/rag_code/ingest_code.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_all_code_files()`: Scans the directory tree and returns a list of file paths to be ingested.
- `ingest_codebase()`: Main function to orchestrate the codebase ingestion process.

### 📄 File: `tools/rag_code/inspect_docs.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `inspect_docs()`

### 📄 File: `tools/rag_code/query_code_db.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `query_codebase()`: Initializes the RAG components and enters a loop to accept user queries.

### 📄 File: `tools/rag_code/test_code_ingestion.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `run_automated_tests()`: Runs a predefined set of queries against the codebase vector database

### 📄 File: `tools/scanners/architecture_auditor.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `audit_workspace()`

### 📄 File: `tools/scanners/architecture_scanner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `analyze_file()`
- `main()`

### 📄 File: `tools/scanners/freelance_scanner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `scan_freelance_jobs()`: Simulates scanning Upwork and vLance for AI automation jobs.

### 📄 File: `tools/scanners/internship_scanner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `scan_internships()`: Simulates scanning job boards (LinkedIn, TopDev, ITviec) for AI Intern positions.

### 📄 File: `tools/scanners/project_stat_analyzer.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `analyze_project()`

### 📄 File: `tools/system/api_mapper.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `extract_env_keys()`: Đọc file .env và trả về danh sách các biến được định nghĩa (không chứa giá trị).
- `scan_file_for_env_usage()`: Dùng AST để quét file Python xem có gọi os.getenv('KEY') hay không.
- `main()`

### 📄 File: `tools/system/apply_updates.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_category()`

### 📄 File: `tools/system/ast_patcher.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `ASTPatcher`: Modifies Python code safely using Abstract Syntax Trees (AST).

**Các Hàm (Functions/Methods):**
- `ASTPatcher.read_ast()`
- `ASTPatcher.write_ast()`
- `ASTPatcher.apply_patch()`: Applies a specific NodeTransformer to a file and saves it.

### 📄 File: `tools/system/auto_mapper.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_system_map()`

### 📄 File: `tools/system/batch_qa_runner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_all_projects()`
- `main()`

### 📄 File: `tools/system/benchmark_apis.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `build_request_args()`
- `test_speed()`
- `send_single_req()`
- `test_rate_limit()`
- `main()`

### 📄 File: `tools/system/build_indexer.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `IndexerAgent`

**Các Hàm (Functions/Methods):**
- `IndexerAgent.__init__()`
- `IndexerAgent._ai_handler()`
- `IndexerAgent._logic_handler()`
- `main()`

### 📄 File: `tools/system/cleanup_docs.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `cleanup_docs()`

### 📄 File: `tools/system/db_migrator.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `migrate_database()`

### 📄 File: `tools/system/delegate_audit.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/system/doc_debate_runner.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SkepticAgent`
- `DefenderAgent`
- `SynthesizerAgent`

**Các Hàm (Functions/Methods):**
- `SkepticAgent.__init__()`
- `SkepticAgent._ai_handler()`
- `SkepticAgent._logic_handler()`
- `DefenderAgent.__init__()`
- `DefenderAgent._ai_handler()`
- `DefenderAgent._logic_handler()`
- `SynthesizerAgent.__init__()`
- `SynthesizerAgent._ai_handler()`
- `SynthesizerAgent._logic_handler()`
- `main()`

### 📄 File: `tools/system/garbage_collector.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `clean_root_directory()`

### 📄 File: `tools/system/gcli_delegate.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_docs_report()`

### 📄 File: `tools/system/generate_flagship_roadmap.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_flagship_roadmap()`

### 📄 File: `tools/system/git_manager.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `GitManager`: Manages Git operations for state management and rollback.

**Các Hàm (Functions/Methods):**
- `GitManager.run_command()`: Runs a shell command and returns (success, stdout, stderr).
- `GitManager.checkout_branch()`: Checks out a git branch.
- `GitManager.stash_changes()`: Stashes current changes.
- `GitManager.merge_branch()`: Merges a branch into the current branch.
- `GitManager.delete_branch()`: Deletes a branch.
- `GitManager.rollback()`: Rolls back changes by switching to main and deleting the temp branch.
- `GitManager.ensure_clean_state()`: Pre-flight Hook: Ensures the repository is clean and on the target branch.

### 📄 File: `tools/system/mass_generate_clinerules.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `generate_domain_rules()`

### 📄 File: `tools/system/rag_ingest.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_file_hash()`: Tính mã băm MD5 của một file.
- `load_hash_cache()`
- `save_hash_cache()`
- `check_resource_guard()`: Kiểm tra xem hệ thống còn đủ RAM để chạy tác vụ nặng không.
- `main()`

### 📄 File: `tools/system/rag_query.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `main()`

### 📄 File: `tools/system/refactor_architecture.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `move_if_exists()`
- `delete_if_exists()`
- `main()`

### 📄 File: `tools/system/root_cleanup.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `root_cleanup()`

### 📄 File: `tools/system/setup_project_foundation.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `create_template()`
- `generate_missing_files()`

### 📄 File: `tools/system/smart_patcher.py`
- **Mô tả File:** Không có mô tả.

**Các Lớp (Classes):**
- `SmartPatcher`: The Smart Patcher: A utility to automatically format and fix Python code.

**Các Hàm (Functions/Methods):**
- `SmartPatcher.__init__()`
- `SmartPatcher.run_ruff()`

### 📄 File: `tools/system/sync_docs.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `print_header()`
- `analyze_directory()`: Quét thư mục gốc và trả về cấu trúc các sub-projects.
- `main()`

### 📄 File: `tools/system/system_cleaner.py`
- **Mô tả File:** Không có mô tả.

**Các Hàm (Functions/Methods):**
- `get_core_sig()`
- `clean_docs()`
- `clean_comfy()`

### 📄 File: `tools/system/__init__.py`
- **Mô tả File:** Không có mô tả.

### 📄 File: `tools/ui/dashboard_app.py`
- **Mô tả File:** Không có mô tả.