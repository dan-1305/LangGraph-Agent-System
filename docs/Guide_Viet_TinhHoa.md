# HƯỚNG DẪN VIẾT FILE TINH HOA (TỪ SÁCH PDF)

## 1. MỤC ĐÍCH CỦA FILE "TINH HOA"
File Tinh Hoa không phải là một bản tóm tắt thông thường (như mục lục sách). Nó là một **"Bản đồ kho báu" (Actionable Map)** giúp người đọc:
- Nắm bắt nhanh các concept cốt lõi của cuốn sách (Big Picture).
- Biết cách **ứng dụng ngay lập tức** các kiến thức đó vào code/project thực tế.
- **Quan trọng nhất:** Biết chính xác **TÌM ĐỌC CHI TIẾT Ở ĐÂU (SỐ TRANG)** nếu muốn đào sâu bản chất toán học hoặc thực hành chi tiết.

## 2. CẤU TRÚC CHUẨN CỦA MỘT FILE TINH HOA
Mọi file Tinh Hoa được gen ra bởi hệ thống AI phải tuân thủ nghiêm ngặt cấu trúc 4 phần sau:

### Phần 1: THÔNG TIN CƠ BẢN
- **Tên sách/Tài liệu:**
- **Tác giả:**
- **Chủ đề chính:**
- **Thông điệp cốt lõi (1 đoạn văn):** Cuốn sách giải quyết nỗi đau gì trong ngành? Tại sao lại phải đọc nó thay vì tài liệu khác?

### Phần 2: BẢN ĐỒ CÁC BÀI HỌC CỐT LÕI (KÈM SỐ TRANG)
*(Quy tắc bắt buộc: Mỗi khái niệm/công thức quan trọng đều PHẢI có tag `[Trang X - Trang Y]` để người dùng dễ dàng lật file PDF ra đọc sâu khi cần thiết).*

- **Khái niệm A [Trang X]:** Giải thích ngắn gọn bằng ngôn ngữ bình dân.
- **Công thức/Thuật toán B [Trang Y - Z]:** Nó hoạt động như thế nào, ưu nhược điểm là gì? Tại sao lại quan trọng?

### Phần 3: ACTIONABLE MAP - ỨNG DỤNG VÀO PROJECT THỰC TẾ
*(Không nói lý thuyết suông. Phải map thẳng lý thuyết vào file code hoặc tư duy giải quyết vấn đề)*
- Nếu đọc phần này [Trang X], ta sẽ biết cách sửa lỗi Overfitting trong file `train_model.py`.
- Nếu đọc phần này [Trang Y], ta biết cách thiết lập kiến trúc Pipeline chống Data Leakage.

### Phần 4: LỜI KHUYÊN HỌC TẬP (TOP-DOWN APPROACH)
- Gợi ý những chương nào mang tính hàn lâm nên **đọc lướt**.
- Gợi ý những chương nào mang tính cốt lõi (Core Mechanics) nên **đọc chậm, dùng giấy bút để nháp** (Deep Reading).

## 3. LƯU Ý CHO HỆ THỐNG AI KHI TẠO FILE
- Tránh dùng văn phong học thuật, khô khan như Wikipedia. Hãy dùng văn phong của một Senior Engineer đang "truyền nghề" (mentoring) cho Junior.
- Đừng cố tóm tắt toàn bộ 100% sách. Hãy chọn lọc 20% lượng kiến thức quan trọng nhất tạo ra 80% hiệu quả thực chiến (Nguyên lý 80/20).
- Nếu không chắc chắn về số trang chính xác trong PDF (do khác biệt version xuất bản), hãy cung cấp **Tên Chương / Tên Mục** thật rõ ràng.
