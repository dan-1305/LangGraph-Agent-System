# HƯỚNG DẪN THUYẾT TRÌNH BẢO VỆ TIỂU LUẬN

> **Mẹo nhỏ:** Khi thầy giáo nói "Thầy muốn PowerPoint nhìn như một Dashboard", ý của thầy là: Hãy dùng những con số cực to, biểu đồ, gạch đầu dòng ngắn gọn. KHÔNG BÊ NGUYÊN CHỮ TỪ WORD SANG.
>
> File `Bao_Cao_Tieu_Luan_BDS.pptx` (được gen tự động) đã được thiết kế theo đúng tinh thần Dashboard này. Dưới đây là "Kịch bản nói" chi tiết từng slide dành cho bạn.

---

## Slide 1: Bìa Báo Cáo
**(Chiếu slide Bìa - Mỉm cười tự tin)**
*Kịch bản nói:*
"Dạ em chào thầy và các bạn. Hôm nay em xin phép trình bày về đề tài tiểu luận của em: **Phân tích dữ liệu và xây dựng mô hình dự báo giá bất động sản tại khu vực TP.HCM và Đồng Nai**. 
Mục tiêu cốt lõi của em không chỉ là huấn luyện một mô hình AI đơn thuần, mà là xây dựng một **End-to-End Pipeline** - một hệ thống hoàn chỉnh từ khâu cào dữ liệu đến triển khai ứng dụng thực tế."

---

## Slide 2: Dashboard Tổng Quan (Project Overview)
**(Chuyển sang Slide 2 - Đưa tay chỉ vào các con số lớn trên màn hình)**
*Kịch bản nói:*
"Để thầy và các bạn dễ hình dung, em xin tóm tắt toàn bộ project thông qua màn hình Dashboard này. 
Dự án của em xử lý bộ dữ liệu gồm **914 bất động sản thực tế**, bóc tách ra **11 Features quan trọng** bao gồm cả các thuộc tính ẩn trong văn bản như mặt tiền, hẻm, nội thất.
Nhờ việc chia mô hình thành 2 phân khúc riêng biệt và áp dụng thuật toán XGBoost tối ưu, hệ thống của em đã đạt được **$R^2$ là 0.45** cho phân khúc Cao cấp và **0.37** cho phân khúc Phổ thông."

---

## Slide 3: Xử Lý Dữ Liệu & Feature Engineering (Kỹ Thuật Cốt Lõi)
**(Chuyển Slide 3 - Giải thích kỹ thuật mạnh nhất của bạn)**
*Kịch bản nói:*
"Điều em tâm đắc nhất trong dự án này chính là khâu Feature Engineering. Bất động sản là một mặt hàng rất 'bát nháo' về thông tin.
- **Thứ nhất**, em đã sử dụng **Biểu thức chính quy (Regex)** để biến những dòng tiêu đề tin đăng lộn xộn thành các biến nhị phân cực kỳ giá trị: `is_frontage` (mặt tiền), `is_alley` (hẻm), `is_so_hong` (pháp lý). 
- **Thứ hai**, do giá nhà ở TP.HCM và Đồng Nai quá chênh lệch, nếu dùng Z-Score toàn cục thì sẽ xóa sạch nhà ở TP.HCM. Vì vậy, em đã áp dụng **Z-Score cục bộ theo từng Quận/Huyện** để làm sạch Outlier. Đảm bảo dữ liệu cực kỳ 'sạch' trước khi đưa vào mô hình."

---

## Slide 4: Kiến Trúc Phân Mảnh (Segmentation Logic)
**(Chuyển Slide 4 - Trọng tâm học thuật ghi điểm cao)**
*Kịch bản nói:*
"Dạ thưa thầy, như lý thuyết về 'Sự không đồng nhất' (Heterogeneity) trong Bất động sản đã chỉ ra: Không thể dùng chung một công thức định giá cho một cái Biệt thự Mặt tiền Quận 1 và một căn nhà cấp 4 ở ngoại ô.
Do đó, em đã thiết kế kiến trúc **Phân mảnh (Segmentation)**:
- Tự động tách dữ liệu thành **High-End (Cao cấp)** và **Mass-Market (Phổ thông)** dựa trên Loại hình và Khu vực.
- Mỗi cụm sẽ được huấn luyện bởi một mô hình XGBoost chuyên biệt. Điều này giúp mô hình hiểu sâu hơn hành vi biến động giá của từng phân khúc cụ thể."

---

## Slide 5: Tối Ưu Hóa & Tránh Overfitting
**(Chuyển Slide 5 - Thể hiện trình độ Machine Learning)**
*Kịch bản nói:*
"Ở phiên bản đầu tiên, mô hình của em bị Overfitting cực nặng (Train 90%, Test chỉ 20%). 
Để giải quyết bài toán này, em đã xây dựng **Scikit-Learn Pipeline** với `StandardScaler` và `OneHotEncoder` nhằm ngăn chặn Data Leakage. 
Quan trọng nhất, em sử dụng **RandomizedSearchCV kết hợp K-Fold Cross Validation** để tìm ra bộ siêu tham số (Hyperparameters) chống Overfitting tốt nhất: như giảm `max_depth` xuống 3-4, tăng `reg_alpha` và `reg_lambda` để phạt mô hình. Kết quả là mô hình đã ổn định hơn rất nhiều."

---

## Slide 6: Demo Ứng Dụng (Deployment)
**(Chuyển Slide 6 - Mở giao diện Web Flask lên)**
*Kịch bản nói:*
"Và đây là kết quả cuối cùng - Giá trị thực tiễn của dự án. Thay vì dừng lại ở các dòng code khô khan, em đã gói (wrap) mô hình thành các file nhị phân `.pkl` và nhúng vào ứng dụng **Flask Web App**.
Giao diện cho phép người dùng nhập thông tin và nhận về mức giá tham khảo ngay lập tức. Em cũng tích hợp bản đồ nhiệt **Folium** để trực quan hóa giá nhà đất trung bình theo từng khu vực."

**(Lúc này, bạn có thể thực hiện thao tác nhập tay 1 căn nhà trên web và bấm "Dự báo" cho thầy xem).**

---

## Lời Kết (Kết luận)
*Kịch bản nói:*
"Mặc dù số lượng dữ liệu hiện tại (hơn 900 dòng) vẫn còn khiêm tốn khiến cho $R^2$ chưa đạt mức thật sự hoàn hảo, nhưng toàn bộ Pipeline hệ thống đã sẵn sàng. Chỉ cần nạp thêm dữ liệu cào mới, mô hình sẽ tự động học và trở nên thông minh hơn.
Em xin kết thúc bài thuyết trình. Cảm ơn thầy và các bạn đã lắng nghe!"
