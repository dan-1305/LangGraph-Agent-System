import os
from projects.auto_affiliate_video.src.auto_uploader import AutoUploader

# Lấy video mp4 đầu tiên trong thư mục output
output_dir = "projects/auto_affiliate_video/data/output"
video_files = [f for f in os.listdir(output_dir) if f.endswith(".mp4")]

if not video_files:
    print("Khong tim thay video nao de test!")
else:
    video_path = os.path.join(output_dir, video_files[0])
    print(f"Dang test voi video: {video_path}")
    
    uploader = AutoUploader()
    uploader.upload_to_tiktok(video_path=os.path.abspath(video_path), caption="Test upload tu API #test")
