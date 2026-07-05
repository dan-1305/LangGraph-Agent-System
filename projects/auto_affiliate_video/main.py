import os
from pathlib import Path
from src.script_generator import ScriptGenerator
from src.tts_engine import TTSEngine
from src.video_editor import VideoEditor

def main():
    print("="*50)
    print("🚀 AUTO-AFFILIATE VIDEO GENERATOR")
    print("="*50)
    
    # Cấu hình sản phẩm
    product_name = input("Nhập tên sản phẩm (VD: Robot Hút Bụi Xiaomi): ")
    key_features = input("Nhập 2-3 tính năng nổi bật: ")
    bg_video_name = input("Nhập tên file video nền (VD: background_1.mp4): ")
    
    if not product_name:
        product_name = "Tai nghe Bluetooth Sony"
        key_features = "Chống ồn chủ động, Pin 30 tiếng, Bass cực căng"
        bg_video_name = "sample.mp4"
        print(f"\n⚠️ Dùng cấu hình mẫu: {product_name}")

    base_dir = Path(__file__).resolve().parent
    output_dir = base_dir / "data" / "output"
    bg_dir = base_dir / "data" / "background_videos"
    
    # 1. Tạo kịch bản
    sg = ScriptGenerator()
    script = sg.generate_short_video_script(product_name, key_features)
    print("\n[KỊCH BẢN]")
    print(script)
    print("-" * 50)
    
    # 2. Tạo Audio
    tts = TTSEngine()
    audio_filename = f"{product_name.replace(' ', '_').lower()}_audio.mp3"
    audio_path = str(output_dir / audio_filename)
    audio_path = tts.generate_audio(script, audio_path)
    
    if not audio_path:
        print("❌ Dừng quá trình do lỗi tạo Audio.")
        return

    # 3. Ghép Video
    bg_path = str(bg_dir / bg_video_name)
    if not os.path.exists(bg_path):
        print(f"\n⚠️ KHÔNG TÌM THẤY VIDEO NỀN: {bg_path}")
        print("💡 HƯỚNG DẪN: ")
        print("1. Tải một đoạn video nền (ví dụ cảnh thiên nhiên, đường phố, hoặc quay sản phẩm) từ Pexels/Pixabay.")
        print(f"2. Bỏ vào thư mục: {bg_dir}")
        print(f"3. Đặt tên file là: {bg_video_name} và chạy lại.")
        return
        
    editor = VideoEditor()
    output_video_name = f"{product_name.replace(' ', '_').lower()}_final.mp4"
    success = editor.create_short_video(audio_path, bg_path, output_video_name)
    
    if success:
        print("\n🎉 HOÀN TẤT!")
        print(f"Video đã sẵn sàng để up lên TikTok/Shorts: {output_dir / output_video_name}")
        print("Đừng quên gắn Link Affiliate vào bio hoặc mô tả nhé!")

if __name__ == "__main__":
    main()