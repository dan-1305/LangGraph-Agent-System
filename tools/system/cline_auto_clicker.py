import time
import sys
import os

try:
    import pyautogui
except ImportError:
    print("Thư viện pyautogui chưa được cài đặt. Đang tiến hành cài đặt...")
    os.system(f"{sys.executable} -m pip install pyautogui")
    import pyautogui

def main():
    print("==================================================")
    print("🚀 CLINE AUTO-CLICKER (INFINITE LOOP ENABLER) 🚀")
    print("==================================================")
    print("\n[HƯỚNG DẪN CÀI ĐẶT]")
    print("1. Chuyển sang cửa sổ VS Code có giao diện Cline.")
    print("2. Di chuyển con trỏ chuột đến đúng vị trí sẽ hiện nút 'Approve' hoặc 'Start New Task'.")
    print("3. Giữ nguyên chuột ở vị trí đó. Tọa độ sẽ được khóa sau 5 giây.")
    print("---")
    
    for i in range(5, 0, -1):
        print(f"Khóa tọa độ trong {i} giây...", end='\r', flush=True)
        time.sleep(1)
        
    x, y = pyautogui.position()
    try:
        target_color = pyautogui.pixel(x, y)
    except Exception:
        # Fallback if pixel() fails on some systems
        target_color = (0, 0, 0)
        
    print(f"\n✅ ĐÃ KHÓA TỌA ĐỘ TẠI: X={x}, Y={y}")
    print(f"🎨 MÀU MỤC TIÊU (RGB): {target_color}")
    print("\n[ĐANG HOẠT ĐỘNG]")
    print("Script sẽ tự động click chuột trái vào vị trí này mỗi 10 giây nếu màu sắc khớp.")
    print("Để dừng Auto-Clicker, hãy quay lại cửa sổ này và nhấn Ctrl+C.")
    print("--------------------------------------------------")
    
    try:
        click_count = 0
        miss_count = 0
        while True:
            try:
                current_color = pyautogui.pixel(x, y)
                # Manual tolerance check to avoid any pyscreeze/pyautogui version issues
                tolerance = 30
                color_match = all(abs(current_color[i] - target_color[i]) <= tolerance for i in range(3))
            except Exception:
                # If pixel read fails, just click blindly (fallback)
                color_match = True
                current_color = "Unknown"
                
            if color_match:
                pyautogui.click(x, y)
                click_count += 1
                miss_count = 0
                print(f"[{time.strftime('%H:%M:%S')}] 🎯 Đã click lần {click_count} tại (X={x}, Y={y}) - Color: {current_color}")
            else:
                miss_count += 1
                print(f"[{time.strftime('%H:%M:%S')}] ⏳ Bỏ qua click do sai màu (Current: {current_color} != Target: {target_color}). Miss: {miss_count}")
                
                # Fallback: If 30 misses (5 minutes) occur, we might be stuck on an empty chat prompt
                if miss_count >= 30:
                    print(f"[{time.strftime('%H:%M:%S')}] ⚠️ Phát hiện kẹt task trống quá lâu. Kích hoạt Auto-Typing Fallback...")
                    pyautogui.click(x, y - 50)  # Click slightly above to focus the text box
                    time.sleep(1)
                    # Gõ lệnh bằng tiếng Anh không dấu để tránh lỗi bộ gõ tiếng Việt
                    pyautogui.write("Doc ACTIVE_THOUGHTS.md va tiep tuc task ke tiep trong che do Auto-Pilot", interval=0.05)
                    time.sleep(1)
                    pyautogui.press('enter')
                    miss_count = 0  # Reset
                
            time.sleep(10)
    except KeyboardInterrupt:
        print("\n🛑 Đã nhận lệnh thoát. Auto-Clicker đã dừng.")
        sys.exit(0)

if __name__ == "__main__":
    main()
