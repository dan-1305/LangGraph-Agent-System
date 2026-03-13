# Minh Chung PDF Generator - Project Summary & Guide

## 1. Tổng quan dự án
Minh Chung PDF Generator là một script tiện ích nhỏ giúp sinh tự động file PDF tổng hợp các hình ảnh "minh chứng" điểm rèn luyện của sinh viên, được sắp xếp theo các mục và tiêu chí rõ ràng.

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
- `generate_minhchung_pdf.py`: Script duy nhất thực hiện việc quét thư mục ảnh, căn chỉnh kích thước và sử dụng `fpdf` để xuất ra file PDF.

## 3. Cấu trúc thư mục
- `generate_minhchung_pdf.py`: Script chạy chính.
- `MinhChung/`: Thư mục chứa các thư mục con tương ứng với từng mục tiêu chí (VD: `1.1.2.2`, `2.4`, `3.2.2`, v.v.). Mỗi thư mục con chứa các file ảnh minh chứng.
- `MinhChung_Result.pdf`: File PDF đầu ra.

## 4. Luồng hoạt động chính
1. **Cấu hình mục:** Code định nghĩa sẵn một mảng `sections` map giữa tên mục ("Mục 1"), nội dung tiêu chí ("6/Xếp loại học tập") và đường dẫn thư mục chứa ảnh ("MinhChung/1.1.2.2").
2. **Quét ảnh:** Script vào từng folder, lấy tất cả ảnh (`.jpg`, `.png`, `.bmp`), giữ nguyên thứ tự.
3. **Xử lý ảnh & PDF:** Dùng `PIL` để convert ảnh (tránh lỗi định dạng), tính toán kích thước vừa vặn khổ A4, tự động ngắt trang (page break) nếu hết chỗ.
4. **Thêm Caption:** Tên file ảnh (đã bỏ số thứ tự ở đầu) sẽ được dùng làm chú thích (caption) cho ảnh trong PDF.
5. **Xuất PDF:** Lưu thành file `MinhChung_Result.pdf`.

## 5. Lưu ý quan trọng
- Thư viện `fpdf` hỗ trợ tiếng Việt thông qua việc add font TrueType (`arial.ttf`). Cần đảm bảo môi trường có font này ở `C:\Windows\Fonts\` (với hệ điều hành Windows).
- Ảnh sẽ được resize chiều ngang tối đa 170mm và chiều cao tối đa 230mm để vừa khổ A4.