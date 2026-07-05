import os
import easyocr

def extract_text(folder_path, output_file):
    print(f"Starting OCR for folder: {folder_path}")
    reader = easyocr.Reader(['en'], gpu=False) # CPU mode as default to prevent errors
    
    text_results = []
    
    # Sort files by name to read in order
    files = sorted([f for f in os.listdir(folder_path) if f.endswith(('.webp', '.jpg', '.png'))], 
                   key=lambda x: int(''.join(filter(str.isdigit, x))) if any(c.isdigit() for c in x) else 0)
    
    # Limit to first 10 pages to avoid extremely long runtime for a quick analysis
    for file in files[:10]:
        file_path = os.path.join(folder_path, file)
        print(f"Processing: {file}")
        try:
            # Read image using cv2
            # Some webp might need special handling, but easyocr usually handles it via cv2
            result = reader.readtext(file_path, detail=0)
            page_text = " ".join(result)
            if page_text.strip():
                text_results.append(f"--- Page {file} ---\n{page_text}")
        except Exception as e:
            print(f"Error processing {file}: {e}")
            
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n\n".join(text_results))
    print(f"OCR completed. Results saved to {output_file}")

if __name__ == "__main__":
    base_dir = "data/Hentai"
    
    folders_to_scan = [
        "[Punpunn] Hestia Full version [Bleached]",
        "[Punpunn] Eris NTR [Bleached]",
        "[PunPunn] Shuuko vs Tadano-kun (uncensored)"
    ]
    
    for folder_name in folders_to_scan:
        folder_path = os.path.join(base_dir, folder_name)
        output_file = os.path.join(base_dir, f"ocr_result_{folder_name.replace(' ', '_').replace('[', '').replace(']', '')}.txt")
        if os.path.exists(folder_path):
            extract_text(folder_path, output_file)
        else:
            print(f"Folder not found: {folder_path}")
