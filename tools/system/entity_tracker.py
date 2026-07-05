import os
import json
from pathlib import Path

class EntityTracker:
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.map_path = self.root_dir / "context" / "entity_map.json"
        self._ensure_map_exists()

    def _ensure_map_exists(self):
        if not self.map_path.exists():
            default_map = {
                "paths": {
                    "storage_dir": "D:/Users/Admin/Downloads/LangGraphStorage",
                    "history_cline": "D:/Users/Admin/Downloads/LangGraphStorage/Intellectual_Property/History_Cline"
                },
                "active_entities": {},
                "last_update": ""
            }
            self.save_map(default_map)

    def load_map(self):
        with open(self.map_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_map(self, data):
        from datetime import datetime
        data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.map_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def track_path(self, name, path):
        data = self.load_map()
        data["paths"][name] = str(path)
        self.save_map(data)
        print(f"📍 Đã ghi nhớ đường dẫn: {name} -> {path}")

if __name__ == "__main__":
    tracker = EntityTracker()
    # Test track một path
    tracker.track_path("recent_history_v4", "analysis_user/all_user_input_v4.md")
