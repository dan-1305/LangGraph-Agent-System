import asyncio
import os
from pathlib import Path
import edge_tts
from pydub import AudioSegment
import sys

# Setup relative paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR.parent.parent))

class TTSEngine:
    """Dong co chuyen doi van ban thanh giong noi (TTS) da ngon ngu cao cap."""
    
    def __init__(self, voice: str = "vi-VN-HoaiMyNeural"):
        self.voice = voice
        self.output_dir = BASE_DIR / "data" / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_audio(self, text: str, filename: str) -> str:
        """Sinh ra file mp3 tu van ban bang Edge-TTS."""
        output_path = self.output_dir / filename
        print(f"🎙️ Dang tao giong doc AI (Voice: {self.voice})...")
        
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(str(output_path))
        
        # [UPGRADE] Them hieu ung Fade-out bang pydub
        self._apply_audio_effects(output_path)
        
        return str(output_path)

    def _apply_audio_effects(self, audio_path: Path):
        """Ap dung cac hieu ung am thanh chuyen nghiep."""
        try:
            audio = AudioSegment.from_mp3(str(audio_path))
            # Fade out 2 giay o cuoi
            fade_out_duration = 2000 # ms
            audio = audio.fade_out(fade_out_duration)
            audio.export(str(audio_path), format="mp3")
            print("🔊 Da ap dung hieu ung Fade-out chuyen nghiep.")
        except Exception as e:
            print(f"⚠️ Khong the ap dung hieu ung am thanh: {e}")

if __name__ == "__main__":
    engine = TTSEngine()
    test_text = "Chào mừng bạn đến với vương triều AI Sovereign. Chúng tôi đang kiến tạo tương lai."
    asyncio.run(engine.generate_audio(test_text, "test_pro.mp3"))
