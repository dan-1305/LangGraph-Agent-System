import time
import random

class PlaywrightStealth:
    @staticmethod
    def random_scroll(page, min_scrolls=2, max_scrolls=5):
        scrolls = random.randint(min_scrolls, max_scrolls)
        for _ in range(scrolls):
            direction = 1 if random.random() < 0.7 else -1
            distance = random.randint(300, 800) * direction
            try:
                page.mouse.wheel(0, distance)
                time.sleep(random.uniform(1.0, 3.0))
            except:
                pass
            
    @staticmethod
    def human_pause(min_sec=3.0, max_sec=6.0):
        time.sleep(random.uniform(min_sec, max_sec))

class BaseConfig:
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    DISTRICTS_DONGNAI = [
        "Biên Hòa", "Long Thành", "Nhơn Trạch", "Trảng Bom", "Vĩnh Cửu", 
        "Thống Nhất", "Cẩm Mỹ", "Định Quán", "Xuân Lộc", "Tân Phú", "Long Khánh"
    ]
