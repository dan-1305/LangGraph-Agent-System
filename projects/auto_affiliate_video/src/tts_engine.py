import edge_tts
import asyncio
from pathlib import Path

class TTSEngine:
    def __init__(self, voice="vi-VN-HoaiMyNeural"):
        """
        Khởi tạo Edge-TTS engine.
        Một số giọng tiếng Việt phổ biến:
        - vi-VN-HoaiMyNeural (Nữ, chuẩn, hay dùng review)
        - vi-VN-NamMinhNeural (Nam, trầm ấm)
        """
        self.voice = voice

    async def _generate_audio_async(self, text: str, output_path: str):
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)

    def generate_audio(self, text: str, output_path: str) -> str:
        """
        Tạo file âm thanh MP3 từ đoạn text bằng Edge-TTS (Dùng giọng AI Microsoft).
        Trả về đường dẫn file đã tạo.
        """
        print(f"🎙️ Đang tạo giọng đọc AI (Voice: {self.voice})...")
        try:
            asyncio.run(self._generate_audio_async(text, output_path))
            print(f"✅ Đã lưu file âm thanh tại: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Lỗi khi tạo TTS: {e}")
            return ""

if __name__ == "__main__":
    # Test script
    tts = TTSEngine()
    
    test_text = "Bạn có biết bàn phím cơ không dây Xinmeng đang làm mưa làm gió trên thị trường không? Bấm ngay vào link bên dưới để mua nhé!"
    
    # Đảm bảo thư mục tồn tại
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "data" / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = str(output_dir / "test_voice.mp3")
    tts.generate_audio(test_text, output_file)