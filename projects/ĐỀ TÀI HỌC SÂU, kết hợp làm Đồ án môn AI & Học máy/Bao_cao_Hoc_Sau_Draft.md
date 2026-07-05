# ĐỀ CƯƠNG CHI TIẾT: ĐỒ ÁN MÔN HỌC SÂU (DEEP LEARNING)

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI NGHIÊN CỨU

Chương này giới thiệu bối cảnh thị trường tài chính, những thách thức trong việc dự báo giá chứng khoán và vạch ra lộ trình ứng dụng AI từ phân tích chuỗi thời gian đơn thuần đến các hệ thống giao dịch tự động.

### 1.1. Lý do chọn đề tài và tính cấp thiết
1.1.1. Sự biến động phức tạp của thị trường chứng khoán và nhu cầu quản trị rủi ro đầu tư
1.1.2. Những giới hạn của phân tích kỹ thuật bằng mắt thường và sự chi phối của cảm xúc tâm lý giao dịch
1.1.3. Tiềm năng của Trí tuệ nhân tạo trong giao dịch thuật toán (Algorithmic Trading) và xử lý dữ liệu lớn

### 1.2. Mục tiêu và phạm vi nghiên cứu
1.2.1. Mục tiêu tổng quát của hệ thống dự báo xu hướng và hỗ trợ quyết định giao dịch
1.2.2. Mục tiêu cụ thể: Áp dụng Học Sâu (Deep Learning) như mạng LSTM để dự báo chuỗi thời gian.
1.2.3. Phạm vi nghiên cứu (giới hạn rổ chỉ số VN30 hoặc một số mã cổ phiếu blue-chip trên sàn HOSE)

### 1.3. Phương pháp nghiên cứu
1.3.1. Phương pháp thu thập dữ liệu giao dịch lịch sử (OHLCV)
1.3.2. Phương pháp mô hình hóa chuỗi thời gian nâng cao
1.3.3. Phương pháp kiểm chứng chiến lược giao dịch trong quá khứ (Backtesting)

### 1.4. Yêu cầu cấu hình các bản Demo
1.4.1. Chức năng Demo Học sâu: Sử dụng mạng nơ-ron hồi quy Keras LSTM (Backend PyTorch) để dự báo Multi-step (giá đóng cửa của 5 phiên tiếp theo) dựa trên chuỗi giá lịch sử 60 ngày. Có cơ chế tự giảm Learning Rate để tối ưu quá trình học.

### 1.5. Cấu trúc của báo cáo
1.5.1. Tóm tắt nội dung Chương 1 và Chương 2
1.5.2. Tóm tắt nội dung Chương 3
1.5.3. Tóm tắt nội dung Chương 4 và các tài liệu tham khảo

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KỸ THUẬT HỌC SÂU (DEEP LEARNING)

Chương này trình bày nền tảng Mạng nơ-ron hồi quy, nền tảng cho việc phân tích dữ liệu tuần tự.

### 2.1. Kiến trúc Học sâu trong dự báo chuỗi thời gian tài chính
2.1.1. Hiện tượng tiêu biến đạo hàm (Vanishing Gradient) ở mạng RNN truyền thống khi học dữ liệu chứng khoán dài hạn
2.1.2. Mạng bộ nhớ ngắn hạn dài (LSTM) và mạng GRU trong việc ghi nhớ chu kỳ biến động giá
2.1.3. Phương pháp trượt cửa sổ thời gian (Sliding Window) biến đổi dữ liệu tuần tự thành dữ liệu có giám sát cho mạng nơ-ron

### 2.2. Tiền xử lý dữ liệu cho Học sâu
2.2.1. Chuẩn hóa dữ liệu (Min-Max Scaling) chuẩn bị đầu vào cho LSTM
2.2.2. Cấu trúc tensor 3D: (Samples, Time Steps, Features)
2.2.3. Chia tách dữ liệu tập Train/Test theo trình tự thời gian nghiêm ngặt.

### 2.3. Tối ưu hóa mô hình Học sâu
2.3.1. Các hàm mất mát (Loss functions: MSE, MAE) và thuật toán tối ưu (Adam Optimizer)
2.3.2. Sử dụng cơ chế LearningRateScheduler (ReduceLROnPlateau) để linh hoạt giảm tốc độ học khi Validation Loss bị chững lại.
2.3.3. Ngăn chặn Overfitting thông qua việc đan xen các lớp Dropout (0.2).

---

## CHƯƠNG 3: TRIỂN KHAI THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ

Chương này minh họa quá trình thực nghiệm dự báo giá đóng cửa bằng mạng Deep Learning.

### 3.1. Kịch bản, dữ liệu và môi trường thực nghiệm
3.1.1. Cấu hình môi trường phân tích dữ liệu và các thư viện chuyên dụng (PyTorch / TensorFlow)
3.1.2. Thu thập tập dữ liệu chứng khoán của VN30 trong 5 năm (2021-2026)
3.1.3. Phương pháp phân chia tập Train/Val/Test tuân thủ chặt chẽ tính tuần tự của thời gian (Không rò rỉ dữ liệu tương lai)

### 3.2. Kết quả thực nghiệm: Dự báo giá đóng cửa bằng Học sâu (LSTM) (Phần Trọng Tâm)
3.2.1. Phân tích đồ thị Loss: Theo dõi đường Training Loss và Validation Loss để chứng minh mô hình hội tụ tốt và không bị Overfitting.
3.2.2. Phân tích sai số hồi quy (RMSE) giữa tập giá dự báo 5 ngày và giá thực tế.
3.2.3. Giao diện Demo Học sâu (Streamlit): Đồ thị phân tích hiển thị dạng chuỗi (Multi-step) 5 ngày liên tiếp dự đoán chồng lên giá thực tế của FPT.

### 3.3. Thực nghiệm mở rộng: Tích hợp Đa phương thức (Giới thiệu ngắn gọn)
3.3.1. Đánh giá độ chính xác phân loại cảm xúc tin tức tài chính của FinBERT/PhoBERT ở quy mô nhỏ
3.3.2. Kết hợp tín hiệu từ LSTM và tin tức để nâng cao độ chính xác dự báo (Nêu sơ lược ý tưởng và một vài kết quả tiêu biểu).

---

## CHƯƠNG 4: KẾT LUẬN

### 4.1. Kết luận chung về đề tài
- Việc ứng dụng Học Sâu (LSTM) chứng minh khả năng vượt trội trong việc ghi nhớ các chu kỳ giá và dự báo dữ liệu dạng chuỗi thời gian so với ML truyền thống.
- Mặc dù vẫn có sai số trong các khoảng thời gian thị trường biến động mạnh, LSTM bắt nhịp rất tốt với xu hướng chính.

### 4.2. Hạn chế
- Cần tài nguyên tính toán lớn hơn (GPU).
- Cấu trúc "Hộp đen" (Black-box) của Deep Learning khiến việc diễn giải lý do dự báo gặp khó khăn đối với các chuyên gia tài chính truyền thống.

### 4.3. Hướng phát triển
- Tối ưu hóa kiến trúc Attention/Transformer.
- Mở rộng xử lý Đa phương thức (Multimodal) một cách sâu sắc hơn trong Đồ án Tốt Nghiệp.