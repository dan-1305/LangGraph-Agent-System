# 📜 TECHNICAL CHRONICLES (LANGGRAPH AGENT SYSTEM)

*Tài liệu lưu trữ các cột mốc kiến trúc, những rủi ro kỹ thuật (Tech Debt), và các bài toán đã/chưa được giải quyết trong quá trình phát triển hệ thống.*

---

## 📚 BẢNG THUẬT NGỮ KIẾN TRÚC (The Architectural Glossary)
- **Nhà Máy AI (AI Software Factory):** Kiến trúc cốt lõi tại `src/factory/`. Hệ thống được thiết kế dạng pipeline (Planner -> Coder -> Tester -> QA -> Fixer) nhằm tự động hóa việc sinh code.
- **Triage Director:** Node đóng vai trò chặn đứng các request không khả thi, điều phối vòng lặp tự sửa lỗi (Self-Correction Loop).
- **Overlord Agent:** Node định tuyến dựa trên `Constitution`. Quyết định Workflow (Sản xuất phần mềm hay Tranh luận khoa học).
- **Smart Parallelism (Song song thông minh):** Cơ chế giới hạn số luồng (Thread/Process) hợp lý để tránh sập hệ điều hành trên Workstation Xeon E5.
- **Ma trận API (API Matrix):** Cấu trúc Load Balancing (`create_fallback_chain`) giữa nhiều provider LLM để rào lỗi 429 (Rate Limit).
- **Reverse Casual Free Use & Nhịp Đập Thế Giới:** Cơ chế System Prompt ép LLM tuân thủ logic vật lý thay vì sa đà vào miêu tả lãng mạn rẻ tiền trong môi trường Roleplay (SillyTavern).

---

## 🛠 MỐC 1: Khởi Tạo LangGraph & Bypass Cloudflare (Đầu Tháng 03/2026)

**Triển khai & Kiến trúc:**
- Tích hợp `add_init_script` của Playwright để tiêm token thẳng vào LocalStorage, qua mặt hàng rào Webpack của Discord/X cho dự án Airdrop Guerrilla.
- Giả lập Stateful Profile lưu trữ Session JSON, duy trì phiên đăng nhập thay vì login lại từ đầu.
- Xây dựng model XGBoost dự đoán giá BĐS, đạt MAE ~ 3.15. Mã hóa AES-128 bảo vệ Private Keys trong SQLite.
- Thiết lập bộ khung LangGraph sơ khai (Level 4 - High Automation).

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Thực thi trên Iframe:** Iframe bảo mật của Cloudflare thường xuyên gây `TimeoutError`. Khó có thể chạy tự động 100% mà không tích hợp các API giải Captcha bên thứ ba.
- **Tài nguyên Playwright (Thời i3-1215u):** Bị ràng buộc nghiêm ngặt ở chế độ Headless và Max 1 Tab do CPU/RAM yếu. Bản chất Playwright vẫn là "con quái vật" ngốn RAM.
- **Tuổi thọ của Bypass:** Các cơ chế Cookie Injection hay LocalStorage Injection có tuổi thọ rất ngắn. Nền tảng có thể đổi kiến trúc bất cứ lúc nào khiến script vô dụng.

**Khuyến nghị Kiến trúc:**
- Sử dụng `context.add_init_script` thay vì `page.evaluate` để nạp token trước khi load DOM.
- Tích hợp sẵn cơ chế API 2Captcha hoặc capsolver cho các flow dính Iframe Cloudflare.

---

## 🛠 MỐC 2: Tự Động Hóa Giao Dịch Bằng CCXT (10/03/2026)

**Triển khai & Kiến trúc:**
- Gắn thêm tín hiệu "Whale Alert" đẩy Confidence lên 9/10 nếu có biến động on-chain tiêu cực lớn.
- Khắc phục lỗi lệch Timestamp của Binance (-1021) bằng `adjustForTimeDifference=True` trong CCXT.
- Hạ cấp thư viện Pydantic xuống `< 3.0` để khắc phục lỗi tương thích (Incompatibility) với chuẩn JSON parser cũ của Langchain.
- Xây dựng `Paper_Trade_Portfolio` trên SQLite để logging PnL.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Vấn đề Cronjob Local:** Việc dùng Windows Task Scheduler (`.bat`) cực kỳ rủi ro vì phụ thuộc vào trạng thái nguồn điện và mạng của PC cá nhân. Bot Trading không thể được coi là "Tự động hóa 24/7" nếu chạy ở Local.
- **Sập API do quá tải (403):** Chạy chung 1 API Key cho nhiều luồng (Trading, Scraping) dẫn đến tắc nghẽn. Bot sẽ rớt vào trạng thái bảo toàn vốn (bán ra USDT) không mong muốn.

**Khuyến nghị Kiến trúc:**
- Bắt buộc phải đưa module Trading lên môi trường VPS (Linux) và chạy qua `pm2` hoặc `systemd/cron` để đảm bảo độ tin cậy.
- Không được tháo `timeout=10000` của CCXT để ngăn treo Thread khi Binance API phản hồi chậm.

---

## 🛠 MỐC 3: Tiêu Chuẩn Hóa Import & Môi Trường (Giữa Tháng 03/2026)

**Triển khai & Kiến trúc:**
- Cấu trúc lại toàn bộ Monorepo thành **Editable Package** qua `setup.py`. Thay thế toàn bộ Relative Import bằng Absolute Import (`projects.ai_trading_agent.src...`).
- Chuyển đổi engine âm thanh từ `edge-tts` sang `gTTS` do vấn đề về DNS timeout nội vùng.
- Tích hợp module `config.py` dùng `.env` để bảo vệ API Keys thay vì hardcode. Bổ sung `analytics.py` ghi nhận log và PnL.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Refactoring quy mô lớn:** Quá trình chuyển đổi từ Relative sang Absolute Import dễ gây gãy vỡ (Break) ngầm trong các file không được scan tới.
- **Đánh đổi chất lượng âm thanh:** `gTTS` ổn định hơn `edge-tts` về kết nối nhưng thua xa về độ tự nhiên (Natural Voice). Đây là một sự đánh đổi chất lượng UX lấy độ tin cậy của hệ thống (Reliability).

**Khuyến nghị Kiến trúc:**
- Nghiêm cấm sử dụng `sys.path.append` và `sys.path.insert`.
- Ưu tiên cập nhật Type Hinting và Docstrings trong các lần maintain tới để giảm Tech Debt.

---

## 🛠 MỐC 4: Xử Lý Import Trên Streamlit & UI (Cuối Tháng 03/2026)

**Triển khai & Kiến trúc:**
- Thiết kế Streamlit UI bóc tách JSON metadata (`name`, `tags`) không cần load toàn bộ file. Dùng `@st.cache_data` giảm tải băng thông.
- Xây dựng `AutoTranslatorAgent` dịch file JSON thông minh, bảo tồn Regex và Macro (`{{user}}`).
- Khắc phục lỗi `ModuleNotFoundError` ẩn trên môi trường Streamlit.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Rate Limit Khi Dịch Hàng Loạt:** Việc scan và nạp 142 file JSON liên tục làm cạn kiệt API Quota. Cần phải đưa vào hàng đợi (Queue) có cơ chế sleep chống Rate Limit. Thời gian thực thi tăng đáng kể.
- **Rủi ro Dịch Thuật LLM:** LLM (Flash) đôi lúc vẫn tự ý dịch hoặc làm biến dạng các thẻ code (như Regex). Yêu cầu phải có Regex rà soát lại (Post-processing) sau khi dịch.

**Khuyến nghị Kiến trúc:**
- Mọi hàm load IO nặng trên Streamlit phải được Wrap qua decorator `@st.cache_data`.
- Chống chỉ định dùng vòng lặp For gọi API trực tiếp mà không có cơ chế Try-Catch/Exponential Backoff.

---

## 🛠 MỐC 5: Tối Ưu Hóa Fundamental Analysis & Render Video (Cuối Tháng 03/2026)

**Triển khai & Kiến trúc:**
- Bổ sung `Fundamental Analyst` lấy data từ `yfinance` để cung cấp bối cảnh P/E, Cap bên cạnh Technical Analysis.
- Viết pipeline sinh video `auto_affiliate_video`: OpenAI sinh script -> TTS -> `moviepy` dựng video tự động.
- Sửa lỗi phân mảnh đường dẫn (Path Fragmentation) trong Database bằng `Path(__file__).resolve()`.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Render Video trên CPU:** Thư viện `moviepy` rất nặng. Buộc phải đánh đổi chất lượng (chạy `preset="ultrafast"`) và giới hạn `threads` để tránh crash OS. Không phù hợp làm giải pháp scale lớn nếu không có GPU rendering (như FFmpeg NVENC).
- **Dependency Hell của Pillow:** Phải tháo gỡ hardcode version của Pillow để cài được `moviepy`, dẫn đến rủi ro vỡ layout ảnh (Deprecation của thuộc tính `ANTIALIAS`).
- **Data Scraping (PDF):** OCR các file PDF dạng ảnh tốn kém và tỷ lệ sai cao. Tạm thời phải hardcode (khai báo cứng) một số file tham chiếu để bỏ qua lỗi OCR.

**Khuyến nghị Kiến trúc:**
- Thống nhất cơ chế tìm Root Path chuẩn.
- Đối với `moviepy`, nếu có RX580, cần nghiên cứu tích hợp Hardware Acceleration (Render qua GPU) thay vì ép CPU.

---

## 🛠 MỐC 6: Xây Dựng RAG & Khung Overlord (30/03/2026)

**Triển khai & Kiến trúc:**
- Cấu hình `KnowledgeBaseAgent` (`ingest_code.py`) sử dụng ChromaDB để nhúng (embed) mã nguồn dự án thành VectorDB.
- Khởi tạo `Overlord Agent` và tích hợp cơ chế `Human-in-the-Loop` tại `main.py` làm "cầu chì" (người dùng phải xác nhận trước khi script thực thi).
- Refactor luồng workflow thành các `sub-graph` và kết nối thông qua một `meta-graph`.

**Rủi ro Kỹ thuật & Đánh đổi (Tech Debt):**
- **Xung đột `PYTHONPATH`:** Thiết kế thư mục lồng nhau gây ra lỗi `ModuleNotFoundError` liên tục. Việc dùng `sys.path.append` ở đầu file là một giải pháp tạm bợ (patch), làm giảm tính toàn vẹn của mã nguồn.
- **Ảo giác của LLM (Hallucination):** Agent thường xuyên báo cáo thành công giả mạo (ví dụ: lỗi `UnicodeEncodeError` ở runtime nhưng LLM vẫn cho rằng đã sinh file thành công). Hệ thống chưa có cơ chế verify tự động đủ mạnh ở giai đoạn này.
- **State Management:** Việc gộp chung các State vào `FactoryState` dẫn đến rủi ro ghi đè dữ liệu bất đồng bộ.

**Khuyến nghị Kiến trúc:**
- Không tin tưởng vào report của Agent nếu thiếu kết quả từ lệnh `list_files` hoặc `read_file`.

---

## 🛠 MỐC 7: Cấu Hình Tự Động Hóa QA Agent & Cơ Chế Auto-Fix (Đầu Tháng 04/2026)

**Triển khai & Kiến trúc:**
- Thêm node QA Agent dùng Vision AI và phân tích tĩnh để rà soát rò rỉ API key, nợ Docstrings và các lỗi logic cơ bản.
- Cấp quyền gọi ToolNode (`replace_in_file`, `run_command`) cho Auto-Fixer để tái cơ cấu mã nguồn tự động nếu điểm QA dưới ngưỡng.
- Áp dụng cấu trúc Fallback (`.with_fallbacks`) để chuyển đổi tự động giữa các LLM Provider (ví dụ: ggchan sang catiecli).

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Proxy Rate Limit:** Việc dùng API free/proxy gây ra giới hạn kết nối (8 req/min), làm quá trình Auto-Fix thường xuyên bị Timeout hoặc 429 Quota Exhausted. Giải pháp Fallback chỉ làm giảm triệu chứng, không giải quyết được core issue.
- **Giới hạn API Tool Calling:** Một số provider (như Zhipu) khóa tính năng gọi API qua backend Python thông thường, chỉ cho phép qua Tool (như Cline). Dẫn đến lãng phí chi phí mua API.
- **QA Agent Parse Lỗi:** LLM thường xuyên lấy nhầm file log cũ để chấm điểm do không phân tách được Context, yêu cầu phải bổ sung module parse JSON cứng (hardcode parsing) để đảm bảo độ chính xác.

**Khuyến nghị Kiến trúc:**
- Cần có sự giám sát của người điều phối khi cấp quyền `write_to_file` trên môi trường Production.
- Nghiên cứu mua API trả phí hoặc Local LLM để tránh tình trạng "thắt cổ chai" do Rate Limit của Proxy.

---

## 🛠 MỐC 8: Cấu Trúc Hóa "Nhịp Đập Thế Giới" Roleplay (01/04/2026)

**Triển khai & Kiến trúc:**
- Áp dụng xúc xắc d100 tự hành (Autonomous Engine) vào System Prompt (`CONSTITUTION.json`). 
- Đưa khái niệm "Reverse Casual Free Use" và "Song Tu" về dạng quy tắc vật lý/xác suất.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Sự trôi dạt của LLM (Drifting):** Trong Roleplay, dù ép System Prompt cực gắt, sau khoảng 10-15 lượt chat, LLM (Gemini/OpenAI) vẫn có xu hướng bị trôi về "bản tính mặc định" (thích viết lan man, sến súa). Lệnh Meta Tối Thượng chỉ làm chậm lại quá trình trôi dạt, không triệt tiêu được hoàn toàn.

**Khuyến nghị Kiến trúc:**
- Luôn kiểm tra lại Vector Injection Order của `CONSTITUTION.json` nếu LLM bị trôi dạt.

---

## 🛠 MỐC 9: Thiết Lập Factory Pipeline & Giải Quyết Async (Đầu Tháng 04/2026)

**Triển khai & Kiến trúc:**
- Xây dựng chuẩn `BaseNode` cho kiến trúc `AI Factory`. Chuyển đổi thành đồ thị LangGraph với `Triage Director` chặn đầu.
- Tách `requirements.txt` theo từng dự án con.
- Khắc phục lỗi `Event loop is closed` trong kiến trúc Async. Tích hợp `MemorySaver` của LangGraph để bảo toàn `State`. Bọc JSON (`json.dumps`) cho mọi Tool Calling để qua mặt proxy bị lỗi Protobuf (400 Bad Request).
- Xây dựng Local Embeddings ChromaDB (`sentence-transformers`) cho kho tài liệu nội bộ.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **State Size (Context Window):** Trong quá trình lặp (Self-Correction), State bị phình to dẫn đến lố Token Limit. Đây là rào cản khiến AI Factory chỉ thực thi tốt với script nhỏ. Đối với Repo lớn, cần phải triển khai kỹ thuật "Memory Trimming" (cắt tỉa context).
- **Pydantic Validation:** Chuyển đổi giữa Pydantic V1 và V2 gây `ValidationError` thường xuyên (đặc biệt ở cấu trúc Dict/List linh hoạt như JSON của SillyTavern).
- **Ảo Giác Công Cụ (Tool Hallucination):** Agent lạm dụng `sequentialthinking` đốt token vô ích thay vì thực thi ngay. Bắt buộc phải hard-prompt để giới hạn số lần gọi tool.

**Khuyến nghị Kiến trúc:**
- Không thay đổi các khóa chính (như `product_requirements_document`) trong State để tránh mất data qua các vòng lặp.
- Chỉ định rõ kiểu dữ liệu gốc (`List[Dict[str, Any]]`) cho các trường linh hoạt thay vì ép kiểu Pydantic Model cứng ngắc.

---

## 🛠 MỐC 10: Cập Nhật Phần Cứng & Di Cư Hệ Thống (05/04/2026 - 18/04/2026)

**Triển khai & Kiến trúc:**
- Di chuyển hệ thống lên Xeon E5 2676v3 (24 threads), 16GB RAM, RX 580 8GB.
- Bật `Smart Parallelism`: Cho phép Scraping 3 Tabs song song, tăng Batch Size Deep Learning.

**Rủi ro Kỹ thuật & Đánh đổi:**
- Thói quen "tiết kiệm quá mức" từ thời dùng i3 khiến hệ thống ban đầu không dám bung sức. Phải tiến hành rà soát và gỡ bỏ hàng loạt các quy định hardcode giới hạn tài nguyên cũ trong code.
- Việc chuyển sang chạy đa luồng đòi hỏi quản lý RAM khéo léo hơn để tránh việc "ngáo sức mạnh" dẫn đến mở quá nhiều luồng (ví dụ mở hẳn 24 luồng) gây lag máy.

**Khuyến nghị Kiến trúc:**
- Giới hạn Max Threads `n_jobs=8` hoặc `12`, không set `n_jobs=-1` để giữ OS ổn định.

---

## 🛠 MỐC 11: Kỷ Nguyên EdTech & Vượt Bão Ôn Thi (20/04 - 23/04/2026)

**Triển khai & Kiến trúc:**
- (EdTech) Xây dựng format "Mindset vs Giấy thi" và "Podcast có nhịp ngưng Fade-out" bằng `gTTS`. Dựng App trắc nghiệm bằng Tkinter/PyQt tĩnh cho các môn BMTT và QTKDCKS.

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Sự phản bội của Edge-TTS:** Các thẻ SSML để ngắt nhịp (`<break time="2s"/>`) bị đọc thẳng ra thành chữ, sau đó là những chuỗi ngày đứt kết nối liên tục (`NoAudioReceived`). Phải "quay xe" về thư viện cổ điển `gTTS` và dùng Python xử lý ghép byte nhị phân mới ra được sản phẩm.
- **Xử lý Audio/Math thủ công:** Lỗi thao tác mảng (Hàng x Hàng thay vì Hàng x Cột) trong thuật toán Hill cho thấy sự yếu kém của LLM ở mảng Logic Toán Học cứng. Việc dùng `pydub` mà thiếu `ffmpeg` ép Dev phải ghép byte stream `.mp3` thủ công (dễ corrupt header file).

**Khuyến nghị Kiến trúc:**
- Các phép tính toán ma trận, Hash, hay Logic bắt buộc phải gọi sang code Python (Numpy/Crypto) thay vì bắt LLM tự suy luận.

---

## 🛠 MỐC 12: Triển Khai DirectML ComfyUI (25/04/2026)

**Triển khai & Kiến trúc:**
- Triển khai dự án ClothOff độc lập. Ép ComfyUI chạy trên GPU AMD qua `--directml --highvram`. Tích hợp Inpainting và Segment Anything Model (SAM3).

**Rủi ro Kỹ thuật & Đánh đổi:**
- **Sập VRAM (Out of Memory):** Dù dùng lệnh `--highvram`, việc load SAM3 (2.5GB) kèm Stable Diffusion Checkpoint trên GPU 8GB cực kỳ rủi ro. LangGraph và ComfyUI KHÔNG THỂ chạy cùng lúc. Phải cấu trúc ComfyUI thành một folder/môi trường cách ly hoàn toàn.
- **Tắt Âm Thanh Tránh Crash:** Lỗi thiếu DLL từ `torchaudio` trên Windows không thể khắc phục triệt để. Quyết định đánh đổi (Trade-off): Xóa/comment out toàn bộ module xử lý âm thanh trong source code `sd.py` của ComfyUI để ép nó chạy được môi trường thuần ảnh.

**Khuyến nghị Kiến trúc:**
- Bất kỳ dự án Sinh Ảnh/Sinh Video nặng nào cũng phải cô lập (Isolate) ra khỏi luồng LangGraph chính để bảo vệ Memory.

---

## 🏥 BÁO CÁO SỨC KHỎE HỆ THỐNG (System Health Report) - Cuối Tháng 04/2026

**1. Cơ Sở Hạ Tầng (Infrastructure):**
- Trạng thái: **Khỏe (Healthy).** Server Xeon E5 đáp ứng tốt. Tuy nhiên việc chạy trên Windows cá nhân tiềm ẩn rủi ro Downtime. (Cần xem xét WSL hoặc Linux VPS).

**2. Core LangGraph Factory:**
- Trạng thái: **Ổn định (Stable).** Vòng lặp `QA -> Triage -> Auto-Fixer` chạy mượt. State Management không còn bị mất Context. (Rủi ro: Context Window phình to nếu số lượng lỗi lặp lại quá 4 lần).

**3. Các Phân Hệ Chức Năng (Modules):**
- **AI Trading Agent:** Đang chạy (Proof of Concept). Data pipeline (InfluxDB) hoạt động tốt, nhưng rủi ro không chạy 24/7 vì thiếu VPS.
- **Airdrop / Scraping:** Đang chạy (High Maintenance). Cơ chế Bypass hoạt động nhưng cần update thường xuyên do nền tảng đổi luật.
- **Video & EdTech:** Đang chạy (Stable). Script ổn định nhưng tốn CPU/Time để render.
- **SillyTavern Generator:** Hoàn thiện (Production Ready).
- **ComfyUI (DirectML):** Đang chạy (Fragile). Cách ly hoàn toàn. Rất dễ văng lỗi VRAM nếu load ảnh độ phân giải quá cao. Dễ crash nếu đụng tới module Audio.

**Tổng kết:**
Hệ thống đã đạt đến giới hạn cao nhất của tự động hóa trên nền tảng Workstation Windows hiện tại. Mục tiêu kế tiếp KHÔNG PHẢI là thêm tính năng mới, mà là **Tối ưu hóa Context Window (Memory Trimming)**, **Triển khai VPS (Linux)** cho các tác vụ thời gian thực, và **Xử lý triệt để các Nợ Kỹ Thuật (Type Hint, Docstrings, API Rate Limit)**.