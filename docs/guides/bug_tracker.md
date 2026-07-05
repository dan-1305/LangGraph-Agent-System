# 🚨 URGENT TECH DEBT & BUG TRACKER

*Báo cáo tự động từ phiên làm việc ngày 2026-06-17/18*

## 🔴 BUG 1: Airdrop Guerrilla "Đột Tử" Hậu Refactor
- **Tình trạng:** Module `Airdrop Guerrilla` trước đây hoạt động bình thường, nhưng sau đợt tái cấu trúc (chia 4 Tiers, áp dụng phân mảnh `.clinerules`) thì không thể chạy được nữa.
- **Giả thuyết nguyên nhân (Cần rà soát gấp):**
  1. **Gãy Import Paths:** Quá trình di dời file (vệ sinh thư mục `tools/` và đưa về đúng Tier) có thể đã làm đứt gãy dependency nội bộ của Airdrop.
  2. **Vi phạm Strict Data Contracts:** BaseAgent mới ép Pydantic Validation quá chặt. Dữ liệu đầu vào của Airdrop (kiểu cũ) có thể đang bị reject.
  3. **Vướng API Guard:** Cấu hình mới ép dùng `httpx` và kiểm soát gọi mạng khắt khe. Có thể agent Airdrop đang cố gọi các RPC Node (ZkSync, Linea...) và bị chặn đứng lại bởi hệ thống bảo vệ.
- **Yêu cầu hành động cho Ca sau:** Đọc lại trace log của Airdrop Guerrilla, đối chiếu với bộ Global Rules mới ở root để tìm điểm xung đột logic và vá lại ngay lập tức. (File `wallet_manager.py` vừa được revert về nguyên bản để user test lại với .env mới).

## 🟡 BUG 2: Streamlit Dashboard UI "Lỏ" & Đối Phó
- **Tình trạng:** UI V1 xây dựng cẩu thả, mang tính chất hardcode đối phó, không phản ánh đúng kiến trúc động của dự án.
- **Lỗi cụ thể:**
  1. **Hardcode phi logic:** Dự án có 11 sub-projects nhưng lại hardcode hiển thị cố định đúng 3 projects (Trading, Airdrop, QA). 
  2. **Mất Schema Mapping:** Các tham số quan trọng (như chọn Network của Airdrop) lẽ ra phải là Dropdown list lấy từ Pydantic Schema, nhưng hiện tại lại render thành ô nhập Text tự do, cực kỳ dễ gây lỗi typo.
- **Trạng thái:** ✅ **Đã xử lý (Fixed)** - Đã cập nhật thành `tools/ui/dashboard_app.py` với tính năng **Dynamic Scanner** quét tự động thư mục `projects/`.

## 🟢 BUG 3: Rate Limit & Lỗi sập API GCLI (Đã giải quyết)
- **Tình trạng:** Tài khoản Gemini Free Tier thường xuyên bị cạn Quota (Lỗi 429), kết hợp với sự mất ổn định của trạm proxy GCLI bên ngoài khiến toàn bộ hệ thống bị tê liệt liên tục.
- **Trạng thái:** ✅ **Đã xử lý (Fixed)** triệt để thông qua kiến trúc **Local Proxy Server**.
- **Cơ chế:** Proxy nội bộ chạy ở `http://localhost:8000` được trang bị **Fail-on-Demand Key Rotation**. Khi một key trong danh sách `GEMINI_API_KEYS` bị lỗi 429/403, proxy sẽ âm thầm chuyển sang key khác và retry mà Agent không hề bị ngắt kết nối.
