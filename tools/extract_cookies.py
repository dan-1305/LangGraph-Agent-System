import os
import json
import subprocess
from playwright.sync_api import sync_playwright

def extract_tiktok_cookies():
    """
    Script trích xuất Cookies tự động từ profile Microsoft Edge của Admin.
    Không cần đăng nhập lại, tái sử dụng trực tiếp session hiện có.
    """
    print("🚀 Đang khởi động Playwright với Microsoft Edge (Profile có sẵn)...")
    print("⚠️ LƯU Ý QUAN TRỌNG: Bạn PHẢI TẮT HẾT các cửa sổ Edge hiện tại trước khi chạy script này, nếu không Playwright sẽ bị lỗi locked.")
    
    cookies_path = "projects/auto_affiliate_video/data/tiktok_cookies.json"
    os.makedirs(os.path.dirname(cookies_path), exist_ok=True)
    
    # Đường dẫn tới Profile Edge của Windows mặc định
    edge_user_data_dir = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data")
    
    if not os.path.exists(edge_user_data_dir):
        print(f"❌ Không tìm thấy thư mục Profile Edge ở {edge_user_data_dir}")
        return

    # Tắt ép buộc Edge để tránh lỗi Lock Profile (Optional)
    try:
        subprocess.run(["taskkill", "/F", "/IM", "msedge.exe"], capture_output=True)
    except:
        pass
        
    with sync_playwright() as p:
        try:
            # Dùng launch_persistent_context để load thẳng Profile Edge thay vì tạo trình duyệt ảo trắng
            context = p.chromium.launch_persistent_context(
                user_data_dir=edge_user_data_dir,
                channel="msedge", # Ép buộc dùng Edge thay vì Chrome
                headless=False # Mở lên cho Admin thấy
            )
            
            page = context.pages[0] if context.pages else context.new_page()
            
            print("🌐 Đang mở trang chủ TikTok để quét Session...")
            page.goto("https://www.tiktok.com/")
            
            print("🕒 Chờ 5 giây để TikTok load xong và nhả cookie...")
            page.wait_for_timeout(5000)
            
            print("💾 Đang trích xuất và lưu Cookies...")
            cookies = context.cookies()
            
            # Ghi đè vào file JSON
            with open(cookies_path, "w") as f:
                json.dump(cookies, f)
                
            print(f"✅ Đã lưu thành công {len(cookies)} cookies vào {cookies_path}")
            
            # Kiểm tra xem có cookie đăng nhập ('sessionid') không
            has_session = any(c.get("name") == "sessionid" for c in cookies)
            if has_session:
                print("🌟 TUYỆT VỜI: Đã tìm thấy Session ID. Tức là Edge đã được đăng nhập TikTok!")
            else:
                print("⚠️ CẢNH BÁO: Chưa tìm thấy 'sessionid'. Vui lòng kiểm tra lại xem trên Edge bạn đã đăng nhập Tiktok thành công chưa.")
            
            context.close()
            
        except Exception as e:
            print(f"❌ Lỗi khi tải Profile Edge: {e}")
            print("💡 Hãy chắc chắn rằng BẠN ĐÃ TẮT TOÀN BỘ CỬA SỔ Microsoft Edge (kể cả chạy ngầm dưới khay hệ thống) trước khi chạy.")

if __name__ == "__main__":
    extract_tiktok_cookies()
