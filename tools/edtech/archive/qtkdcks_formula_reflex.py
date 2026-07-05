import tkinter as tk
from tkinter import messagebox
import random

# --- NGÂN HÀNG PHẢN XẠ CÔNG THỨC (DỰA VÀO CHEATSHEET QTKDCKS) ---
FORMULA_QUESTIONS = [
    # CHƯƠNG 2: RA QUYẾT ĐỊNH
    {
        "question": "? = Lợi nhuận × Xác suất + Lợi nhuận × Xác suất... -> CHỌN MAX ?",
        "options": ["A. EOL", "B. EVPI", "C. EMV", "D. LNTT"],
        "answer": 2,
        "explain": "EMV (Giá trị tiền tệ kỳ vọng) = Lợi nhuận × Xác suất. Tiêu chí này thì phải luôn luôn CHỌN MAX."
    },
    {
        "question": "Bước 1 tính EOL: Lập ma trận tiếc nuối bằng cách lấy [?] - Các giá trị trong cột đó.",
        "options": ["A. Min cột", "B. Max cột", "C. 0", "D. Max hàng"],
        "answer": 1,
        "explain": "Lập ma trận tiếc nuối luôn lấy Max của Cột đó trừ đi các con số trong cột (Chứ không lấy Max hàng)."
    },
    {
        "question": "EOL = Giá trị tiếc nuối × Xác suất... -> CHỌN [?] EOL.",
        "options": ["A. MAX", "B. MIN", "C. BẰNG 0", "D. TRUNG BÌNH"],
        "answer": 1,
        "explain": "Tổn thất cơ hội kỳ vọng (EOL) thì ai cũng muốn tổn thất là thấp nhất. Nên BẮT BUỘC CHỌN MIN EOL."
    },
    {
        "question": "EVPI (Giá trị thông tin hoàn hảo) = [?] EOL.",
        "options": ["A. MAX", "B. TỔNG", "C. MIN", "D. TRUNG BÌNH"],
        "answer": 2,
        "explain": "Giá mua thông tin (EVPI) có công thức mẹo: luôn luôn BẰNG với Min EOL của phương án tối ưu."
    },
    {
        "question": "Quyết định không chắc chắn: Tiêu chuẩn Maximax là chọn [?] của những cái [?].",
        "options": ["A. MIN / MIN", "B. MAX / MIN", "C. MIN / MAX", "D. MAX / MAX"],
        "answer": 3,
        "explain": "Maximax là tiêu chuẩn siêu lạc quan. Chọn cái Lời nhất (Max) trong số những cái Lời nhất (Max)."
    },
    {
        "question": "Quyết định không chắc chắn: Tiêu chuẩn Maximin là chọn [?] của những cái [?].",
        "options": ["A. MIN / MIN", "B. MAX / MIN", "C. MIN / MAX", "D. MAX / MAX"],
        "answer": 1,
        "explain": "Maximin là tiêu chuẩn bi quan. Chọn cái Lỗ ít nhất (Max) trong số những cái Lỗ nhất (Min)."
    },
    {
        "question": "Tiêu chuẩn Hurwicz (hệ số α): H = α × [?] + (1 - α) × [?].",
        "options": ["A. Min / Max", "B. Max / Min", "C. Lãi / Lỗ", "D. Nợ / Vốn"],
        "answer": 1,
        "explain": "Hurwicz là sự kết hợp: α × Max (lạc quan) + (1-α) × Min (bi quan). Cuối cùng Chọn Max H."
    },

    # CHƯƠNG 3, 4: KẾ TOÁN & TÀI CHÍNH
    {
        "question": "[?] = Tổng Nợ + Vốn Chủ Sở Hữu.",
        "options": ["A. Lợi nhuận", "B. Doanh thu", "C. Giá vốn", "D. Tổng Tài Sản"],
        "answer": 3,
        "explain": "Đây là phương trình căn bản của Bảng cân đối kế toán. Tài sản luôn được tạo ra từ Tiền vay (Nợ) và Tiền tự có (VCSH)."
    },
    {
        "question": "Tổng Tài Sản = [?] + [?].",
        "options": ["A. Lợi nhuận + Chi phí", "B. Tổng Nợ + Vốn Chủ Sở Hữu", "C. TS Ngắn Hạn + Lãi Vay", "D. Doanh Thu + Cổ Tức"],
        "answer": 1,
        "explain": "Tổng Tài Sản luôn luôn bằng Tổng Nợ (vay người khác) cộng với Vốn Chủ Sở Hữu (vốn tự có)."
    },
    {
        "question": "[?] = Doanh thu - Giá vốn hàng bán.",
        "options": ["A. Lãi gộp", "B. LNTT", "C. LNST", "D. Tỷ số nợ"],
        "answer": 0,
        "explain": "Lãi gộp (Lợi nhuận gộp) là khoản tiền đầu tiên thu được sau khi lấy Doanh thu bán hàng trừ đi tiền vốn nhập hàng (Giá vốn hàng bán)."
    },
    {
        "question": "LNTT (Lợi nhuận trước thuế) = Lãi gộp - [?] - Lãi vay.",
        "options": ["A. Thuế", "B. Cổ tức", "C. Giá vốn", "D. Chi phí hoạt động"],
        "answer": 3,
        "explain": "Lợi nhuận trước thuế (LNTT) được tính bằng: Lãi gộp trừ đi Chi phí hoạt động (bán hàng, quản lý) trừ tiếp Lãi vay."
    },
    {
        "question": "Lợi nhuận giữ lại cuối kỳ = LNGL đầu kỳ + [?] - Cổ tức.",
        "options": ["A. LNTT", "B. LNST", "C. Lãi gộp", "D. Doanh thu"],
        "answer": 1,
        "explain": "Lợi nhuận dùng để trích lại hoặc chia cổ tức phải là Lợi nhuận SAU THUẾ (LNST)."
    },
    {
        "question": "Tỷ số nợ = [?] / Tổng tài sản.",
        "options": ["A. Nợ ngắn hạn", "B. Lãi vay", "C. Tổng nợ", "D. Nợ dài hạn"],
        "answer": 2,
        "explain": "Tỷ số nợ đo lường tổng thể tỷ lệ tiền đi vay trên tổng tài sản. Vậy nó phải là Tổng nợ / Tổng tài sản."
    },
    {
        "question": "Thanh toán hiện hành (Current ratio) = [?] / Nợ ngắn hạn.",
        "options": ["A. Tài sản cố định", "B. Tài sản lưu động", "C. Tổng tài sản", "D. Tiền mặt"],
        "answer": 1,
        "explain": "Khả năng thanh toán hiện hành đo khả năng dùng TS xoay vòng nhanh (Tài sản lưu động) để trả cục Nợ ngắn hạn sắp đến hạn."
    },
    {
        "question": "Thanh toán nhanh (Quick ratio) = (Tài sản lưu động - [?]) / Nợ ngắn hạn.",
        "options": ["A. Lợi nhuận", "B. Khoản phải thu", "C. Hàng tồn kho", "D. Khấu hao"],
        "answer": 2,
        "explain": "Thanh toán nhanh khắt khe hơn hiện hành, vì phải TRỪ ĐI Hàng tồn kho (không bán ngay ra tiền được) ra khỏi Tử số."
    },
    {
        "question": "Vòng quay tài sản = [?] / Tổng tài sản.",
        "options": ["A. LNST", "B. Doanh thu", "C. Giá vốn", "D. Lãi gộp"],
        "answer": 1,
        "explain": "Vòng quay tài sản đo lường việc tài sản đẻ ra được bao nhiêu đồng Doanh thu."
    },
    {
        "question": "Kỳ thu tiền bình quân = Khoản phải thu / [?].",
        "options": ["A. Nợ ngắn hạn", "B. LNTT", "C. Doanh thu / 365", "D. Hàng tồn kho"],
        "answer": 2,
        "explain": "Kỳ thu tiền (số ngày chờ đòi nợ) = Khoản phải thu chia cho Doanh thu bình quân của 1 ngày (Doanh thu năm / 365)."
    },

    # CHƯƠNG 5: HÀNG TỒN KHO
    {
        "question": "[?] = √(2*D*S / H)",
        "options": ["A. ROP", "B. EOQ", "C. EVPI", "D. EMV"],
        "answer": 1,
        "explain": "EOQ là Điểm đặt hàng tối ưu (Economic Order Quantity). Công thức Căn bậc 2 kinh điển."
    },
    {
        "question": "Trong công thức EOQ, H đại diện cho gì?",
        "options": ["A. Nhu cầu năm", "B. Chi phí 1 lần đặt hàng", "C. Chi phí lưu trữ 1 đơn vị/năm", "D. Thời gian chờ"],
        "answer": 2,
        "explain": "D (Demand) là Nhu cầu năm. S (Setup) là Chi phí đặt hàng. H (Holding) là Chi phí lưu trữ."
    },
    {
        "question": "Số lần đặt hàng (N) = [?] / EOQ.",
        "options": ["A. S", "B. H", "C. D", "D. ROP"],
        "answer": 2,
        "explain": "Số lần đặt hàng trong 1 năm bằng Tổng Nhu cầu (D) chia cho Số lượng mỗi lần đặt (EOQ)."
    },
    {
        "question": "Điểm đặt hàng lại (ROP) = (Nhu cầu bình quân ngày * [?]) + [?].",
        "options": ["A. H / S", "B. D / EOQ", "C. Lead time / Dự trữ an toàn", "D. Te / Phương sai"],
        "answer": 2,
        "explain": "ROP = (Nhu cầu 1 ngày * Thời gian chờ giao hàng Lead time) + Lượng hàng dự trữ an toàn."
    },

    # CHƯƠNG 7: QUẢN TRỊ DỰ ÁN
    {
        "question": "Thời gian hoàn thành dự án = Tổng thời gian của [?].",
        "options": ["A. Đường găng (Nhánh dài nhất)", "B. Nhánh ngắn nhất", "C. Các công việc trung bình", "D. Công việc A và B"],
        "answer": 0,
        "explain": "Thời gian dự án chính là tổng thời gian của nhánh (đường đi) DÀI NHẤT, còn được gọi là Đường găng (Critical Path)."
    },
    {
        "question": "Các công việc nằm TRÊN ĐƯỜNG GĂNG có Thời gian dự trữ (Slack) bằng bao nhiêu?",
        "options": ["A. Lớn hơn 0", "B. Nhỏ hơn 0", "C. Bằng 0", "D. Bằng 1"],
        "answer": 2,
        "explain": "Các công việc trên Đường găng tuyệt đối không được trễ 1 ngày nào, nên Thời gian dự trữ (Slack) bắt buộc phải BẰNG 0."
    },
    {
        "question": "Thời gian kỳ vọng (Te) = (a + [?] + b) / 6.",
        "options": ["A. 2m", "B. 3m", "C. 4m", "D. 6m"],
        "answer": 2,
        "explain": "Công thức PERT: Thời gian kỳ vọng Te = (Lạc quan a + 4 lần Bình thường m + Bi quan b) / 6."
    },
    {
        "question": "Phương sai dự án (V) = (([?] - [?]) / 6)^2.",
        "options": ["A. m - a", "B. b - a", "C. a - b", "D. b - m"],
        "answer": 1,
        "explain": "Phương sai = (Bi quan (b) - Lạc quan (a)) chia 6, tất cả đem Bình phương."
    }
]

class FormulaQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("App Luyện Phản Xạ Công Thức QTKDCKS")
        self.root.geometry("900x700") # Tăng kích thước
        self.root.configure(bg="#2c3e50")
        # Phím Enter chuyển câu
        self.root.bind("<Return>", lambda event: self.handle_enter())
        
        self.current_question = 0
        self.score = 0
        
        # Xáo trộn ngân hàng công thức
        random.shuffle(FORMULA_QUESTIONS)
        
        self.build_ui()
        self.load_question()

    def build_ui(self):
        # Tiêu đề App
        self.lbl_title = tk.Label(self.root, text="🔥 PHẢN XẠ CÔNG THỨC SIÊU TỐC 🔥", font=("Helvetica", 22, "bold"), bg="#f39c12", fg="white", pady=15)
        self.lbl_title.pack(fill=tk.X)
        
        # Tracking điểm
        self.frame_top = tk.Frame(self.root, bg="#2c3e50")
        self.frame_top.pack(fill=tk.X, padx=20, pady=10)
        
        self.lbl_status = tk.Label(self.frame_top, text="Công thức: 1/25", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.lbl_status.pack(side=tk.LEFT)
        
        self.lbl_score = tk.Label(self.frame_top, text="Điểm: 0", font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#2ecc71")
        self.lbl_score.pack(side=tk.RIGHT)
        
        # Khung chứa câu hỏi
        self.frame_q = tk.Frame(self.root, bg="white", bd=5, relief=tk.RIDGE)
        self.frame_q.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.lbl_question = tk.Label(self.frame_q, text="", font=("Courier New", 18, "bold"), bg="white", fg="#c0392b", wraplength=700, justify="center")
        self.lbl_question.pack(pady=30, padx=10, fill=tk.X)
        
        # Các nút đáp án
        self.btn_opts = []
        for i in range(4):
            btn = tk.Button(self.frame_q, text="", font=("Helvetica", 14, "bold"), bg="#34495e", fg="white", 
                            activebackground="#2c3e50", activeforeground="white", cursor="hand2",
                            command=lambda i=i: self.check_answer(i))
            btn.pack(fill=tk.X, padx=60, pady=8, ipady=8)
            self.btn_opts.append(btn)
            
        # Vùng giải thích đáp án
        self.lbl_explain = tk.Label(self.frame_q, text="", font=("Helvetica", 13, "italic"), bg="white", fg="#27ae60", wraplength=700, justify="left")
        self.lbl_explain.pack(pady=15, padx=10, fill=tk.X)
        
        # Nút Next
        self.btn_next = tk.Button(self.root, text="Phản xạ tiếp (Enter) >>", font=("Helvetica", 16, "bold"), bg="#e74c3c", fg="white", 
                                  activebackground="#c0392b", activeforeground="white", cursor="hand2", command=self.next_question)
        self.btn_next.pack(pady=10, ipady=8, ipadx=30)
        self.btn_next.config(state=tk.DISABLED)

    def handle_enter(self):
        if self.btn_next['state'] == tk.NORMAL:
            self.next_question()

    def load_question(self):
        if self.current_question >= len(FORMULA_QUESTIONS):
            messagebox.showinfo("Tốt Nghiệp", f"Đỉnh chóp! Bạn đã nhớ hết công thức.\nĐiểm số của bạn: {self.score}/{len(FORMULA_QUESTIONS)}")
            self.root.quit()
            return
            
        q_data = FORMULA_QUESTIONS[self.current_question]
        self.lbl_status.config(text=f"Công thức: {self.current_question + 1}/{len(FORMULA_QUESTIONS)}")
        self.lbl_score.config(text=f"Điểm: {self.score}")
        
        self.lbl_question.config(text=q_data["question"])
        self.lbl_explain.config(text="")
        
        for i in range(4):
            self.btn_opts[i].config(text=q_data["options"][i], bg="#34495e", state=tk.NORMAL)
            
        self.btn_next.config(state=tk.DISABLED)

    def check_answer(self, selected_idx):
        q_data = FORMULA_QUESTIONS[self.current_question]
        correct_idx = q_data["answer"]
        
        # Vô hiệu hóa nút sau khi bấm
        for btn in self.btn_opts:
            btn.config(state=tk.DISABLED)
            
        if selected_idx == correct_idx:
            self.btn_opts[selected_idx].config(bg="#27ae60") # Xanh lá
            self.score += 1
            self.lbl_score.config(text=f"Điểm: {self.score}")
            self.lbl_explain.config(text=f"✅ CHÍNH XÁC!\n\nNhắc bài: {q_data['explain']}")
            self.lbl_explain.config(fg="#27ae60")
        else:
            self.btn_opts[selected_idx].config(bg="#c0392b") # Đỏ
            self.btn_opts[correct_idx].config(bg="#27ae60") # Hiện đáp án đúng màu xanh
            self.lbl_explain.config(text=f"❌ SAI LẦM TAI HẠI!\n\nNhắc bài: {q_data['explain']}")
            self.lbl_explain.config(fg="#c0392b")
            
        self.btn_next.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1
        self.load_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = FormulaQuizApp(root)
    root.mainloop()