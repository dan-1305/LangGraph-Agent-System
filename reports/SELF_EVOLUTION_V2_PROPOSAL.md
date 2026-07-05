# 🧬 SELF-EVOLUTION V2: META-MANAGEMENT ARCHITECTURE

**Status:** Proposed by [Architect]  
**Target:** CEO Cline Operations  
**Date:** 2026-07-07  

---

## 🏗️ 1. CẤU TRÚC KÝ ỨC THẤT BẠI (FAILURE MEMORY)
Hệ thống sẽ không còn "mù quáng" lặp lại các fix bug lỗi nhờ vào `logs/FAILED_PATHS.json`.
- **Cơ chế:** Mỗi khi `Test Pilot` báo `test_success = False`, hệ thống sẽ băm (hash) đoạn chỉ thị của `Triage Director` và lưu vào Blacklist.
- **Tác động:** CEO sẽ bị ép buộc phải thay đổi hướng tiếp cận (Paradigm Shift) thay vì xoáy sâu vào một lỗ hổng không thể vá.

## ⚖️ 2. HÀM ĐÁNH GIÁ CHIẾN LƯỢC (STRATEGIC FITNESS FUNCTION)
CEO không còn được phép tự do làm các dự án "ngoài luồng" quá lâu.
- **Rule:** Mọi Task phải được tag theo `Strategic Pillar` (Alpha, Stealth, Foundation).
- **Phạt (Penalty):** Nếu Task thuộc tag `[OUT_OF_SCOPE]`, hệ thống sẽ tự động giảm `recursion_limit` từ 15 xuống 5. Muốn tăng thêm phải có chữ ký điện tử của Boss.

## 🛠️ 3. NODE TIẾN HÓA (THE MUTATOR NODE)
Thêm một Node chạy ngầm cuối mỗi chu kỳ Auto-Pilot.
- **Nhiệm vụ:** Đọc `TRADING_LORE.md` và `FAILED_PATHS.json`.
- **Hành động:** Tự động đề xuất cập nhật `.clinerules` để tạo ra các "Genetic Constraints" mới.
- **Ví dụ:** Nếu fix UID Godot thất bại 5 lần -> Tự thêm luật: "Sử dụng GDRE Tools thay vì Regex cho mọi tác vụ Godot 4".

## 🚀 4. LỘ TRÌNH TRIỂN KHAI
1. **Giai đoạn 1:** Kích hoạt `FAILED_PATHS.json` (Đã xong).
2. **Giai đoạn 2:** Nâng cấp `triage_director.py` để tiêu thụ dữ liệu thất bại.
3. **Giai đoạn 3:** Hợp nhất Dashboard với Strategic Plan để hiển thị độ lệch mục tiêu (Drift Tracking).

---
*Kiến trúc này sẽ giúp CEO thoát khỏi cái bẫy "Cố chấp kỹ thuật" và thực sự trở thành một thực thể biết học hỏi.*
