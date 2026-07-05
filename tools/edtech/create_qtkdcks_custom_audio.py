import os
from gtts import gTTS

TEXT_CHUNKS = [
    "Câu 1: Các bước trong quy trình ra quyết định quản lý. Tham khảo: Chương 2 Ra quyết định.",
    "1. Nhận diện vấn đề: Xác định tình huống hoặc thách thức cần giải quyết.",
    "2. Xác định tiêu chuẩn: Đưa ra các mốc, chỉ tiêu để đánh giá. Ví dụ: chi phí, thời gian, chất lượng.",
    "3. Đánh giá trọng số: Phân bổ mức độ quan trọng cho từng tiêu chuẩn.",
    "4. Phát triển các phương án: Liệt kê tất cả các giải pháp khả thi.",
    "5. Lựa chọn phương án: Đánh giá và chọn ra phương án tối ưu nhất dựa trên các tiêu chuẩn.",
    "6. Thực thi và đánh giá: Triển khai phương án đã chọn và đo lường tính hiệu quả.",
    
    "Câu 2: Phân biệt quyết định trong điều kiện chắc chắn, rủi ro và không chắc chắn. Tham khảo: Chương 2 Ra quyết định, trang 27 đến 28.",
    "Chắc chắn: Người ra quyết định biết chính xác 100 phần trăm kết quả của từng phương án sẽ xảy ra. Môi trường hoàn toàn tĩnh.",
    "Rủi ro: Không biết chắc kết quả, nhưng biết được xác suất, tỷ lệ phần trăm xảy ra của từng trường hợp. Môi trường có biến động nhưng đo lường được.",
    "Không chắc chắn: Hoàn toàn mù mờ, không có thông tin và cũng không biết xác suất xảy ra của các trường hợp. Môi trường hoàn toàn vô định.",

    "Câu 3: Cấu trúc bảng cân đối kế toán và mối quan hệ Tài sản – Nợ – Vốn. Tham khảo: Chương 3 Kế toán tài chính, trang 7 đến 16.",
    "Tài sản: Toàn bộ nguồn lực mang lại lợi ích kinh tế mà doanh nghiệp đang sở hữu. Ví dụ: Tiền mặt, Hàng tồn kho, Máy móc, Bất động sản.",
    "Nguồn vốn: Nơi cung cấp nguồn lực để hình thành nên Tài sản. Bao gồm:",
    "Nợ phải trả: Vay mượn từ bên ngoài như Ngân hàng, nhà cung cấp.",
    "Vốn chủ sở hữu: Tiền tự có của chủ doanh nghiệp hoặc cổ đông.",
    "Mối quan hệ cốt lõi: TỔNG TÀI SẢN bằng TỔNG NỢ cộng VỐN CHỦ SỞ HỮU.",

    "Câu 4: Cấu trúc báo cáo kết quả kinh doanh và ý nghĩa. Tham khảo: Chương 3 Kế toán tài chính.",
    "Cấu trúc: Đi từ Doanh thu thuần, Trừ Giá vốn hàng bán, thành Lãi gộp. Trừ Chi phí hoạt động, thành Lợi nhuận trước thuế. L N T T. Trừ Thuế, thành Lợi nhuận sau thuế. L N S T.",
    "Ý nghĩa: Cho biết bức tranh Lời Lỗ của doanh nghiệp trong một khoảng thời gian nhất định, thường là quý hoặc năm. Đánh giá trực tiếp hiệu quả hoạt động kinh doanh.",

    "Câu 5: Ý nghĩa các tỷ số tài chính cơ bản. Tham khảo: Chương 3 Kế toán tài chính, trang 33 đến 39.",
    "1. Tỷ số nợ. Bằng Tổng nợ chia Tổng tài sản: Cho biết bao nhiêu phần trăm tài sản được tài trợ bằng tiền đi vay. Tỷ lệ càng cao, rủi ro tài chính càng lớn.",
    "2. Tỷ số thanh toán hiện hành. Bằng Tài sản lưu động chia Nợ ngắn hạn: Đo lường khả năng trả các khoản nợ sắp đến hạn bằng tài sản ngắn hạn. Tốt nhất lớn hơn 1.",
    "3. Tỷ số thanh toán nhanh. Bằng Tài sản lưu động trừ Hàng tồn kho, rồi chia Nợ ngắn hạn: Giống tỷ số trên nhưng loại bỏ Hàng tồn kho vì Hàng tồn kho khó quy đổi ra tiền mặt ngay lập tức. Đánh giá tính thanh khoản khắt khe hơn.",
    "4. Vòng quay tài sản. Bằng Doanh thu chia Tổng tài sản: Đo lường hiệu suất sử dụng tài sản để tạo ra doanh thu. Số vòng quay càng lớn, quản lý tài sản càng hiệu quả.",

    "Phần Công thức:",
    "1. RA QUYẾT ĐỊNH. CHƯƠNG 2.",
    "E M V. Giá trị tiền tệ kỳ vọng, Bằng Lợi nhuận nhân Xác suất, cộng Lợi nhuận nhân Xác suất. Suy ra, CHỌN MAX E M V.",
    "E O L. Tổn thất cơ hội kỳ vọng:",
    "Bước 1: Lập ma trận tiếc nuối. Lấy Max cột trừ Các giá trị trong cột đó.",
    "Bước 2: E O L bằng Giá trị tiếc nuối nhân Xác suất. Suy ra, CHỌN MIN E O L.",
    "E V P I. Giá trị thông tin hoàn hảo, bằng Min E O L.",
    "Maximax: Lạc quan, Suy ra, CHỌN MAX CỦA NHỮNG CÁI MAX.",
    "Maximin: Bi quan, Suy ra, CHỌN MAX CỦA NHỮNG CÁI MIN. Chọn lỗ ít nhất.",
    "Hurwicz. Với hệ số alpha: H bằng alpha nhân Max cộng 1 trừ alpha nhân Min. Suy ra, CHỌN MAX H.",

    "2. KẾ TOÁN VÀ TÀI CHÍNH. CHƯƠNG 3.",
    "TỔNG TÀI SẢN bằng TỔNG NỢ cộng VỐN CHỦ SỞ HỮU.",
    "Lãi gộp bằng Doanh thu trừ Giá vốn hàng bán.",
    "Lợi nhuận trước thuế bằng Lãi gộp trừ Chi phí Hoạt động trừ Lãi vay.",
    "Lợi nhuận sau thuế bằng Lợi nhuận trước thuế trừ Thuế. Hoặc Lợi nhuận trước thuế nhân 1 trừ Thuế suất.",
    "Lợi nhuận giữ lại cuối kỳ bằng Lợi nhuận giữ lại đầu kỳ cộng Lợi nhuận sau thuế trừ Cổ tức.",
    "Tỷ số nợ bằng Tổng nợ chia Tổng tài sản.",
    "Thanh toán hiện hành, Current ratio, bằng Tài sản lưu động chia Nợ ngắn hạn.",
    "Thanh toán nhanh, Quick ratio, bằng Tài sản lưu động trừ Hàng tồn kho chia Nợ ngắn hạn.",
    "Vòng quay tài sản bằng Doanh thu chia Tổng tài sản.",
    "Kỳ thu tiền bình quân bằng Khoản phải thu chia Doanh thu chia 365. Hoặc lấy Khoản phải thu chia Doanh thu bình quân ngày.",

    "3. QUẢN LÝ HÀNG TỒN KHO. E O Q và R O P. CHƯƠNG 7.",
    "Điểm đặt hàng tối ưu E O Q, Bằng Căn bậc hai của 2 nhân D nhân S chia H.",
    "Trong đó: D là Nhu cầu năm, S là Chi phí 1 lần đặt hàng, H là Chi phí lưu trữ 1 đơn vị trên năm.",
    "Số lần đặt hàng N bằng D chia E O Q.",
    "Chu kỳ đặt hàng T bằng Số ngày làm việc trong năm chia N.",
    "Tổng chi phí T C bằng D chia E O Q nhân S cộng E O Q chia 2 nhân H.",
    "Nhu cầu bình quân ngày d nhỏ, Bằng Nhu cầu năm chia Số ngày làm việc.",
    "Điểm đặt hàng lại R O P bằng d nhỏ nhân Lead time cộng Dự trữ an toàn, Nếu có.",

    "4. QUẢN TRỊ DỰ ÁN. P E R T, C P M, CHƯƠNG 9.",
    "Thời gian hoàn thành dự án bằng Tổng thời gian của NHÁNH DÀI NHẤT, còn gọi là Đường găng.",
    "Đường găng, Critical Path: Là nhánh dài nhất. Các công việc trên đường găng có Thời gian dự trữ Slack bằng 0.",
    "Thời gian dự trữ Slack bằng Thời gian hoàn thành dự án Max trừ Thời gian của nhánh chứa công việc đó.",
    "Thời gian kỳ vọng T e bằng a cộng 4 m cộng b chia 6.",
    "Phương sai V bằng b trừ a chia 6 tất cả bình phương."
]

OUTPUT_FILE = "docs/QTKDCKS/Podcast_Custom_QTKDCKS.mp3"

def create_audio():
    print("Khoi tao gTTS va noi file MP3 truc tiep...")
    with open(OUTPUT_FILE, 'wb') as outfile:
        for i, text in enumerate(TEXT_CHUNKS):
            print(f"Dang render doan {i+1}/{len(TEXT_CHUNKS)}...")
            chunk_file = f"temp_chunk_custom_{i}.mp3"
            try:
                # Chèn vài dấu chấm để có khoảng ngưng nhỏ
                text_with_pause = text + " . . . "
                tts = gTTS(text=text_with_pause, lang='vi', slow=False)
                tts.save(chunk_file)
                with open(chunk_file, 'rb') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                print(f"Loi o doan {i}: {e}")
            finally:
                if os.path.exists(chunk_file):
                    os.remove(chunk_file)
            
    print(f"Hoan thanh! Ban co the nghe thu file Podcast tai: {OUTPUT_FILE}")

if __name__ == "__main__":
    os.makedirs("docs/QTKDCKS", exist_ok=True)
    create_audio()
