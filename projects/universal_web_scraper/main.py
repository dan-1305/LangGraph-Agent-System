import os
import requests
from pathlib import Path

# Cấu hình đường dẫn
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_FILE = RAW_DIR / "full_page.html"

# Bộ headers giả lập Browser (Chống bot-block cơ bản)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def download_html(url: str) -> bool:
    """
    Tải toàn bộ mã nguồn HTML từ một URL và lưu vào file cục bộ.
    
    Args:
        url (str): Đường dẫn trang web cần cào dữ liệu.
        
    Returns:
        bool: True nếu tải và lưu thành công, False nếu thất bại.
    """
    print(f"[*] Đang tiến hành kết nối tới: {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()  # Báo lỗi nếu HTTP Status != 200
        
        # Lưu file
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"[+] Thành công! HTML đã được lưu tại: {OUTPUT_FILE}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"[-] Lỗi khi kết nối hoặc tải trang: {e}")
        return False
    except Exception as e:
        print(f"[-] Đã xảy ra lỗi hệ thống: {e}")
        return False

def main():
    print("=== UNIVERSAL WEB SCRAPER ===")
    
    # Cho phép người dùng nhập từ CLI hoặc tự động fallback (tiện cho test tự động)
    try:
        url = input("Nhập URL cần cào dữ liệu: ").strip()
    except EOFError:
        url = ""
        
    if not url:
        print("[!] Không nhận được URL, sử dụng URL test mặc định...")
        url = "https://example.com"
        
    if not url.startswith("http"):
        url = "https://" + url
        
    download_html(url)

if __name__ == "__main__":
    main()
