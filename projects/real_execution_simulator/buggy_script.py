# Cố tình import sai thư viện để tạo lỗi ModuleNotFoundError
import requests_not_exist
import math

def calculate_square_root():
    num = 16
    # Cố tình dùng sai tên hàm để tạo AttributeError
    result = math.squareroot(num)
    print(f"Square root of {num} is {result}")

if __name__ == "__main__":
    print("Bắt đầu chạy script lỗi...")
    calculate_square_root()
    print("Script đã chạy xong!")
