import tkinter as tk
from tkinter import messagebox
import random

# --- NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM BÁM SÁT ĐỀ CƯƠNG QTKDCKS ---
QUESTIONS = [
    # --- PHẦN 1: RA QUYẾT ĐỊNH ---
    {
        "question": "Ra quyết định trong tình huống biết được XÁC SUẤT xảy ra của từng trạng thái tự nhiên được gọi là gì?",
        "options": ["A. Chắc chắn", "B. Rủi ro", "C. Không chắc chắn", "D. Mơ hồ"],
        "answer": 1,
        "explain": "Rủi ro là khi bạn ước lượng được xác suất (VD: 60% mưa, 40% nắng) thông qua số liệu lịch sử. Chắc chắn là biết 100%. Không chắc chắn là hoàn toàn mù mờ."
    },
    {
        "question": "Mô hình ra quyết định nào thể hiện sự 'Lạc quan' tuyệt đối (Kỳ vọng điều tốt nhất sẽ xảy ra)?",
        "options": ["A. Maximin", "B. Minimax", "C. Maximax", "D. Hurwicz"],
        "answer": 2,
        "explain": "Maximax là Tiêu chuẩn Lạc quan (Chọn Max của các giá trị Max). Tức là luôn mong đợi kết quả rực rỡ nhất."
    },
    {
        "question": "Tiêu chuẩn Maximin (Wald) thường được dùng bởi những người ra quyết định có thái độ như thế nào?",
        "options": ["A. Lạc quan", "B. Chủ nghĩa hiện thực", "C. Bi quan", "D. Dựa vào may rủi"],
        "answer": 2,
        "explain": "Maximin là Tiêu chuẩn Bi quan. Người ra quyết định cho rằng điều tồi tệ nhất sẽ xảy ra, nên họ chọn phương án có 'kết quả xấu nhất' (Min) nhưng lại mang lại giá trị cao nhất trong đám xấu nhất đó."
    },
    {
        "question": "Trong tiêu chuẩn Minimax (Tiêu chuẩn tiếc nuối Savage), bước đầu tiên cần làm là gì?",
        "options": ["A. Tính giá trị EMV", "B. Lập bảng tiếc nuối", "C. Tìm Max của từng dòng", "D. Xác định hệ số alpha"],
        "answer": 1,
        "explain": "Bước 1 là lập Bảng tiếc nuối: Lấy giá trị lớn nhất của từng cột trừ đi các con số trong chính cột đó."
    },
    {
        "question": "Công thức của tiêu chuẩn Hurwicz (với hệ số lạc quan α) là gì?",
        "options": ["A. H = α.Max + (1 - α).Min", "B. H = α.Min + (1 - α).Max", "C. H = (Max + Min)/2", "D. H = α.EMV + (1-α).EOL"],
        "answer": 0,
        "explain": "H = α.Max + (1 - α).Min. Nó kết hợp giữa mức độ lạc quan (Max) và bi quan (Min)."
    },

    # --- PHẦN 2: QUẢN TRỊ CÔNG NGHỆ (THIO) ---
    {
        "question": "Trong mô hình THIO cấu thành công nghệ, chữ 'T' (Technoware) đại diện cho cái gì?",
        "options": ["A. Thông tin, quy trình", "B. Máy móc, thiết bị, dây chuyền", "C. Kỹ năng con người", "D. Tổ chức, quản lý"],
        "answer": 1,
        "explain": "Technoware là phần Vật thể/Phần cứng (Máy móc, thiết bị, công cụ)."
    },
    {
        "question": "Các bí quyết (know-how), công thức, tài liệu, quy trình sản xuất thuộc về yếu tố nào trong mô hình THIO?",
        "options": ["A. Technoware (T)", "B. Humanware (H)", "C. Inforware (I)", "D. Orgaware (O)"],
        "answer": 2,
        "explain": "Inforware (I) là phần Thông tin, dữ liệu, phần mềm, tài liệu hướng dẫn."
    },
    {
        "question": "Kinh nghiệm và năng lực sáng tạo của người lao động thuộc yếu tố nào?",
        "options": ["A. Humanware (H)", "B. Orgaware (O)", "C. Technoware (T)", "D. Inforware (I)"],
        "answer": 0,
        "explain": "Humanware là phần Con người: bao gồm kiến thức, kỹ năng, kinh nghiệm và thái độ."
    },

    # --- PHẦN 3: MARKETING 4P ---
    {
        "question": "Trong Marketing Mix (4P), chữ P nào là yếu tố DUY NHẤT tạo ra doanh thu cho doanh nghiệp?",
        "options": ["A. Product", "B. Price", "C. Place", "D. Promotion"],
        "answer": 1,
        "explain": "Price (Giá cả) là chữ P duy nhất mang tiền về. 3 chữ P còn lại đều làm tốn chi phí của doanh nghiệp."
    },
    {
        "question": "Hoạt động Quảng cáo, Quan hệ công chúng (PR), và Khuyến mãi thuộc về chữ P nào?",
        "options": ["A. Product", "B. Price", "C. Place", "D. Promotion"],
        "answer": 3,
        "explain": "Promotion là Xúc tiến thương mại / Truyền thông, giúp nhắc nhở và thuyết phục khách hàng mua sản phẩm."
    },

    # --- PHẦN 4: BÀI TOÁN TỒN KHO ---
    {
        "question": "Công thức đúng để tính Lượng đặt hàng kinh tế (EOQ) là gì? (D: Nhu cầu, S: Phí đặt hàng, H: Phí tồn trữ)",
        "options": ["A. √(2DS / H)", "B. √(DS / 2H)", "C. √(2DH / S)", "D. (D×S) / H"],
        "answer": 0,
        "explain": "EOQ = Căn bậc hai của (2 × D × S / H). Nhớ kỹ công thức này đi thi chắc chắn có!"
    },
    {
        "question": "Nếu đề bài cho Chi phí tồn trữ (H) là một tỷ lệ phần trăm (i%) thay vì số tiền cụ thể, ta tính H bằng cách nào?",
        "options": ["A. H = i%", "B. H = i% × Chi phí đặt hàng (S)", "C. H = i% × Giá mua (P)", "D. H = i% × Nhu cầu (D)"],
        "answer": 2,
        "explain": "H = i × P. Ví dụ: Chi phí lưu kho bằng 15% giá mua, thì H = 0.15 × Giá mua."
    },
    {
        "question": "Trong bài toán Tồn kho có CHIẾT KHẤU THEO SỐ LƯỢNG, khi tính Tổng chi phí (TC) ta bắt buộc PHẢI CỘNG THÊM chi phí nào?",
        "options": ["A. Dự trữ an toàn", "B. Chi phí đặt hàng", "C. Chi phí lưu kho", "D. Chi phí mua hàng (D × P)"],
        "answer": 3,
        "explain": "Đây là BẪY TỬ THẦN! Khi có chiết khấu, giá mua P thay đổi nên tổng tiền mua hàng (D.P) sẽ khác nhau. Phải cộng (D.P) vào TC để so sánh."
    },
    {
        "question": "Công thức tính Thời gian chu kỳ giữa 2 lần đặt hàng (T) là gì?",
        "options": ["A. T = D / EOQ", "B. T = Số ngày làm việc / N", "C. T = D / Số ngày làm việc", "D. T = EOQ / D"],
        "answer": 1,
        "explain": "T = Tổng số ngày làm việc trong năm chia cho Số lần đặt hàng (N)."
    },
    {
        "question": "Công thức tính Điểm tái đặt hàng (ROP) khi có dự trữ an toàn (SS) là gì? (d: nhu cầu mỗi ngày, L: thời gian giao hàng)",
        "options": ["A. ROP = d × L", "B. ROP = d / L + SS", "C. ROP = d × L + SS", "D. ROP = EOQ + SS"],
        "answer": 2,
        "explain": "ROP = Nhu cầu trong thời gian chờ (d × L) cộng thêm Lượng dự trữ an toàn (SS)."
    },

    # --- PHẦN 5: QUẢN LÝ DỰ ÁN (AON & PERT) ---
    {
        "question": "Trong sơ đồ mạng AON, khi tính thời gian SỚM NHẤT (ES, EF) - Tức là ĐI TỚI, nếu một nút nhận 2 mũi tên chĩa vào, ta lấy giá trị gì?",
        "options": ["A. Lấy giá trị MIN của các EF trước đó", "B. Lấy giá trị MAX của các EF trước đó", "C. Cộng các EF lại", "D. Lấy Trung bình cộng"],
        "answer": 1,
        "explain": "ĐI TỚI CHỌN MAX. Vì công việc này phải chờ TẤT CẢ các công việc trước nó hoàn thành xong mới được bắt đầu, nên phải chờ thằng xong trễ nhất (Max)."
    },
    {
        "question": "Trong sơ đồ mạng AON, khi tính thời gian MUỘN NHẤT (LS, LF) - Tức là ĐI LÙI, nếu một nút chĩa 2 mũi tên ra sau, ta lấy giá trị gì?",
        "options": ["A. Lấy giá trị MIN của các LS sau đó", "B. Lấy giá trị MAX của các LS sau đó", "C. Lấy giá trị 0", "D. Lấy EF của nó"],
        "answer": 0,
        "explain": "ĐI LÙI CHỌN MIN. Để không làm trễ thằng yêu cầu khắt khe nhất phía sau, nó phải xong sớm hơn (Min)."
    },
    {
        "question": "Thời gian dự trữ (Slack - S) của các công việc nằm trên ĐƯỜNG GĂNG bằng bao nhiêu?",
        "options": ["A. S > 0", "B. S < 0", "C. S = Thời gian dự án", "D. S = 0"],
        "answer": 3,
        "explain": "Công việc găng là công việc sống còn, không được phép chậm trễ dù chỉ 1 ngày => Dự trữ S = 0."
    },
    {
        "question": "Công thức tính Thời gian kỳ vọng (Te) trong sơ đồ PERT là gì? (a: lạc quan, m: bình thường, b: bi quan)",
        "options": ["A. (a + m + b) / 3", "B. (a + 2m + b) / 4", "C. (a + 4m + b) / 6", "D. (b - a) / 6"],
        "answer": 2,
        "explain": "Te = (a + 4m + b) / 6. Trọng số lớn nhất (4) dồn vào m (thời gian thường gặp nhất)."
    },
    {
        "question": "Công thức tính Phương sai (V) của một công việc trong PERT là gì?",
        "options": ["A. ((b - a) / 6)²", "B. (b - a) / 6", "C. ((b + a) / 6)²", "D. (a + 4m + b) / 6"],
        "answer": 0,
        "explain": "Phương sai = Bình phương của độ lệch chuẩn = ((b - a) / 6)²."
    },
    {
        "question": "BẪY TỬ THẦN: Khi tính Phương sai của TỔNG DỰ ÁN (V_p), ta tính bằng cách nào?",
        "options": ["A. Cộng phương sai của TẤT CẢ công việc lại", "B. Chỉ cộng phương sai của các công việc TRÊN ĐƯỜNG GĂNG", "C. Lấy Phương sai lớn nhất", "D. Lấy Trung bình cộng các phương sai"],
        "answer": 1,
        "explain": "CHỈ CỘNG PHƯƠNG SAI CỦA CÁC CÔNG VIỆC TRÊN ĐƯỜNG GĂNG. Rất nhiều bạn cộng hết nguyên cột là sai hoàn toàn nhé!"
    },
    {
        "question": "Để tính xác suất hoàn thành dự án bằng phân phối chuẩn, công thức tính Z-score là gì?",
        "options": ["A. Z = (Te - T) / σ", "B. Z = (T - Te) / σ", "C. Z = (T - Te) / V_p", "D. Z = T / Te"],
        "answer": 1,
        "explain": "Z = (Thời gian đề yêu cầu T - Thời gian kỳ vọng dự án Te) chia cho Độ lệch chuẩn σ (Căn bậc 2 của phương sai dự án V_p)."
    }
]

class DecuongQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Luyện Phản Xạ - Đề Cương QTKDCKS")
        self.root.geometry("950x700")
        self.root.configure(bg="#f5f6fa")
        
        # Phím Enter chuyển câu
        self.root.bind("<Return>", lambda event: self.handle_enter())
        
        self.current_question = 0
        self.score = 0
        
        # Xáo trộn câu hỏi
        random.shuffle(QUESTIONS)
        
        self.build_ui()
        self.load_question()

    def build_ui(self):
        # Tiêu đề
        self.lbl_title = tk.Label(self.root, text="LUYỆN PHẢN XẠ - ĐỀ CƯƠNG QTKD CHO KỸ SƯ", font=("Helvetica", 18, "bold"), bg="#192a56", fg="white", pady=15)
        self.lbl_title.pack(fill=tk.X)
        
        # Tracking điểm và số câu
        self.frame_top = tk.Frame(self.root, bg="#f5f6fa")
        self.frame_top.pack(fill=tk.X, padx=20, pady=10)
        
        self.lbl_status = tk.Label(self.frame_top, text="Câu hỏi: 1/22", font=("Helvetica", 13, "bold"), bg="#f5f6fa", fg="#c23616")
        self.lbl_status.pack(side=tk.LEFT)
        
        self.lbl_score = tk.Label(self.frame_top, text="Điểm: 0", font=("Helvetica", 13, "bold"), bg="#f5f6fa", fg="#44bd32")
        self.lbl_score.pack(side=tk.RIGHT)
        
        # Khung chứa câu hỏi
        self.frame_q = tk.Frame(self.root, bg="white", bd=2, relief=tk.GROOVE)
        self.frame_q.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.lbl_question = tk.Label(self.frame_q, text="", font=("Helvetica", 15, "bold"), bg="white", wraplength=800, justify="left", fg="#2f3640")
        self.lbl_question.pack(pady=25, padx=15, fill=tk.X)
        
        # Các nút đáp án
        self.btn_opts = []
        for i in range(4):
            btn = tk.Button(self.frame_q, text="", font=("Helvetica", 13), bg="#0097e6", fg="white", 
                            activebackground="#00a8ff", activeforeground="white", cursor="hand2",
                            command=lambda i=i: self.check_answer(i))
            btn.pack(fill=tk.X, padx=50, pady=8, ipady=6)
            self.btn_opts.append(btn)
            
        # Vùng giải thích đáp án
        self.lbl_explain = tk.Label(self.frame_q, text="", font=("Helvetica", 13, "italic"), bg="white", fg="#e1b12c", wraplength=800, justify="left")
        self.lbl_explain.pack(pady=20, padx=15, fill=tk.X)
        
        # Nút Next
        self.btn_next = tk.Button(self.root, text="Câu Tiếp Theo (Enter) >>", font=("Helvetica", 14, "bold"), bg="#4cd137", fg="white", 
                                  activebackground="#44bd32", activeforeground="white", cursor="hand2", command=self.next_question)
        self.btn_next.pack(pady=15, ipady=8, ipadx=30)
        self.btn_next.config(state=tk.DISABLED)

    def handle_enter(self):
        if self.btn_next['state'] == tk.NORMAL:
            self.next_question()

    def load_question(self):
        if self.current_question >= len(QUESTIONS):
            messagebox.showinfo("Hoàn Thành", f"Chúc mừng bạn đã hoàn thành bài Test!\n\nĐiểm số của bạn: {self.score}/{len(QUESTIONS)}\n\nLàm lại nhiều lần để tạo phản xạ nhé!")
            self.root.quit()
            return
            
        q_data = QUESTIONS[self.current_question]
        self.lbl_status.config(text=f"Câu hỏi: {self.current_question + 1}/{len(QUESTIONS)}")
        self.lbl_score.config(text=f"Điểm: {self.score}")
        
        self.lbl_question.config(text=q_data["question"])
        self.lbl_explain.config(text="")
        
        for i in range(4):
            self.btn_opts[i].config(text=q_data["options"][i], bg="#0097e6", state=tk.NORMAL)
            
        self.btn_next.config(state=tk.DISABLED)

    def check_answer(self, selected_idx):
        q_data = QUESTIONS[self.current_question]
        correct_idx = q_data["answer"]
        
        # Vô hiệu hóa nút sau khi bấm
        for btn in self.btn_opts:
            btn.config(state=tk.DISABLED)
            
        if selected_idx == correct_idx:
            self.btn_opts[selected_idx].config(bg="#4cd137") # Xanh lá
            self.score += 1
            self.lbl_score.config(text=f"Điểm: {self.score}")
            self.lbl_explain.config(text=f"✅ CHÍNH XÁC!\n=> {q_data['explain']}")
        else:
            self.btn_opts[selected_idx].config(bg="#e84118") # Đỏ
            self.btn_opts[correct_idx].config(bg="#4cd137") # Hiện đáp án đúng màu xanh
            self.lbl_explain.config(text=f"❌ SAI RỒI!\n=> {q_data['explain']}")
            
        self.btn_next.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1
        self.load_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = DecuongQuizApp(root)
    root.mainloop()