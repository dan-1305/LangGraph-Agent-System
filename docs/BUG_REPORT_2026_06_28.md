# 🐛 BÁO CÁO FIX BUG TỔNG HỢP (Ngày 28/06/2026)

Tài liệu này ghi chú lại những lỗi (Bugs) cực kỳ hóc búa đã được xử lý trong phiên làm việc hôm nay. Đây là những lỗi đặc thù của Python và kiến trúc hệ thống lớn, lưu lại để làm "sách giáo khoa" cho các đợt maintain sau này.

---

## 1. Vụ án PyTest sập toàn tập: `ValueError: underlying buffer has been detached`
- **Tình trạng:** Khi gõ `uv run pytest tests/`, toàn bộ framework Test văng lỗi và báo `collected 0 items`.
- **Nguyên nhân gốc rễ (Root Cause):** Để hiển thị Emoji trên CMD Windows không bị lỗi `gbk`, các file Python trong dự án lạm dụng dòng code `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`. Khi PyTest chạy, nó tạo ra một phễu ảo (CaptureManager) để gom log, phễu này KHÔNG CÓ `.buffer`. Lệnh kia đã chọc thủng phễu của PyTest khiến nó sập.
- **Cách khắc phục:** Viết script `patch_stdout.py` quét 37 file Python trong dự án và thay thế bằng lệnh chuẩn tắc của Python 3.7+:
  ```python
  if hasattr(sys.stdout, 'reconfigure'):
      sys.stdout.reconfigure(encoding='utf-8')
  ```

---

## 2. Vụ án Naming Collision: `ModuleNotFoundError: No module named 'src.database'`
- **Tình trạng:** `live_advisor.py` và `full_auto_cli.py` liên tục báo không tìm thấy module `src` mặc dù thư mục rõ ràng đang sờ sờ ra đó.
- **Nguyên nhân gốc rễ:** Hệ thống có thư mục gốc là `src/` và các dự án con cũng có thư mục `src/` (vd: `projects/ai_trading_agent/src/`). Do các thư mục này đều chứa file `__init__.py`, Python coi chúng là các "Regular Package" độc lập. Khi script chạy ở thư mục con, nó tìm thấy `src/` nội bộ và DỪNG TÌM KIẾM, dẫn đến không thấy các file ở `src/` gốc.
- **Cách khắc phục:** Đã **XÓA BỎ** các file `__init__.py` ở cả `src/` gốc và `src/` con. Đưa chúng về dạng **Namespace Packages** (Tính năng của Python 3.3+). Nhờ vậy, Python tự động "gộp" (merge) tất cả các thư mục `src` lại với nhau trên `sys.path`, giúp `src.database` và `src.factory` chung sống hòa bình.

---

## 3. Vụ án PnL bị âm 74,000 USD (-88%) trong AI Trading
- **Tình trạng:** Bot báo lỗ khổng lồ dù đang cầm 10,000 USDT.
- **Nguyên nhân gốc rễ:** Thuật toán tính PnL `daily_pnl` lấy mốc tham chiếu là `paper_history[-1][1]`. Lệnh này bốc đúng cái record **cũ nhất** trong giới hạn 100 dòng của DB (vô tình trúng ngày 15/06).
- **Cách khắc phục:** Viết lại vòng lặp duyệt ngược `paper_history`, tìm đúng record đầu tiên có chữ `2026-06-28` (hoặc lấy record cuối cùng của ngày hôm qua nếu sáng nay chưa chạy).

---

## 4. Vụ án Airdrop Guerrilla "phân thân" nhiều lần buổi sáng
- **Tình trạng:** Sáng ra bật máy, Bot Airdrop nhảy ra cày 3-4 lần liên tục.
- **Nguyên nhân gốc rễ (Race Condition):** Hàm `update_job_state()` (lưu ngày giờ đã chạy) bị đặt ở TẬN CÙNG sau khi Bot cày xong (mất cả tiếng đồng hồ). Trong lúc nó đang cày, nếu Scheduler quét lại, nó thấy "Ủa hôm nay chưa chạy" nên lại spawn thêm 1 con Bot nữa.
- **Cách khắc phục:** Dời `update_job_state()` (Lock State) lên ĐẦU TIÊN ngay trước khi kích hoạt Bot. Đánh dấu "đã cày" ngay lập tức để chặn các luồng khác.

---

## 5. Vụ án Blockscout Soneium báo lỗi 422
- **Tình trạng:** Giao dịch Airdrop báo thành công trên Terminal, nhưng bấm vào link Explorer thì web Blockscout báo `422 Request cannot be processed`.
- **Nguyên nhân gốc rễ:** Hàm `tx_hash.hex()` của thư viện `web3.py` trả về chuỗi hash **KHÔNG có chữ `0x` ở đầu**. Blockscout bắt buộc URL phải có `0x`, nếu không nó sẽ quăng lỗi 422.
- **Cách khắc phục:** Cập nhật `evm_base.py`, thêm đoạn code kiểm tra và gắn `0x` vào `tx_hex`:
  ```python
  if not tx_hex.startswith("0x"):
      tx_hex = "0x" + tx_hex
  ```

---
*Kết luận: Đừng khinh thường các lỗi nhỏ lặt vặt. Một hệ thống đồ sộ như LangGraph Agent System đòi hỏi sự nghiêm ngặt về Namespace, File Locking và System Path để có thể chạy mượt mà 24/7.*