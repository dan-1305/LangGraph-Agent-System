# Universal Web Scraper - Project Summary & Guide

## 1. Tổng quan dự án
Universal Web Scraper là một dự án chuyên thu thập (cào) dữ liệu từ các trang web đa dạng. Dự án này hỗ trợ cả hai phương pháp:
- **Scraping tĩnh (Basic):** Sử dụng thư viện `requests` để tải mã nguồn HTML cơ bản.
- **Scraping động (Advanced):** Sử dụng Playwright để vượt qua các cơ chế chặn bot, render JavaScript và tương tác với trang web (đã tích hợp cho các trang bất động sản như alonhadat, batdongsan).

## 2. Các tệp tin cốt lõi (Core Files) - CẦN ĐỌC KHI MỞ CHAT MỚI
Nếu bắt đầu một phiên chat mới và cần làm việc với dự án này, hãy đọc các tệp sau đầu tiên để lấy ngữ cảnh:
- `main.py`: File chạy chính cho phương pháp scraping tĩnh (sử dụng `requests` kèm headers giả lập browser).
- `src/batdongsan_playwright.py` & `src/alonhadat_playwright.py`: Các script sử dụng Playwright để xử lý các trang bất động sản có cơ chế chặn bot nâng cao.
- `src/parser.py` / `src/alonhadat_parser.py`: Các script đảm nhận việc bóc tách dữ liệu (Parsing) từ HTML thô ra dữ liệu có cấu trúc.

## 3. Cấu trúc thư mục
- `main.py`: Entry point cơ bản để tải HTML.
- `src/`: Thư mục mã nguồn chính, bao gồm các kịch bản Playwright, kịch bản bóc tách dữ liệu (parser) và xử lý làm sạch dữ liệu (`cleaner.py`).
- `data/raw/`: Lưu trữ các file HTML thô sau khi tải về (VD: `full_page.html`).
- `data/output/`: Nơi lưu trữ kết quả cuối cùng dưới dạng file CSV/Log (VD: `alonhadat_dongnai.csv`, `batdongsan_dongnai_pw.csv`).

## 4. Luồng hoạt động chính
1. **Thu thập dữ liệu (Fetch/Scrape):** Dùng `requests` (cho web đơn giản) hoặc `playwright` (cho web phức tạp/chống bot) tải HTML thô về thư mục `data/raw/`.
2. **Bóc tách (Parse):** Đọc HTML thô, dùng parser để trích xuất các trường thông tin cần thiết (Tiêu đề, Giá, Diện tích, v.v.).
3. **Làm sạch (Clean):** Xử lý, chuẩn hóa các định dạng dữ liệu (ví dụ: đổi chuỗi giá thành số).
4. **Xuất file (Export):** Lưu dữ liệu đã xử lý vào thư mục `data/output/` dưới dạng `.csv`.

## 5. Lưu ý quan trọng
- Máy đang sử dụng cấu hình i3-1215u, việc sử dụng Playwright mở nhiều tab/trình duyệt cùng lúc (Song song/Concurrency) sẽ làm quá tải hệ thống. Phải luôn chạy tuần tự (Sequential) hoặc set `n_jobs=1`.
- Project có module Playwright tích hợp, hãy kiểm tra các thay đổi về thẻ HTML/Classes của trang web mục tiêu vì chúng rất dễ thay đổi theo thời gian.