# BẢNG PHÂN TÍCH ĐỘ KHÓ & MỤC TIÊU NÂNG CAO (STRESS TEST)
*(Dựa trên Đề cương Gốc của Giáo viên)*

## 1. SO SÁNH THỰC TẾ vs YÊU CẦU GỐC

| Tiêu chí | Yêu cầu trong Đề cương (Docx) | Thực tế Code hiện tại (Của chúng ta) | Trạng thái / Đánh giá |
|----------|-----------------------------|--------------------------------------|-----------------------|
| **Phạm vi Data** | 5 mã VN30 đại diện (2021-2026) | Chỉ mới lấy 1 mã (FPT_VN) từ 2021-2026 | ⚠️ **Thiếu:** Cần viết vòng lặp cào thêm 4 mã nữa (VD: HPG, VNM, MWG, VIC). |
| **Demo Học Máy** | Dự đoán Tăng/Giảm/Đi ngang ngày hôm sau. Dùng RF hoặc SVM. | Đã dùng RF (47%), SVM (51%). Đã vẽ Feature Importance. Nhưng chỉ dự đoán Tăng/Giảm (Binary), thiếu "Đi ngang". | ⚠️ **Thiếu:** Cần định nghĩa lại Target thành 3 nhãn (Tăng, Giảm, Đi ngang/Sideway). Độ chính xác 51% là quá thấp. |
| **Demo Học Sâu** | Dự báo mức giá cụ thể của **3-5 phiên tiếp theo** (Multi-step). Dùng LSTM/GRU. | Đang dùng LSTM. Đã tính RMSE (5642) và vẽ chart. Nhưng chỉ mới dự báo **1 phiên** tiếp theo. | ⚠️ **Lệch yêu cầu:** Thầy yêu cầu dự báo 3-5 ngày. Cần nâng cấp mô hình. |
| **Đồ án Tốt Nghiệp** | Multimodal: Time-series + FinBERT. Tích hợp Backtesting. | Mới có Placeholder trong cấu trúc thư mục, chưa có code. | ⏳ **Đang chờ:** Mục tiêu dài hạn. |

---

## 2. KẾ HOẠCH BÀI TEST TĂNG ĐỘ KHÓ (STRESS TEST)

Để Đồ án đạt điểm tuyệt đối (9-10) và không bị thầy bắt bẻ "Model học vẹt", chúng ta cần đặt ra các bài test (Stress Test) nhằm thử thách giới hạn của 2 mô hình.

### A. Đối với Môn Học Máy (Machine Learning) - Mục tiêu: Vượt mốc 60%
*Hiện tại RF đang đạt 47% (thua cả tung đồng xu). Cần cải thiện gấp.*

- **Bài Test 1: Bẫy "Đi ngang" (Sideway Trap):** 
  - *Mô tả:* Thay vì chỉ đoán Tăng/Giảm, ép Model phải phân loại 3 nhãn: Tăng (Return > 1%), Giảm (Return < -1%), Đi ngang (Return từ -1% đến 1%).
  - *Kỳ vọng:* Mô hình SVM sẽ gặp khó khăn. Ta sẽ giải quyết bằng cách áp dụng GridSearchCV để tìm Hyperparameter (C, Gamma) tốt nhất.
- **Bài Test 2: Nạp thêm Feature (Chỉ báo mới):**
  - *Mô tả:* Nạp thêm Bollinger Bands và Stochastic Oscillator vào đầu vào.
  - *Kỳ vọng:* Random Forest tự động chọn ra chỉ báo nào mạnh nhất để bắt xu hướng.

### B. Đối với Môn Học Sâu (Deep Learning) - Mục tiêu: Dự báo chuỗi 5 ngày
*Hiện tại RMSE là 5642 (sai số khá lớn với mã FPT). Cần ép LSTM làm việc khó hơn.*

- **Bài Test 1: Dự báo Đa bước (Multi-step Forecasting 5 Days):**
  - *Mô tả:* Thay vì xuất ra `Dense(1)` (1 ngày), ta ép mô hình xuất ra `Dense(5)` (dự báo luôn giá của thứ Hai đến thứ Sáu tuần sau).
  - *Kỳ vọng:* Biểu đồ sẽ không chỉ là 1 điểm nối tiếp, mà là các đoạn thẳng nhỏ 5 ngày trượt trên biểu đồ thực tế. Rất trực quan và chuẩn yêu cầu thầy.
- **Bài Test 2: Bẫy Nhiễu (Noise Injection):**
  - *Mô tả:* Lấy 20% dữ liệu Test, cố tình cộng thêm hoặc trừ đi 5% giá trị (Giả lập thị trường bị nhiễu loạn / Thiên nga đen).
  - *Kỳ vọng:* Xem Dropout(0.2) của LSTM có gánh được không, hay biểu đồ dự đoán sẽ bị văng xa tít mù tắp. Nếu nó vẫn bám được xu hướng, chúng ta sẽ có cớ để chém gió trong Slide "Khả năng chống chịu nhiễu của LSTM".

---

## 3. LỘ TRÌNH TRIỂN KHAI CẢI TIẾN
*(Admin / Tiến sẽ làm ngay sau khi đã chốt bản Sinh tồn)*

1. **Mai (Bổ sung Data):** Sửa file `01_Tien_Data_Pipeline.ipynb` để chạy vòng lặp tải luôn `['FPT.VN', 'HPG.VN', 'VNM.VN', 'MWG.VN', 'VIC.VN']`.
2. **Tuần sau (Nâng cấp Học Sâu):** Đổi kiến trúc mạng ở file `03_Danh_LSTM_Models.ipynb` từ `Dense(1)` thành `Dense(5)` và tinh chỉnh vòng lặp Sliding Window để predict 5 ngày.
3. **Gần Deadline (Cứu Học Máy):** Thêm 3 nhãn (Tăng/Giảm/Đi ngang) vào mô hình Random Forest để thỏa mãn chuẩn "Demo Học máy" trong Docx.