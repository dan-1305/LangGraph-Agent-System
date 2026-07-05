import asyncio
import edge_tts

# Kịch bản với các dấu chấm để ép AI ngừng đọc (mỗi dấu chấm ngưng khoảng 0.5s)
TEXT = """
Chào các bạn sinh viên kỹ thuật. . . . Chào mừng các bạn đến với buổi tổng ôn thần tốc môn Quản trị Kinh doanh cho Kỹ sư. . . . . .
Hôm nay, cô sẽ hướng dẫn các bạn cách tư duy để xử lý gọn gàng các dạng bài tập thực hành thường gặp trong đề thi. Các bạn hãy thả lỏng và lắng nghe nhé. . . . . .

Chúng ta bắt đầu với CHƯƠNG HAI: Ra quyết định. . . .
Dạng bài đầu tiên là Quyết định Rủi ro, khi đề bài cho sẵn bảng lợi nhuận và XÁC SUẤT. . . .
Các bạn hãy nhớ ba công thức thần thánh: E M V, E O L và E V P I. . . .
E M V là Giá trị tiền tệ kỳ vọng. Công thức rất đơn giản: Lấy Lợi nhuận nhân với Xác suất tương ứng rồi cộng lại. Tính cho từng phương án, và nhớ là CHỌN PHƯƠNG ÁN CÓ E M V LỚN NHẤT. . . . . .
E O L là Tổn thất cơ hội kỳ vọng. Bước một, lập ma trận tiếc nuối bằng cách lấy giá trị LỚN NHẤT của từng cột trừ đi các giá trị trong cột đó. . . . Bước hai, lấy giá trị tiếc nuối nhân với Xác suất. Trái ngược với E M V, ở đây các bạn phải CHỌN PHƯƠNG ÁN CÓ E O L NHỎ NHẤT, vì chẳng ai muốn hối tiếc nhiều cả. . . . . .
E V P I là Giá trị thông tin hoàn hảo. Nó luôn bằng giá trị E O L nhỏ nhất mà các bạn vừa tìm được. Dùng nó để so sánh với giá mua thông tin xem có đáng tiền không nhé. . . . . . . .

Tiếp theo là Quyết định Không chắc chắn, khi đề bài KHÔNG cho xác suất. . . .
Maximax là tiêu chuẩn lạc quan. Chọn cái LỜI NHẤT trong những cái lời nhất. . . .
Maximin là tiêu chuẩn bi quan. Trong những trường hợp xấu nhất, hãy chọn phương án LỖ ÍT NHẤT. . . .
Còn tiêu chuẩn Hurwicz thì dùng hệ số alpha. Lấy alpha nhân với Max, cộng cho một trừ alpha nhân với Min. Chốt lại là chọn phương án có giá trị lớn nhất. . . . . . . .

Bây giờ chúng ta sang CHƯƠNG BA và BỐN: Tài chính Kế toán. . . . . .
Trong Bảng Cân đối kế toán, hãy khắc cốt ghi tâm nguyên tắc: Tổng Tài Sản luôn luôn bằng Tổng Nợ cộng Vốn Chủ Sở Hữu. . . . . .
Với Báo cáo kết quả kinh doanh, hãy nhớ thứ tự trừ tiền: . . .
Doanh thu trừ Giá vốn ra Lãi gộp. . . . Lãi gộp trừ Chi phí hoạt động trừ Lãi vay ra Lợi nhuận trước thuế. . . . Cuối cùng, trừ đi Thuế là ra Lợi nhuận sau thuế. . . . . . . .
            
Về các tỷ số tài chính, cô lưu ý hai tỷ số hay thi nhất: . . .
Tỷ số thanh toán hiện hành bằng Tài sản lưu động chia cho Nợ ngắn hạn. . . .
Tỷ số thanh toán nhanh thì khắt khe hơn, phải lấy Tài sản lưu động TRỪ ĐI Hàng tồn kho, rồi mới chia cho Nợ ngắn hạn. Vì hàng tồn kho đâu thể bán ngay ra tiền được đúng không nào? . . . . . . . .

Chúng ta đi tiếp sang CHƯƠNG NĂM: Quản lý hàng tồn kho. . . . . .
E O Q là điểm đặt hàng tối ưu. Công thức: Căn bậc hai của, hai nhân D nhân S, tất cả chia cho H. . . . Trong đó D là Nhu cầu năm, S là Chi phí một lần đặt, H là Chi phí lưu kho. . . . . .
Khi tính Điểm đặt hàng lại R O P, các bạn lấy nhu cầu bình quân một NGÀY nhân với thời gian giao hàng. Nếu đề có cho Dự trữ an toàn thì nhớ CỘNG THÊM vào nhé. . . . . . . .

Cuối cùng là CHƯƠNG BẢY: Quản trị dự án sơ đồ PERT, CPM. . . . . .
Đường găng, hay Critical Path, chính là nhánh có thời gian DÀI NHẤT từ đầu đến cuối dự án. Thời gian của đường găng chính là thời gian hoàn thành dự án. . . . . .
Các công việc nằm trên đường găng có thời gian dự trữ Slack bằng KHÔNG. Tuyệt đối không được chậm trễ. . . . . .
Còn với sơ đồ PERT, để tính thời gian kỳ vọng T e, các bạn lấy: Thời gian Lạc quan, cộng với 4 lần thời gian Bình thường, cộng thời gian Bi quan. Tất cả đem chia cho 6. . . . . . . . . .

Bây giờ, hãy thả lỏng và để kiến thức tự ngấm vào đầu... . . . . . .
E M V. . . chọn Max. . . . . .
E O L. . . chọn Min. . . . . .
E V P I. . . bằng Min E O L. . . . . .
Tổng tài sản. . . bằng Tổng nợ cộng Vốn chủ sở hữu. . . . . .
Thanh toán nhanh. . . nhớ trừ đi hàng tồn kho. . . . . .
E O Q. . . căn bậc hai của hai D S chia H. . . . . .
Đường găng. . . là đường dài nhất. . . . . . . . . .
Mọi kiến thức đã lưu vào bộ nhớ. Chúc các bạn kỹ sư tương lai ngủ ngon... và thi tốt...
"""

VOICE = "vi-VN-HoaiMyNeural"
OUTPUT_FILE = "docs/QTKDCKS/Podcast_QTKDCKS_Fix.mp3"

async def amain() -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE, rate="-10%", pitch="-5Hz")
    await communicate.save(OUTPUT_FILE)
    print(f"Done saving to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(amain())
