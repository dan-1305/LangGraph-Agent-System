# 🧠 Tóm tắt Kiến thức (Knowledge Base) - Master Wrap-up

Tài liệu này lưu trữ các bài học đắt giá và logic kỹ thuật cốt lõi (Core Logic) được đúc kết sau hàng loạt pha "chạm trán" với hệ thống Anti-bot của các nền tảng lớn.

---

## 1. Bí kíp Bypass 3.0 (Session Persistence)
Để vượt qua rào cản đăng nhập (Login/2FA/Captcha) mà không cần thao tác UI, hệ thống `Airdrop_Guerrilla` sử dụng kỹ thuật **Session Persistence** thông qua Playwright.

### 🐦 X (Twitter) - Cookie Injection
- **Cơ chế:** Nạp trực tiếp `auth_token` vào Browser Context trước khi mở trang.
- **Bắt buộc:** 
  - Domain phải được set cho cả `.twitter.com` và `.x.com`.
  - Phải có cờ `secure: True` và `httpOnly: True` để được công nhận là Cookie xác thực hợp lệ.
  - Phải dùng kèm `fake-useragent` để tránh bị hệ thống quét ra bot.

### 🎮 Discord - InitScript Injection (Đẳng cấp cao)
- **Vấn đề:** Discord không dùng Cookie mà dùng `LocalStorage`. Nếu dùng `page.evaluate()` tiêm LocalStorage sau khi tải trang, hệ thống Webpack của Discord sẽ phát hiện sự bất thường và lập tức "đá" văng ra ngoài trang Login.
- **Giải pháp:** Sử dụng `context.add_init_script()`.
  ```javascript
  window.localStorage.setItem('token', '"TOKEN_CỦA_BẠN_ĐƯỢC_BỌC_TRONG_NHÁY_KÉP"');
  ```
- **Lý thuyết:** Lệnh này được Playwright đẩy thẳng vào Engine của trình duyệt. Trước khi bất kỳ mã Javascript nào của trang `discord.com` kịp tải xuống và chạy, LocalStorage đã có sẵn Token. Discord bị "đánh lừa" rằng bạn đã đăng nhập từ phiên trước đó.

---

## 2. Bài học từ Sự cố Timeout (Step 3: Faucet)
- **Triệu chứng:** Bot điền ví vào form Faucet nhưng văng lỗi `TimeoutError` sau 30 giây.
- **Nguyên nhân:** Các trang Faucet (ví dụ Monad Testnet) thường nhúng Input Form vào bên trong một **Iframe** bảo mật (của Cloudflare Turnstile hoặc Google reCAPTCHA) để chống bot cào. Lệnh `page.fill` thông thường không thể "nhìn thấy" các thẻ HTML bên trong Iframe.
- **Kế hoạch xử lý (Ngày mai):**
  1. Dùng `page.frame_locator("iframe-selector").locator("input")` để chui vào trong Iframe.
  2. Tích hợp API **2Captcha / Anti-Captcha** để giải quyết hộp kiểm "I am human" trước khi submit.

---

## 3. Tổng kết Dự án Bất Động Sản (Real Estate Prediction)
- **Trạng thái Dữ liệu:** Nhờ chiến thuật "Cào Du Kích" (Guerrilla Scraping) với Random Sleep và Fake User-Agent, hệ thống đã thu thập vượt mốc **1.000 dòng dữ liệu siêu sạch** (mục tiêu hướng tới 10.000 dòng).
- **Phân tích của Gemini / Deep Research:**
  - Dữ liệu đã được bóc tách sâu bằng NLP Regex: Trích xuất `Property_Type` (Nhà/Đất/Xưởng/Căn hộ) và `Legal_Status` (Sổ hồng riêng).
  - Áp dụng bộ lọc Outlier đa tầng dựa trên `Price_per_m2` (Lọc giá <1tr và >300tr/m2, kèm Z-score).
- **Kết quả Mô hình:** Nhờ dữ liệu sạch và phân khúc rõ ràng, mô hình **XGBoost Regressor** đã đạt thành tích:
  - **$R^2$ Train:** `0.8954`
  - **$R^2$ Test:** `0.5051` (Tăng vọt so với các phiên bản trước)
  - **MAE (Sai số tuyệt đối):** Giảm xuống chỉ còn **~3.15 Tỷ VNĐ**, một con số cực kỳ ấn tượng trong môi trường dữ liệu nhiễu loạn của thị trường BĐS Việt Nam.

---

## 4. Bảo mật (Security Posture)
- **Database:** Chuyển đổi thành công toàn bộ dữ liệu JSON sang SQLite (`airdrop_guerrilla.db`).
- **Encryption:** 100% Private Keys và Social Tokens được mã hóa bằng thuật toán `AES-128 (Fernet)`.
- **Môi trường:** Tất cả API Key (Telegram, Gemini, 2Captcha) được cách ly tuyệt đối trong file `.env`.