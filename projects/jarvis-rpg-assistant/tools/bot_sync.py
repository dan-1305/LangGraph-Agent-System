import datetime
import json
import os
import re
import threading
import time
import tkinter as tk
from tkinter import filedialog, scrolledtext

import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tkinterdnd2 import DND_FILES, TkinterDnD  # Thư viện Kéo Thả
from webdriver_manager.chrome import ChromeDriverManager

# --- CẤU HÌNH ---
load_dotenv()
MY_USERNAME = os.getenv("USER_NAME")
MY_PASSWORD = os.getenv("USER_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CALENDAR_ID = 'primary'

# Cấu hình AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')


# Sử dụng TkinterDnD.Tk thay vì tk.Tk để hỗ trợ kéo thả
class ScheduleSyncApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Schedule Sync Center 🚀")
        self.root.geometry("700x600")

        # --- UI COMPONENTS ---

        # Tiêu đề
        lbl_title = tk.Label(root, text="HỆ THỐNG ĐỒNG BỘ LỊCH HỌC (DRAG & DROP)", font=("Arial", 16, "bold"),
                             fg="#1a73e8")
        lbl_title.pack(pady=10)

        # Khung chứa nút Web
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.btn_web = tk.Button(btn_frame, text="🌐 Lấy từ Web Trường", font=("Arial", 11),
                                 bg="#4CAF50", fg="white", width=25, height=2,
                                 command=self.start_web_sync_thread)
        self.btn_web.pack()

        # --- VÙNG KÉO THẢ (DROP ZONE) ---
        self.drop_frame = tk.LabelFrame(root, text="Kéo ảnh TKB vào đây", font=("Arial", 10, "bold"), fg="#FF9800",
                                        width=600, height=150)
        self.drop_frame.pack(pady=15, padx=20, fill="x")
        self.drop_frame.pack_propagate(False)  # Giữ kích thước cố định

        self.lbl_drop = tk.Label(self.drop_frame, text="📸 KÉO THẢ ẢNH VÀO ĐÂY\n(Hoặc bấm để chọn file)",
                                 font=("Arial", 12), fg="gray", bg="#f0f0f0", cursor="hand2")
        self.lbl_drop.pack(expand=True, fill="both", padx=5, pady=5)

        # Đăng ký sự kiện Kéo Thả
        self.lbl_drop.drop_target_register(DND_FILES)
        self.lbl_drop.dnd_bind('<<Drop>>', self.handle_drop)

        # Bấm vào vùng này cũng mở chọn file được
        self.lbl_drop.bind("<Button-1>", lambda e: self.start_img_sync_thread())

        # Log Area
        tk.Label(root, text="Nhật ký hoạt động:", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(5, 0))
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=12, state='disabled', font=("Consolas", 9))
        self.log_area.pack(pady=5, padx=20)

        # Footer
        tk.Label(root, text="Powered by Jarvis & Gemini 2.0 Flash", fg="gray").pack(side=tk.BOTTOM, pady=10)

    # --- HÀM LOGGING GUI ---
    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    # --- LUỒNG XỬ LÝ ---
    def start_web_sync_thread(self):
        threading.Thread(target=self.run_web_sync, daemon=True).start()

    def start_img_sync_thread(self, file_paths=None):
        # Nếu không có file path truyền vào (bấm nút), thì mở hộp thoại chọn
        if not file_paths:
            file_paths = filedialog.askopenfilenames(title="Chọn ảnh TKB", filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
            if not file_paths: return

        # Chuyển list hoặc tuple thành list chuẩn để xử lý
        if isinstance(file_paths, tuple):
            file_paths = list(file_paths)

        threading.Thread(target=self.run_process_images, args=(file_paths,), daemon=True).start()

    # --- XỬ LÝ SỰ KIỆN KÉO THẢ ---
    def handle_drop(self, event):
        raw_data = event.data
        # TkinterDnD trả về chuỗi dạng: C:/file1.jpg {C:/file co dau cach.jpg} C:/file2.png
        # Cần dùng Regex để tách ra
        # Regex này tìm: Hoặc là chuỗi trong ngoặc {}, Hoặc là chuỗi không chứa dấu cách
        files = re.findall(r'\{.*?\}|[^ ]+', raw_data)

        clean_files = []
        for f in files:
            # Bỏ ngoặc nhọn nếu có
            clean_path = f.strip('{}')
            clean_files.append(clean_path)

        if clean_files:
            self.log(f"⚡ Phát hiện {len(clean_files)} ảnh được kéo vào!")
            self.start_img_sync_thread(clean_files)

    # --- LOGIC 1: WEB SYNC ---
    def run_web_sync(self):
        self.log("🚀 Bắt đầu lấy lịch từ Web...")
        self.btn_web.config(state='disabled')
        try:
            self.log("Đang mở trình duyệt ẩn...")
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://sinhvien.mit.vn/sinh-vien-dang-nhap.html")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "UserName"))).send_keys(MY_USERNAME)
            driver.find_element(By.ID, "Password").send_keys(MY_PASSWORD)

            self.log("⚠️ Vui lòng GIẢI CAPTCHA trên trình duyệt...")
            WebDriverWait(driver, 300).until(EC.staleness_of(driver.find_element(By.ID, "UserName")))
            self.log("✅ Đăng nhập thành công!")

            driver.get("https://sinhvien.mit.vn/lich-theo-tuan.html?pLoaiLich=1")
            time.sleep(5)

            try:
                raw_data = driver.find_element(By.TAG_NAME, "table").text
            except:
                raw_data = driver.find_element(By.TAG_NAME, "body").text

            driver.quit()
            self.process_with_ai(raw_data, is_image=False)

        except Exception as e:
            self.log(f"❌ Lỗi Web Sync: {e}")
        finally:
            self.btn_web.config(state='normal')

    # --- LOGIC 2: XỬ LÝ DANH SÁCH ẢNH ---
    def run_process_images(self, file_paths):
        self.lbl_drop.config(bg="#e0f7fa", text="⏳ ĐANG XỬ LÝ ẢNH...")
        try:
            for path in file_paths:
                self.log(f"--- Đang đọc ảnh: {os.path.basename(path)} ---")
                try:
                    img = Image.open(path)
                    self.process_with_ai(img, is_image=True)
                except Exception as e:
                    self.log(f"❌ Lỗi file {path}: {e}")
        finally:
            self.log("🏁 Hoàn tất xử lý ảnh.")
            self.lbl_drop.config(bg="#f0f0f0", text="📸 KÉO THẢ ẢNH VÀO ĐÂY")

    # --- LOGIC CHUNG: GỌI AI & PUSH ---
    def process_with_ai(self, input_data, is_image=False):
        current_year = datetime.datetime.now().year

        # --- CẬP NHẬT PROMPT ĐỂ LỌC MÔN NGHỈ ---
        prompt_text = f"""
        Đây là dữ liệu thời khóa biểu (Text hoặc Ảnh). Năm hiện tại: {current_year}.

        NHIỆM VỤ:
        1. Trích xuất danh sách môn học thành JSON.
        2. Tự suy luận ngày tháng chuẩn xác.
        3. ⚠️ QUAN TRỌNG: Nếu môn học có nhãn/chữ "Tạm ngưng", "Đã hủy", "Nghỉ", hoặc gạch ngang -> TUYỆT ĐỐI BỎ QUA, KHÔNG ĐƯA VÀO LIST.

        OUTPUT JSON FORMAT:
        [
          {{
            "summary": "Tên Môn",
            "location": "Phòng học",
            "start": "YYYY-MM-DDTHH:MM:SS",
            "end": "YYYY-MM-DDTHH:MM:SS"
          }}
        ]
        Chỉ trả về JSON thuần.
        """

        try:
            if is_image:
                self.log("🧠 Đang soi ảnh & Lọc môn 'Tạm ngưng'...")
                response = model.generate_content([prompt_text, input_data])
            else:
                self.log("🧠 Đang đọc lịch & Lọc môn 'Tạm ngưng'...")
                response = model.generate_content(f"{prompt_text}\nDATA:\n{input_data}")

            json_result = response.text.strip()
            if json_result.startswith("```"):
                json_result = json_result.strip("```json").strip("```")

            self.push_to_google_calendar(json_result)

        except Exception as e:
            self.log(f"❌ Lỗi AI: {e}")

    def push_to_google_calendar(self, events_json):
        token_path = 'data/token.json' if os.path.exists('../data/token.json') else 'token.json'
        if not os.path.exists(token_path):
            self.log("❌ Không tìm thấy token.json!")
            return

        try:
            # SỬA LỖI INVALID_SCOPE: Bỏ định dạng Markdown thừa thãi
            creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/calendar'])
            service = build('calendar', 'v3', credentials=creds)
            events = json.loads(events_json)

            if not events:
                self.log("⚠️ Không tìm thấy lịch nào.")
                return

            for event in events:
                event_body = {
                    'summary': event['summary'],
                    'location': event.get('location', 'Trường Học'),
                    'description': 'Jarvis Sync',
                    'start': {'dateTime': event['start'], 'timeZone': 'Asia/Ho_Chi_Minh'},
                    'end': {'dateTime': event['end'], 'timeZone': 'Asia/Ho_Chi_Minh'},
                }
                service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
                self.log(f"✅ Đã thêm: {event['summary']}")

        except Exception as e:
            self.log(f"❌ Lỗi Sync: {e}")


if __name__ == "__main__":
    # KHỞI TẠO TKINTER DND (QUAN TRỌNG)
    root = TkinterDnD.Tk()
    app = ScheduleSyncApp(root)
    root.mainloop()
