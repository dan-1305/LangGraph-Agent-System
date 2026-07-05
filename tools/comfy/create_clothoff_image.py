import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("segmind_API_KEY")
URL = "https://api.segmind.com/v1/sdxl-inpaint"

def to_base64(image_path):
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def generate_clothoff(image_path, mask_path, output_path, prompt="naked, bare skin, nsfw, highly detailed, realistic"):
    print(f"Loading image from {image_path} and mask from {mask_path}...")
    
    try:
        img_b64 = to_base64(image_path)
        mask_b64 = to_base64(mask_path)
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    payload = {
        "image": img_b64,
        "mask": mask_b64,
        "prompt": prompt,
        "negative_prompt": "clothes, ugly, low quality, deformed, censored",
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

    print("Sending request to Segmind API...")
    response = requests.post(URL, json=payload, headers=headers)

    if response.status_code == 200:
        print("Success! Saving generated image...")
        # Lấy nội dung ảnh nhị phân trả về
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Saved generated image to {output_path}")
    else:
        print(f"Failed to generate image. Status Code: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create ClothOff Image using Segmind API")
    parser.add_argument("--image", type=str, required=True, help="Path to input image")
    parser.add_argument("--mask", type=str, required=True, help="Path to mask image (white = area to change, black = keep)")
    parser.add_argument("--output", type=str, default="output/clothoff_result.png", help="Path to save output image")
    parser.add_argument("--prompt", type=str, default="naked, bare skin, nsfw, highly detailed, realistic", help="Prompt for generation")
    
    args = parser.parse_args()
    
    # Đảm bảo thư mục output tồn tại
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    generate_clothoff(args.image, args.mask, args.output, args.prompt)
