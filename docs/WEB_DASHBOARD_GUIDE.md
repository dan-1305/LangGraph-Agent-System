# 🚀 HƯỚNG DẪN KIẾN TRÚC & SỬ DỤNG WEB DASHBOARD V4.0

**Tên file:** `web_dashboard.py`
**Công nghệ sử dụng:** Python, Streamlit, Subprocess, OS Signals.

Tài liệu này mô tả chi tiết kiến trúc UI/UX của Master Dashboard, các cơ chế an toàn, và cách mở rộng hệ thống. Tài liệu này được thiết kế để nạp vào hệ thống RAG, giúp các AI Agent sau này có thể tự đọc và hiểu cách bảo trì giao diện.

---

## 1. CÁC TÍNH NĂNG CỐT LÕI (CORE FEATURES)

### 1.1. Live Status Metrics (Thông số thời gian thực)
- **Cơ chế:** Đọc dữ liệu từ các file log nội bộ (`logs/drip_feed_stats.json`, `logs/scheduler_state.json`) và hiển thị thành các Widget Metric.
- **Auto-Healing Local Proxy:** Hàm `ensure_local_proxy_running()` sẽ ping vào `localhost:8000`. Nếu phát hiện Local Proxy chưa chạy, nó sẽ tự động dùng `subprocess` bật nền proxy lên. Điều này tuân thủ nguyên lý *Hiding Complexity*, người dùng không cần phải tự mở proxy bằng tay.

### 1.2. Nút bấm Chạy ngầm (Background Task Execution)
- **Cơ chế:** Hàm `run_script_bg(script_path)` sử dụng `subprocess.Popen` để đẩy các tác vụ nặng (như Backtest, AI Trading, Cào dữ liệu) xuống hệ điều hành chạy nền.
- **Lợi ích UX:** Giao diện Streamlit không bị "đóng băng" (Zero-Freeze) khi chờ các luồng xử lý AI lên đến 5-10 phút. Ngay sau khi bấm, trả về hiệu ứng `st.toast()` mượt mà.

### 1.3. Bộ lọc chống Spam (Debounce & Lock)
- **Vấn đề:** Nếu người dùng bấm liên tục nút "Chạy", hệ thống sẽ sinh ra nhiều tiến trình trùng lặp, gây cạn kiệt RAM và API Quota.
- **Giải pháp:** Sử dụng cơ chế File Lock. Khi khởi chạy, PID của tiến trình được lưu vào `logs/running_processes.json`. Nếu người dùng bấm tiếp, hệ thống quét thấy PID đang sống -> từ chối chạy và hiển thị cảnh báo `st.warning()`.

### 1.4. Dọn dẹp Tiến trình Ma (Zombie Process Guard)
- **Vấn đề:** Các tiến trình chạy ngầm nếu không được quản lý sẽ nằm mãi trong RAM.
- **Giải pháp:** Thêm nút **[🛑 Dừng]** bên cạnh mỗi tác vụ. Khi bấm, hàm `stop_process()` sẽ đọc PID từ log, sau đó gọi `taskkill /F /PID` (trên Windows) hoặc `os.kill(SIGTERM)` (trên Linux/Mac) để tiêu diệt tận gốc tiến trình, giải phóng bộ nhớ (Garbage Collection).

---

## 2. HẠN CHẾ VÀ LƯU Ý KỸ THUẬT (CAVEATS & LIMITATIONS)

1. **Vấn đề Cây tiến trình con (Process Tree Kill):**
   - Khi dùng `taskkill` hoặc `os.kill` trên PID của Python, nó chỉ giết được tiến trình Python đó. Nếu Python đã đẻ ra các tiến trình con (Ví dụ: Trình duyệt Chrome do Playwright bật lên để cào dữ liệu), các trình duyệt này có thể vẫn sống dai dẳng dưới dạng mồ côi (Orphan process).
   - *Hướng khắc phục sau này:* Dùng thư viện `psutil` để quét và tiêu diệt cả Process Tree thay vì chỉ giết PID cha.

2. **Độ trễ của File Polling so với SSE:**
   - Việc cập nhật Live Metrics hiện tại dựa trên việc Streamlit load lại trang và đọc file JSON trên ổ cứng. Đây là cơ chế Polling thô sơ.
   - Nó không phải là Real-time thực thụ như giao thức SSE (Server-Sent Events) hay WebSocket. Dù vậy, với quy mô Dashboard cá nhân, tốc độ này là đủ tốt và tiết kiệm công sức setup Server.

3. **An toàn Encoding trên Windows (UTF-8):**
   - Luôn phải ép `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')` ở đầu file. Nếu mất dòng này, các ký tự Emojis (🚀, 🛑) sẽ gây lỗi `UnicodeEncodeError` làm sập toàn bộ Dashboard trên CMD của Windows.

---

## 3. HƯỚNG DẪN DÀNH CHO AI AGENT KHI BẢO TRÌ/MỞ RỘNG

Nếu một AI Agent trong tương lai được yêu cầu thêm một chức năng mới vào Web Dashboard, hãy làm theo quy trình sau:

1. Xác định Tab phù hợp (Drip-Feed, Trading, Airdrop, Quản trị).
2. Sử dụng hàm `create_task_row(label, script_path, key)` đã được viết sẵn để tạo hàng nút bấm nhanh chóng:
   ```python
   # Ví dụ thêm tác vụ cào tin tức Crypto
   create_task_row("Cào Tin Tức Crypto", "projects/ai_trading_agent/src/news_scraper.py", "news_scrape")
   ```
   *Lưu ý: Parameter `key` phải là DUY NHẤT (Unique) để Streamlit không báo lỗi Duplicate Key.*
3. Tuyệt đối không thay thế `run_script_bg` bằng các hàm đồng bộ (như `os.system` hay `subprocess.run(check=True)`), vì nó sẽ làm treo giao diện Web.