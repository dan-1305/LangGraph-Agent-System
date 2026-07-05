import os
import time
import argparse
import sys
from pathlib import Path

# Setup Path để đảm bảo root được nhận diện (Sửa lỗi ModuleNotFoundError: No module named 'projects')
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import logging
from projects.auto_affiliate_video.src.config import Config
from projects.auto_affiliate_video.src.analytics import VideoAnalytics
from projects.auto_affiliate_video.src.script_generator import ScriptGenerator
from projects.auto_affiliate_video.src.tts_engine import TTSEngine
from projects.auto_affiliate_video.src.video_editor import VideoEditor
from projects.auto_affiliate_video.src.broll_fetcher import BRollFetcher

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.PROJECT_ROOT / "data/video_generation.log", encoding='utf-8', mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main() -> None:
    """Hàm main điều phối quá trình tự động tạo video Affiliate."""
    parser = argparse.ArgumentParser(description="Auto Affiliate Video Generator")
    parser.add_argument("--product", type=str, default="Tai nghe Bluetooth Sony", help="Tên sản phẩm cần tạo video")
    parser.add_argument("--features", type=str, default="Chống ồn chủ động, Pin 30 tiếng, Bass cực căng", help="Tính năng nổi bật")
    parser.add_argument("--query", type=str, default=None, help="Từ khóa tìm video nền (tiếng Anh)")
    
    args = parser.parse_args()
    
    logging.info("="*50)
    logging.info("AUTO-AFFILIATE VIDEO GENERATOR")
    logging.info("="*50)
    
    analytics = VideoAnalytics()
    
    try:
        product_name = args.product
        key_features = args.features
        bg_query = args.query if args.query else f"technology {product_name.split()[0]}"
        
        logging.info(f"Sản phẩm: {product_name}")
        logging.info(f"Tính năng: {key_features}")

        analytics.set_product(product_name)
        
        # 1. Tạo kịch bản
        t0 = time.time()
        sg = ScriptGenerator()
        script, llm_tokens = sg.generate_short_video_script(product_name, key_features)
        analytics.log_step_time("script", t0)
        analytics.log_usage(llm_tokens=llm_tokens)
        logging.info("[KỊCH BẢN]")
        logging.info(script)
        
        # 2. Tạo Audio
        t1 = time.time()
        tts = TTSEngine()
        audio_filename = f"{product_name.replace(' ', '_').lower()}_audio.mp3"
        audio_path = str(Config.OUTPUT_DIR / audio_filename)
        audio_path, tts_chars = tts.generate_audio(script, audio_path)
        analytics.log_step_time("tts", t1)
        analytics.log_usage(tts_chars=tts_chars)
        
        if not audio_path:
            logging.error("Dừng quá trình do lỗi tạo Audio.")
            analytics.save_metrics(success=False)
            return

        # 3. Tải Video Nền (B-Roll)
        t2 = time.time()
        broll_fetcher = BRollFetcher()
        bg_path = broll_fetcher.fetch_video(query=bg_query, output_filename="auto_bg.mp4")
        analytics.log_step_time("broll", t2)
        
        if not bg_path or not os.path.exists(bg_path):
            logging.warning("Không thể tải video nền tự động, sẽ sử dụng video nền mặc định.")
            default_videos = list(Config.BG_DIR.glob("*.mp4"))
            if not default_videos:
                logging.error("Không tìm thấy video nền mặc định nào trong data/background_videos. Dừng chương trình.")
                analytics.save_metrics(success=False)
                return
            bg_path = str(default_videos[0])
            logging.info(f"Sử dụng video nền mặc định: {bg_path}")
            
        # 4. Ghép Video
        t3 = time.time()
        editor = VideoEditor()
        output_video_name = f"{product_name.replace(' ', '_').lower()}_final.mp4"
        success = editor.create_short_video(audio_path, bg_path, output_video_name, script_text=script)
        analytics.log_step_time("render", t3)
        
        analytics.save_metrics(success=success)
        
        if success:
            logging.info("HOÀN TẤT!")
            logging.info(f"Video đã sẵn sàng để up lên TikTok/Shorts: {Config.OUTPUT_DIR / output_video_name}")
            logging.info("Đừng quên gắn Link Affiliate vào bio hoặc mô tả nhé!")
    
    except Exception as e:
        logging.error(f"Đã xảy ra lỗi hệ thống: {e}", exc_info=True)
        analytics.save_metrics(success=False)

if __name__ == "__main__":
    main()
