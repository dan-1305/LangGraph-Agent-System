# 🚀 MASTER PLAN: HỆ THỐNG KIẾN TRÚC MỞ RỘNG (SYSTEM IMPROVEMENT QUESTS)

Sau quá trình audit lại toàn bộ kiến trúc LangGraph Agent System, dưới đây là danh sách các khiếm khuyết hiện tại và các ý tưởng (Quest) để nâng tầm dự án này thành một **Hệ sinh thái AI tự động hoàn toàn (Autonomous AI Ecosystem)**.

---

## 🛡️ TẦNG 1: QUẢN TRỊ & BẢO MẬT (INFRASTRUCTURE & SECURITY)

### 1. Unified Notification Gateway (Hệ thống Thông báo Tập trung)
- **Vấn đề:** Hiện tại, logic gửi Telegram đang bị hardcode rải rác trong `binance_executor.py`, v.v. Nếu muốn đổi sang Discord hay Slack, phải sửa hàng loạt file.
- **Giải pháp:** Tạo `core_utilities/notification_gateway.py`. Mọi Agent muốn báo cáo sếp đều đẩy tin nhắn qua Gateway này. Hỗ trợ Rate Limit tin nhắn, phân loại mức độ khẩn cấp (INFO, WARNING, CRITICAL).
- **Độ khó:** Dễ (30 phút).

### 2. Auto-Healing & Process Watchdog (Đặc vụ Y Tế)
- **Vấn đề:** Các kịch bản chạy ngầm (Web Automation, Chrome, Playwright) rất dễ sinh ra tiến trình ma (Zombie Processes) gây tràn RAM (Memory Leak). `disk_cleaner` chỉ dọn file rác chứ không dọn RAM.
- **Giải pháp:** Xây dựng `Resource Watchdog Agent`. Liên tục ping CPU/RAM, tự động kill các tiến trình Python/Chrome mồ côi (Orphan) nếu chiếm > 80% RAM.
- **Độ khó:** Trung bình (45 phút).

---

## 🧠 TẦNG 2: SỰ KẾT NỐI GIỮA CÁC ĐẶC VỤ (INTER-AGENT COMMUNICATION)

### 3. Tích hợp RAG Trading (Đưa sách vào Não Phải)
- **Vấn đề:** `AI Trading Agent` hiện tại chỉ phân tích dựa trên prompt tĩnh và dữ liệu realtime (Tin tức, Giá). Nó thiếu "kiến thức uyên thâm" từ các sách giao dịch.
- **Giải pháp:** Tích hợp `knowledge_base_agent` (RAG) vào `live_advisor.py`. Khi gặp tình huống thị trường sập mạnh, Trading Agent sẽ tự động query RAG: *"Sách của Mark Minervini khuyên nên làm gì khi thị trường giảm 10%?"* rồi đưa ra quyết định.
- **Độ khó:** Khó (60 - 90 phút).

### 4. Cross-Project Data Sharing (Chia sẻ dữ liệu chéo)
- **Vấn đề:** `Auto-X Bot` và `AI Trading Agent` đang chạy độc lập. 
- **Giải pháp:** Tạo một "Shared Memory" qua SQLite. Khi `AI Trading Agent` vừa vào một lệnh BUY rất đẹp, nó sẽ bắn tín hiệu qua Shared Memory -> `Auto-X Bot` đọc được và lập tức đăng Tweet: *"AI của tôi vừa múc BTC ở giá $60k vì RSI quá bán! #Crypto"*. Điều này tạo ra sự kết nối siêu việt giữa các project.
- **Độ khó:** Khó (60 phút).

---

## 🎨 TẦNG 3: MỞ RỘNG TÍNH NĂNG ĐỘC LẬP (NEW DOMAIN QUESTS)

### 5. Auto-X Content Creator (Tạo Content X Tự Động)
- **Vấn đề:** Bot X hiện mới có khung API, chưa có nội dung.
- **Giải pháp:** Dùng LLM kết hợp `news_scraper.py` để mỗi ngày tự động soạn 3-5 tweets chất lượng cao, hẹn giờ lên bài, tracking lượt Like/Retweet lưu vào Database.
- **Độ khó:** Trung bình (45 phút).

### 6. AI Crypto Wallet Tracker (Theo dõi Ví Cá Voi)
- **Vấn đề:** Phần Whale Alert cũ đang bị tắt vì tốn $30/tháng.
- **Giải pháp:** Viết một tool cào dữ liệu miễn phí từ các block explorer (Etherscan, Solscan) hoặc các tài khoản X chuyên track cá voi, sau đó dùng LLM phân tích xem cá voi đang gom hay xả hàng để đưa tín hiệu về cho Trading Agent.
- **Độ khó:** Trung bình (45 - 60 phút).

---

## 🎯 HÀNH ĐỘNG TIẾP THEO (NEXT STEPS)

Sếp có thể chọn bất kỳ Quest nào ở trên, hoặc chúng ta sẽ xử lý theo thứ tự ưu tiên:
1. **Unified Notification Gateway** (Để chuẩn hóa core) -> 2. **Auto-X Content Creator** (Để có sản phẩm chạy ra output ngay) -> 3. **Cross-Project Data Sharing** (Để kết nối 2 thằng lại với nhau).