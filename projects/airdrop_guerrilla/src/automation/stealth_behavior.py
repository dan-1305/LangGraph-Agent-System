import time
import random

class StealthBehavior:
    """
    Giả lập hành vi của con người (Natural Browsing) để tránh bị gắn cờ Bot (Sybil/Anti-bot).
    Tối ưu hóa các thao tác để chạy nhẹ nhàng trên hệ thống (i3-1215u).
    """
    
    @staticmethod
    def random_scroll(page, min_scrolls=2, max_scrolls=5):
        """
        Cuộn trang lên xuống ngẫu nhiên.
        """
        print("   🖱️ [Stealth] Bắt đầu cuộn trang ngẫu nhiên...")
        scrolls = random.randint(min_scrolls, max_scrolls)
        for _ in range(scrolls):
            # Chọn hướng cuộn (70% xuống, 30% lên)
            direction = 1 if random.random() < 0.7 else -1
            # Khoảng cách cuộn ngẫu nhiên
            distance = random.randint(300, 800) * direction
            
            # Thực thi cuộn bằng mouse wheel (giả lập cuộn chuột thật)
            page.mouse.wheel(0, distance)
            
            # Tạm dừng giữa các lần cuộn để giống người đang đọc
            time.sleep(random.uniform(1.0, 3.5))

    @staticmethod
    def human_pause(min_sec=5.0, max_sec=15.0):
        """
        Nghỉ ngẫu nhiên giả vờ đang đọc nội dung hoặc rời mắt khỏi màn hình.
        """
        pause_time = random.uniform(min_sec, max_sec)
        print(f"   ☕ [Stealth] Đang dừng đọc bài (Pause {pause_time:.1f}s)...")
        time.sleep(pause_time)

    @staticmethod
    def explore_section(page):
        """
        Giả lập việc click chuyển sang tab 'Explore' hoặc lướt Newfeed ngẫu nhiên.
        """
        print("   🧭 [Stealth] Đang dạo quanh mục Explore / Timeline...")
        try:
            # Chờ trang tải hoàn tất các selector
            page.wait_for_load_state("domcontentloaded")
            
            # Random click vào một vài tab phổ biến (Ví dụ: Home, Explore, Notifications) trên Twitter
            nav_selectors = [
                "a[data-testid='AppTabBar_Explore_Link']",
                "a[data-testid='AppTabBar_Home_Link']"
            ]
            
            # Tìm xem selector nào tồn tại
            for selector in nav_selectors:
                if page.locator(selector).count() > 0:
                    page.click(selector)
                    break
                    
            StealthBehavior.human_pause(3.0, 7.0)
            StealthBehavior.random_scroll(page, 1, 3)
            
        except Exception as e:
            # Nếu có lỗi khi click, chỉ in ra (để không làm sập flow chính)
            print("   ⚠️ [Stealth] Bỏ qua bước Explore (Không tìm thấy nút).")

    @staticmethod
    def perform_warmup(page):
        """
        Tổng hợp chuỗi hành động "Khởi động" trước khi thực hiện Action chính.
        Giúp tài khoản tăng độ Trust.
        """
        print("\n   🎭 [Stealth] Kích hoạt chế độ Human Warm-up (Tránh bị đánh dấu Bot)...")
        # Nghỉ 1 chút ngay khi vừa mở trang
        StealthBehavior.human_pause(2.0, 5.0)
        
        # Cuộn trang một chút
        StealthBehavior.random_scroll(page)
        
        # Thỉnh thoảng đi dạo sang mục khác (tỉ lệ 50%)
        if random.random() < 0.5:
            StealthBehavior.explore_section(page)
            
        # Quay lại trang cũ hoặc dừng thêm 1 chút
        StealthBehavior.human_pause(2.0, 4.0)
        print("   ✅ [Stealth] Hoàn tất Warm-up, chuẩn bị thực thi nhiệm vụ!")
