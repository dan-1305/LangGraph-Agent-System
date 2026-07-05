# ĐỀ CƯƠNG CHI TIẾT: ĐỒ ÁN MÔN HỌC MÁY VÀ AI

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI NGHIÊN CỨU

**1.1. Lý do chọn đề tài và tính cấp thiết**
1.1.1. Sự biến động phức tạp của thị trường chứng khoán và nhu cầu quản trị rủi ro đầu tư: Thị trường chứng khoán thường xuyên biến động mạnh, đặc biệt với rổ VN30. Các chỉ báo kỹ thuật tĩnh bộc lộ độ trễ lớn, khiến nhà đầu tư giao dịch thủ công dễ thua lỗ. Việc xây dựng hệ thống AI tự động hóa giúp tính toán tỷ lệ rủi ro dựa trên kỷ luật toán học.
1.1.2. Những giới hạn của phân tích kỹ thuật bằng mắt thường và sự chi phối của tâm lý: Phần lớn thanh khoản đến từ nhà đầu tư cá nhân dễ bị chi phối bởi FOMO và FUD. Giới hạn sinh học khiến con người không thể xử lý đồng thời lượng lớn chỉ báo kỹ thuật trên nhiều mã cổ phiếu.

**1.2. Mục tiêu và phạm vi nghiên cứu**
1.2.1. Mục tiêu tổng quát: Phát triển hệ thống dự báo xu hướng thị trường ứng dụng Học máy nhằm cung cấp các tín hiệu khách quan hỗ trợ quyết định giao dịch.
1.2.2. Mục tiêu cụ thể (Cấp độ Học máy): Xây dựng mô hình phân loại (Random Forest, SVM, Logistic Regression) dựa trên các chỉ báo kỹ thuật để dự báo xu hướng giá ngắn hạn (Tăng/Giảm/Đi ngang).
1.2.3. Phạm vi nghiên cứu: Giới hạn ở rổ chỉ số VN30. Dữ liệu giao dịch (OHLCV) được thu thập trong 5 năm gần nhất (2021 – 2026).

**1.3. Phương pháp nghiên cứu**
1.3.1. Phương pháp thu thập dữ liệu giao dịch lịch sử (OHLCV): Sử dụng thư viện `vnstock` tải dữ liệu khung thời gian ngày (Daily), làm sạch và khử nhiễu.
1.3.2. Phương pháp mô hình hóa:
- **Kỹ nghệ đặc trưng:** Tính toán RSI, MACD, Bollinger Bands thông qua thư viện `pandas-ta`.
- **Nhãn đa lớp:** Gán nhãn Tăng/Giảm/Đi ngang dựa trên biên độ biến động giá đóng cửa.
- **Mô hình Học máy Baseline:** Áp dụng Random Forest, SVM. Đánh giá thông qua Confusion Matrix và độ phủ Precision/Recall.

**1.4. Yêu cầu cấu hình các bản Demo**
Chức năng Demo Học máy: Ứng dụng mô hình Random Forest hoặc SVM để phân loại xu hướng giá cho phiên giao dịch ngày hôm sau dựa trên các chỉ báo kỹ thuật tĩnh.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ KỸ THUẬT HỌC MÁY ÁP DỤNG

**2.1. Tổng quan lý thuyết thị trường và phân tích chứng khoán**
2.1.1. Giả thuyết thị trường hiệu quả (EMH) và Tài chính hành vi.
2.1.2. Các thành phần của dữ liệu giao dịch: OHLCV đóng vai trò là ma trận đặc trưng cơ sở.
2.1.3. Thách thức của nhiễu thị trường (Market Noise) và giải pháp Log Returns.

**2.2. Các thuật toán Học máy áp dụng trong dự báo xu hướng**
2.2.1. Hồi quy Logistic: Cung cấp hàm phân phối xác suất liên tục.
2.2.2. Support Vector Machine (SVM): Tìm siêu phẳng phân cách xu hướng kết hợp Kernel Trick xử lý dữ liệu phi tuyến tính.
2.2.3. Random Forest và XGBoost: Đánh giá tầm quan trọng của các chỉ báo kỹ thuật (feature_importances) giúp triệt tiêu nguy cơ quá khớp.

**2.3. Kỹ thuật tiền xử lý dữ liệu và tạo đặc trưng (Feature Engineering)**
2.3.1. Tính toán chỉ báo kỹ thuật: RSI, MACD, MA, Bollinger Bands làm đầu vào cho mô hình.
2.3.2. Chuẩn hóa dữ liệu: Áp dụng Standard Scaler và Log Returns để cân bằng độ chênh lệch thang đo giữa giá và khối lượng.
2.3.3. Xử lý mất cân bằng nhãn: Sử dụng kỹ thuật SMOTE và Under-sampling để xử lý hiện tượng số ngày tăng áp đảo ngày giảm, giúp mô hình không bị thiên vị.

**2.4. Môi trường phát triển Học máy**
Khai thác dữ liệu qua `vnstock`, xử lý bảng dữ liệu đa chiều bằng Pandas/NumPy, xây dựng mô hình qua thư viện Scikit-Learn trên Google Colab.

**2.5. Các phương pháp đánh giá mô hình phân loại**
Sử dụng Confusion Matrix, Precision, Recall, F1-Score, và ROC-AUC để đo lường năng lực phân tách xu hướng thay vì chỉ dùng Accuracy.

---

## CHƯƠNG 3: TRIỂN KHAI THỰC NGHIỆM VÀ ĐÁNH GIÁ KẾT QUẢ

**3.1. Kịch bản, dữ liệu và môi trường thực nghiệm**
3.1.1. Cấu hình môi trường: Sử dụng Python, Pandas, Scikit-Learn và Streamlit.
3.1.2. Thu thập dữ liệu: 5 mã VN30 đại diện (FPT, HPG, MBB, MWG, VNM) trong 5 năm (2021-2026).
3.1.3. Phân chia dữ liệu: Chia tập Train/Val/Test (70:15:15) theo trục thời gian tuyến tính chống hiện tượng rò rỉ dữ liệu (Data Leakage).

**3.2. Kết quả thực nghiệm: Dự báo xu hướng giá bằng Học máy**
3.2.1. Đánh giá độ chính xác (Accuracy): Random Forest đạt Accuracy khoảng 39% cho bài toán 3 lớp. Precision cho lớp Đi ngang rất tốt (67%), nhưng Recall lớp Tăng cao dẫn đến nhiều tín hiệu giả (False Positive).
3.2.2. Giao diện Demo: Bảng điều khiển Streamlit cho phép nhập mã chứng khoán và hiển thị "Khuyến nghị: MUA (Xác suất 65%)".
3.2.3. Đánh giá hạn chế: Mô hình Học máy tĩnh có độ trễ rất lớn tại các điểm đảo chiều đột ngột do phụ thuộc vào chỉ báo kỹ thuật truyền thống.

---

## CHƯƠNG 4: TỔNG KẾT VÀ HƯỚNG PHÁT TRIỂN

**4.1. Kết luận chung**
Đề tài đã xây dựng thành công đường ống dữ liệu, làm chủ các kỹ thuật xử lý dữ liệu chứng khoán không nhiễu. Việc ứng dụng Học máy chứng minh được tính kỷ luật, tự động hóa phân tích khách quan, giảm thiểu tác động của yếu tố cảm xúc.

**4.2. Những mặt đạt được và hạn chế**
- **Đạt được:** Xử lý mất cân bằng nhãn thành công với SMOTE; xây dựng luồng phân tích dữ liệu tự động thay thế con người.
- **Hạn chế:** Các mô hình ML bất lực trước các sự kiện "Thiên nga đen" và có độ trễ pha so với thị trường tại các vùng đỉnh/đáy.

**4.3. Hướng phát triển tương lai**
Đề xuất nâng cấp lên các mạng nơ-ron hồi quy tiên tiến hơn (Deep Learning) để khắc phục nhược điểm tĩnh của mô hình Học máy cơ bản, hướng đến việc ghi nhớ các chu kỳ giá dài hạn.