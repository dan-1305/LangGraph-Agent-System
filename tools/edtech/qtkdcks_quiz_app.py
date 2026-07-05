import tkinter as tk
from tkinter import messagebox
import random

# --- NGÂN HÀNG CÂU HỎI TRẮC NGHIỆM QTKDCKS ---
QUESTIONS = [
    # 1. LÝ THUYẾT CỐT LÕI
    {
        "question": "Trong quy trình ra quyết định quản lý, bước đầu tiên là gì?",
        "options": ["A. Lựa chọn phương án", "B. Phát triển các phương án", "C. Nhận diện vấn đề", "D. Xác định tiêu chuẩn đánh giá"],
        "answer": 2,
        "explain": "Bước đầu tiên là phải 'Nhận diện vấn đề' để biết mình cần quyết định việc gì. (Trích: Chương 2)"
    },
    {
        "question": "Quyết định trong điều kiện 'Không chắc chắn' có đặc điểm gì?",
        "options": ["A. Biết chính xác kết quả", "B. Biết được xác suất xảy ra của từng trường hợp", "C. Không biết xác suất xảy ra", "D. Môi trường hoàn toàn tĩnh"],
        "answer": 2,
        "explain": "Trong điều kiện Không chắc chắn, môi trường hoàn toàn vô định, người ra quyết định KHÔNG THỂ biết được xác suất xảy ra (Trích: Chương 2)."
    },
    {
        "question": "Phương trình cơ bản nhất của Bảng cân đối kế toán là gì?",
        "options": ["A. Tổng Tài Sản = Tổng Nợ - Vốn Chủ Sở Hữu", "B. Tổng Tài Sản = Tổng Nợ + Vốn Chủ Sở Hữu", "C. Lợi nhuận = Doanh thu - Chi phí", "D. Tổng Nợ = Tổng Tài Sản + Vốn Chủ Sở Hữu"],
        "answer": 1,
        "explain": "Đúng! Tài sản (cái doanh nghiệp sở hữu) luôn được tài trợ từ 2 nguồn: Đi vay (Tổng Nợ) và Tiền tự có (Vốn Chủ Sở Hữu)."
    },
    {
        "question": "Chỉ số 'Thanh toán nhanh' khác với 'Thanh toán hiện hành' ở điểm nào?",
        "options": ["A. Trừ đi Lợi nhuận", "B. Cộng thêm Lãi vay", "C. Trừ đi Hàng tồn kho", "D. Nhân với Doanh thu"],
        "answer": 2,
        "explain": "Thanh toán nhanh (Quick ratio) khắt khe hơn, bắt buộc phải TRỪ ĐI Hàng tồn kho ra khỏi Tài sản lưu động, vì hàng tồn kho không thể bán lấy tiền ngay lập tức."
    },
    
    # 2. CÔNG THỨC TÍNH TOÁN
    {
        "question": "Khi tính Giá trị tiền tệ kỳ vọng (EMV), ta sử dụng công thức nào?",
        "options": ["A. Lợi nhuận + Xác suất", "B. Tổng (Lợi nhuận × Xác suất)", "C. Lợi nhuận / Xác suất", "D. Max(Lợi nhuận) - Min(Lợi nhuận)"],
        "answer": 1,
        "explain": "EMV = Tổng của (Lợi nhuận ở từng trạng thái × Xác suất của trạng thái đó). Chọn phương án có Max EMV."
    },
    {
        "question": "Công thức tính điểm đặt hàng tối ưu EOQ là?",
        "options": ["A. √(2DS/H)", "B. √(DS/2H)", "C. √(2DH/S)", "D. (D×S)/H"],
        "answer": 0,
        "explain": "EOQ = Căn bậc 2 của (2 × Nhu cầu D × Chi phí đặt hàng S / Chi phí lưu kho H)."
    },
    {
        "question": "Thời gian kỳ vọng (Te) trong sơ đồ PERT được tính như thế nào? (Với a: Lạc quan, m: Bình thường, b: Bi quan)",
        "options": ["A. (a + m + b)/3", "B. (a + 2m + b)/4", "C. (a + 4m + b)/6", "D. (b - a)/6"],
        "answer": 2,
        "explain": "Đúng! Te = (a + 4m + b)/6. Còn (b - a)/6 dùng để tính Độ lệch chuẩn (Sigma)."
    },
    {
        "question": "Trong quản trị dự án (PERT/CPM), Thời gian dự trữ (Slack) của các công việc nằm trên ĐƯỜNG GĂNG bằng bao nhiêu?",
        "options": ["A. Lớn hơn 0", "B. Bằng 0", "C. Nhỏ hơn 0", "D. Bằng thời gian hoàn thành dự án"],
        "answer": 1,
        "explain": "Các công việc trên đường găng (đường dài nhất) KHÔNG CÓ thời gian dự trữ (Slack = 0). Nếu trễ 1 ngày thì toàn bộ dự án sẽ trễ theo."
    },

    # 3. MÔ PHỎNG TÍNH TOÁN NHANH
    {
        "question": "Cho Doanh thu = 10,000; Giá vốn hàng bán = 60% doanh thu. Tính Lãi gộp?",
        "options": ["A. 10,000", "B. 6,000", "C. 4,000", "D. 16,000"],
        "answer": 2,
        "explain": "Lãi gộp = Doanh thu - Giá vốn. Giá vốn = 60% * 10.000 = 6.000. Suy ra Lãi gộp = 10.000 - 6.000 = 4.000."
    },
    {
        "question": "Cho Tổng tài sản = 500,000; Tổng nợ = 200,000. Vốn chủ sở hữu bằng bao nhiêu?",
        "options": ["A. 700,000", "B. 300,000", "C. 200,000", "D. 2.5"],
        "answer": 1,
        "explain": "Phương trình kế toán: Tổng Tài sản = Tổng Nợ + Vốn chủ sở hữu. Suy ra Vốn chủ sở hữu = 500.000 - 200.000 = 300.000."
    },
    {
        "question": "Doanh nghiệp có TS lưu động = 300,000; Hàng tồn kho = 100,000; Nợ ngắn hạn = 150,000. Tỷ số thanh toán nhanh (Quick ratio) là bao nhiêu?",
        "options": ["A. 2.0", "B. 1.33", "C. 0.75", "D. 2.66"],
        "answer": 1,
        "explain": "Thanh toán nhanh = (TS lưu động - Hàng tồn kho) / Nợ ngắn hạn = (300.000 - 100.000) / 150.000 = 200.000 / 150.000 = 1.33."
    },
    {
        "question": "Một dự án PERT có Thời gian Lạc quan (a) = 2, Bình thường (m) = 4, Bi quan (b) = 8. Tính Thời gian kỳ vọng (Te)?",
        "options": ["A. 4.66", "B. 4.00", "C. 4.33", "D. 1.00"],
        "answer": 2,
        "explain": "Te = (a + 4m + b)/6 = (2 + 4*4 + 8)/6 = 26/6 = 4.33."
    },
    {
        "question": "Với dự án trên (a=2, m=4, b=8), Phương sai (V) bằng bao nhiêu?",
        "options": ["A. 1", "B. 6", "C. 36", "D. 1.33"],
        "answer": 0,
        "explain": "Phương sai V = ((b-a)/6)^2 = ((8-2)/6)^2 = (6/6)^2 = 1^2 = 1."
    },
    {
        "question": "Để tìm Điểm đặt hàng lại (ROP) khi có Dự trữ an toàn, ta dùng công thức nào?",
        "options": ["A. ROP = Nhu cầu * Lead time", "B. ROP = (Nhu cầu * Lead time) + Dự trữ an toàn", "C. ROP = Nhu cầu / Lead time", "D. ROP = EOQ + Dự trữ an toàn"],
        "answer": 1,
        "explain": "Điểm đặt hàng lại (khi kho còn bao nhiêu thì gọi mua tiếp) = Nhu cầu sử dụng trong số ngày chờ giao hàng (Lead time) + Lượng dự trữ an toàn phòng ngừa rủi ro."
    },

    # 4. PHẢN XẠ CÔNG THỨC (ĐIỀN CHỖ TRỐNG)
    {
        "question": "[?] = Tổng Nợ + Vốn Chủ Sở Hữu",
        "options": ["A. Lợi Nhuận", "B. Giá Vốn", "C. Tổng Tài Sản", "D. Doanh Thu"],
        "answer": 2,
        "explain": "Đúng! Phương trình cơ bản: Tổng Tài Sản luôn bằng nguồn tiền vay (Tổng Nợ) cộng với nguồn tiền tự có (Vốn Chủ Sở Hữu)."
    },
    {
        "question": "Lợi nhuận trước thuế (LNTT) = Lãi gộp - [?] - Lãi vay",
        "options": ["A. Thuế TNDN", "B. Chi phí hoạt động", "C. Giá vốn hàng bán", "D. Khấu hao"],
        "answer": 1,
        "explain": "Từ Lãi gộp, ta phải trừ đi Chi phí hoạt động (bán hàng, quản lý) và Lãi vay thì mới ra Lợi nhuận trước thuế."
    },
    {
        "question": "Thanh toán nhanh = (Tài sản lưu động - [?]) / Nợ ngắn hạn",
        "options": ["A. Tiền mặt", "B. Khoản phải thu", "C. Lợi nhuận", "D. Hàng tồn kho"],
        "answer": 3,
        "explain": "Vì Hàng tồn kho rất khó thanh khoản (bán ngay ra tiền) nên tỷ số thanh toán nhanh khắt khe yêu cầu phải loại bỏ Hàng tồn kho ra khỏi Tài sản lưu động."
    },
    {
        "question": "Vòng quay tài sản = [?] / Tổng tài sản",
        "options": ["A. Vốn chủ sở hữu", "B. Lợi nhuận", "C. Doanh thu", "D. Nợ"],
        "answer": 2,
        "explain": "Vòng quay tài sản đo lường mức độ hiệu quả: 1 đồng tài sản tạo ra được bao nhiêu đồng Doanh thu."
    },
    {
        "question": "Thời gian kỳ vọng (Te) = (a + [?] + b) / 6",
        "options": ["A. 2m", "B. 3m", "C. 4m", "D. 6m"],
        "answer": 2,
        "explain": "Công thức PERT: Thời gian kỳ vọng Te = (Lạc quan + 4 × Bình thường + Bi quan) / 6."
    },
    {
        "question": "EOQ = Căn bậc hai của (2 × D × S / [?])",
        "options": ["A. H", "B. N", "C. ROP", "D. T"],
        "answer": 0,
        "explain": "H là Chi phí lưu kho một đơn vị trong một năm. EOQ = √(2DS/H)."
    },
    {
        "question": "Lợi nhuận giữ lại cuối kỳ = LNGL đầu kỳ + [?] - Cổ tức",
        "options": ["A. Doanh thu", "B. Lợi nhuận sau thuế", "C. Lợi nhuận trước thuế", "D. Lãi gộp"],
        "answer": 1,
        "explain": "Phần lợi nhuận sau khi đã đóng thuế (LNST), doanh nghiệp sẽ dùng để chia cổ tức, phần còn lại mới được giữ lại."
    },
    {
        "question": "Hệ số Hurwicz (H) = α × [?] + (1 - α) × [?]",
        "options": ["A. Min, Max", "B. Lãi, Lỗ", "C. Max, Min", "D. EMV, EOL"],
        "answer": 2,
        "explain": "Hệ số Hurwicz = α × Giá trị Max + (1 - α) × Giá trị Min. Trọng số α thường nghiêng về phía lạc quan (Max)."
    },
    {
        "question": "Kỳ thu tiền bình quân = Khoản phải thu / [?]",
        "options": ["A. Hàng tồn kho", "B. Lợi nhuận gộp", "C. Doanh thu bình quân ngày", "D. Nợ ngắn hạn"],
        "answer": 2,
        "explain": "Kỳ thu tiền (bao nhiêu ngày mới đòi được nợ) = Khoản phải thu / (Doanh thu cả năm / 365 ngày)."
    },

    # 5. BẪY & CÚ LỪA HAY GẶP LÚC THI
    {
        "question": "BẪY TỬ THẦN: Khi lập ma trận EOL (Tổn thất cơ hội), ta lấy giá trị nào trừ đi giá trị trong cột?",
        "options": ["A. Lấy giá trị Min của cột đó", "B. Lấy 0", "C. Lấy giá trị Max của cột đó", "D. Lấy giá trị Max của cả bảng"],
        "answer": 2,
        "explain": "Cú lừa kinh điển! Phải tìm giá trị MAX của CỘT đang xét, sau đó lấy chính số Max đó TRỪ đi từng con số trong cột (chứ không phải lấy số trong cột trừ đi Max đâu nha)."
    },
    {
        "question": "BẪY TỬ THẦN: Khi so sánh các phương án bằng EOL, ta sẽ chọn phương án nào?",
        "options": ["A. Có EOL bằng 0", "B. Có EOL cao nhất (Max EOL)", "C. Có EOL thấp nhất (Min EOL)", "D. Bằng với EVPI"],
        "answer": 2,
        "explain": "Chính xác! Cẩn thận nhầm với EMV (chọn Max). Đối với Tổn thất cơ hội EOL, ai cũng muốn rủi ro/tiếc nuối ít nhất, nên BẮT BUỘC PHẢI CHỌN MIN EOL."
    },
    {
        "question": "CÚ LỪA: Lợi nhuận gộp (Lãi gộp) được tính bằng:",
        "options": ["A. Doanh thu - Chi phí hoạt động", "B. Doanh thu - Lãi vay", "C. LNTT - Thuế", "D. Doanh thu - Giá vốn hàng bán"],
        "answer": 3,
        "explain": "Nhiều sinh viên hay lấy Doanh thu trừ thẳng Chi phí hoạt động. Sai bét! Phải lấy Doanh thu trừ Giá vốn (Tiền mua hàng) ra Lãi gộp trước đã!"
    },
    {
        "question": "CÚ LỪA: Công thức tính Phương sai (V) trong PERT là gì?",
        "options": ["A. ((b - a)/6)^2", "B. (b - a)/6", "C. (a + 4m + b)/6", "D. ((a + b)/2)^2"],
        "answer": 0,
        "explain": "Đừng nhầm với Độ lệch chuẩn! Độ lệch chuẩn là (b-a)/6. Phương sai (Variance) là bình phương của Độ lệch chuẩn, tức là ((b-a)/6)^2."
    },
    {
        "question": "BẪY TỪ KHÓA: Tiêu chuẩn Hurwicz là tiêu chuẩn gì?",
        "options": ["A. Lạc quan", "B. Bi quan", "C. Đồng khả năng", "D. Sử dụng hệ số α"],
        "answer": 3,
        "explain": "Lạc quan là Maximax. Bi quan là Maximin. Còn Hurwicz là nửa nọ nửa kia, lai ghép giữa Max và Min bằng cách dùng hệ số alpha (α)."
    },
    {
        "question": "EVPI (Giá trị thông tin hoàn hảo) luôn bằng với giá trị nào?",
        "options": ["A. Max EMV", "B. Min EOL", "C. Max EOL", "D. Min EMV"],
        "answer": 1,
        "explain": "Một mẹo giải nhanh siêu đỉnh: Giá trị thông tin (EVPI) LUÔN LUÔN BẰNG giá trị Min EOL. Nhớ cái này để check chéo đáp án bài toán."
    }
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Luyện Thi Trắc Nghiệm QTKDCKS")
        self.root.geometry("900x700") # Tăng kích thước
        self.root.configure(bg="#f4f6f9")
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
        self.lbl_title = tk.Label(self.root, text="LUYỆN THI QTKD CHO KỸ SƯ", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="white", pady=15)
        self.lbl_title.pack(fill=tk.X)
        
        # Tracking điểm và số câu
        self.frame_top = tk.Frame(self.root, bg="#f4f6f9")
        self.frame_top.pack(fill=tk.X, padx=20, pady=10)
        
        self.lbl_status = tk.Label(self.frame_top, text="Câu hỏi: 1/14", font=("Helvetica", 12, "bold"), bg="#f4f6f9", fg="#e74c3c")
        self.lbl_status.pack(side=tk.LEFT)
        
        self.lbl_score = tk.Label(self.frame_top, text="Điểm: 0", font=("Helvetica", 12, "bold"), bg="#f4f6f9", fg="#27ae60")
        self.lbl_score.pack(side=tk.RIGHT)
        
        # Khung chứa câu hỏi
        self.frame_q = tk.Frame(self.root, bg="white", bd=2, relief=tk.GROOVE)
        self.frame_q.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.lbl_question = tk.Label(self.frame_q, text="", font=("Helvetica", 14, "bold"), bg="white", wraplength=700, justify="left")
        self.lbl_question.pack(pady=20, padx=10, fill=tk.X)
        
        # Các nút đáp án
        self.btn_opts = []
        for i in range(4):
            btn = tk.Button(self.frame_q, text="", font=("Helvetica", 13), bg="#3498db", fg="white", 
                            activebackground="#2980b9", activeforeground="white", cursor="hand2",
                            command=lambda i=i: self.check_answer(i))
            btn.pack(fill=tk.X, padx=40, pady=8, ipady=5)
            self.btn_opts.append(btn)
            
        # Vùng giải thích đáp án
        self.lbl_explain = tk.Label(self.frame_q, text="", font=("Helvetica", 12, "italic"), bg="white", fg="#e67e22", wraplength=700, justify="left")
        self.lbl_explain.pack(pady=15, padx=10, fill=tk.X)
        
        # Nút Next
        self.btn_next = tk.Button(self.root, text="Câu Tiếp Theo (Enter) >>", font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white", 
                                  activebackground="#27ae60", activeforeground="white", cursor="hand2", command=self.next_question)
        self.btn_next.pack(pady=10, ipady=5, ipadx=20)
        self.btn_next.config(state=tk.DISABLED)

    def handle_enter(self):
        if self.btn_next['state'] == tk.NORMAL:
            self.next_question()

    def load_question(self):
        if self.current_question >= len(QUESTIONS):
            messagebox.showinfo("Hoàn Thành", f"Chúc mừng bạn đã hoàn thành bài Test!\nĐiểm số của bạn: {self.score}/{len(QUESTIONS)}")
            self.root.quit()
            return
            
        q_data = QUESTIONS[self.current_question]
        self.lbl_status.config(text=f"Câu hỏi: {self.current_question + 1}/{len(QUESTIONS)}")
        self.lbl_score.config(text=f"Điểm: {self.score}")
        
        self.lbl_question.config(text=q_data["question"])
        self.lbl_explain.config(text="")
        
        for i in range(4):
            self.btn_opts[i].config(text=q_data["options"][i], bg="#3498db", state=tk.NORMAL)
            
        self.btn_next.config(state=tk.DISABLED)

    def check_answer(self, selected_idx):
        q_data = QUESTIONS[self.current_question]
        correct_idx = q_data["answer"]
        
        # Vô hiệu hóa nút sau khi bấm
        for btn in self.btn_opts:
            btn.config(state=tk.DISABLED)
            
        if selected_idx == correct_idx:
            self.btn_opts[selected_idx].config(bg="#2ecc71") # Xanh lá
            self.score += 1
            self.lbl_score.config(text=f"Điểm: {self.score}")
            self.lbl_explain.config(text=f"✅ CHÍNH XÁC!\nGiải thích: {q_data['explain']}")
        else:
            self.btn_opts[selected_idx].config(bg="#e74c3c") # Đỏ
            self.btn_opts[correct_idx].config(bg="#2ecc71") # Hiện đáp án đúng màu xanh
            self.lbl_explain.config(text=f"❌ SAI RỒI!\nGiải thích: {q_data['explain']}")
            
        self.btn_next.config(state=tk.NORMAL)

    def next_question(self):
        self.current_question += 1
        self.load_question()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
