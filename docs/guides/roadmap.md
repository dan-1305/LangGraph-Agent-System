Chắc chắn rồi. Với vai trò là Giám đốc Sản phẩm, tôi sẽ tổng hợp các báo cáo QA và đưa ra một lộ trình phát triển tập trung vào các tính năng kỹ thuật cốt lõi cần thực hiện ngay. Đây là tài liệu để đội ngũ kỹ thuật bắt tay vào việc.

---

# 🚀 FLAGSHIP PROJECTS ROADMAP

## 1. AI Trading Agent

Dự án này đang ở mức "Proof of Concept". Ưu tiên hàng đầu là xây dựng nền tảng kỹ thuật vững chắc và khả năng đo lường hiệu quả trước khi thêm bất kỳ logic giao dịch phức tạp nào.

-   [ ] **Tính năng 1: Xây dựng Module Cấu hình và Bảo mật Tập trung.**
    *   **Mô tả:** Tạo một file `config.py` để quản lý tất cả các tham số hệ thống (tickers, ngưỡng giao dịch, đường dẫn, v.v.) và tích hợp thư viện `python-dotenv` để quản lý API keys và các thông tin nhạy cảm qua file `.env`.
    *   **Lý do:** Loại bỏ rủi ro bảo mật nghiêm trọng do hardcode API key và giúp hệ thống có thể được cấu hình, triển khai một cách linh hoạt mà không cần sửa đổi mã nguồn. Đây là yêu cầu bắt buộc để đưa dự án ra khỏi giai đoạn thử nghiệm.

-   [ ] **Tính năng 2: Xây dựng Module Báo cáo Hiệu suất (Performance Dashboard).**
    *   **Mô tả:** Code một module mới có chức năng ghi nhận, tính toán và xuất báo cáo các chỉ số tài chính cốt lõi sau mỗi phiên backtest hoặc giao dịch thực tế. Các chỉ số bắt buộc: PnL (Profit and Loss), ROI (Return on Investment), Sharpe Ratio, Max Drawdown, và Tỷ lệ thắng/thua.
    *   **Lý do:** Hiện tại chúng ta không thể đánh giá dự án có hiệu quả hay không. Module này cung cấp dữ liệu định lượng để chứng minh giá trị của sản phẩm và là cơ sở để ra quyết định cải tiến chiến lược.

-   [ ] **Tính năng 3: Tái cấu trúc và Chuẩn hóa Mã nguồn (Codebase Refactoring).**
    *   **Mô tả:** Áp dụng Type Hinting trên toàn bộ codebase. Chuẩn hóa việc quản lý đường dẫn bằng `pathlib` thay vì `sys.path`. Di chuyển các logic nghiệp vụ (như `mini_backtest.py`) về đúng thư mục chức năng. Tạo file `.gitignore` chuẩn.
    *   **Lý do:** Nâng cao chất lượng mã nguồn, giúp dễ bảo trì, giảm lỗi và tăng tốc độ phát triển trong dài hạn. Đây là việc đầu tư vào nền móng của dự án.

## 2. Auto Affiliate Video

Dự án có nền tảng kỹ thuật tốt nhưng lại như một "hộp đen" - chúng ta không biết nó hoạt động hiệu quả ra sao và chi phí thế nào. Các tính năng sau sẽ giải quyết vấn đề này.

-   [ ] **Tính năng 1: Xây dựng Hệ thống Cấu hình và Quản lý Secrets.**
    *   **Mô tả:** Tạo một file cấu hình tập trung (ví dụ: `config.yaml` hoặc `config.py`) để quản lý các tham số như đường dẫn, model prompts, v.v. Tích hợp `python-dotenv` để quản lý API keys của LLM và TTS qua file `.env`.
    *   **Lý do:** Giải quyết rủi ro bảo mật (lộ API key) và rủi ro bảo trì (hardcode tham số), giúp dự án dễ dàng cấu hình và triển khai trên các môi trường khác nhau.

-   [ ] **Tính năng 2: Xây dựng Module Đo lường và Ghi nhận (Analytics & Logging).**
    *   **Mô tả:** Code một module mới có chức năng ghi lại (log) các chỉ số hiệu suất cho mỗi lần tạo video:
        1.  **Thời gian thực thi:** Tổng thời gian và thời gian cho từng bước (tạo kịch bản, TTS, dựng video).
        2.  **Chi phí API:** Ghi nhận số token/ký tự đã sử dụng và ước tính chi phí cho mỗi dịch vụ (LLM, TTS).
        3.  **ID Video:** Gán một ID duy nhất cho mỗi video được tạo ra để theo dõi hiệu quả sau này.
    *   **Lý do:** Cung cấp dữ liệu định lượng để trả lời các câu hỏi cốt lõi: "Tạo một video tốn bao nhiêu tiền và thời gian?". Đây là cơ sở để tối ưu hóa quy trình và tính toán ROI.

## 3. SillyTavern World Card Generator

Dự án có kiến trúc tốt và đầu ra chất lượng, nhưng thiếu các tiêu chuẩn chuyên nghiệp để đảm bảo sự ổn định và dễ bảo trì.

-   [ ] **Tính năng 1: Nâng cấp Chất lượng và Tiêu chuẩn Mã nguồn.**
    *   **Mô tả:** Thực hiện một đợt refactor lớn: áp dụng Type Hinting và Docstrings cho tất cả các hàm và module. Đóng gói các script tiện ích trong cấu trúc `if __name__ == "__main__":` để có thể tái sử dụng và kiểm thử.
    *   **Lý do:** Tăng cường khả năng bảo trì, giảm thiểu lỗi tiềm ẩn và giúp các nhà phát triển mới dễ dàng tiếp cận dự án. Đây là bước cần thiết để chuyên nghiệp hóa sản phẩm.

-   [ ] **Tính năng 2: Xây dựng Module Đo lường Hiệu năng và Chi phí (Performance & Cost Tracking).**
    *   **Mô tả:** Tích hợp logic để đo lường và ghi nhận các KPI sau cho mỗi lần tạo thẻ:
        1.  Thời gian trung bình để tạo một thẻ.
        2.  Chi phí API (số token LLM sử dụng).
        3.  Tỷ lệ tạo thẻ thành công (không gặp `ValidationError`).
    *   **Lý do:** Cung cấp dữ liệu để xác định các điểm nghẽn về hiệu năng, tối ưu hóa chi phí và đánh giá độ ổn định của quy trình tạo thẻ.

-   [ ] **Tính năng 3: Xây dựng Giao diện Người dùng Nâng cao với Gradio/Streamlit.**
    *   **Mô tả:** Dựa trên roadmap đã có, bắt đầu xây dựng một giao diện người dùng mới bằng Gradio hoặc Streamlit, cho phép người dùng tùy chỉnh các tham số đầu vào (ví dụ: độ dài mô tả, phong cách, các yếu tố cần nhấn mạnh) thay vì chỉ chạy script.
    *   **Lý do:** Cải thiện đáng kể trải nghiệm người dùng, tăng tính tương tác và giá trị của công cụ. Đây là bước đi chiến lược để biến một công cụ nội bộ thành một sản phẩm tiềm năng.