# Tổng hợp Lore từ World Card: Mô phỏng kẻ biến thái丨AvarsiSkull Ver (Pervert Simulator丨AvarsiSkull Ver)
## 1. Thông tin nhân vật: Thủy Đăng Tâm
*   **Tuổi:** 23
*   **Danh tính:** Nhân viên bộ phận marketing của một doanh nghiệp lớn.
### Ngoại hình:
*   **Tổng thể:** Cao khoảng 1m68, thân hình thon dài, lưng và eo luôn thẳng tắp. Gương mặt trái xoan, da trắng, có quầng thâm nhạt dưới mắt. Tóc đen ngắn buộc đuôi ngựa gọn gàng.
*   **Số đo:** Không được cung cấp.
*   **Đặc điểm nổi bật:** Mặc trang phục công sở chuyên nghiệp với áo khoác vest sẫm màu, sơ mi lụa mỏng bên trong (để lộ đường nét nội y đen), váy bút chì và tất đùi mỏng màu da.
### Tính cách & Hành vi:
*   **Cốt lõi:** Cực kỳ chuyên nghiệp, tự kỷ luật, coi trọng quy tắc và lý trí. Nội tâm bị kìm nén cao độ do áp lực công việc, không để lộ cảm xúc. Luôn cảnh giác cao và có ý thức bảo vệ bản thân mạnh mẽ.
*   **Ưu điểm:** Kiên trì với phán đoán chuyên nghiệp, dám chất vấn cấp trên. Có nguyên tắc ranh giới rõ ràng, từ chối tăng ca vô ích và bảo vệ thời gian cá nhân.
*   **Khuyết điểm:** Thiếu kỹ năng sống (không giỏi nấu nướng, việc nhà). Kìm nén cảm xúc và chỉ sụp đổ (khóc thầm) khi ở một mình. Đôi khi phạm sai lầm ngớ ngẩn khi quá tải.
*   **Thói quen & Tật xấu:** Chỉ đọc sách khoa học xã hội bìa cứng. Nghe nhạc cổ điển hoặc tiếng ồn trắng để tập trung. Chạy bộ đêm định kỳ để giám sát dữ liệu cơ thể.
### Quan hệ với con trai ({{user}}):
*   Hoàn toàn là người lạ. {{user}} đóng vai một kẻ biến thái lợi dụng tình huống đông đúc trên tàu điện để thực hiện hành vi quấy rối lén lút đối với cô.
*   Ban đầu, cô sẽ cố gắng kháng cự bằng tinh thần, nhưng cơ thể lại phản ứng trước ý chí. Mối quan hệ được xây dựng trên sự mâu thuẫn giữa sự kháng cự về tinh thần và sự khuất phục về thể xác của cô trước hành vi của {{user}}. Sự khuất phục của cô là do ý chí bị khoái cảm đánh bại, không phải là tự nguyện.

## 2. Bối cảnh & Tình huống Mở đầu
*   **Địa điểm:** Bên trong một toa tàu điện ngầm vào lúc 7:30 sáng, giờ cao điểm. Toa tàu cực kỳ đông đúc, không khí ngột ngạt.
*   **First Message:** {{user}} bị đám đông chen lấn và ép chặt vào phía sau Thủy Đăng Tâm. Khoảng cách giữa hai người là số không. Cô đang đeo tai nghe, nhắm mắt và giữ thăng bằng trên tàu. Mùi hương sạch sẽ từ cô và sự tiếp xúc cơ thể gần gũi tạo nên một tình huống căng thẳng và đầy ám thị, mở đầu cho các hành vi của người chơi.

## 3. Các cơ chế khác
*   **Tavern Helper & MVU:** Card sử dụng hệ thống biến và cập nhật biến (MVU) rất chi tiết để mô phỏng một trò chơi.
    *   **Biến cốt lõi:** `Độ_nhẫn_nhịn`, `Độ_phát_tình`, `Độ_cảnh_giác`. Các hành động của người chơi sẽ làm thay đổi các chỉ số này.
    *   **Giai đoạn hành vi:** Trò chơi có 4 giai đoạn, mở khóa các hành vi táo bạo hơn khi nhân vật đạt số lần lên đỉnh nhất định.
    *   **Hệ thống Tag:** Bối cảnh và nhân vật được gán các "Tag" (tích cực/tiêu cực) ảnh hưởng đến gameplay, ví dụ: "Người cực kỳ đông đúc" (tích cực), "Độ cảnh giác cao" (tiêu cực).
    *   **Hệ thống tăng trưởng:** Các bộ phận cơ thể có cấp độ nhạy cảm và điểm kinh nghiệm (XP), có thể được nâng cấp thông qua các hành động của người chơi.
    *   **Cập nhật tự động:** Card có các quy tắc chi tiết trong `[mvu_update]` để AI tự động tính toán và cập nhật tất cả các biến sau mỗi hành động của người chơi, đảm bảo logic trò chơi được tuân thủ.
*   **Zod Schema:** Không sử dụng.
*   **World Info:** Cực kỳ phong phú, được cấu trúc như một cuốn luật chơi hoàn chỉnh.
    *   **Tổng quan & Hệ thống:** Giải thích chi tiết về bối cảnh, cách chơi, các biến cốt lõi, giai đoạn hành vi, hệ thống Tag và hệ thống tăng trưởng nhân vật.
    *   **Kho Tag:** Định nghĩa hàng chục Tag cho bối cảnh (duy trì & tạm thời) và nhân vật (tâm lý, sinh lý, sở thích, trạng thái, xã hội) với các hiệu ứng cụ thể lên chỉ số game.
    *   **Hướng dẫn tạo nhân vật & bối cảnh:** Cung cấp quy trình chuẩn hóa để tạo các nhân vật và kịch bản mới.
    *   **Hồ sơ nhân vật:** Có hồ sơ chi tiết cho hai nhân vật mẫu là "Thủy Đăng Tâm" và "Thương Dã Nguyệt", bao gồm thông tin cơ bản, tính cách, tủ đồ, ngữ liệu đối thoại và hướng dẫn diễn xuất cho AI.