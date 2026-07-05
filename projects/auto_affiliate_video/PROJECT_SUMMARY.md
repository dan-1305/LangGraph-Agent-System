# Auto Affiliate Video - Project Summary & Guide

## 1. Tổng quan dự án
Auto Affiliate Video Generator là một công cụ tự động hóa toàn bộ quy trình tạo video ngắn (Shorts, TikTok, Reels) dùng để làm tiếp thị liên kết (Affiliate Marketing). Hệ thống tự động sinh kịch bản từ tên sản phẩm, tạo giọng đọc (TTS) và ghép video nền thành một thành phẩm hoàn chỉnh.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `main.py`: File chạy chính. Quản lý toàn bộ pipeline từ nhận input -> sinh kịch bản -> sinh audio -> ghép video.
- `src/script_generator.py`: Module sinh kịch bản dùng AI.
- `src/tts_engine.py`: Module Text-to-Speech tạo giọng đọc.
- `src/video_editor.py`: Module dùng thư viện (như `moviepy`) để ghép âm thanh vào video nền.

## 3. Cấu trúc thư mục
- `main.py`: File thực thi.
- `src/`: Thư mục chứa các module nghiệp vụ (Kịch bản, TTS, Edit Video).
- `data/background_videos/`: Nơi người dùng phải bỏ video nền (background) vào để ghép.
- `data/output/`: Nơi xuất ra file audio (.mp3) và file video cuối cùng (.mp4).

## 4. Luồng hoạt động chính
1. **Input:** Người dùng nhập Tên sản phẩm, Tính năng nổi bật và tên file Video Nền.
2. **Generate Script:** Hệ thống dùng `ScriptGenerator` sinh kịch bản ngắn bán hàng bằng LLM.
3. **Generate Audio:** Hệ thống dùng `TTSEngine` đọc kịch bản thành file audio `.mp3`.
4. **Edit Video:** `VideoEditor` lấy file audio và file video nền (từ thư mục `data/background_videos`), ghép lại thành file `.mp4` hoàn chỉnh trong thư mục output.

## 5. Lưu ý quan trọng
- Dự án yêu cầu người dùng phải chủ động tải video nền (từ Pexels/Pixabay) vào thư mục `data/background_videos` trước khi chạy.
- Khuyến khích gắn link affiliate sau khi video được xuất ra.