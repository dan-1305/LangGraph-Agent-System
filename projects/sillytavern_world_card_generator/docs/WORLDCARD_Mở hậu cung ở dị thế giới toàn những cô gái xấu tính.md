# Tổng hợp Lore từ World Card: Mở hậu cung ở dị thế giới toàn những cô gái xấu tính

Đây là tóm tắt các yếu tố lore chính được trích xuất từ file JSON `Mở hậu cung ở dị thế giới toàn những cô gái xấu tính.json` để tiện tham khảo.

## 1. Thế giới quan & Bối cảnh (Telorun)

*   **Chủ đề**: Hoàng hôn của Thần linh, Tận thế buông xuống, Âm mưu, Lợi ích là trên hết.
*   **Tone**: Dã tâm cuộn trào, Mục nát và nguy cơ, Cảm giác sử thi.
*   **Bản chất**: Thế giới đang trong giai đoạn suy tàn. Sức mạnh Thần linh phụ thuộc vào tín ngưỡng và đang yếu dần. Pháp tắc thế giới bị xé rách, ma pháp trở nên hỗn loạn. Mọi mối quan hệ, kể cả giữa các Thần linh, đều dựa trên trao đổi lợi ích.
*   **Thánh vị (Sainthood)**: Đỉnh cao sức mạnh, vượt qua cả Thần linh, bằng cách khắc dấu ấn của mình lên bản chất thế giới. Có 2 cấp:
    *   **Ngụy Thánh**: Phụ thuộc vào thế giới nguyên sinh.
    *   **Chân Thánh**: Siêu việt khỏi một thế giới đơn nhất.
*   **Khế ước pháp tắc**: Các thỏa thuận siêu phàm được thế giới công nhận và cưỡng chế thi hành, từ Phàm tục huyết khế, Linh hồn thệ ước đến Thần huyết minh ước.
*   **Sinh thái**: Đa dạng nhưng hỗn loạn, với các quần thể thực vật/động vật ma pháp, biến dị và các khu vực bị ô nhiễm bởi năng lượng Hỗn Độn hoặc công nghiệp.

## 2. Các Chủng tộc Chính

*   **Nhân loại**: Số lượng đông nhất, tính thích nghi cao, nội đấu không ngừng.
*   **Tinh linh**: Ưu nhã nhưng ngạo mạn và bài ngoại. Có nhiều nhánh như Cao đẳng Tinh linh, Nguyệt Tinh linh (bị diệt tộc), Long mạch Tinh linh.
*   **Ải nhân (Người lùn)**: Thợ thủ công tài ba nhưng cực kỳ tham lam và chỉ tín ngưỡng khế ước.
*   **Long mạch duệ**: Hậu duệ của rồng, mạnh mẽ, ngạo mạn, xã hội tàn khốc dựa trên huyết thống.
*   **Thú nhân tộc**: Giữ bản năng động vật, xã hội dựa trên sức mạnh và sinh sản, thường bị bắt làm nô lệ.
*   **Giao nhân**: Kẻ thống trị đại dương, xảo trá, coi các chủng tộc trên cạn là con mồi.
*   **Thần duệ**: Hậu duệ của Thần linh, mạnh mẽ nhưng thường bị coi là công cụ/quân cờ.
*   **Ma duệ**: Hậu duệ lai với ác ma, bị kỳ thị, tính cách cực đoan.
*   **Huyết tộc**: Ma cà rồng cổ xưa, bất tử, đam mê quyền lực và hưởng lạc.
*   **Ám tộc**: Họ hàng của Tinh linh dưới lòng đất, xã hội mẫu hệ, giỏi độc dược và dụ dỗ.

## 3. Nhân vật & Tình huống Mở đầu

*   **First Message 1 (Bản gốc)**:
    *   **Nhân vật chính (MC)**: Một người hiện đại vô tình xuyên không vào một thần điện đổ nát.
    *   **Hệ thống**: Sở hữu **"Bản_nguyên_Dung_lô"** có thể tiêu hao điểm để tiến hóa năng lực.
    *   **Gặp gỡ**: Gặp **Innitia Vesetta**, một tu nữ với vẻ ngoài thánh khiết nhưng thực chất là "Người trọng sinh" đầy mưu mô. Ả nhận ra sự đặc biệt của MC và lên kế hoạch kiểm soát cậu.
*   **Alternate Greetings (Các kịch bản xuyên không khác)**:
    *   **Xuyên không vào chiến trường**: MC rơi vào giữa trận chiến của liên quân phàm nhân và ác ma.
    *   **Xuyên không vào phòng tắm và bị dụ dỗ**: MC xuyên không vào phòng ngủ và gặp ngay Innitia trong bộ đồ lót tình thú đang chủ động quyến rũ.
    *   **Xuyên không vào phòng thí nghiệm**: MC tỉnh dậy trong một phòng thí nghiệm bỏ hoang và gặp một "Điêu khắc sống" (nữ nhân trần truồng với tâm trí trống rỗng).
    *   **Xuyên không vào ổ tà giáo**: MC rơi vào giữa một nghi thức hiến tế của tà giáo và vô tình hấp thụ toàn bộ năng lượng của nghi thức.
    *   **Xuyên không vào cuộc đối đầu giữa các thế lực**: MC rơi vào một trận giao tranh giữa các thế lực lớn, trở thành biến số trong cuộc chiến.

## 4. Các Logic và Cơ chế Điều khiển (JSON Patch)

*   World Card này sử dụng hệ thống **JSON Patch** để tự động cập nhật trạng thái thế giới (thời gian, địa điểm, sự kiện), thông tin nhân vật, và các mối quan hệ dựa trên lựa chọn và hành động trong các kịch bản khác nhau.
*   Hệ thống này cho phép một world card có thể bắt đầu từ nhiều điểm xuất phát khác nhau với các tình huống và nhân vật được thiết lập sẵn, tạo ra trải nghiệm đa dạng và năng động.
*   Nó quản lý chi tiết trạng thái của các phe phái, kẻ địch, và thậm chí cả "nội tâm OS" (suy nghĩ nội tâm) của các nhân vật NPC.