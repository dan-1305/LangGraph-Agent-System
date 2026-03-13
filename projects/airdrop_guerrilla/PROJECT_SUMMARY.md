# Airdrop Guerrilla - Project Summary & Guide

## 1. Tổng quan dự án
Airdrop Guerrilla là một hệ thống "Stealth Engine Automation" chuyên săn airdrop tự động. Nó sử dụng Playwright để tự động hóa các tác vụ trên trình duyệt như tương tác Twitter, Discord, Faucet, và các nhiệm vụ airdrop khác, đồng thời áp dụng nhiều kỹ thuật ẩn danh (Stealth Behavior) để chống lại các cơ chế Anti-Sybil.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `src/automation/executor.py`: Nơi quản lý việc thực thi các kịch bản tự động hóa (automation scripts).
- `src/automation/stealth_behavior.py`: Định nghĩa các hành vi giả lập người dùng thật và kỹ thuật ẩn danh tránh bị phát hiện bot (Anti-Sybil).
- `src/automation/session_manager.py`: Quản lý Storage State (lưu trữ phiên đăng nhập, cookie, localStorage) để tránh phải đăng nhập lại nhiều lần, vượt qua các lớp bảo mật của Twitter (X) và Discord.
- `docs/status_report_20260302.md`: Lịch sử và trạng thái phát triển gần nhất, ghi chú các điểm nghẽn và thành tựu (VD: Cookie injection, InitScript bypass).

## 3. Cấu trúc thư mục
- `src/automation/`: Chứa các script chính cho tự động hóa (executor, session_manager, stealth_behavior, wallet_manager, zealy_bot).
- `src/analysis/`: Các script phân tích và chấm điểm kèo airdrop (scoring).
- `src/scrapers/`: Mã nguồn để scrape dữ liệu (VD: defillama_funding_parser.py).
- `src/utils/`: Công cụ hỗ trợ, gửi thông báo Telegram (notifier) và database.
- `data/`: Lưu trữ CSDL (`airdrop_guerrilla.db`), các bản kế hoạch chạy (`action_plans/`), session files (`sessions/`), và output bằng chứng (ảnh chụp màn hình).
- `docs/`: Chứa tài liệu, báo cáo trạng thái, và kế hoạch làm việc.

## 4. Các tính năng chính & Bảo mật
- **Tự động hóa trình duyệt**: Vượt qua đăng nhập X và Discord.
- **Stealth & Anti-Sybil**: Tĩnh 1 User-Agent duy nhất được hash theo địa chỉ ví.
- **Bảo mật mạnh**: Mã hóa Private Key và Token theo chuẩn AES-128 (Fernet). Các thông tin nhạy cảm khác lưu ở `.env`.
- **Hệ thống cảnh báo**: Tự động thông báo qua Telegram khi kèo có điểm cao (>1200 điểm) hoặc bot bị lỗi timeout.

## 5. Lưu ý quan trọng
- Vì máy tính chạy chip Intel i3-1215u, dự án này cần được cấu hình tối ưu tài nguyên, tránh mở quá nhiều trình duyệt hoặc xử lý tính toán song song quá nặng.
- Trở ngại hiện tại: Cần cẩn thận khi đối mặt với các trang Faucet dùng Cloudflare Turnstile hoặc reCAPTCHA nhúng trong Iframe, vì Playwright dễ bị timeout ở những tác vụ này.