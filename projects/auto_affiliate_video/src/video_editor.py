import os
from pathlib import Path
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

class VideoEditor:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.bg_dir = self.base_dir / "data" / "background_videos"
        self.output_dir = self.base_dir / "data" / "output"
        
        # Tạo thư mục nếu chưa có
        self.bg_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_short_video(self, audio_path: str, background_video_path: str, output_filename: str = "final_video.mp4"):
        """
        Ghép Audio AI vào Video Background.
        Tự động cắt video nền cho bằng với độ dài của Audio.
        Lưu ý: MoviePy có thể chạy chậm trên i3, nên render độ phân giải thấp (720p) trước để test.
        """
        print(f"🎬 Đang render video: {output_filename}...")
        
        try:
            if not os.path.exists(audio_path):
                print(f"❌ Không tìm thấy file âm thanh: {audio_path}")
                return False
                
            if not os.path.exists(background_video_path):
                print(f"❌ Không tìm thấy file video nền: {background_video_path}. Vui lòng tải video .mp4 bỏ vào folder 'data/background_videos'.")
                return False

            # Load Audio và Video
            audio = AudioFileClip(audio_path)
            video = VideoFileClip(background_video_path)
            
            # Xử lý độ dài: Cắt video sao cho bằng độ dài của audio
            if video.duration < audio.duration:
                # Nếu video ngắn hơn, lặp lại video (Loop)
                num_loops = int(audio.duration / video.duration) + 1
                video = concatenate_videoclips([video] * num_loops)
                
            # Cắt video đúng bằng độ dài audio
            video = video.subclip(0, audio.duration)
            
            # Gắn audio vào video
            final_video = video.set_audio(audio)
            
            # Xuất file (Lưu ý: dùng preset ultrafast để chạy nhẹ trên i3)
            output_path = str(self.output_dir / output_filename)
            final_video.write_videofile(
                output_path, 
                fps=30, 
                codec="libx264", 
                audio_codec="aac", 
                preset="ultrafast", 
                threads=1  # Limit thread để không treo máy i3
            )
            
            # Đóng file để giải phóng RAM
            audio.close()
            video.close()
            final_video.close()
            
            print(f"✅ Đã render thành công: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi dựng video: {e}")
            return False

if __name__ == "__main__":
    editor = VideoEditor()
    # Chạy lệnh này sẽ báo lỗi nếu bạn chưa bỏ file background_sample.mp4 vào thư mục.
    # editor.create_short_video("test_voice.mp3", "background_sample.mp4")