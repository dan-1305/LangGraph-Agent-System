# ĐỀ CƯƠNG CHI TIẾT: ĐỒ ÁN MÔN HỌC MÁY (MACHINE LEARNING)

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI NGHIÊN CỨU

Chương này giới thiệu bối cảnh thị trường tài chính, những thách thức trong việc dự báo giá chứng khoán và vạch ra lộ trình ứng dụng AI từ phân tích chuỗi thời gian đơn thuần đến các hệ thống giao dịch tự động.

### 1.1. Lý do chọn đề tài và tính cấp thiết
1.1.1. Sự biến động phức tạp của thị trường chứng khoán và nhu cầu quản trị rủi ro đầu tư
1.1.2. Những giới hạn của phân tích kỹ thuật bằng mắt thường và sự chi phối của cảm xúc tâm lý giao dịch
1.1.3. Tiềm năng của Trí tuệ nhân tạo trong giao dịch thuật toán (Algorithmic Trading) và xử lý dữ liệu lớn

### 1.2. Mục tiêu và phạm vi nghiên cứu
1.2.1. Mục tiêu tổng quát của hệ thống dự báo xu hướng và hỗ trợ quyết định giao dịch
1.2.2. Mục tiêu cụ thể: Ứng dụng Học Máy để phân loại xu hướng giá.
1.2.3. Phạm vi nghiên cứu (giới hạn rổ chỉ số VN30 hoặc một số mã cổ phiếu blue-chip trên sàn HOSE)

### 1.3. Phương pháp nghiên cứu
1.3.1. Phương pháp thu thập dữ liệu giao dịch lịch sử (OHLCV)
1.3.2. Phương pháp mô hình hóa chuỗi thời gian
1.3.3. Phương pháp kiểm chứng chiến lược giao dịch trong quá khứ (Backtesting)

### 1.4. Yêu cầu cấu hình các bản Demo
1.4.1. Chức năng Demo Học máy: Ứng dụng mô hình Random Forest hoặc SVM để phân loại xu hướng giá đa nhãn (Tăng/Giảm/Đi ngang) cho phiên giao dịch ngày hôm sau dựa trên các chỉ báo kỹ thuật. Tích hợp GridSearchCV để dò tìm siêu tham số tối ưu.

### 1.5. Cấu trúc của báo cáo
1.5.1. Tóm tắt nội dung Chương 1 và Chương 2
1.5.2. Tóm tắt nội dung Chương 3 (Triển khai) và Chương 4 (Kết luận)

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KỸ THUẬT HỌC MÁY ÁP DỤNG

Chương này tập trung vào lý thuyết thị trường, các chỉ báo kỹ thuật tài chính và thuật toán phân loại Học máy để giải quyết bài toán dự đoán xu hướng ngắn hạn.

### 2.1. Tổng quan lý thuyết thị trường và phân tích chứng khoán
2.1.1. Giả thuyết thị trường hiệu quả (EMH) và Tài chính hành vi (Behavioral Finance)
2.1.2. Các thành phần của dữ liệu giao dịch: Mở cửa (Open), Cao nhất (High), Thấp nhất (Low), Đóng cửa (Close), Khối lượng (Volume)
2.1.3. Thách thức của nhiễu thị trường (Market Noise) và tính ngẫu nhiên (Random Walk)

### 2.2. Các thuật toán Học máy áp dụng trong dự báo xu hướng
2.2.1. Hồi quy Logistic (Logistic Regression) trong việc dự báo xác suất xu hướng
2.2.2. Máy học véc-tơ hỗ trợ (Support Vector Machine - SVM) tìm siêu phẳng phân cách xu hướng (Đa nhãn)
2.2.3. Rừng ngẫu nhiên (Random Forest) và XGBoost trong việc đánh giá tầm quan trọng của các chỉ báo kỹ thuật. Áp dụng cơ chế GridSearchCV tối ưu siêu tham số.

### 2.3. Kỹ thuật tiền xử lý dữ liệu và tạo đặc trưng (Feature Engineering)
2.3.1. Tính toán các chỉ báo kỹ thuật (RSI, MACD, Moving Averages, Bollinger Bands) làm đầu vào cho mô hình
2.3.2. Chuẩn hóa dữ liệu tài chính đa thang đo (Min-Max Scaler, Standard Scaler) và biến đổi Logarit lợi suất (Log Returns)
2.3.3. Kỹ thuật xử lý mất cân bằng nhãn xu hướng (ví dụ: số ngày tăng nhiều hơn số ngày giảm)

### 2.4. Công cụ và môi trường phát triển Học máy
2.4.1. Thư viện pandas-ta hoặc TA-Lib để tính toán chỉ báo kỹ thuật nhanh chóng
2.4.2. Khai thác dữ liệu chứng khoán Việt Nam qua API của VnDirect, SSI hoặc thư viện vnstock
2.4.3. Quản lý luồng xử lý và huấn luyện trên môi trường Jupyter Notebook/Google Colab

### 2.5. Các phương pháp đánh giá mô hình phân loại xu hướng
2.5.1. Đánh giá tính chính xác qua Ma trận nhầm lẫn (Confusion Matrix) và Accuracy
2.5.2. Chỉ số Precision và Recall trong việc hạn chế tín hiệu mua sai (False Positive)
2.5.3. Sử dụng đường cong ROC và diện tích AUC để đo lường sức mạnh phân loại của mô hình

---

## CHƯƠNG 3: TRIỂN KHAI THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ

Chương này minh họa quá trình thực nghiệm dự báo xu hướng bằng Machine Learning.

### 3.1. Kịch bản, dữ liệu và môi trường thực nghiệm
3.1.1. Cấu hình môi trường phân tích dữ liệu và các thư viện chuyên dụng
3.1.2. Thu thập tập dữ liệu chứng khoán của 5 mã VN30 đại diện trong 5 năm (2021-2026)
3.1.3. Phương pháp phân chia tập Train/Val/Test tuân thủ chặt chẽ tính tuần tự của thời gian (Không rò rỉ dữ liệu tương lai)

### 3.2. Kết quả thực nghiệm: Dự báo xu hướng giá bằng Học máy
3.2.1. Đánh giá độ chính xác (Accuracy) của Random Forest và SVM trong việc đoán đúng hướng đi của ngày mai (Tăng/Giảm/Đi ngang).
3.2.2. So sánh hiệu năng trước và sau khi sử dụng GridSearchCV (Lưới tối ưu).
3.2.3. Giao diện Demo Học máy: Nhập mã cổ phiếu, hệ thống load dữ liệu kỹ thuật, hiển thị biểu đồ Feature Importance và đưa ra khuyến nghị.
3.2.4. Đánh giá hạn chế: Mô hình ML tĩnh thường bị trễ so với thị trường ở những đoạn đảo chiều đột ngột và gặp khó với tính ngẫu nhiên cao của chứng khoán.

---

## CHƯƠNG 4: TỔNG KẾT VÀ KẾT LUẬN

### 4.1. Kết luận chung về đề tài
- Quá trình ứng dụng Học Máy cơ bản (Random Forest, SVM kết hợp GridSearchCV) đã cho thấy khả năng phân loại xu hướng giá ngắn hạn (Tăng/Giảm/Đi ngang) ở mức an toàn.
- Dù có những điểm trễ nhất định ở các đoạn đảo chiều, Học Máy vẫn mang lại góc nhìn khách quan dựa trên kỹ thuật.
- Học Máy có thể là bước đệm tốt để phát triển các hệ thống phức tạp hơn.

### 4.2. Khó khăn và Hạn chế
- Mô hình tĩnh thường trễ so với các biến động "Thiên nga đen" và phụ thuộc nhiều vào chất lượng Feature Engineering (các chỉ báo kỹ thuật).

### 4.3. Hướng phát triển tương lai
- Có thể áp dụng mạng Học Sâu (Deep Learning) để xử lý dữ liệu phi tuyến tính tốt hơn thay vì chỉ dùng Học máy truyền thống.