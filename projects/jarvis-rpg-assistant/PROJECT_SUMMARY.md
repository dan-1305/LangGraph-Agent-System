# Jarvis RPG Assistant - Project Summary & Guide

## 1. Tổng quan dự án
Jarvis V1.0 là một trợ lý ảo cá nhân (Personal DevOps Assistant) được thiết kế như một hệ thống Game RPG đời thực. Hệ thống sử dụng Google Gemini API để quản lý công việc hàng ngày, dạy từ vựng tiếng Anh, ghi chú nhanh và tự động tính điểm kinh nghiệm (XP) / thăng cấp (Level) cho người dùng dựa trên năng suất.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
- `main.py`: CLI dispatcher chính của dự án, tiếp nhận và điều hướng các lệnh như `daily`, `hunt`, `teach`, `evolve`, `note`.
- `jarvis_core/`: Thư mục lõi chứa logic hạ tầng (AI Agent, SQLite Database, Key Manager xoay vòng API, Error Notifier qua Telegram).
- `src/`: Thư mục chứa các kịch bản nghiệp vụ chính (bot báo cáo hàng ngày, bot giáo viên, bot tính XP).
- `tools/dashboard.py`: File Streamlit để khởi chạy giao diện RPG Dashboard trực quan hiển thị Level và tiến độ.

## 3. Cấu trúc thư mục (Chuẩn Production)
Dự án được thiết kế theo kiến trúc Modular Microservices:
- `jarvis_core/`: Hạ tầng kỹ thuật, có cơ chế chịu lỗi (Fault Tolerance) cực tốt như Auto Key Rotation, Time-Based Cooldown và Model Fallback.
- `data/`: Lưu trữ Database SQLite (`jarvis.db`) và hồ sơ người dùng (`user_profile.txt`).
- `tests/`: Thư mục chứa Unit Tests sử dụng `pytest` với tỷ lệ pass 100%.
- `docker-compose.yml` & `Dockerfile`: Kịch bản container hóa.
- `.github/workflows/`: Cấu hình CI/CD tự động test và build image.

## 4. Luồng hoạt động chính
1. **Daily Briefing:** `bot_daily.py` (chạy 4 lần/ngày) lấy thông tin từ Google Calendar, thời tiết để báo cáo.
2. **AI Teacher:** Tự động săn từ mới (`auto_learn.py`) và tương tác dò bài người dùng (`bot_teacher.py`).
3. **Evolve Protocol:** `bot_evolve.py` (chạy cuối ngày) tính toán hiệu suất hoàn thành task, cộng XP, lên Level và tự động commit data lên GitHub.
4. **Dashboard:** Mở bằng lệnh Streamlit để theo dõi thanh quá trình như chơi game thật.

## 5. Lưu ý quan trọng
- Đây là dự án đạt cấp độ **Production**, khi thêm/sửa tính năng ở `jarvis_core/`, AI phải đảm bảo code có kèm theo Unit Test và tuân thủ nguyên tắc Modular.
- Hệ thống hỗ trợ xử lý việc quá tải API (Rate Limit 429) bằng cách xoay vòng danh sách các API Keys (cấu hình trong `.env`).
- Hỗ trợ triển khai Docker toàn diện. Luôn dùng `.env.example` làm mẫu, tuyệt đối không hardcode credentials.