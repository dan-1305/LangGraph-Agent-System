# 🚨 PENDING TECHNICAL DEBT (NỢ KỸ THUẬT ĐANG CHỜ XỬ LÝ)

*Tài liệu này lưu trữ các điểm nghẽn (bottlenecks) và lỗi phát sinh trong quá trình Benchmark (The Grand Arena) của hệ thống. Những mục này cần được ưu tiên xử lý trong các phiên làm việc tiếp theo.*

---

## 1. Tàn dư Dependency (Dependency Debt) (ĐÃ GIẢI QUYẾT)
- Toàn bộ `requirements.txt` rác trong các sub-project (`ai_trading_agent`, `auto_affiliate_video`, `airdrop_guerrilla`, `sillytavern_world_card_generator`, `jarvis-rpg-assistant`) đã được dọn dẹp sạch sẽ để tuân thủ `uv workspace`.

## 2. Vi phạm Trụ cột Sinh Tồn (Circuit Breaker Debt) (ĐÃ GIẢI QUYẾT)
- Toàn bộ 4 file vi phạm đã được refactor để sử dụng `create_fallback_chain` của thư mục lõi `src/`. Hệ thống được bọc an toàn.

## 3. Phân mảnh Kiến trúc (Architectural Fragmentation) (ĐÃ GIẢI QUYẾT)
- Dự án `jarvis-rpg-assistant` đã được sáp nhập đồng bộ với kiến trúc Fallback Chain lõi, loại bỏ hơn hàng trăm dòng code tự chế dư thừa (DRY).

*(Lưu ý: Các lỗi về API Rate Limit 429, Schema Hallucination và Blank Hallucination ở tầng lõi BaseAgent ĐÃ ĐƯỢC GIẢI QUYẾT thông qua việc áp dụng Tenacity Jitter Backoff và Langchain `with_structured_output`.)*
