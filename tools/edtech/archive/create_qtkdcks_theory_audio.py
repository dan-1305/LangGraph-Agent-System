import asyncio
import edge_tts
import os

TEXT_CHUNKS = [
    "Chào các bạn. Sau đây cô sẽ ôn tập nhanh cho các bạn 5 câu lý thuyết cốt lõi của môn Quản trị Kinh doanh cho Kỹ sư.",
    "Các bạn chú ý những từ khóa ăn điểm nhé.",
    
    "Câu 1: Các bước trong quy trình ra quyết định quản lý.",
    "Quy trình này gồm 6 bước, các bạn học thuộc lòng thứ tự sau đây:",
    "Bước một: Nhận diện vấn đề.",
    "Bước hai: Xác định tiêu chuẩn đánh giá.",
    "Bước ba: Đánh giá trọng số cho từng tiêu chuẩn.",
    "Bước bốn: Phát triển các phương án.",
    "Bước năm: Lựa chọn phương án tối ưu nhất.",
    "Và bước sáu: Thực thi và đánh giá kết quả.",
    
    "Câu 2: Phân biệt quyết định trong ba điều kiện: Chắc chắn, Rủi ro và Không chắc chắn.",
    "Chắc chắn là khi ta biết chính xác 100% kết quả sẽ xảy ra. Môi trường hoàn toàn tĩnh.",
    "Rủi ro là khi ta không biết chắc kết quả, nhưng ta biết được XÁC SUẤT xảy ra của từng trường hợp. Môi trường này có biến động nhưng đo lường được.",
    "Không chắc chắn là khi ta hoàn toàn mù mờ, KHÔNG có thông tin và KHÔNG biết xác suất xảy ra. Môi trường hoàn toàn vô định.",
    
    "Câu 3: Cấu trúc bảng cân đối kế toán và mối quan hệ Tài sản – Nợ – Vốn.",
    "Các bạn chỉ cần nhớ một phương trình bất di bất dịch: TỔNG TÀI SẢN bằng TỔNG NỢ cộng VỐN CHỦ SỞ HỮU.",
    "Tài sản là những gì doanh nghiệp đang sở hữu như Tiền mặt, Hàng tồn kho hay Máy móc.",
    "Nguồn vốn là nơi cung cấp tiền để mua tài sản đó. Nó chia làm hai loại: Nợ phải trả, tức là tiền đi vay. Và Vốn chủ sở hữu, tức là tiền tự có của cổ đông.",
    
    "Câu 4: Cấu trúc báo cáo kết quả kinh doanh và ý nghĩa.",
    "Báo cáo này đi từ trên xuống dưới theo thứ tự trừ dần chi phí.",
    "Lấy Doanh thu trừ Giá vốn hàng bán, ta được Lãi gộp.",
    "Lấy Lãi gộp trừ Chi phí hoạt động và Lãi vay, ta được Lợi nhuận trước thuế.",
    "Cuối cùng, trừ đi Thuế là ra Lợi nhuận sau thuế.",
    "Ý nghĩa của nó là cho biết bức tranh Lời Lỗ của doanh nghiệp trong một năm, giúp đánh giá hiệu quả kinh doanh.",
    
    "Câu 5: Ý nghĩa của 4 tỷ số tài chính cơ bản. Các bạn ghi nhớ từ khóa nhé.",
    "Thứ nhất: Tỷ số nợ. Tính bằng Tổng nợ chia Tổng tài sản. Nó cho biết tỷ lệ tài sản được tài trợ bằng tiền đi vay. Tỷ lệ này càng cao thì rủi ro phá sản càng lớn.",
    "Thứ hai: Tỷ số thanh toán hiện hành. Bằng Tài sản lưu động chia cho Nợ ngắn hạn. Đo lường khả năng trả các khoản nợ sắp đến hạn.",
    "Thứ ba: Tỷ số thanh toán nhanh. Khắt khe hơn cái số hai. Nó phải lấy Tài sản lưu động TRỪ ĐI Hàng tồn kho, rồi mới chia cho Nợ ngắn hạn. Lý do là hàng tồn kho rất khó bán ngay ra tiền mặt.",
    "Thứ tư: Vòng quay tài sản. Bằng Doanh thu chia Tổng tài sản. Đo lường hiệu suất sử dụng tài sản để đẻ ra doanh thu. Số vòng quay càng lớn thì công ty quản lý tài sản càng hiệu quả.",
    
    "Đó là 5 câu lý thuyết trọng tâm. Các bạn hãy nghe đi nghe lại để nhớ kỹ các từ khóa ăn điểm nhé. Chúc các bạn thi tốt!"
]

VOICE = "vi-VN-HoaiMyNeural"
FINAL_FILE = "docs/QTKDCKS/Podcast_Ly_Thuyet_QTKDCKS.mp3"

async def amain() -> None:
    print("Bat dau xu ly tung cau thoai...")
    files_to_merge = []
    
    for i, chunk in enumerate(TEXT_CHUNKS):
        chunk_file = f"temp_chunk_{i}.mp3"
        print(f"Dang render doan {i+1}/{len(TEXT_CHUNKS)}...")
        
        # Dùng thông số mặc định hoàn toàn để tránh lỗi
        communicate = edge_tts.Communicate(chunk, VOICE)
        await communicate.save(chunk_file)
        files_to_merge.append(chunk_file)
        
        # Tạo thêm 1 file im lặng 1.5s (silence) giữa các chunk
        # Thay vì sinh file mp3 phức tạp, mình sẽ ghép nối trực tiếp byte streams mp3.
        
    print(f"Tien hanh ghep noi {len(files_to_merge)} file...")
    
    # Chắp nối các MP3 bằng Python (nối byte cơ bản)
    with open(FINAL_FILE, 'wb') as outfile:
        for chunk_file in files_to_merge:
            with open(chunk_file, 'rb') as infile:
                outfile.write(infile.read())
            # Dọn rác
            os.remove(chunk_file)
            
    print(f"Xong! File hoan chinh da luu tai: {FINAL_FILE}")

if __name__ == "__main__":
    asyncio.run(amain())
