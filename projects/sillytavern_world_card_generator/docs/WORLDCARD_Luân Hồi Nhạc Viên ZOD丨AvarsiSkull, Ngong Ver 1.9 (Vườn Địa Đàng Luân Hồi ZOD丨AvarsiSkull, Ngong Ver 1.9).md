# Tổng hợp Lore từ World Card: Luân Hồi Nhạc Viên ZOD丨AvarsiSkull, Ngong Ver 1.9 (Vườn Địa Đàng Luân Hồi ZOD丨AvarsiSkull, Ngong Ver 1.9)
## 1. Thông tin nhân vật: Nhân Vật Chính ({{user}})
*   **Tuổi:** Không xác định.
*   **Danh tính:** Kẻ Giao Ước của Luân Hồi Nhạc Viên (Contractor of Reincarnation Paradise).
### Ngoại hình:
*   **Tổng thể:** Mặc trang phục chiến đấu tiêu chuẩn của Nhạc Viên.
*   **Số đo:** Không xác định.
*   **Đặc điểm nổi bật:** Không xác định.
### Tính cách & Hành vi:
*   **Cốt lõi:** Không xác định.
*   **Ưu điểm:** Không xác định.
*   **Khuyết điểm:** Không xác định.
*   **Thói quen & Tật xấu:** Không xác định.
### Quan hệ với con trai ({{user}}):
*   Không áp dụng, nhân vật chính là {{user}}.
## 2. Bối cảnh & Tình huống Mở đầu
*   **Địa điểm:** Trung Tâm Nhạc Viên · Phòng Riêng (Reincarnation Paradise Center · Private Room).
*   **First Message:** `[kscg]` - Kịch bản/Khai cục tự do, không có lời chào đầu cố định. Người dùng tự do bắt đầu câu chuyện trong bối cảnh Nhạc Viên.
## 3. Các cơ chế khác
*   **Tavern Helper & MVU:** Card này sử dụng hệ thống `[mvu_update]` và `[mvu_plot]` rất phức tạp để quản lý một thế giới RPG dựa trên Zod Schema. Nó định nghĩa chi tiết cách AI phải phân tích cốt truyện và cập nhật các biến trạng thái của người chơi, NPC, thế giới, nhiệm vụ... thông qua định dạng `JSONPatch`. Các quy tắc này bao gồm việc quản lý thời gian, tính toán chỉ số, xử lý vật phẩm, kỹ năng, và dọn dẹp NPC.
*   **Zod Schema:** Đây là một World Card được xây dựng hoàn toàn trên Zod Schema, một hệ thống quản lý biến số cực kỳ chi tiết cho SillyTavern. Toàn bộ `character_book` là một bản hướng dẫn khổng lồ cho AI về cách đọc và ghi dữ liệu vào một cấu trúc JSON phức tạp, bao gồm:
    *   **Nhân Vật Chính:** Quản lý mọi chỉ số từ cơ bản (Sức mạnh, Thể chất...) đến các chỉ số phái sinh (HP, ATK, DEF), trang bị, kỹ năng, thiên phú, nghề nghiệp và trạng thái.
    *   **Kho Hồ Sơ Nhân Vật:** Một cơ sở dữ liệu động để theo dõi tất cả NPC gặp trong truyện, bao gồm cả thông tin cá nhân, chỉ số, trang bị, và một cơ chế "Đếm Ngược Xóa Bỏ" để tự động dọn dẹp các nhân vật không còn liên quan.
    *   **Hệ Thống Nhạc Viên:** Quản lý nhiệm vụ, độ khó thế giới, tiến độ cốt truyện.
    *   **Hệ Thống Vật Phẩm, Kỹ Năng, Trang Bị:** Định nghĩa chi tiết về phẩm cấp (Trắng, Lục, Lam... Vĩnh Hằng), điểm đánh giá, từ tố, và các quy tắc cường hóa, khảm nạm.
    *   **Hệ Thống Thế Lực & Danh Vọng:** Theo dõi mối quan hệ của người chơi với các phe phái khác nhau.
*   **World Info:** Toàn bộ `character_book` đóng vai trò như một World Info cực lớn và có cấu trúc, định nghĩa toàn bộ vũ trụ của "Luân Hồi Nhạc Viên":
    *   **Bối Cảnh Vĩ Mô:** Một đa vũ trụ tàn khốc với 5 Nhạc Viên lớn (Luân Hồi, Thiên Khải, Thánh Quang, Tử Vong, Thủ Vọng) cạnh tranh tài nguyên bằng cách cử Kẻ Giao Ước đến các thế giới khác nhau (Diễn Sinh, Nguyên Sinh, Chiến Tranh...). Cây Hư Không (Void Tree) đóng vai trò công chứng viên trung lập.
    *   **Các Nhạc Viên:** Mỗi Nhạc Viên có đặc điểm riêng: Luân Hồi ("Chó điên", tinh nhuệ hung tàn), Thiên Khải ("Cừu béo", giàu tài nguyên, thiên về công nghệ), Thánh Quang ("Thần côn", hệ tín ngưỡng, hỗ trợ mạnh), Tử Vong ("Lão Âm Bỉ", hệ ám sát/vong linh), Thủ Vọng ("Mai rùa", phòng thủ mạnh).
    *   **Hệ Thống Sức Mạnh:** Sức mạnh được phân chia thành 9 Giai Vị (Tier), mỗi giai vị tương ứng với một cấp độ hủy diệt nhất định (từ cấp đường phố đến cấp phá hủy văn minh). Các thuộc tính có "Vách Ngăn" (threshold), khi đạt đến mốc nhất định sẽ nhận được thưởng đặc biệt.
    *   **Quy Tắc Thế Giới:** Bao gồm các quy tắc về cái chết, thời gian, tổng kết nhiệm vụ, và "Điều Lệ Ban Đầu" cho phép Kẻ Giao Ước phá hoại cốt truyện để thu lợi nhuận cao hơn.
    *   **Kinh Tế:** Sử dụng Nhạc Viên Tệ (Paradise Coins), Linh Hồn Tiền Tệ (Soul Coins), và Huân Chương Vinh Dự (Honor Medals) làm tiền tệ chính. Có hệ thống cửa hàng, đấu giá, và thu hồi vật phẩm.