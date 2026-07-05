# 🎮 HƯỚNG DẪN CẤU HÌNH CHẾ ĐỘ CHƠI (CASUAL vs HARDCORE)

Tài liệu này hướng dẫn bạn cách phối hợp giữa **Lorebook** và **Preset** để chuyển đổi nhanh giữa phong cách chơi "Nhẹ nhàng (Casual)" và "Thô tục (Hardcore)" trong SillyTavern.

---

## 🌸 1. Chế độ CASUAL (Nhẹ nhàng, Tập trung cảm giác)

Dùng khi bạn muốn cốt truyện diễn ra tự nhiên, các nhân vật phản ứng nhẹ nhàng, không quá kịch tính hay thô thiển.

### Cấu hình Lorebook (World Info):
*   **BẬT (Enable):**
    *   `03_FETISH_Casual.json`
    *   `Free Use.json`
    *   `！！Table - Worldbook 丨AvarsiSkull Ver.json` (Core)
    *   `02_ANATOMY_Body_Interaction.json` (Core)
    *   `04_MECHANICS_RPG.json` (Core)
*   **TẮT (Disable):**
    *   `01_CORE_Engine.json`
    *   `06_RANDOM_CUM_MECHANICS.json`

### Cấu hình Preset:
*   Sử dụng Preset: **`Tawa_Casual.json`**
*   *Đặc điểm:* Đã tắt các bộ từ vựng thô tục mạnh và các Engine thúc đẩy drama NSFW quá nhanh. Giữ nguyên phong cách kể chuyện thực tế, chậm rãi.

---

## 🔥 2. Chế độ HARDCORE (Thô tục, Drama mạnh)

Dùng khi bước vào các phân cảnh cao trào, yêu cầu ngôn từ trần trụi và các cơ chế đặc biệt như xuất tinh sớm lặp lại hoặc bụng phồng.

### Cấu hình Lorebook (World Info):
*   **BẬT (Enable):**
    *   `01_CORE_Engine.json`
    *   `06_RANDOM_CUM_MECHANICS.json`
    *   `Free Use.json` (Có thể bật để giữ luật thế giới)
    *   `！！Table - Worldbook` (Core)
    *   `02_ANATOMY_Body_Interaction.json` (Core)
    *   `04_MECHANICS_RPG.json` (Core)
*   **TẮT (Disable):**
    *   `03_FETISH_Casual.json` (Để tránh xung đột từ ngữ)

### Cấu hình Preset:
*   Sử dụng Preset: **`Tawa_Hardcore.json`** (hoặc bản gốc v3)
*   *Đặc điểm:* Kích hoạt toàn bộ các Engine: `Punpunn_Visual`, `erotic_intensity`, `erotic_simulation`. AI sẽ sử dụng ngôn từ cực kỳ táo bạo và mô tả chi tiết vật lý da thịt.

---

## 💡 Mẹo chuyển đổi nhanh (Pro Tips)

1.  **Sử dụng Groups trong World Info:** Bạn có thể gom các file vào Group `[CASUAL]` và `[HARDCORE]` trong SillyTavern để bật/tắt cả nhóm chỉ bằng một click.
2.  **Ưu tiên Model:** 
    *   Chế độ **Casual** hoạt động rất tốt với *Gemini 1.5 Flash* (Tiết kiệm token).
    *   Chế độ **Hardcore** nên dùng *Gemini 1.5 Pro* hoặc *Claude 3.5 Sonnet* để có sự mô tả sắc nét và logic sinh học chuẩn xác nhất.
3.  **Lưu ý về Token:** Bộ Hardcore tiêu tốn thêm khoảng 2000-3000 token so với bản Casual. Hãy chú ý thanh ngữ cảnh nếu bạn đang dùng các Model có giới hạn thấp.

---
*Tài liệu được tạo bởi AI để tối ưu trải nghiệm người dùng.*
