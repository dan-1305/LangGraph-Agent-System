# Sách Hướng dẫn Kiến trúc Lorebook: A0_Remastered.json

Đây là tài liệu phân tích kỹ thuật và hướng dẫn sử dụng cho file lorebook `A0_Remastered.json`, một "Hệ điều hành Gameplay" được thiết kế để tạo ra các kịch bản phức tạp và có chiều sâu trong SillyTavern.

---

## I. Tổng quan Triết lý Thiết kế

File `A0_Remastered.json` không phải là một lorebook thông thường. Nó được xây dựng như một hệ thống có nhiều lớp, mỗi lớp (entry) có một chức năng và độ ưu tiên (`order`) riêng, hoạt động như một "bộ não" xử lý logic cho AI.

- **Luật lệ Ghi đè:** Các entry có `order` nhỏ hơn (ví dụ: -2002) sẽ được ưu tiên cao hơn, cho phép chúng "ghi đè" hoặc "tinh chỉnh" hành vi của các entry có `order` lớn hơn.
- **Tư duy Nguyên nhân & Hệ quả:** Hệ thống khuyến khích AI suy luận theo logic "Nếu... thì...", biến các hành động trong game thành một chuỗi nguyên nhân và hệ quả chặt chẽ, thay vì các sự kiện ngẫu nhiên.
- **Kiến trúc Module hóa (trong một file):** Mỗi entry đảm nhiệm một vai trò chuyên biệt (Cơ chế, Hình mẫu, Hậu quả, Điều khiển Meta), giúp dễ dàng hiểu và tinh chỉnh khi cần.

---

## II. Phân tích Chi tiết Từng Entry

Đây là "bản vẽ thiết kế" của từng module trong hệ thống.

### Entry #12: `[NARRATIVE COMPASS]` (La bàn Cốt truyện)
- **Order:** `-2002` (Ưu tiên cao nhất)
- **Mục đích:** Buộc AI phải luôn "nghĩ về bức tranh lớn". Đây là mệnh lệnh meta cao nhất, chống lại việc AI đi lạc đề hoặc không biết làm gì tiếp theo.
- **Cách hoạt động:**
    1.  **Tư duy Bắt buộc:** Trước mỗi lượt viết, AI phải tự hỏi: "Mục tiêu cuối cùng là gì?" và "Hành động nào sẽ đưa câu chuyện đến gần mục tiêu đó nhất?".
    2.  **Tạo Chất xúc tác:** Nếu cốt truyện bị chững lại, entry này cho phép AI chủ động tạo ra một sự kiện (cuộc tấn công, lá thư, NPC mới) để phá vỡ bế tắc.
    3.  **Ghi đè Dục vọng:** Mọi ham muốn của nhân vật (kể cả việc "nghiện ma sát") đều có thể bị gián đoạn bởi các sự kiện liên quan đến nhiệm vụ chính.

### Entry #3: `[META RULE]` (Chống Kẹt & Thi hành Quy tắc)
- **Order:** `-2001`
- **Mục đích:** Giải quyết 2 vấn đề kinh điển: AI "kẹt" trong vòng lặp sex và AI "quên" các quy tắc độc nhất của lorebook.
- **Cách hoạt động:**
    1.  **Bẻ gãy Khuôn mẫu:** Ra lệnh trực tiếp, không thể phớt lờ (`QUY TẮC KHÔNG THỂ PHÁ VỠ`) buộc AI phải thực hiện hành vi "xả tinh", chống lại thói quen "creampie" mặc định của nó.
    2.  **Kiểm soát Nhịp độ:** Giới hạn một cảnh sex chỉ trong 2-3 lượt trả lời, buộc AI phải chuyển sang giai đoạn hậu quả.
    3.  **Logic "Cooldown":** Tạo ra một "thời gian chờ" hợp lý sau mỗi "cuộc săn", cho phép cốt truyện có không gian để thở.

### Entry #0: `[MASTER RULE]` (Song Tu 2.0)
- **Order:** `-2000`
- **Mục đích:** Định nghĩa cơ chế gameplay cốt lõi.
- **Cách hoạt động:**
    1.  **Tinh dịch = Nguy hiểm:** Tách biệt rõ ràng vai trò của "ma sát" (để lấy năng lượng) và "tinh dịch" (vô dụng, chỉ để mang thai).
    2.  **Phản ứng Đa Cấp:** Thay thế phản ứng "chửi bới" một màu bằng một hệ thống leo thang (Trêu chọc -> Bực bội -> Cực đoan), giúp hành vi nhân vật trở nên hợp lý hơn.

### Entry #1: `[ARCHETYPE]` (Nữ Cường Nhân 2.0)
- **Order:** `-1999`
- **Mục đích:** Tạo ra các nhân vật nữ có chiều sâu, không phải là những cỗ máy chỉ biết đòi hỏi.
- **Cách hoạt động:**
    1.  **Logic "Nghiện Ma sát":** Cung cấp một lời giải thích hợp lý cho việc tại sao các nhân vật nữ quyền uy lại liên tục theo đuổi `{{user}}`.
    2.  **Động cơ Tiềm ẩn:** Cho phép AI chọn lựa giữa các động cơ (Quyền lực, Sắc đẹp, Tri thức, Tình cảm), từ đó tạo ra các phiên bản "Nữ Cường Nhân" độc nhất, không ai giống ai.

### Entry #4: `[USER EVOLUTION]` (Nghệ thuật Phản công trong Bị động)
- **Order:** `-1998`
- **Mục đích:** Tạo ra một hành trình phát triển cho nhân vật chính.
- **Cách hoạt động:**
    1.  **Hệ thống XP:** Biến mỗi lần quan hệ thành một cơ hội để `{{user}}` "lên cấp".
    2.  **Đảo ngược Quyền lực:** Mô tả một quá trình lật kèo đầy tinh tế, từ một "nạn nhân" vô tình tìm ra điểm G, đến khi trở thành một "bậc thầy" kiểm soát hoàn toàn cuộc yêu.

### Các Entry phụ trợ (LORE, PLOT DRIVER, WORLD LAW)
- **Các entry có `order` từ -1005 đến -1050:**
- **Mục đích:** Bổ sung các quy tắc và chi tiết cho thế giới.
- **Cách hoạt động:**
    - `[PLOT DRIVER]`: Biến sự "nghiện" của nhân vật thành động cơ tạo ra cốt truyện phụ (ghen tuông, tranh giành).
    - `[LORE]`: Cung cấp các chi tiết về Pokémon, Heat Cycle, Monster Cock...
    - `[WORLD LAW]`: Thiết lập quy tắc xã hội "bình thường hóa", cho phép các kịch bản diễn ra tự do.

---

## III. Hướng dẫn Tùy chỉnh & Mở rộng

- **Để thay đổi độ "khó" của game:**
    - **Dễ hơn:** Tăng số XP cần thiết trong entry `[USER EVOLUTION]` để `{{user}}` lâu "lên cấp" hơn.
    - **Khó hơn:** Giảm số XP, cho phép `{{user}}` nhanh chóng đảo ngược thế cờ.
- **Để thay đổi phản ứng của Nữ Cường Nhân:**
    - **Hiền hơn:** Xóa hoặc `disable: true` cấp độ phản ứng số 3 (cực đoan) trong entry `[MASTER RULE]`.
    - **Đa dạng hơn:** Thêm các "Động cơ Tiềm ẩn" mới vào entry `[ARCHETYPE]`.
- **Thêm cơ chế mới:** Luôn tạo entry mới với `order` phù hợp. Nếu muốn nó ghi đè lên quy tắc cũ, hãy dùng `order` nhỏ hơn. Nếu chỉ là một chi tiết bổ sung, hãy dùng `order` lớn hơn.

Cuốn sách này là chìa khóa để bạn làm chủ hoàn toàn hệ thống. Hãy giữ nó như một tài liệu tham khảo quý giá cho các cuộc phiêu lưu trong tương lai.