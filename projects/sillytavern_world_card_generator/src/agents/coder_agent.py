"""
Coder Agent:
Nhiệm vụ: Tạo ra các file Regex Script và UI Extension (HTML/CSS/JS) để người dùng dùng trực tiếp trên SillyTavern.
Logic: Nhận danh sách tính năng (ví dụ: "Có thanh HP", "Có hệ thống Gacha") và sinh ra code Regex/HTML tương ứng.
"""

from typing import List, Dict

# --- PROMPT TEMPLATE CHO CODER ---
CODER_PROMPT = """
Bạn là một Lập trình viên SillyTavern (SillyTavern Coder) chuyên nghiệp.
Nhiệm vụ của bạn là viết các mã Regex Script và HTML/CSS/JS Extensions dựa trên yêu cầu người dùng.

THÔNG TIN INPUT:
- Theme: {theme}
- Danh sách tính năng: {features} (Ví dụ: ["Stat Bars", "Gacha UI", "Class Selection"])

QUY TẮC PHÁT TRIỆN:
1. Regex Script: Dùng để can thiệp text chat của LLM.
   - Nếu yêu cầu "Stat Bars": Tạo Regex can thiệp `HP: \d+/\d+` thành thanh sức sống hình chữ I màu đỏ/đen.
   - Nếu yêu cầu "Gacha": Tạo Regex phát hiện `|🎲 Gacha|` và nút tung xúc xắc emoji.
2. HTML/CSS Extension:
   - Tạo UI đẹp mắt, tương thích Dark Mode (dùng màu neon xanh/tím cho Cyberpunk, màu vàng/truyền thống cho Tu tiên).
   - Code phải đặt trong tag <script> hoặc <style> trong thẻ html được yêu cầu.

OUTPUT JSON FORMAT:
[
  {
    "filename": "stats_bar.css",
    "content": "<style>...</style>",
    "type": "css",
    "description": "Thanh trạng thái HP/MP màu đỏ."
  },
  ...
]
"""

class CoderAgent:
    def __init__(self, model_name: str = "gemini-pro"):
        self.model_name = model_name
        
    def generate_extensions(self, user_idea: Dict) -> List[Dict]:
        """
        Sinh ra các file extension dựa trên tính năng được yêu cầu.
        """
        scripts = []
        features = user_idea.get("features", [])
        theme = user_idea.get("theme", "")
        
        import json
        from pathlib import Path
        
        # Đường dẫn tới thư mục template
        template_dir = Path(__file__).resolve().parent.parent.parent / "data" / "templates" / "regex"
        
        # Cấu hình map tính năng với file template
        feature_map = {
            "stat": "regex-thanh_trang_thai_hp.json",  # Giả sử tên file, nếu không có sẽ dùng default
            "gacha": "regex-giao_dien_gacha.json",
            "class selection": "regex-bang_lua_chon_hanh_dong.json" # Match với "regex-bảng_lựa_chọn_hành_động.json"
        }
        
        # Helper load template
        def load_template(filename: str, default_data: dict) -> dict:
            try:
                # Cố gắng tìm file json trong thư mục
                file_path = template_dir / filename
                if file_path.exists():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Đôi khi file json gốc xuất ra array, nếu là array lấy phần tử đầu
                        if isinstance(data, list) and len(data) > 0:
                            return data[0]
                        return data
                # Nếu sai tên do tiếng Việt có dấu, tìm kiếm mờ
                for file in template_dir.glob("*.json"):
                    if filename.replace(".json", "").replace("_", "") in file.name.replace("_", "").replace("-", ""):
                        with open(file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list) and len(data) > 0:
                                return data[0]
                            return data
            except Exception as e:
                print(f"Lỗi load template regex {filename}: {e}")
            
            return default_data

        # Xử lý feature "Stat Bars"
        if any("stat" in f.lower() for f in features):
            default_stat = {
                "id": "stat_bar_script_id_123",
                "scriptName": "Thanh Trạng Thái HP/MP",
                "disabled": False,
                "runOnEdit": True,
                "findRegex": "/<hp_mp_display>/s",
                "replaceString": f"<!-- Auto-generated HP/MP UI for {theme} -->\n<div style='color: red; font-weight: bold;'>[ HP / MP System Loaded ]</div>",
                "trimStrings": [],
                "placement": [1, 2],
                "substituteRegex": 0,
                "minDepth": None,
                "maxDepth": None,
                "markdownOnly": True,
                "promptOnly": False
            }
            scripts.append(load_template("regex-thanh_trang_thai.json", default_stat))
            
        # Xử lý feature "Gacha"
        if any("gacha" in f.lower() for f in features):
            default_gacha = {
                "id": "gacha_script_id_456",
                "scriptName": "Giao diện Gacha",
                "disabled": False,
                "runOnEdit": True,
                "findRegex": "/<gacha_roll>/s",
                "replaceString": f"<!-- Gacha UI for {theme} -->\n<button style='background: gold; color: black;'>🎲 Rút Thẻ Gacha</button>",
                "trimStrings": [],
                "placement": [1, 2],
                "substituteRegex": 0,
                "minDepth": None,
                "maxDepth": None,
                "markdownOnly": True,
                "promptOnly": False
            }
            scripts.append(load_template("regex-giao_dien_gacha.json", default_gacha))
            
        # Xử lý tính năng Class Selection (Bảng lựa chọn)
        if any("class" in f.lower() or "chọn" in f.lower() for f in features):
            default_class = {
                "id": "class_selection_789",
                "scriptName": "Bảng lựa chọn hành động",
                "disabled": False,
                "runOnEdit": True,
                "findRegex": "/<choices>(.*?)</choices>/s",
                "replaceString": f"<!-- Action Panel -->\n<div style='border:1px solid #3498db;'>$1</div>",
                "trimStrings": [],
                "placement": [1, 2],
                "substituteRegex": 0,
                "minDepth": None,
                "maxDepth": None,
                "markdownOnly": True,
                "promptOnly": False
            }
            scripts.append(load_template("regex-bảng_lựa_chọn_hành_động.json", default_class))
            
        return scripts

# Mock function
def generate_code_mock(user_idea: Dict):
    agent = CoderAgent()
    return agent.generate_extensions(user_idea)
