import os
import sys
import time
import base64
import requests
from dotenv import load_dotenv

# Thử import tkinter để mở hộp thoại chọn file
try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

# Nạp API key
load_dotenv()
API_KEY = os.getenv("segmind_API_KEY")
URL = "https://api.segmind.com/v1/sdxl-inpaint"

# Thư mục lưu ảnh
OUTPUT_DIR = "images_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def to_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def select_file(title):
    if HAS_TKINTER:
        root = tk.Tk()
        root.withdraw() # Ẩn cửa sổ chính
        file_path = filedialog.askopenfilename(title=title, filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        return file_path
    else:
        return input(f"{title} (Nhập đường dẫn): ").strip()

def main():
    print("="*50)
    print("   🚀 CÔNG CỤ CLOTHOFF AI (SEGMIND API) 🚀")
    print("="*50)

    if not API_KEY:
        print("\n[LỖI] Không tìm thấy API Key của Segmind trong file .env!")
        print("Vui lòng thêm dòng: segmind_API_KEY=YOUR_KEY vào file .env")
        sys.exit(1)

    print("\n[1/4] CHUẨN BỊ ẢNH ĐẦU VÀO")
    image_path = select_file("Chọn ảnh gốc cần xử lý")
    if not image_path or not os.path.exists(image_path):
        print("[LỖI] Không tìm thấy ảnh gốc hoặc bạn chưa chọn ảnh.")
        sys.exit(1)
    print(f" -> Đã chọn ảnh gốc: {image_path}")

    print("\n[2/4] CHUẨN BỊ ẢNH MASK (Vùng cần bôi đen)")
    auto_mask = input("[?] Bạn có muốn AI tự động nhận diện và tạo Mask quần áo không? (y/n): ").strip().lower()
    
    if auto_mask == 'y':
        mask_path = os.path.join(OUTPUT_DIR, "auto_mask_temp.png")
        try:
            print(" -> Đang khởi động AI nhận diện quần áo (rembg)...")
            from rembg import remove, new_session
            from PIL import Image
            session = new_session('u2net_cloth_seg')
            
            img = Image.open(image_path)
            output = remove(img, session=session)
            
            if output.mode == "RGBA":
                alpha = output.split()[3]
                mask = Image.new("RGB", img.size, (0, 0, 0))
                mask.paste((255, 255, 255), mask=alpha)
                mask.save(mask_path)
                print(f" -> Đã tự động tạo Mask thành công tại: {mask_path}")
            else:
                print("[LỖI] Không thể tạo mask tự động. Vui lòng tự chọn ảnh mask.")
                mask_path = select_file("Chọn ảnh mask")
        except ImportError:
            print("[LỖI] Chưa cài đặt thư viện 'rembg' và 'Pillow'. Hãy chạy lệnh: pip install rembg pillow")
            mask_path = select_file("Chọn ảnh mask")
        except Exception as e:
            print(f"[LỖI] Sinh mask thất bại: {e}")
            mask_path = select_file("Chọn ảnh mask")
    else:
        mask_path = select_file("Chọn ảnh mask (vùng trắng là vùng sẽ bị xóa)")
        
    if not mask_path or not os.path.exists(mask_path):
        print("[LỖI] Không tìm thấy ảnh mask hoặc bạn chưa chọn mask.")
        sys.exit(1)
    print(f" -> Đã chọn ảnh mask: {mask_path}")

    prompt = input("\n[?] Nhập prompt NSFW (Mặc định: naked, bare skin, highly detailed): ").strip()
    if not prompt:
        prompt = "naked, bare skin, nsfw, highly detailed, realistic skin texture, masterpiece"

    print("\n[3/4] MÃ HÓA VÀ GỬI DỮ LIỆU LÊN ĐÁM MÂY...")
    try:
        img_b64 = to_base64(image_path)
        mask_b64 = to_base64(mask_path)
        print(" -> Mã hóa Base64 thành công!")
    except Exception as e:
        print(f"[LỖI] Không thể đọc file ảnh: {e}")
        sys.exit(1)

    payload = {
        "image": img_b64,
        "mask": mask_b64,
        "prompt": prompt,
        "negative_prompt": "clothes, ugly, low quality, deformed, censored, blurred, bad anatomy",
        "samples": 1,
        "scheduler": "Euler a",
        "num_inference_steps": 30,
        "guidance_scale": 7.5,
        "strength": 0.8,
        "seed": -1
    }

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    print(" -> Đang chờ máy chủ Segmind xử lý (Khoảng 5 - 15 giây)...")
    start_time = time.time()
    
    try:
        response = requests.post(URL, json=payload, headers=headers)
    except Exception as e:
        print(f"\n[LỖI MẠNG] Không thể kết nối đến máy chủ: {e}")
        sys.exit(1)

    elapsed_time = round(time.time() - start_time, 2)

    print("\n[4/4] NHẬN KẾT QUẢ TỪ MÁY CHỦ")
    if response.status_code == 200:
        timestamp = int(time.time())
        output_path = os.path.join(OUTPUT_DIR, f"clothoff_{timestamp}.png")
        
        with open(output_path, "wb") as f:
            f.write(response.content)
            
        print(f" -> HOÀN TẤT! 🎉 Ảnh đã được xử lý trong {elapsed_time} giây.")
        print(f" -> Kết quả lưu tại: {os.path.abspath(output_path)}")
        
        # Tự động mở ảnh (chỉ hoạt động trên Windows)
        if os.name == 'nt':
            os.startfile(output_path)
            
    else:
        print(f"[THẤT BẠI] Lỗi API (Mã: {response.status_code})")
        print(f"Chi tiết lỗi từ máy chủ: {response.text}")
        print(" -> Có thể tài khoản Segmind của bạn hết Credits hoặc API Key bị lỗi.")

if __name__ == "__main__":
    main()
