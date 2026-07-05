import fitz  # PyMuPDF
import os

pdf_dir = "docs/QTKDCKS"
keywords = {
    "quy trình ra quyết định": "quy trình ra quyết định",
    "chắc chắn, rủi ro": "chắc chắn",
    "cân đối kế toán": "bảng cân đối kế toán",
    "báo cáo kết quả kinh doanh": "báo cáo kết quả kinh doanh",
    "tỷ số nợ": "tỷ số nợ",
    "thanh toán hiện hành": "thanh toán hiện hành",
    "vòng quay tài sản": "vòng quay tài sản",
    "emv": "emv",
    "eol": "eol",
    "evpi": "evpi",
    "maximax": "maximax",
    "hurwicz": "hurwicz",
    "lãi gộp": "lãi gộp",
    "eoq": "eoq",
    "rop": "điểm đặt hàng lại",
    "pert": "pert",
    "đường găng": "đường găng",
    "phương sai": "phương sai"
}

results = {k: [] for k in keywords.keys()}

for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        filepath = os.path.join(pdf_dir, filename)
        try:
            doc = fitz.open(filepath)
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text().lower()
                for key, search_word in keywords.items():
                    if search_word in text:
                        results[key].append(f"{filename} - Trang {page_num + 1}")
        except Exception as e:
            print(f"Lỗi đọc file {filename}: {e}")

# Save results to file to avoid GBK encoding error in print
with open('tools/scan_results.txt', 'w', encoding='utf-8') as f:
    for key, files in results.items():
        f.write(f"\n[{key.upper()}]:\n")
        if files:
            unique_refs = list(set(files))[:3]
            for ref in unique_refs:
                f.write(f"  -> {ref}\n")
        else:
            f.write("  -> Không tìm thấy.\n")
print("Results saved to tools/scan_results.txt")
