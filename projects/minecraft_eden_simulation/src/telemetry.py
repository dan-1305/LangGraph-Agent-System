import json
import time
from pathlib import Path
from datetime import datetime

class EdenTelemetry:
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.start_time = time.time()
        self.end_time = 0
        
        self.stats = {
            "total_ticks_survived": 0,
            "actions_taken": 0,
            "craft_success": 0,
            "craft_failed": 0,
            "damage_taken": 0,
            "deep_reflections": 0,
            "api_calls": 0,
            "items_gathered": 0
        }
        
        self.action_history = []
        
        # Thư mục lưu báo cáo
        root_dir = Path(__file__).resolve().parent.parent.parent.parent
        self.report_dir = root_dir / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
    def record_tick(self):
        self.stats["total_ticks_survived"] += 1
        
    def record_action(self, action: str, success: bool = True):
        self.stats["actions_taken"] += 1
        self.action_history.append({"tick": self.stats["total_ticks_survived"], "action": action, "success": success})
        
        if action.startswith("craft"):
            if success:
                self.stats["craft_success"] += 1
            else:
                self.stats["craft_failed"] += 1
                
        if action.startswith("mine") and success:
            self.stats["items_gathered"] += 1
            
    def record_damage(self, amount: int):
        self.stats["damage_taken"] += amount
        
    def record_reflection(self):
        self.stats["deep_reflections"] += 1
        
    def record_api_call(self):
        self.stats["api_calls"] += 1
        
    def finalize_report(self, death_reason: str = "Survived"):
        self.end_time = time.time()
        duration = round(self.end_time - self.start_time, 2)
        
        report_path = self.report_dir / f"EDEN_SIMULATION_REPORT_{self.run_id}.md"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# 📊 BÁO CÁO MÔ PHỎNG EDEN - RUN ID: {self.run_id}\n\n")
            f.write(f"**Thời gian chạy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Thời lượng mô phỏng:** {duration} giây\n")
            f.write(f"**Kết quả cuối cùng:** {death_reason}\n\n")
            
            f.write("## 📈 SỐ LIỆU TỔNG QUAN\n")
            f.write(f"- **Số lượt sống sót (Ticks):** {self.stats['total_ticks_survived']}\n")
            f.write(f"- **Tổng số lần gọi LLM API:** {self.stats['api_calls']}\n")
            f.write(f"- **Số lần Deep Reflection (Nén Ký Ức):** {self.stats['deep_reflections']}\n")
            f.write(f"- **Tổng sát thương gánh chịu:** {self.stats['damage_taken']} HP\n\n")
            
            f.write("## 🛠️ HIỆU SUẤT CÔNG VIỆC\n")
            f.write(f"- **Tài nguyên thu thập:** {self.stats['items_gathered']} items\n")
            total_craft = self.stats['craft_success'] + self.stats['craft_failed']
            win_rate = round(self.stats['craft_success'] / total_craft * 100, 2) if total_craft > 0 else 0
            f.write(f"- **Chế tạo thành công:** {self.stats['craft_success']} lần\n")
            f.write(f"- **Chế tạo thất bại (Ảo giác):** {self.stats['craft_failed']} lần\n")
            f.write(f"- **Tỷ lệ chế tạo thành công:** {win_rate}%\n\n")
            
            f.write("## 📝 LỊCH SỬ HÀNH ĐỘNG (10 HÀNH ĐỘNG CUỐI)\n")
            for h in self.action_history[-10:]:
                status = "✅" if h['success'] else "❌"
                f.write(f"- [Tick {h['tick']}] {status} Action: `{h['action']}`\n")
                
        print(f"\n📊 [Telemetry] Đã xuất báo cáo tại: {report_path}")
