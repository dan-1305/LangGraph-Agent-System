from gtts import gTTS
import os
from pathlib import Path
from projects.auto_affiliate_video.src.video_telemetry import measure_latency

class TTSEngine:
    """Động cơ chuyển đổi văn bản thành giọng nói (Text-to-Speech)."""
    
    def __init__(self, lang: str = "vi") -> None:
        """
        Sử dụng Google TTS (gTTS) mặc định để tránh lỗi mạng của edge-tts.
        
        Args:
            lang (str): Ngôn ngữ của giọng đọc, mặc định là "vi" (Tiếng Việt).
        """
        self.lang = lang

    @measure_latency("generate_audio")
    def generate_audio(self, text: str, output_path: str) -> tuple[str, int]:
        """
        Sinh ra file mp3 từ văn bản và trả về đường dẫn cùng số ký tự.
        """
        try:
            print(f"Đang tạo giọng đọc AI bằng Google TTS (Lang: {self.lang})...")
            # Đảm bảo thư mục tồn tại
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            tts = gTTS(text=text, lang=self.lang, slow=False)
            tts.save(output_path)
            
            char_count = len(text)
            print(f"Đã tạo Audio thành công: {output_path}")
            return output_path, char_count
        except Exception as e:
            print(f"Lỗi khi tạo TTS: {e}")
            return "", 0

if __name__ == "__main__":
    # Test script
    tts = TTSEngine()
    
    test_text = "Bạn có biết bàn phím cơ không dây Xinmeng đang làm mưa làm gió trên thị trường không? Bấm ngay vào link bên dưới để mua nhé!"
    
    # Đảm bảo thư mục tồn tại
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = str(output_dir / "test_voice.mp3")
    path, count = tts.generate_audio(test_text, output_file)
    if path:
        print(f"Test audio saved to {path}, characters: {count}")
