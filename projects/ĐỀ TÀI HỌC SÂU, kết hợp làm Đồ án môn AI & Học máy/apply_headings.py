import os
import re
from docx import Document

def apply_styles(doc_path):
    doc = Document(doc_path)
    
    # Ensure styles exist or just apply by name. python-docx handles standard 'Heading 1' out of the box if it exists in the template.
    for p in doc.paragraphs:
        text = p.text.strip()
        if not text:
            continue
            
        # Heading 1
        if re.match(r'^CHƯƠNG\s+\d+', text):
            try:
                p.style = 'Heading 1'
            except Exception as e:
                print(f"Warning: Could not apply Heading 1 to '{text[:20]}...' - {e}")
            continue
            
        # Heading 3
        if re.match(r'^\d+\.\d+\.\d+[\.\s]', text):
            try:
                p.style = 'Heading 3'
            except Exception as e:
                print(f"Warning: Could not apply Heading 3 to '{text[:20]}...' - {e}")
            continue
            
        # Heading 2
        if re.match(r'^\d+\.\d+[\.\s]', text):
            try:
                p.style = 'Heading 2'
            except Exception as e:
                print(f"Warning: Could not apply Heading 2 to '{text[:20]}...' - {e}")
            continue
            
    doc.save(doc_path)

if __name__ == "__main__":
    base_dir = "projects/ĐỀ TÀI HỌC SÂU, kết hợp làm Đồ án môn AI & Học máy"
    ml_out = os.path.join(base_dir, "FINAL_Do_an_Hoc_may_va_AI.docx")
    dl_out = os.path.join(base_dir, "FINAL_Do_an_Hoc_sau.docx")
    
    apply_styles(ml_out)
    apply_styles(dl_out)
    print("Heading styles applied successfully!")
