# 🗺️ KẾ HOẠCH NÂNG CẤP ĐẾ CHẾ SOVEREIGN (V3.0)

Tài liệu này định nghĩa lộ trình nâng cấp hệ thống trung tâm và các Agent vệ tinh theo mô hình phân cấp Tier List.

---

## 🟢 TIER 0: THE SOVEREIGN CORE (Hệ thống Trung tâm)
**Mục tiêu:** Xây dựng bộ não bất tử, không bao giờ mất trí nhớ và có kỷ luật thép.

1. **Sovereign Awakening System (SIP):**
   - Triển khai script `tools/system/awaken.py` để tự động khôi phục ngữ cảnh.
   - Bắt buộc thực thi One-Command Awakening khi bắt đầu phiên mới.
2. **Principles Enforcer Integration:**
   - Nhúng `PrinciplesEnforcer` vào luồng `Triage Director` để kiểm soát chất lượng từ đầu vào.
3. **Managerial Leverage Engine:**
   - CEO không làm việc của cấp dưới. CEO chỉ phân tích báo cáo và ra phán quyết "Phê duyệt" hoặc "Yêu cầu sửa lại".

---

## 🔵 TIER 1: STRATEGIC SPECIALISTS (Chuyên gia)
**Mục tiêu:** Chuyên môn hóa sâu dựa trên tri thức từ 16 siêu phẩm.

1. **Market Wizards (Trading):**
   - Áp dụng 100% SEPA, VCP và Stage Analysis cho Technical Agent.
   - Sentiment Agent phải phân tích được Whale Behavior và Liquidation Gaps.
2. **Cyber Security Sentinel:**
   - Chuyển đổi DRM sang dạng Integrity-based Protection (Kiểm soát tính toàn vẹn nhị phân).
3. **Knowledge Librarian:**
   - Tự động hóa việc gắn thẻ (Tagging) và nén tri thức (Compression) để RAG luôn chính xác.

---

## 🟡 TIER 2: EXECUTION DRONES (Thực thi)
**Mục tiêu:** Chuẩn hóa đầu ra, tự động hóa sửa lỗi.

1. **Structured Output Enforcement:**
   - Mọi Agent thực thi phải trả về Pydantic Objects.
2. **Self-Healing Loop:**
   - Nếu QA báo lỗi, Coder phải đọc `FAILED_PATHS.json` trước khi sửa.
3. **Managerial Reporting:**
   - Tự động xuất báo cáo hiệu suất (KPI) sau mỗi Task lớn.

---

## 🧠 GIAO THỨC CHỐNG "LÚ" (Anti-Amnesia Protocol)

Mỗi khi phiên làm việc kết thúc, hệ thống BẮT BUỘC thực hiện:
1. Ghi tóm tắt trạng thái hiện tại vào `context/ACTIVE_THOUGHTS.md`.
2. Chạy `auto_mapper.py` để cập nhật bản đồ hệ thống.
3. Chạy `rag_ingest.py` để đồng bộ tri thức mới.

*Phê duyệt bởi CEO Sovereign ngày 2026-07-08.*
