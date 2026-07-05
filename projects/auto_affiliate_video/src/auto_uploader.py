import os
import json
from tiktok_uploader.upload import upload_video
from tiktok_uploader.auth import AuthBackend

class AutoUploader:
    """Module tự động upload video lên mạng xã hội (TikTok/Shorts) sử dụng tiktok-uploader."""
    
    def __init__(self):
        pass

    def upload_to_tiktok(self, video_path: str, caption: str) -> bool:
        if not os.path.exists(video_path):
            print(f"Loi: File video khong ton tai {video_path}")
            return False
            
        cookie_path = "projects/auto_affiliate_video/data/tiktok_cookies.json"
        if not os.path.exists(cookie_path):
            print(f"Loi: Khong tim thay file {cookie_path}. Vui long chay tools/extract_cookies.py truoc.")
            return False
            
        print(f"Bat dau qua trinh Upload len TikTok...\nVideo: {video_path}\nCaption: {caption}")
        
        try:
            # Load cookies from json
            # with open(cookie_path, 'r') as f:
            #     cookies = json.load(f)
            
            # tiktok_uploader expects a path to a cookies.txt file or dictionary, or Playwright JSON
            # However it natively supports Playwright JSON format
            
            print("Goi tiktok-uploader API...")
            
            upload_video(
                video_path,
                description=caption,
                cookies=cookie_path, # Pass the path to cookies json
                headless=False # Set to False for debugging, True for production
            )
            
            print("AutoUploader: Upload thanh cong!")
            return True
            
        except Exception as e:
            print(f"Loi khi upload bang tiktok-uploader: {e}")
            return False
