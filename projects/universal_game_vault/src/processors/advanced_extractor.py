import os
from pathlib import Path
import sys
import io

# Setup sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Force UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')
else:
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from src.base_agent import BaseAgent

class AdvancedExtractor(BaseAgent):
    def __init__(self):
        super().__init__(name="AdvancedExtractor", role="Game Lore Master", agent_label="fast")
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.raw_dir = self.project_root / "data" / "morimens" / "raw"
        self.wiki_dir = self.project_root / "data" / "morimens" / "wiki"

    def _ai_handler(self, state: dict) -> dict: return state
    def _logic_handler(self, state: dict) -> dict: return state

    def run(self):
        print("[START] Extracting Advanced Mechanics and Items...")
        
        # 1. Process Covenants
        extracted_cov = self.raw_dir / "extracted_covenants.txt"
        if extracted_cov.exists():
            with open(extracted_cov, "r", encoding="utf-8") as f:
                text = f.read()
            
            print("🧠 Generating Detailed Covenants Guide...")
            prompt = f"Dựa trên tài liệu sau, hãy viết file 'Covenants_Detailed.md' cực kỳ chi tiết cho game Morimens. Bao gồm cơ chế nâng cấp, substats, và gợi ý bộ đồ cho DPS/Support. Tài liệu: {text[:4000]}"
            content = self._call_llm(prompt)
            if content:
                out = self.wiki_dir / "items" / "Covenants_Detailed.md"
                out.parent.mkdir(parents=True, exist_ok=True)
                with open(out, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Saved: {out}")

        # 2. Process Factions & Realms
        print("🧠 Generating Factions Guide...")
        prompt = "Viết một file Wiki 'Factions.md' chi tiết về 4 hệ trong Morimens: Chaos, Aequor, Caro, Ultra. Giải thích đặc điểm chiến đấu của từng hệ (Vd: Aequor dùng Summon, Caro dùng HP-loss)."
        content = self._call_llm(prompt)
        if content:
            out = self.wiki_dir / "mechanics" / "Factions.md"
            with open(out, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Saved: {out}")

if __name__ == "__main__":
    extractor = AdvancedExtractor()
    extractor.run()
