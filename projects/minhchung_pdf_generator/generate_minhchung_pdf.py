import os
import re
from fpdf import FPDF
from PIL import Image

def get_caption_from_filename(filename):
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Remove leading numbers
    name = re.sub(r'^\d+', '', name)
    # If the name is empty after removing numbers, it means it was just a number (e.g. 6.bmp -> 6)
    if not name:
        name = os.path.splitext(filename)[0]
    return name

def create_pdf():
    # Define mapping based on folder structure
    sections = [
        {
            "muc": "Mục 1",
            "text": "6/Xếp loại học tập",
            "folder": "MinhChung/1.1.2.2"
        },
        {
            "muc": "Mục 2",
            "text": "18/Tham gia đầy đủ, đúng hạn BHYT/BHXH theo thông báo của Trường",
            "folder": "MinhChung/2.4"
        },
        {
            "muc": "Mục 3",
            "text": "22/Tham dự các buổi sinh hoạt, hoạt động chính trị, xã hội, văn hóa, văn nghệ, thể thao tại Trường",
            "folder": "MinhChung/3.2.2"
        },
        {
            "muc": "Mục 4",
            "text": "28/Tích cực tham gia hoạt động tại địa phương, nơi cư trú do doanh nghiệp, tổ chức phi chính phủ tổ chức",
            "folder": "MinhChung/4.2.1"
        },
        {
            "muc": "Mục 5",
            "text": "43/Hỗ trợ và tham gia tích cực vào hoạt động chung của khoa, phòng ban, trung tâm",
            "folder": "MinhChung/5.2.2"
        }
    ]

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Load fonts
    font_path = r"C:\Windows\Fonts\arial.ttf"
    font_bold_path = r"C:\Windows\Fonts\arialbd.ttf"
    
    if os.path.exists(font_path):
        pdf.add_font("Arial", "", font_path, uni=True)
    if os.path.exists(font_bold_path):
        pdf.add_font("Arial", "B", font_bold_path, uni=True)
        
    pdf.add_page()
    
    if os.path.exists(font_path):
        pdf.set_font("Arial", "B", 16)
    else:
        pdf.set_font("Helvetica", "B", 16)
        
    pdf.cell(0, 10, "Minh chứng điểm rèn luyện", ln=True, align="C")
    pdf.ln(5)

    hinh_count = 1

    for section in sections:
        folder_path = section["folder"]
        
        if not os.path.exists(folder_path):
            continue
            
        # Add Mục header
        if os.path.exists(font_path):
            pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, section["muc"], ln=True)
        
        # Add Criteria text
        if os.path.exists(font_path):
            pdf.set_font("Arial", "", 12)
        
        # Multicell for long text
        pdf.multi_cell(0, 8, section["text"])
        pdf.ln(2)
        
        # Get all images in folder
        valid_extensions = {".jpg", ".jpeg", ".png", ".bmp"}
        files = []
        for f in os.listdir(folder_path):
            if os.path.splitext(f)[1].lower() in valid_extensions:
                files.append(f)
                
        # Sort files to ensure order
        files.sort()
        
        for file in files:
            img_path = os.path.join(folder_path, file)
            caption = get_caption_from_filename(file)
            
            # Read image to get aspect ratio
            try:
                with Image.open(img_path) as img:
                    # Convert to RGB if BMP or RGBA to avoid errors in fpdf
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    # Save a temporary JPEG file because fpdf handles jpeg best
                    # Use unique filename to prevent FPDF from caching the first image
                    temp_img_path = f"temp_minhchung_{hinh_count}.jpg"
                    img.save(temp_img_path, "JPEG")
                    
                    w, h = img.size
                    aspect_ratio = h / w
            except Exception as e:
                print(f"Error reading image {img_path}: {e}")
                continue
            
            # Calculate width and height for PDF (A4 page width is 210mm, margins are 10mm each by default, so max width is 190)
            max_w = 170
            img_w = max_w
            img_h = img_w * aspect_ratio
            
            # If image height is too large, limit it
            if img_h > 230:
                img_h = 230
                img_w = img_h / aspect_ratio
                
            # Check if we need a page break for the image
            # remaining height = 297 - current_y - bottom margin (15)
            if pdf.get_y() + img_h + 10 > 280:
                pdf.add_page()
                
            # Calculate X to center the image
            x_pos = (210 - img_w) / 2
            
            pdf.image(temp_img_path, x=x_pos, y=pdf.get_y(), w=img_w, h=img_h)
            pdf.set_y(pdf.get_y() + img_h + 2)
            
            # Caption
            caption_text = f"Hình {hinh_count}: {caption}"
            pdf.set_font("Arial", "I", 11) if os.path.exists(font_path) else pdf.set_font("Helvetica", "I", 11)
            pdf.cell(0, 8, caption_text, ln=True, align="C")
            pdf.ln(5)
            
            if os.path.exists(font_path):
                pdf.set_font("Arial", "", 12)
            
            hinh_count += 1
            
            # Clean up temp image
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)

    output_path = "MinhChung_Result.pdf"
    pdf.output(output_path)
    print(f"Đã tạo file PDF thành công: {output_path}")

if __name__ == "__main__":
    create_pdf()
