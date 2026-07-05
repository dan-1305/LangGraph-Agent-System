# 📚 BÁCH KHOA TOÀN THƯ LỖI (ERROR ENCYCLOPEDIA)

Đây là Knowledge Base lưu trữ tất cả các lỗi đã từng xảy ra trong hệ sinh thái LangGraph Agent System, nguyên nhân gốc rễ và cách khắc phục triệt để. File này được tối ưu để hệ thống RAG có thể tìm kiếm và trích xuất dễ dàng.

---

## 1. LỖI: Silent Crash Telegram Alert (Không gửi được tin nhắn)
- **Triệu chứng (Symptoms):** Tác vụ chạy ngầm hoàn tất thành công (có log "Hoàn tất phiên cày cuốc"), nhưng Telegram không nhận được thông báo. Mở log ra không thấy ghi nhận lỗi `requests.post`.
- **Nguyên nhân gốc (Root Cause):** 
  - File code Python sử dụng sai tên biến môi trường (gọi `TELEGRAM_BOT_TOKEN` thay vì `TELE_TOKEN` như trong `.env`).
  - Lệnh `requests.post()` thiếu `response.raise_for_status()`, dẫn đến lỗi 401/404 bị bỏ qua trong im lặng (Silent Fail) và không chui vào khối `except Exception`.
- **Cách khắc phục triệt để (Action Item):**
  - Đồng bộ gọi `os.getenv("TELE_TOKEN")`.
  - Luôn thêm `response.raise_for_status()` ngay dưới `requests.post()`.

---

## 2. LỖI: UnicodeEncodeError: 'gbk' codec can't encode character (Windows CMD)
- **Triệu chứng (Symptoms):** Bot văng (Crash) ngay lập tức hoặc tiến trình `.bat` tự động đóng khi gọi lệnh `print()` chứa chuỗi tiếng Việt có dấu (VD: `print("Đang gửi...")`) hoặc Emoji.
- **Nguyên nhân gốc (Root Cause):** Hệ điều hành Windows sử dụng CMD/Powershell mặc định không phải mã hóa UTF-8. Khi Python cố in ký tự Unicode ra standard output của hệ thống, nó bị nghẹn và crash tiến trình.
- **Cách khắc phục triệt để (Action Item):**
  - Nếu chạy bằng file `.bat`: Phải bơm 2 lệnh sau lên ĐẦU file:
    ```bat
    chcp 65001 >nul
    set PYTHONIOENCODING=utf8
    ```
  - Nếu chạy tự động bằng `subprocess` trong Python (như file `dashboard.py` hay `scheduler/main_scheduler.py`), phải bơm biến môi trường trước khi gọi:
    ```python
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    subprocess.run([sys.executable, script_path], check=True, env=env)
    ```
    Hoặc ép stdout của sys: `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`

---

## 3. LỖI: ModuleNotFoundError hoặc ImportError (Lỗi Import File)
- **Triệu chứng (Symptoms):** Gọi chạy bot bị báo lỗi `ModuleNotFoundError: No module named 'src'`.
- **Nguyên nhân gốc (Root Cause):** Các file code (như `projects/ai_trading_agent/live_advisor.py`) gọi `from src.config import...` nhưng đang được execute ở thư mục không đúng, khiến Python không hiểu `src` nằm ở đâu.
- **Cách khắc phục triệt để (Action Item):**
  - Chèn đoạn code sau lên đầu file cần chạy để ép Python nhận diện thư mục root:
    ```python
    import sys, os
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if BASE_DIR not in sys.path:
        sys.path.append(BASE_DIR)
    ```

---

## 4. LỖI: Tự viết tay hàm gọi LLM bằng `requests.post()` gây lỗi 404, 429 hoặc Invalid API Key
- **Triệu chứng (Symptoms):** Lỗi `429 Too Many Requests`, `403 Quota Exceeded` hoặc `404 Client Error` khi AI tự ý dùng `requests.post` để gọi API. Hoặc báo lỗi kết nối do quên bật `local_proxy_server`.
- **Nguyên nhân gốc (Root Cause):** Hệ thống được bảo vệ bởi **Local Proxy Server** và lớp giáp `src.base_agent.BaseAgent`. Lớp này chứa cơ chế Fail-on-Demand Key Rotation, Endpoint chuẩn (`http://localhost:8000/v1`), Retry (Tenacity) và Caching. Việc AI tự viết tay `requests.post` phá vỡ toàn bộ kiến trúc này, không được hưởng quyền lợi xoay vòng API Key khi hết Quota, dẫn đến crash dự án.
- **Cách khắc phục triệt để (Action Item):**
  - **TỬ HÌNH KHÔNG CÓ NGOẠI LỆ:** CẤM TUYỆT ĐỐI việc import `requests` để tự post data gọi LLM.
  - Đảm bảo **Local Proxy Server** đang chạy nền ở cổng `8000`.
  - Bắt buộc phải import và kế thừa `BaseAgent`:
    ```python
    from src.base_agent import BaseAgent
    class MyAgent(BaseAgent):
        def __init__(self):
            super().__init__(model_name="gemini-3-flash-preview")
        def do_something(self):
            result = self._call_llm_with_retry("Prompt của bạn")
    ```
