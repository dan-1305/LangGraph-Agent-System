import os
from gtts import gTTS
from pydub import AudioSegment

TEXT_CHUNKS = [
    "Chào bạn, sau đây chúng ta sẽ ôn tập 5 câu lý thuyết môn Quản trị Kinh doanh cho Kỹ sư.",
    "Thay vì học vẹt từng câu chữ khô khan, mình sẽ lấy những ví dụ đời sống thực tế để bạn nghe một lần là hiểu bản chất ngay.",
    "Và khi đã hiểu bản chất, vào phòng thi bạn cứ dùng lời văn của mình mà chém ra là ăn trọn điểm.",
    "Bạn hãy tìm một chỗ nằm thoải mái, cắm tai nghe vào và chúng ta bắt đầu nhé.",

    "Câu số 1: Hãy trình bày các bước trong quy trình ra quyết định quản lý.",
    "Hãy tưởng tượng bạn đang cần mua một chiếc điện thoại mới vì cái cũ vừa bị hư màn hình. Đây chính là quy trình 6 bước:",
    "Bước một: Nhận diện vấn đề. Đó là cái điện thoại của bạn đã hỏng, bạn không có máy để dùng và bắt buộc phải mua cái mới.",
    "Bước hai: Xác định tiêu chuẩn. Bạn đưa ra các mốc để lựa chọn, ví dụ như điện thoại phải dưới 10 triệu, pin trâu để chơi game, và camera chụp ảnh đẹp.",
    "Bước ba: Đánh giá trọng số. Trong ba tiêu chuẩn trên, cái nào quan trọng nhất? Bạn quyết định: Pin trâu chiếm 50% điểm, giá dưới 10 triệu chiếm 30% điểm, còn camera chỉ 20% thôi.",
    "Bước bốn: Phát triển các phương án. Bạn dạo một vòng các cửa hàng và tìm ra 3 ứng cử viên: iPhone cũ, Samsung dòng A, và một con Xiaomi xách tay.",
    "Bước năm: Lựa chọn phương án. Bạn chấm điểm 3 con máy kia dựa trên trọng số ở bước ba. Cuối cùng bạn quyết định chốt mua con Xiaomi vì pin nó trâu nhất và giá lại rẻ.",
    "Và bước sáu: Thực thi và đánh giá. Bạn cầm tiền đi mua con máy về xài thử một tuần. Nếu máy ngon, quy trình kết thúc thành công. Nếu máy lởm, bạn phải bắt đầu lại quy trình để đổi máy khác.",
    "Đấy, 6 bước ra quyết định quản lý trong doanh nghiệp cũng y hệt như quá trình bạn đi mua điện thoại vậy thôi.",

    "Câu số 2: Phân biệt quyết định trong 3 điều kiện: Chắc chắn, rủi ro, và không chắc chắn.",
    "Hãy tưởng tượng bạn cầm 100 triệu đi đầu tư.",
    "Trường hợp 1: Chắc chắn. Bạn mang 100 triệu đó đi gửi tiết kiệm ngân hàng kỳ hạn 1 năm với lãi suất 6%. Bạn biết CHÍNH XÁC 100% là sau 1 năm bạn sẽ thu về 106 triệu. Đó là quyết định chắc chắn.",
    "Trường hợp 2: Rủi ro. Bạn mang 100 triệu đi đánh bài. Bạn không biết chắc chắn mình sẽ thắng hay thua, nhưng bạn biết tỷ lệ thắng của bạn là 50% và tỷ lệ thua là 50%. Có nghĩa là kết quả tuy chưa biết, nhưng XÁC SUẤT xảy ra thì đo lường được. Đó là quyết định rủi ro.",
    "Trường hợp 3: Không chắc chắn. Bạn mang 100 triệu đó ném cho một người bạn khởi nghiệp mở quán cà phê ở một mảnh đất hoang vu chưa ai từng đến. Bạn hoàn toàn mù tịt, không biết liệu quán có khách hay không, cũng KHÔNG THỂ đo lường được xác suất thành công là bao nhiêu phần trăm. Đó là quyết định không chắc chắn.",

    "Câu số 3: Cấu trúc Bảng cân đối kế toán và mối quan hệ Tài sản – Nợ – Vốn.",
    "Bạn cứ hình dung doanh nghiệp như một sinh viên mới ra trường đi mua nhà.",
    "Anh sinh viên mua một căn hộ giá 2 tỷ. Căn hộ đó chính là TÀI SẢN. Tài sản là những gì anh ta ĐANG SỞ HỮU.",
    "Thế tiền ở đâu ra để mua căn hộ 2 tỷ đó? Đó gọi là NGUỒN VỐN. Nguồn vốn chia làm 2 phần:",
    "Phần một là VỐN CHỦ SỞ HỮU. Anh sinh viên đập heo đất và xin bố mẹ được 500 triệu. Đây là tiền tự có, tiền của túi nhà mình.",
    "Phần hai là NỢ PHẢI TRẢ. Anh ta thiếu 1 tỷ rưỡi nên ra ngân hàng vay trả góp. Đây là tiền đi mượn của người khác.",
    "Vậy từ ví dụ trên, ta luôn có một phương trình bất di bất dịch của kế toán: TỔNG TÀI SẢN 2 tỷ, luôn luôn bằng TỔNG NỢ 1 tỷ rưỡi, cộng với VỐN CHỦ SỞ HỮU 500 triệu.",

    "Câu số 4: Cấu trúc Báo cáo kết quả kinh doanh.",
    "Báo cáo này giống như bạn tổng kết một tháng chạy xe ôm công nghệ vậy. Nó đi từ trên xuống dưới để tìm ra số tiền thực sự bạn bỏ túi là bao nhiêu.",
    "Đầu tiên là DOANH THU: Tháng này bạn chạy xe thu được tổng cộng 15 triệu.",
    "Sau đó bạn trừ đi GIÁ VỐN, tức là tiền đổ xăng và thay nhớt mất 3 triệu. Ta ra được LÃI GỘP là 12 triệu.",
    "Từ Lãi gộp, bạn lại trừ đi CHI PHÍ HOẠT ĐỘNG, ví dụ như tiền điện thoại 4G, tiền gửi xe mất thêm 2 triệu. Lúc này bạn có 10 triệu. Số tiền này gọi là LỢI NHUẬN TRƯỚC THUẾ.",
    "Và cuối cùng, bạn phải trích 1 triệu đóng THUẾ thu nhập cá nhân cho nhà nước. Bỏ 1 triệu ra, bạn cầm về nhà 9 triệu. 9 triệu này chính là LỢI NHUẬN SAU THUẾ, số tiền thực sự bạn được xài.",
    "Đó chính là cấu trúc của Báo cáo kết quả kinh doanh. Nó vẽ ra bức tranh Lời Lỗ thực tế của doanh nghiệp.",

    "Câu số 5: Ý nghĩa của 4 tỷ số tài chính.",
    "Tỷ số 1: Tỷ số Nợ. Bằng Tổng Nợ chia cho Tổng tài sản. Ví dụ tỷ số là 0.7, nghĩa là doanh nghiệp có 10 đồng tài sản thì 7 đồng là đi vay. Số này càng cao chứng tỏ công ty vay mượn càng nhiều, rủi ro phá sản càng lớn.",
    "Tỷ số 2: Tỷ số thanh toán hiện hành. Bằng Tài sản ngắn hạn chia cho Nợ ngắn hạn. Ví dụ bạn có 100 triệu tiền mặt trong két, mà tháng tới bạn phải trả cục nợ 80 triệu. Lấy 100 chia 80 được 1.2. Lớn hơn 1 nghĩa là bạn hoàn toàn dư sức trả nợ. Nếu nó nhỏ hơn 1 là bạn chuẩn bị phải bán nhà gán nợ rồi đấy.",
    "Tỷ số 3: Tỷ số thanh toán nhanh. Giống như tỷ số hiện hành, nhưng bạn phải lấy Tài sản ngắn hạn TRỪ ĐI HÀNG TỒN KHO. Lý do là ví dụ 100 triệu tài sản của bạn lại có tới 90 triệu là quần áo chưa bán được. Đến ngày trả nợ 80 triệu, bạn không thể mang đống quần áo ế đó đi gán nợ được, chủ nợ chỉ lấy tiền mặt thôi. Do đó, trừ hàng tồn kho ra sẽ cho biết khả năng ứng phó trả nợ siêu tốc của công ty.",
    "Tỷ số 4: Vòng quay tài sản. Bằng Doanh thu chia cho Tổng tài sản. Giống như việc bạn mua cái xe máy 50 triệu làm tài sản. Một năm bạn dùng xe đó chạy ra được 150 triệu doanh thu. Lấy 150 chia 50 được 3 vòng. Một người khác mua xe 50 triệu nhưng chạy chỉ được 100 triệu, tức là quay được 2 vòng. Vòng quay càng lớn, quản lý tài sản càng hiệu quả.",

    "Đấy, 5 câu lý thuyết quản trị kinh doanh thực chất nó rất gần gũi với đời sống đi mua sắm và kiếm tiền hàng ngày của chúng ta thôi. Bạn hãy ngẫm nghĩ lại các ví dụ trên và chúc bạn có một bài thi cực kỳ xuất sắc nhé."
]

OUTPUT_FILE = "docs/QTKDCKS/Podcast_Ly_Thuyet_Ke_Chuyen_gTTS.mp3"

def create_audio():
    print("Khoi tao gTTS va ghep noi file MP3 truc tiep...")

    with open(OUTPUT_FILE, 'wb') as outfile:
        for i, text in enumerate(TEXT_CHUNKS):
            print(f"Dang doc doan {i+1}/{len(TEXT_CHUNKS)}...")
            chunk_file = f"temp_chunk_lythuyet_{i}.mp3"
            try:
                # Add silence hack by adding dots at the end of each sentence chunk
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
            
    print(f"Hoan thanh! Ban co the nghe thu file Podcast Ke Chuyen tai: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_audio()