import pandas as pd

def find_mod_inverse(a: int, m: int = 26) -> int:
    """Tìm số nghịch đảo a^-1 mod 26."""
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return -1

def export_affine_horizontal(text: str, a: int, b: int, filename: str = "affine_chuan_mau.xlsx") -> None:
    text = text.upper().replace(" ", "")
    a_inv = find_mod_inverse(a)
    
    # 1. Chuẩn bị các hàng dữ liệu
    row_ban_ro = list(text)
    row_x = [ord(c) - ord('A') for c in text]
    row_y_val = [(a * x + b) % 26 for x in row_x]
    row_ban_ma = [chr(y + ord('A')) for y in row_y_val]
    row_giai_ma = [(a_inv * (y - b)) % 26 for y in row_y_val]
    row_chu_giai_ma = [chr(x + ord('A')) for x in row_giai_ma]

    # 2. Tạo DataFrame theo cấu trúc hàng ngang
    data = {
        "Nội dung": ["BẢN RÕ", "X", f"Y={a}*X+{b}", "BẢN MÃ", f"X=(Y-{b})*{a_inv}", "GIẢI MÃ"],
        **{f"Ký tự {i+1}": [row_ban_ro[i], row_x[i], row_y_val[i], 
                             row_ban_ma[i], row_giai_ma[i], row_chu_giai_ma[i]] 
           for i in range(len(text))}
    }

    df = pd.DataFrame(data)

    # 3. Xuất file
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='AFFINE')
        # Tạo thêm bảng tra cứu nhỏ phía trên cho giống mẫu
        lookup_data = {"Chữ": [chr(i + ord('A')) for i in range(26)], "Số": list(range(26))}
        pd.DataFrame(lookup_data).T.to_excel(writer, sheet_name='Lookup_Table')

    print(f"Đã xuất file: {filename}")
    print(f"Khóa nghịch đảo a^-1 của {a} là: {a_inv}")

if __name__ == "__main__":
    # Tham số theo bài của Danh
    export_affine_horizontal("baitaptulamlaydiem", 23, 13)