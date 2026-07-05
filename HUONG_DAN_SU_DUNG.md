# 📖 HƯỚNG DẪN SỬ DỤNG HỆ THỐNG LANGGRAPH AGENT

Chào mừng bạn đến với **LangGraph Agent System** - một hệ sinh thái monorepo mạnh mẽ tích hợp các AI Agent tự vận hành, tự sửa lỗi và giải quyết các bài toán thực tế từ Trading, Bất động sản đến Tự động hóa nội dung.

---

## 🛠️ 1. Cài Đặt Hệ Thống (Setup)

Có hai cách chính để khởi động hệ thống này:

### Cách A: Sử dụng Docker (Khuyến khích - Nhanh & Ổn định)
Cách này giúp bạn tránh được các xung đột thư viện Python.
1.  Đảm bảo đã cài **Docker** và **Docker Compose**.
2.  Mở Terminal tại thư mục gốc và chạy:
    ```bash
    docker-compose up -d --build
    ```
3.  Truy cập các dịch vụ:
    *   **Bất động sản (Web App):** `http://localhost:5000`
    *   **SillyTavern Generator (Streamlit):** `http://localhost:8501`
    *   **Jarvis Dashboard (Streamlit):** `http://localhost:8502`

### Cách B: Cài đặt Thủ công (Local Python)
Dành cho việc chỉnh sửa code và debug nhanh.
1.  Tạo môi trường ảo: `python -m venv venv` và kích hoạt (`venv\Scripts\activate` trên Windows).
2.  Cài đặt thư viện: `pip install -r requirements.txt`.
3.  Cài đặt các thư viện cho từng sub-project nếu cần (nằm trong `projects/<tên_dự_án>/requirements.txt`).

---

## 🔐 2. Cấu Hình Biến Môi Trường (.env)

Hệ thống cần các API Key để hoạt động. Hãy copy file `.env.example` thành `.env` và điền thông tin:

*   **GCLI_API_KEY**: Key của Gemini (Lấy tại [Google AI Studio](https://aistudio.google.com/)).
*   **BINANCE_TESTNET_API_KEY / SECRET**: Nếu muốn dùng Bot Trading thực chiến trên sàn Testnet.
*   **TELE_TOKEN / CHAT_ID**: Để nhận thông báo từ Bot Trading qua Telegram.
*   **DISCORD_TOKEN**: Dành cho các tính năng tự động hóa Discord.
*   **CATIECLI_API_KEY / CATIECLI_BASE_URL**: (Tùy chọn) API Key và Endpoint cho proxy dự phòng.

Hệ thống có cơ chế "Ma trận API" thông minh để tự động chuyển đổi giữa các API nếu một trong số chúng gặp lỗi. Xem chi tiết tại `docs/guides/API_MODEL_STRATEGY.md`.

---

## 🤖 3. Trung Tâm Điều Khiển (Dashboard)

Đây là "Trạm chỉ huy" chính của toàn bộ hệ thống. Hãy chạy lệnh sau:

```bash
streamlit run dashboard.py
```

Giao diện Web sẽ hiện ra với 4 tab chính:
1.  **🏠 Tổng Quan**: Xem điểm số chất lượng (QA Score) của tất cả dự án. Bạn có thể nhấn "Batch QA" để AI quét và chấm điểm lại toàn bộ hệ thống.
2.  **📂 Chi Tiết Dự Án**: Xem tài liệu (Wiki) và điều khiển riêng từng dự án:
    *   **Trading Agent**: Chạy Live Advisor ngay trên web.
    *   **SillyTavern**: Mở giao diện tạo World Card.
    *   **Auto-Fix**: Ra lệnh cho AI tự tìm và sửa lỗi trong code của dự án đó.
3.  **🏭 AI Software Factory**: 
    *   **Tạo dự án mới**: Nhập yêu cầu, AI Agent sẽ tự lên kế hoạch và viết code.
    *   **Hội đồng phản biện (Debate)**: Chọn một file, các AI Agent sẽ tranh luận để tìm ra điểm yếu và đề xuất nâng cấp.
4.  **Quản trị**: Theo dõi chi phí API (Token usage) và dọn dẹp file rác.

---

## 📈 4. Các Dự Án Trọng Tâm (Flagship Projects)

### 1. AI Trading Agent (`projects/ai_trading_agent`)
*   **Chức năng**: Phân tích kỹ thuật (RSI, MACD...), phân tích tin tức (Sentiment) và ra quyết định giao dịch.
*   **Cách chạy**: `python projects/ai_trading_agent/live_advisor.py` hoặc qua Dashboard.
*   **Dữ liệu**: Xem tại `data/trading_market.db`.

### 2. Dự báo Bất động sản (`projects/real_estate_prediction`)
*   **Chức năng**: Cào dữ liệu từ các trang BĐS, dùng XGBoost để dự báo giá và hiển thị bản đồ nhiệt (Heatmap).
*   **Cách chạy**: `python projects/real_estate_prediction/app.py`.

### 3. SillyTavern Generator (`projects/sillytavern_world_card_generator`)
*   **Chức năng**: Tạo thẻ thế giới (World Card) chuẩn JSON v3 cho roleplay.
*   **Cách chạy**: `streamlit run projects/sillytavern_world_card_generator/ui/app.py`.

### 4. Airdrop Guerrilla (`projects/airdrop_guerrilla`)
*   **Chức năng**: Bot tự động cày Airdrop trên các nền tảng Crypto (Twitter, Discord, Zealy).
*   **Cách chạy**: Xem hướng dẫn chi tiết trong `projects/airdrop_guerrilla/README.md`.

### 5. Auto Affiliate Video (`projects/auto_affiliate_video`)
*   **Chức năng**: Tự động tạo video tiếp thị liên kết (Affiliate) từ kịch bản, giọng nói đến dựng video.
*   **Cách chạy**: `python projects/auto_affiliate_video/main.py` hoặc qua Dashboard.

### 6. Lò Luyện Thi AI (EdTech Tools)
*   **Chức năng**: Chuyển đổi đề cương PDF khô khan thành bản giải chi tiết (Mindset nháp + Viết ra giấy thi), tạo "Podcast Ru Ngủ" với giọng nói tự nhiên ngắt nhịp (gTTS), và App Desktop Trắc nghiệm (qtkdcks_quiz_app.py, qtkdcks_formula_reflex.py).
*   **Cách chạy**: Nằm rải rác ở thư mục `tools/` (ví dụ `python tools/qtkdcks_quiz_app.py` hoặc chạy script tạo podcast).

---

## 🚀 5. Các Luồng Công Việc Nâng Cao (Workflows)

Hệ thống tích hợp các workflow chạy ngầm vô cùng thông minh:
*   **Scientific Debate**: Chạy `python run_debate.py` để AI tự phản biện tài liệu/code.
*   **NSFW Writer**: Chạy `python run_nsfw_writer.py` để khởi động luồng viết truyện sáng tạo (Creative Writing).
*   **Auto-Fixer**: Luồng tự sửa lỗi khi code bị crash hoặc không đạt điểm QA.

---

## 📂 6. Cấu Trúc Thư Mục Cần Nhớ

*   `src/`: Chứa bộ não (logic LangGraph cốt lõi).
*   `projects/`: Chứa 11 sub-projects thực thi các nhiệm vụ khác nhau.
*   `data/`: Nơi lưu trữ tất cả các Database SQLite (Logs, Market Data, Real Estate).
*   `docs/`: Thư viện tài liệu hướng dẫn chuyên sâu.

---
*Chúc bạn có những trải nghiệm tuyệt vời với LangGraph Agent System! Nếu có thắc mắc, hãy xem thêm file `docs/guides/MASTER_GUIDE.md`.*
