# 🌅 Kế hoạch Ngày mai (Tomorrow Plan) - Airdrop Guerrilla
**Mục tiêu:** Phá vỡ giới hạn Faucet & Tự động hóa hoàn toàn 100%.

## 🎯 Tiêu điểm 1: Phá băng Faucet (Iframe & Wait Logic)
- **Vấn đề:** Các trang Faucet thường đặt input form bên trong một Iframe bảo mật hoặc load rất chậm, khiến `page.fill` không tìm thấy selector và bị Timeout.
- **Giải pháp:**
  - Nâng cấp `AirdropExecutor`: Sử dụng hàm `page.frame_locator()` để chui vào bên trong Iframe.
  - Tăng thời gian chờ mặc định (`set_default_timeout`) cho riêng Step Faucet để phù hợp với tốc độ tải trang chậm của máy i3.

## 🎯 Tiêu điểm 2: Tích hợp Captcha Solver (Anti-Captcha/2Captcha)
- **Vấn đề:** Faucet luôn yêu cầu giải Captcha (Google reCAPTCHA, Cloudflare Turnstile). Một con bot thông thường không thể tự bấm qua được.
- **Giải pháp:**
  - Lập trình một Service mới tích hợp API của `2Captcha` hoặc `Anti-Captcha`.
  - Quy trình: Nhận diện loại Captcha $\rightarrow$ Gửi request sang dịch vụ giải mã $\rightarrow$ Chờ 15-30s $\rightarrow$ Nạp mã token trả về vào trang web $\rightarrow$ Bypass Faucet.

## 🎯 Tiêu điểm 3: Daily Scheduler (Cronjob Thông minh)
- **Vấn đề:** Hiện tại tôi vẫn đang phải kích hoạt script bằng tay.
- **Giải pháp:**
  - Viết file `run_daily.py` sử dụng thư viện `schedule` của Python.
  - Cấu hình Bot tự động "thức dậy" vào các khung giờ ngẫu nhiên trong ngày (ví dụ: 8h15, 14h30, 21h45) để đi farm hoặc cào data.
  - Khi farm xong tự động tắt hẳn mọi tiến trình.

---
*Chuẩn bị sẵn sàng API Key của 2Captcha để sáng mai chúng ta ghép nối vào hệ thống nhé!*