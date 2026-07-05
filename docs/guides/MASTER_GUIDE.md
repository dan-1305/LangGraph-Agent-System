# 🗺️ MASTER GUIDE - TÀI LIỆU HƯỚNG DẪN TỔNG HỢP

Chào mừng bạn đến với tài liệu "Bản đồ kho báu" của dự án **LangGraph_Agent_System**. Bất cứ khi nào bạn quên cách chạy một dự án hoặc muốn biết cần mở file nào để sửa code, hãy mở file này ra đọc.

---

## 📂 1. CẤU TRÚC THƯ MỤC CỐT LÕI

Hệ thống được chia thành các khối chính:

```text
LangGraph_Agent_System/
│
├── dashboard.py                  <-- TRUNG TÂM ĐIỀU KHIỂN (Chạy file này để mở Menu tổng)
├── auto_scrape_scheduler.py      <-- File chạy ngầm Cronjob để cào BĐS mỗi 30 phút
├── .env                          <-- Nơi lưu trữ TOÀN BỘ Key bảo mật (API, Password)
│
├── src/                          <-- (Khối NÃO) Logic cốt lõi của LangGraph (Graph, Node, State)
│
└── projects/                     <-- (Khối TAY CHÂN) Chứa 3 dự án thực tế
    │
    ├── airdrop_guerrilla/        <-- Dự án 1: Bot cày Airdrop & Tự động hóa Crypto
    │   ├── src/automation/wallet_manager.py  (Mã hóa Key, chống Sybil)
    │   ├── src/automation/executor.py        (Bot chạy Twitter/Discord)
    │   └── src/automation/zealy_bot.py       (Bot cày nhiệm vụ Zealy)
    │
    ├── real_estate_prediction/   <-- Dự án 2: Trí tuệ nhân tạo dự báo giá BĐS
    │   ├── app.py                            (Giao diện Web Flask & Bản đồ)
    │   ├── train_model.py                    (Nơi chứa Regex xử lý chữ và thuật toán XGBoost)
    │   └── generate_word_report.py           (Sinh file báo cáo Tiểu luận tự động)
    │
    ├── ai_trading_agent/         <-- Dự án 3: Bot giao dịch AI (Multi-Agent)
    │   ├── data_fetcher.py                   (Tải dữ liệu đa tài sản & Fear/Greed Index)
    │   ├── news_scraper.py                   (Cào tin tức Crypto & Whale Alert)
    │   ├── langgraph_agent.py                (Bộ não suy luận 3 lớp: Tech, News, Risk)
    │   ├── binance_executor.py               (Bot đặt lệnh tự động trên Binance/Paper Trade)
    │   ├── backtester.py                     (Chạy mô phỏng quá khứ có trừ phí sàn)
    │   └── live_advisor.py                   (Chạy thực chiến báo lệnh hôm nay)
    │
    └── sillytavern_world_card_generator/ <-- Dự án 4: Công cụ AI tạo Thẻ Thế Giới (SillyTavern)
        ├── src/models/world_card_v3.py       (Data Model Pydantic cho chuẩn JSON v3)
        ├── src/agents/                       (Chứa Storyteller, Lore Master, Coder Agents)
        ├── src/world_card_generator.py       (Orchestrator kết nối các AI Agents)
        ├── data/templates/                   (Thư viện các file JSON mẫu: Lorebook, Preset, Regex)
        └── ui/app.py                         (Giao diện Streamlit)
```

---

## 💾 1.1. CƠ SỞ DỮ LIỆU (DATABASE)

Dự án đã được quy hoạch Data Layer rất quy củ, tất cả nằm trong thư mục `data/`:
- `system_logs.db`: Lưu vết mọi quyết định của AI Trading (Paper Trade, Live, Lịch sử hệ thống). Bạn có thể xem nhanh qua `dashboard.py` (Phím 9).
- `real_estate.db`: Dữ liệu nhà đất đã cào và xử lý, dùng cho Web App BĐS.
- `trading_market.db`: Dữ liệu nến OHLCV của BTC, ETH, SOL và các chỉ báo kỹ thuật, được kéo bằng `data_fetcher.py`.
- `airdrop_guerrilla.db`: (Nếu có) Dữ liệu các ví Crypto và thông tin Airdrop.

---

## ️ 2. HƯỚNG DẪN BẢO TRÌ & NÂNG CẤP (DÀNH CHO BẠN)

Khi tay nghề code của bạn lên cao, hoặc khi bạn nảy ra ý tưởng mới, đây là nơi bạn cần tìm đến:

### A. Nếu muốn sửa Bot Trading (Dự án 3)
- **Muốn thêm coin mới (Ví dụ thêm XRP, ADA):** Mở file `projects/ai_trading_agent/data_fetcher.py` và `projects/ai_trading_agent/live_advisor.py` để thêm Ticker vào list.
- **Muốn thêm chỉ báo kỹ thuật mới (như MACD, Bollinger Bands):** Mở file `projects/ai_trading_agent/data_fetcher.py` và sửa hàm tính toán pandas.
- **Muốn cấu hình API Binance để trade thật:** Mở file `.env` và điền `BINANCE_TESTNET_API_KEY` cùng `SECRET`. Hệ thống sẽ tự động tắt chế độ Paper Trading.
- **Muốn dạy cho AI cách đánh khác (sửa logic Risk Manager / Whale Alert):** Mở file `projects/ai_trading_agent/langgraph_agent.py` và sửa nội dung Prompt.

### B. Nếu muốn sửa Mô hình BĐS (Dự án 2)
- **Gặp từ viết tắt mới khó hiểu (như "nhà nát", "hxg"):** Mở file `projects/real_estate_prediction/train_model.py`, tìm đến phần `# FEATURE ENGINEERING (Extract from Title)` để thêm Regex.
- **Muốn sửa giao diện Web / Bản đồ:** Mở `projects/real_estate_prediction/app.py` và thư mục `templates/index.html`.

### C. Nếu muốn nâng cấp Bot Airdrop (Dự án 1)
- **Tài khoản Discord bị bắt đăng nhập lại:** Hãy cập nhật `discord_token` mới trong file Database bằng `WalletManager`.
- **Muốn cày nền tảng khác ngoài Zealy (như Galxe):** Tạo một file mới (vd: `galxe_bot.py`) dựa trên cấu trúc mẫu của `zealy_bot.py`.

### D. Nếu muốn tùy chỉnh Hệ thống Tạo World Card (Dự án 4)
- **Muốn cho AI học cách viết Lorebook mới:** Bỏ thêm các file JSON chuẩn của bạn vào `projects/sillytavern_world_card_generator/data/templates/lorebook/`.
- **Muốn sửa giao diện Web Generator:** Mở `projects/sillytavern_world_card_generator/ui/app.py` (Streamlit).
- **Muốn đổi logic sinh văn bản của AI:** Chỉnh sửa System Prompt trong các file tại `projects/sillytavern_world_card_generator/src/agents/`.

---

## 🚀 3. CÁCH CHẠY CÁC DỰ ÁN DỄ DÀNG NHẤT

Bạn không cần nhớ lệnh phức tạp nữa. Từ nay, hãy luôn đứng ở thư mục gốc `LangGraph_Agent_System`, mở Terminal lên và gõ:

```bash
python dashboard.py
```

Một Menu tương tác sẽ hiện ra. Bạn chỉ cần nhập số (1, 2, 3...) và bấm Enter, hệ thống sẽ tự động gọi đúng file script nằm sâu bên trong để chạy cho bạn.
