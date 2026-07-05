import base64
import os

def encode_image(image_path: str) -> str:
    """
    Chuyển đổi hình ảnh sang định dạng Base64.
    
    Args:
        image_path (str): Đường dẫn tuyệt đối hoặc tương đối tới file ảnh.
        
    Returns:
        str: Chuỗi mã hóa Base64 của ảnh.
        
    Raises:
        FileNotFoundError: Nếu file ảnh không tồn tại.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"[-] Error: Image {image_path} not found.")
        
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
