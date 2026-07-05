# BÁO CÁO TIỂU LUẬN CHI TIẾT
**Tên đề tài: Phân tích dữ liệu và xây dựng mô hình dự báo giá bất động sản tại khu vực TP.HCM và Đồng Nai**

---

## CHƯƠNG 1: TỔNG QUAN VỀ ĐỀ TÀI

### 1.1. Mục tiêu tổng quát
Mục tiêu tổng quát của đề tài là ứng dụng quy trình Khoa học Dữ liệu (Data Science Pipeline) để xây dựng một hệ thống Trí tuệ Nhân tạo (AI) toàn diện, có khả năng tự động hóa việc định giá bất động sản tại khu vực TP.HCM và Đồng Nai. Hệ thống này hướng tới việc giải quyết bài toán thiếu minh bạch về giá trị nhà đất thông qua việc phân tích lượng lớn dữ liệu thô, từ đó cung cấp một thước đo giá trị khách quan giúp người mua, người bán đưa ra các quyết định tài chính an toàn.

### 1.2. Lý do chọn đề tài
Thị trường bất động sản (BĐS) tại khu vực kinh tế trọng điểm phía Nam (cụ thể là TP.HCM và Đồng Nai) luôn biến động mạnh mẽ. Giá trị BĐS bị chi phối bởi vô số yếu tố: từ định lượng (diện tích, số tầng) đến định tính (vị trí, pháp lý, tiện ích). Đối với bộ môn Nhập môn Khoa học Dữ liệu, đây là một bài toán hoàn hảo để thực hành trọn vẹn quy trình từ thu thập dữ liệu (Data Collection), làm sạch (Data Cleaning), khai phá đặc trưng (Feature Engineering) cho đến mô hình hóa (Modeling).

### 1.3. Mục tiêu nghiên cứu cụ thể
- Thu thập bộ dữ liệu thực tế từ các nền tảng BĐS lớn tập trung vào khu vực TP.HCM và Đồng Nai.
- Thực hiện làm sạch dữ liệu chuyên sâu và loại bỏ các giá trị ngoại lai (Outliers) để đảm bảo chất lượng đầu vào.
- Ứng dụng kỹ thuật khai phá văn bản (Regex) để trích xuất các đặc trưng quan trọng từ tiêu đề tin đăng (mặt tiền, số lầu, tính pháp lý).
- Huấn luyện và đánh giá mô hình học máy (XGBoost) nhằm dự báo giá nhà.
- Xây dựng ứng dụng Web minh họa để đưa mô hình vào thực tiễn.

### 1.4. Đối tượng và phạm vi nghiên cứu
- **Đối tượng nghiên cứu:** Quy trình phân tích dữ liệu, các phương pháp làm sạch ngoại lai (Z-Score), kỹ thuật Text Mining và thuật toán hồi quy Gradient Boosting.
- **Phạm vi nghiên cứu:** Dữ liệu tin đăng BĐS tại khu vực TP.Hồ Chí Minh và Tỉnh Đồng Nai, giới hạn phân khúc nhà đất, căn hộ có diện tích từ 10m2 đến 1000m2.

---

## CHƯƠNG 2: CƠ SỞ LÝ THUYẾT VÀ TỔNG QUAN TÀI LIỆU

### 2.1. Các yếu tố định giá Bất động sản
Giá trị bất động sản được cấu thành từ:
- **Yếu tố vật lý:** Diện tích sàn, số lượng tầng, chiều ngang, và độ rộng hẻm tiếp cận.
- **Yếu tố vị trí & pháp lý:** Khu vực hành chính (Quận/Huyện thuộc TP.HCM hoặc Đồng Nai), tình trạng mặt tiền hay hẻm, và sự bảo đảm về mặt pháp lý (Sổ hồng, sổ đỏ).

### 2.2. Khai phá dữ liệu văn bản (Text Mining)
Khác với các bộ dữ liệu chuẩn hóa, dữ liệu BĐS trên mạng phần lớn là văn bản tự do. Biểu thức chính quy (Regex) được sử dụng như một kỹ thuật cốt lõi trong Data Science để bóc tách thông tin ẩn (vd: "nhà 3 lầu, hẻm 4m, SHR") thành các biến số phân loại độc lập có thể tính toán được.

### 2.3. Thuật toán XGBoost trong Hồi quy
XGBoost (eXtreme Gradient Boosting) là thuật toán Ensemble Learning tiên tiến. Khả năng chống Overfitting mạnh mẽ và khả năng xử lý tốt cả biến phân loại lẫn biến liên tục giúp XGBoost vượt trội trong bài toán định giá BĐS.

---

## CHƯƠNG 3: PHƯƠNG PHÁP NGHIÊN CỨU

Nghiên cứu được thiết kế bám sát vào Quy trình Khoa học Dữ liệu (Data Science Pipeline) bao gồm 5 bước cốt lõi:
1. **Data Collection:** Thu thập dữ liệu thô.
2. **Data Cleaning & EDA:** Xử lý dữ liệu khuyết thiếu và phân tích khám phá để hiểu phân phối giá.
3. **Feature Engineering:** Làm giàu dữ liệu thông qua việc biến đổi biến mục tiêu (Log Transformation) và trích xuất đặc trưng mới.
4. **Modeling:** Xây dựng Pipeline huấn luyện với tỷ lệ chia tập dữ liệu 80:20.
5. **Deployment:** Triển khai mô hình dưới dạng dịch vụ Web.

---

## CHƯƠNG 4: THU THẬP VÀ XỬ LÝ DỮ LIỆU

### 4.1. Thu thập dữ liệu
Dữ liệu đầu vào (`raw_data.csv`) được cào tự động bằng thư viện Playwright từ các nền tảng bất động sản lớn, với thiết lập vị trí đích danh là TP.HCM và Đồng Nai. Cấu trúc dữ liệu ban đầu bao gồm: Giá (`Price_VND`), Diện tích (`Area_m2`), Quận/Huyện (`District`), Tỉnh (`Province`), và Tiêu đề (`Title`).

### 4.2. Tiền xử lý dữ liệu (Data Preprocessing)
Quá trình làm sạch dữ liệu là khâu quan trọng nhất quyết định độ chính xác của toàn bộ dự án:
- **Xử lý missing values:** Loại bỏ lập tức các dòng bị khuyết thông tin trọng yếu như Giá và Diện tích.
- **Lọc tính hợp lý lý thuyết:** Chỉ giữ lại các bản ghi có `Area_m2` từ 10m2 đến 1000m2.
- **Lọc biên độ giá:** Tạo ra biến Đơn giá (`Price_per_m2`). Áp dụng ngưỡng cứng: loại bỏ bất động sản có đơn giá bất hợp lý (< 1 triệu hoặc > 300 triệu VNĐ/m2) nhằm loại bỏ rác/tin spam.

### 4.3. Xử lý dữ liệu ngoại lai (Outlier Detection) bằng Z-Score
Do giá nhà tại TP.HCM khác biệt rất lớn so với Đồng Nai, phương pháp Z-Score cục bộ được áp dụng thay vì Z-Score toàn cục:
- Hệ thống tự động tính Giá trị trung bình (Mean) và Độ lệch chuẩn (Std) của Đơn giá theo từng khu vực Quận/Huyện cụ thể.
- Tính điểm Z-Score cho mỗi bản ghi. Dữ liệu có $|Z| > 3$ (lệch quá 3 độ lệch chuẩn) bị xem là giá "ảo" và bị loại bỏ. Khâu này giúp dữ liệu trở nên cực kỳ sạch và đáng tin cậy.

### 4.4. Trích xuất đặc trưng (Feature Engineering)
Nhằm tối đa hóa thông tin từ cột `Title`, kỹ thuật xử lý ngôn ngữ cơ bản được áp dụng để sinh ra 8 đặc trưng mới, tạo sức mạnh cho mô hình máy học:
1. `is_frontage`: Nhận diện "mặt tiền", "mặt đường".
2. `is_alley`: Nhận diện "hẻm", "hxh".
3. `has_furniture`: Tình trạng nội thất ("full đồ").
4. `num_floors`: Số lượng lầu/tầng (dạng số).
5. `width_m`: Bề ngang lô đất.
6. `alley_width_m`: Độ rộng hẻm tiếp cận.
7. `Property_Type`: Phân loại thành Nhà, Đất, Căn hộ, Kho xưởng.
8. `is_so_hong`: Đảm bảo tính pháp lý.

---

## CHƯƠNG 5: KẾT QUẢ NGHIÊN CỨU

### 5.1. Thiết lập huấn luyện mô hình
Do biến mục tiêu (`Price_VND`) có phân phối lệch rất mạnh, dữ liệu được chuyển đổi qua hàm Logarit tự nhiên (`np.log1p`) để đưa về phân phối chuẩn (Normal Distribution). Điểm nổi bật trong kiến trúc mới là **Hệ thống Phân mảnh (Segmentation Logic)**. Dữ liệu được chia làm 2 phân khúc: Cao Cấp (High-End) và Phổ Thông (Mass-Market). Mỗi phân khúc được huấn luyện bằng một mô hình XGBoost riêng biệt.

Đồng thời, hệ thống ứng dụng **RandomizedSearchCV** kết hợp **K-Fold Cross Validation** để tự động dò tìm siêu tham số (Hyperparameter Tuning), giúp chống Overfitting hiệu quả (vd: `max_depth=3-4`, `reg_alpha`, `reg_lambda`). Dữ liệu trước khi vào mô hình được đưa qua `Pipeline` xử lý chuẩn hóa bằng `StandardScaler` và mã hóa vector qua `OneHotEncoder`.

### 5.2. Kết quả đánh giá mô hình
Trên tập kiểm thử (Test set), các mô hình đạt được kết quả khả quan và kiểm soát tốt hiện tượng Overfitting:
- **Phân khúc High-End:** Chỉ số R-squared ($R^2$) đạt ~0.4525. Sai số tuyệt đối trung bình (MAE) xấp xỉ ~4.6 Tỷ VNĐ.
- **Phân khúc Mass-Market:** Chỉ số R-squared ($R^2$) đạt ~0.3731. Sai số tuyệt đối trung bình (MAE) xấp xỉ ~1.93 Tỷ VNĐ.

Việc tách phân khúc và dò tìm tham số tự động giúp hệ thống dự báo bám sát hơn với đặc thù cực kỳ biến động của thị trường BĐS.

### 5.3. Triển khai ứng dụng (Deployment)
Thể hiện đúng tinh thần của khoa học dữ liệu là mang lại giá trị thực tiễn, nhóm đã xuất mô hình thành file nhị phân (`model.pkl`) và xây dựng ứng dụng Web với Flask. Giao diện trực quan cho phép người dùng cấu hình tham số BĐS và nhận lại mức giá tham khảo ngay tức thì.

---

## CHƯƠNG 6: KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 6.1. Kết luận
Đề tài đã hoàn thành một vòng đời (life-cycle) hoàn chỉnh của dự án Khoa học Dữ liệu: từ cào dữ liệu, làm sạch sâu, xử lý outlier, trích xuất đặc trưng văn bản, cho đến mô hình hóa và triển khai thành công ứng dụng thực tiễn cho thị trường TP.HCM và Đồng Nai.

### 6.2. Hạn chế và Hướng phát triển
- **Hạn chế:** Các luật Regex phân tích văn bản tĩnh chưa thể thấu hiểu hoàn toàn các từ lóng hay cách hành văn viết tắt phức tạp của môi giới BĐS.
- **Phát triển:** Trong các nghiên cứu nâng cao hơn, có thể tích hợp mô hình ngôn ngữ như PhoBERT để xử lý triệt để ngữ nghĩa văn bản. Đồng thời, thu thập thêm dữ liệu về khoảng cách địa lý (tọa độ GPS, khoảng cách đến trường học/bệnh viện) thông qua OpenStreetMap để tăng độ chính xác ($R^2$) của mô hình định giá.