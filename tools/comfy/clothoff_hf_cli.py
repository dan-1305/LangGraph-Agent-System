import os
import sys
import time
import shutil

# Thử import tkinter để mở hộp thoại chọn file
try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

try:
    from gradio_client import Client, handle_file
except ImportError:
    print("[LỖI] Chưa cài đặt thư viện 'gradio_client'. Đang cài đặt tự động...")
    os.system(f"{sys.executable} -m pip install gradio_client")
    from gradio_client import Client, handle_file

# Thư mục lưu ảnh
OUTPUT_DIR = "images_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def select_file(title):
    if HAS_TKINTER:
        root = tk.Tk()
        root.withdraw() # Ẩn cửa sổ chính
        root.attributes('-topmost', True) # Luôn hiện trên cùng
        file_path = filedialog.askopenfilename(title=title, filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        root.destroy()
        return file_path
    else:
        return input(f"{title} (Nhập đường dẫn): ").strip()

def main():
    print("="*60)
    print("   🚀 CÔNG CỤ CLOTHOFF AI (HUGGINGFACE MIỄN PHÍ) 🚀")
    print("="*60)

    print("\n[1/4] CHUẨN BỊ ẢNH GỐC")
    image_path = select_file("Chọn ảnh gốc cần xử lý")
    if not image_path or not os.path.exists(image_path):
        print("[LỖI] Bạn chưa chọn ảnh gốc hoặc file không tồn tại.")
        sys.exit(1)
    print(f" -> Đã tải ảnh gốc: {image_path}")

    print("\n[2/4] CHUẨN BỊ ẢNH MASK")
    print("Lưu ý: Bạn có thể tự mở Paint bôi màu trắng lên vùng quần áo, màu đen cho vùng còn lại.")
    mask_path = select_file("Chọn ảnh Mask (Trắng: vùng xóa, Đen: vùng giữ lại)")
    if not mask_path or not os.path.exists(mask_path):
        print("[LỖI] Bạn chưa chọn ảnh mask hoặc file không tồn tại.")
        sys.exit(1)
    print(f" -> Đã tải ảnh mask: {mask_path}")

    prompt = input("\n[?] Nhập prompt NSFW (Ấn Enter để dùng mặc định: naked, bare skin...): ").strip()
    if not prompt:
        prompt = "naked, bare skin, nsfw, highly detailed, realistic skin texture, masterpiece, 8k resolution"

    print("\n[3/4] ĐANG KẾT NỐI LÊN MÁY CHỦ ĐÁM MÂY (HuggingFace Spaces)...")
    try:
        start_time = time.time()
        client = Client("diffusers/stable-diffusion-xl-1.0-inpainting-0.1")
        
        print(" -> Đã kết nối thành công! Đang tiến hành tạo ảnh (quá trình này mất khoảng 20-40 giây)...")
        
        result = client.predict(
            prompt=prompt,
            image=handle_file(image_path),
            mask_image=handle_file(mask_path),
            negative_prompt="clothes, ugly, low quality, deformed, censored, blurred, bad anatomy, text, watermark",
            num_inference_steps=30,
            guidance_scale=7.5,
            strength=0.8,
            api_name="/predict"
        )
        
        elapsed_time = round(time.time() - start_time, 2)
        print(f" -> Đã nhận được ảnh trả về từ máy chủ sau {elapsed_time} giây!")

        print("\n[4/4] ĐANG LƯU KẾT QUẢ")
        # result trả về tuple hoặc string (tuỳ phiên bản gradio client)
        if isinstance(result, tuple):
            output_file = result[0]
        else:
            output_file = result
            
        timestamp = int(time.time())
        final_output_path = os.path.join(OUTPUT_DIR, f"clothoff_hf_{timestamp}.png")
        
        shutil.copy(output_file, final_output_path)
        print(f" -> HOÀN TẤT! 🎉 Ảnh đã được lưu thành công tại:\n    {os.path.abspath(final_output_path)}")
        
        # Tự động mở ảnh trên Windows
        if os.name == 'nt':
            os.startfile(final_output_path)

    except Exception as e:
        print(f"\n[THẤT BẠI] Lỗi kết nối hoặc xử lý từ máy chủ API: {e}")
        print("Có thể HuggingFace đang quá tải hoặc prompt bị bộ lọc (safety filter) chặn. Thử thay đổi prompt nhẹ nhàng hơn.")

if __name__ == "__main__":
    main()
