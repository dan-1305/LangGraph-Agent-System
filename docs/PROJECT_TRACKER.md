# 📋 BẢNG THEO DÕI TIẾN ĐỘ DỰ ÁN (PROJECT TRACKER)

*Tài liệu này dùng để lưu trữ Milestones, check-list và kết quả của các Task. Cập nhật liên tục để AI giữ được ngữ cảnh (Context) sau mỗi lần khởi động lại.*

---

## 🎯 MỤC TIÊU HIỆN TẠI: THƯƠNG MẠI HÓA SẢN PHẨM (COMMERCIALIZATION)

### 🚩 MILESTONE 1: BỌC THÉP HẠ TẦNG CỐT LÕI (Core Resilience)
*Mục tiêu: Đảm bảo server proxy chạy cực kỳ trâu bò, chống lỗi 429, chống sập DB.*
- [x] **Zero Token Leakage:** Gắn hàm đếm `tiktoken` vào Proxy Middleware (file `adapter.py`), tự động băm/cắt context nếu vượt 30,000 ký tự.
- [x] **Smart Exponential Backoff:** Nâng cấp thuật toán xoay Key (`rotation_manager.py`). Xử lý lỗi 429 lũy tiến `60s -> 5m -> 1h` để bảo vệ tài khoản Google.
- [x] **Database Sinh tồn & Anti-Replay:** Tạo file `billing.db` với `PRAGMA journal_mode=WAL;` và `timeout=30.0`. Viết endpoint `/api/v1/billing` để đối soát TxHash USDT.

**Kết quả Milestone 1:** Đã hoàn thành! Local Proxy Server giờ đây đạt chuẩn Enterprise. Không còn tình trạng kẹt token hay sập database do Request đồng thời.

---

### 🚩 MILESTONE 2: DECOUPLING & GIAO DIỆN "MÌ ĂN LIỀN"
*Mục tiêu: Tách biệt logic và làm UI thân thiện cho người dùng Non-Tech.*
- [x] **Tách Bot (Decoupling):** Trích xuất logic bot Bất động sản và Airdrop ra các package độc lập để bán riêng (tạo `.env.example`, bỏ sys.path hardcode liên kết với root).
- [x] **Đại tu UI Streamlit:** Thêm Tab `[⚙️ Infrastructure Config]` vào Dashboard. Cho phép dán 3 API Key (Gemini) và 1 địa chỉ Ví Phụ USDT (TRC-20/BSC).

**Kết quả Milestone 2:** Đã hoàn thành! UI cực kỳ thân thiện "Mì ăn liền", khách hàng chỉ cần dán key và địa chỉ ví trên Web UI là xong, không đụng tới file code. Các bot con (Airdrop/BĐS) cũng đã được tách rời độc lập sẵn sàng mang bán.

---

### 🚩 MILESTONE 3: KỶ NGUYÊN ĐÓNG GÓI & DRM (Packaging)
*Mục tiêu: Chống crack và tối ưu quá trình cài đặt 1-Click.*
- [x] **Cython DRM:** Viết đoạn script dịch file chứa logic kiểm tra License sang nhị phân `.pyd` / `.so` để chống dịch ngược (Reverse Engineering) (đã tạo `core/drm_validator.py` và `tools/compile_drm.py`).
- [x] **Portable Python + `run.bat`:** Đóng gói môi trường bằng `uv` hoặc `miniconda`. Viết file `run.bat` để click đúp là chạy ngầm, không mở Terminal Console hù dọa user (đã tạo `run.bat`).

**Kết quả Milestone 3:** Đã hoàn thành! Code đã bọc thép chống dịch ngược bằng cơ chế biên dịch Cython. Thêm vào đó, khách hàng đã có thể mở app 1-click qua `run.bat` mà không bị rối mắt với cửa sổ terminal chi chít chữ.

---

### 🚩 MILESTONE 4: DATA-DRIVEN MARKETING
*Mục tiêu: Lấy số liệu đập vào mặt khách hàng.*
- [x] Dùng Playwright Scraper cào Reddit/X/IndieHackers để tìm các bài than phiền về Gemini Rate Limit hoặc Python Framework rườm rà.
- [x] Chạy Stress-Test toàn bộ proxy. Xuất báo cáo `FOUNDATION_CAPABILITY_REPORT.md` làm tư liệu Marketing (The Pitch).

**Kết quả Milestone 4:** Đã sinh file Báo cáo & Lời chào hàng `docs/FOUNDATION_CAPABILITY_REPORT.md`. Báo cáo đánh trúng 4 nỗi đau lớn nhất của tệp khách hàng, phô diễn các tính năng "chỉ có ở Polymorphic AI Master" như Hot Wallet, Zero-Freeze, 1-Click Install.

---

### 🚩 MILESTONE 5: BETA LAUNCH & QA FUZZING
*Mục tiêu: Đưa sản phẩm cho thực tiễn cào xé.*
- [x] Chạy QA Chaos Agent để Fuzz testing (kiểm thử chịu tải/lỗi) các UI Streamlit và các module Python.
- [x] Lập kịch bản Launch bản Beta (đóng gói giới hạn thời gian 7 ngày, viết bài PR lên Reddit/X thu thập feedback).

**Kết quả Milestone 5:** Đã tạo kịch bản Launch Beta chi tiết tại `IdeaAndBlueprint/BETA_LAUNCH_STRATEGY.md`. QA Chaos Agent đã được tích hợp để tự động quét lỗi Import và Crash trước giờ G.

🚀 **TOÀN BỘ QUÁ TRÌNH THƯƠNG MẠI HÓA VÀ QA ĐÃ HOÀN TẤT MỸ MÃN!** 🚀

---

### 🚩 MILESTONE 7: 30 DAYS SURVIVAL PLAN - TUẦN 2 (Database & Backup)
*Mục tiêu: Khóa chặt dữ liệu, không để mất mát log, và sẵn sàng cho môi trường Production thu nhỏ.*
- [x] **Task 2.1: Giải quyết thắt cổ chai SQLite:** Xây dựng **Log Writer Queue** (Singleton & Thread Daemon) trong `src/database.py`. Mọi Agent giờ ném data vào Queue thay vì ghi trực tiếp để chống lỗi `Database is locked`.
- [x] **Task 2.2: Mock Test cho Trading Agent:** Viết Unit Test dùng `pytest-mock` giả lập Binance API lỗi -2015 hoặc LLM trả về rỗng để kiểm chứng cơ chế tự vệ.
- [x] **Task 2.3: System Monitoring & Alerts:** Tích hợp `RotatingFileHandler` và cảnh báo Telegram khi CPU > 90% hoặc RAM Available < 1GB vào `core_utilities/process_watchdog.py`.
- [x] **Task 2.4: Backup & Version Control:** Viết script `core_utilities/backup_manager.py` tự động nén (zip) toàn bộ file `.db` và `.sqlite3` hàng ngày.

### 🚩 MILESTONE 8: PHỤC HỒI HỆ THỐNG TỪ VS CODE HISTORY
- [x] **Phục hồi Code:** Đã quét toàn bộ 473 thư mục History của VS Code và khôi phục 440 file mới nhất để thay thế code cũ từ Git.
- [x] **Fix Workspace:** Tạo `pyproject.toml` cho `projects/LocalRelay` để sửa lỗi `uv workspace` member missing.
- [x] **Đồng bộ RAG:** Chạy `auto_mapper.py` và `rag_ingest.py` để cập nhật lại bản đồ hệ thống và não bộ AI.

### 🚩 MILESTONE 6: 30 DAYS SURVIVAL PLAN - TUẦN 1
*Mục tiêu: Đảm bảo code chạy không lỗi vặt, có test cơ bản, và hệ thống không sập khi Google khóa Key.*
- [x] **Task 1.6: RAM Optimization & Resource Guard (Git Hook Fix):** Đã vô hiệu hóa tự động RAG Ingest trong `post-commit` hook để cứu máy khỏi tình trạng ăn 11GB RAM. Thêm Resource Guard vào `rag_ingest.py` để chặn đứng tác vụ nếu RAM free < 2.5GB.
- [x] **Task 1.1: Diệt tận gốc `sys.path.insert`:** Đã loại bỏ hoàn toàn `sys.path.append` và `sys.path.insert` trên toàn hệ thống. Áp dụng chuẩn `uv pip install -e .`
- [ ] **Task 1.2: Tích hợp Ollama (Local Fallback)**
- [x] **Task 1.3: Thêm API Backup cho Proxy (Groq/OpenRouter)**: Đã tích hợp tính năng fallback API sang Groq và OpenRouter khi toàn bộ Key Gemini cạn kiệt.
- [x] **Task 1.4: Rút ống thở UI Streamlit cho tác vụ nặng:** Đã tạo `tools/telegram_bot_controller.py` đóng vai trò Command Center siêu nhẹ thay thế Streamlit để trigger bot.
- [x] **Task 1.5: Viết Unit Test Cơ bản (Khẩn cấp):** Đã khởi tạo `test_base_agent.py` và `test_local_proxy.py`.

**Kết quả Milestone 6 (Tuần 1):** Đang triển khai. Đã hoàn thành xử lý module system path và cài đặt nền tảng test pytest thành công.
