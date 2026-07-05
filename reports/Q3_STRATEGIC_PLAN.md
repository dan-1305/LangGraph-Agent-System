# 🗺️ STRATEGIC PLAN Q3-Q4 2026: THE CEO DIRECTIVE

*Dựa trên kết quả Audit toàn diện ngày 2026-07-05, tôi - CEO Cline - vạch ra lộ trình chiến lược nhằm tối ưu hóa lợi nhuận và bọc thép hệ thống.*

---

## 🎯 1. CÁC MỤC TIÊU TRỌNG ĐIỂM (CORE OBJECTIVES)

### 📈 CHIẾN DỊCH ALPHA: NÂNG CẤP TRADING AGENT
- **Hành động:** Ép `ai_trading_agent` kế thừa `BaseAgent` để đồng bộ hóa tri thức.
- **Tối ưu:** Chuyển đổi sang model `gemini-3.1-flash-lite` để vận hành 24/7 với chi phí 0đ.
- **Tính năng:** Nghiên cứu giải pháp scraping tin tức Whale miễn phí để khôi phục "Whale Alert".

### 🥷 CHIẾN DỊCH STEALTH: CỨU VIỆN AIRDROP BOT
- **Hành động:** Giải quyết bài toán timeout khi gặp Cloudflare Turnstile nhúng trong Iframe.
- **Bảo mật:** Rà soát và mã hóa toàn bộ Session trong `./chrome_profile`.
- **Hạ tầng:** Tích hợp cơ chế xoay Proxy tự động để tránh bị chặn IP diện rộng.

### 🧩 CHIẾN DỊCH NỀN TẢNG: UNIFIED MONOREPO
- **Hành động:** Xóa bỏ hoàn toàn các folder rác, đóng gói các project simulation không còn giá trị kinh doanh.
- **Đồng bộ:** Buộc mọi dự án phải có `pyproject.toml` và `.env.example` chuẩn chỉnh.

---

## 🛠️ 2. QUY TRÌNH "HẬU VỆ" (DEFENSIVE PROTOCOL)
1.  **Circuit Breaker:** Kích hoạt cầu dao cứng trên toàn hệ thống (Abort sau 3 lỗi lặp lại).
2.  **Sentinel Backup:** Tự động Full Backup vào ổ D sau mỗi task lớn.
3.  **Cross-Role Debate:** Mọi thay đổi code lõi phải được duyệt qua `context/DEBATE_ROOM.md`.

---

## 📅 3. LỘ TRÌNH THỰC THI (TIMELINE)
- **Tuần 1:** Đồng bộ hóa `BaseAgent` cho toàn bộ Monorepo.
- **Tuần 2:** Fix lỗi Cloudflare cho Airdrop Bot.
- **Tuần 3:** Stress Test hệ thống Trading trên môi trường thực tế.

---
*Phê duyệt bởi: [CEO Cline Operations]*
*Lệnh thực thi: [IMMEDIATE]*
