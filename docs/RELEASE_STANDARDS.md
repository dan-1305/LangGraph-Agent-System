# 🎯 BỘ TIÊU CHUẨN XUẤT XƯỞNG (RELEASE STANDARDS)
*[ACTIVE ROLE: Production Release Auditor]*

Đây là 4 tiêu chuẩn "Bọc Thép" bắt buộc mọi sản phẩm trong hệ sinh thái Jarvis (đặc biệt là các bản đóng gói bán cho Non-Tech) phải vượt qua trước khi tung ra thị trường (Commercialization). Nếu vi phạm dù chỉ 1 tiêu chuẩn, tuyệt đối không được Release!

---

## 1. TIÊU CHUẨN ZERO-SETUP (1-CLICK RUN)
**Vấn đề:** Khách hàng Non-tech không biết mở Terminal, không biết gõ `pip install`, không biết cài biến môi trường.
**Tiêu chuẩn:**
- Tích hợp sẵn môi trường **Portable Python** (thông qua `uv` hoặc `miniconda` folder).
- Tích hợp sẵn các file thực thi nhị phân phụ thuộc (VD: `ffmpeg.exe` cho Video Bot, `playwright` browsers cho Bot Cào Data) thẳng vào thư mục gốc.
- Phải có file **`Start.bat`** (trên Windows) bọc lệnh khởi chạy. Khách hàng chỉ cần giải nén và **Click đúp** là Web UI (Streamlit/FastAPI) sẽ tự động bật lên trên trình duyệt.

## 2. TIÊU CHUẨN ANTI-CRASH (BẢO VỆ GIAO DIỆN)
**Vấn đề:** Các lỗi vặt như mất mạng, API Key hết tiền, hoặc input rỗng có thể ném văng mã lỗi Python `Traceback` đỏ lòm lên màn hình, làm khách hàng hoảng sợ và đánh giá Tool là "Rác".
**Tiêu chuẩn:**
- Mọi logic gọi API mạng, xử lý file đều phải bọc trong khối `try...except`.
- Giao diện UI (Streamlit) chỉ được phép in ra các câu thông báo thân thiện (VD: `st.warning("⚠️ Mạng chậm, đang thử kết nối lại...")` hoặc `st.error("❌ Key API không hợp lệ, vui lòng kiểm tra lại tại Tab Config")`). CẤM để lọt Traceback ra UI.

## 3. TIÊU CHUẨN STATE RECOVERY (LƯU TIẾN TRÌNH TỰ ĐỘNG)
**Vấn đề:** Đang render video 99% hoặc bot đang chạy được nửa danh sách thì cúp điện/sập trình duyệt. Mở lên bắt chạy lại từ đầu sẽ khiến user tức điên.
**Tiêu chuẩn:**
- Mọi tiến trình dài hạn (Long-running task) phải ghi nhận trạng thái (Status, Progress) liên tục vào `SQLite` (Bật WAL mode) hoặc file `state.json`.
- Khi khởi động lại app, hệ thống tự động nhận diện tiến trình đang dang dở và đề xuất **Resume (Chạy tiếp)** thay vì Restart.

## 4. TIÊU CHUẨN TỐI GIẢN UI (IDIOT-PROOF DESIGN)
**Vấn đề:** Giao diện có quá nhiều thông số kỹ thuật (Temperature, Top-K, Prompt kỹ sư) làm người dùng bối rối.
**Tiêu chuẩn:**
- **Màn hình chính (Main Tab):** Chỉ để lại đúng 1-2 ô Input thiết yếu nhất (Ví dụ: "Nhập chủ đề video") và 1 nút bấm khổng lồ "🚀 CHẠY TỰ ĐỘNG".
- **Màn hình phụ (Advanced Config Tab):** Nơi giấu tất cả các cài đặt chuyên sâu (API Key, Chọn Model, System Prompt). Mặc định phải có giá trị Default chuẩn nhất, người dùng không chỉnh gì vẫn chạy tốt.

---
**🚀 Áp dụng Quy chuẩn:** Mọi bản cập nhật cho các sản phẩm Hero (VD: Auto Affiliate Video, X Bot) phải được dán nhãn "Passed Release Standards V1.0" trong Changelog.