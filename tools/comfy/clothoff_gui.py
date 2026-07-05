import os
import time
import gradio as gr
from gradio_client import Client, handle_file

# Đảm bảo thư mục output tồn tại
OUTPUT_DIR = "images_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_clothoff(dict_input, prompt):
    if dict_input is None or "image" not in dict_input or "mask" not in dict_input:
        return None, "Vui lòng tải ảnh và vẽ mask bôi đen vùng cần chỉnh sửa."

    img = dict_input["image"]
    mask = dict_input["mask"]

    # Lưu tạm ảnh ra file để gửi qua API Gradio Client
    temp_img_path = "temp_image.png"
    temp_mask_path = "temp_mask.png"
    
    img.save(temp_img_path, format="PNG")
    mask.save(temp_mask_path, format="PNG")

    try:
        print("Đang kết nối tới máy chủ AI HuggingFace miễn phí...")
        # Sử dụng HuggingFace Space SDXL Inpainting (Miễn phí)
        client = Client("diffusers/stable-diffusion-xl-1.0-inpainting-0.1")
        
        result = client.predict(
            prompt=prompt,
            image=handle_file(temp_img_path),
            mask_image=handle_file(temp_mask_path),
            negative_prompt="clothes, ugly, low quality, deformed, censored, blurred, bad anatomy",
            num_inference_steps=25,
            guidance_scale=7.5,
            strength=0.8,
            api_name="/predict"
        )
        
        # result trả về tuple hoặc đường dẫn file
        if isinstance(result, tuple):
            output_file = result[0]
        else:
            output_file = result
            
        # Di chuyển file kết quả vào thư mục output
        timestamp = int(time.time())
        final_output_path = os.path.join(OUTPUT_DIR, f"clothoff_hf_{timestamp}.png")
        
        import shutil
        shutil.copy(output_file, final_output_path)
        
        print(f"Thành công! Ảnh đã lưu tại: {final_output_path}")
        
        # Xóa file tạm
        os.remove(temp_img_path)
        os.remove(temp_mask_path)
        
        return final_output_path, f"Tạo ảnh thành công! Đã lưu vào {OUTPUT_DIR}"

    except Exception as e:
        err_msg = f"Lỗi API từ máy chủ: {str(e)}"
        print(err_msg)
        return None, err_msg

# Tạo giao diện Gradio
with gr.Blocks(title="NSFW AI ClothOff (Free API)") as demo:
    gr.Markdown("# 🎨 Giao Diện Tạo Ảnh ClothOff (Dùng API Miễn Phí)")
    gr.Markdown("Kéo thả ảnh vào khung dưới, **dùng cọ bôi đen** phần quần áo, nhập prompt và nhấn Generate. Xử lý cực nhanh qua máy chủ đám mây HuggingFace!")
    
    with gr.Row():
        with gr.Column():
            # Công cụ upload ảnh và vẽ mask
            img_input = gr.ImageMask(
                label="1. Kéo thả ảnh & Vẽ mask", 
                type="pil"
            )
            
            prompt_input = gr.Textbox(
                label="2. Nhập Prompt (Mô tả NSFW)",
                value="naked, bare skin, nsfw, highly detailed, realistic skin texture, masterpiece",
                lines=3
            )
            
            submit_btn = gr.Button("🚀 BẮT ĐẦU TẠO ẢNH", variant="primary")
            
        with gr.Column():
            output_img = gr.Image(label="Kết Quả", type="filepath")
            status_text = gr.Textbox(label="Trạng thái", interactive=False)
            
    submit_btn.click(
        fn=process_clothoff,
        inputs=[img_input, prompt_input],
        outputs=[output_img, status_text]
    )

if __name__ == "__main__":
    print(f"Đang khởi động giao diện... Các ảnh sẽ được lưu vào: {os.path.abspath(OUTPUT_DIR)}")
    demo.launch(server_name="127.0.0.1", server_port=7861, inbrowser=True)
