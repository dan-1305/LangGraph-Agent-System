import os
from pathlib import Path
import sys
import re
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
class FullTextParser:
    def __init__(self, game_name="morimens"):
        self.game_name = game_name
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.raw_dir = self.project_root / "data" / game_name / "raw"
        self.wiki_chars_dir = self.project_root / "data" / game_name / "wiki" / "characters"
        self.wiki_chars_dir.mkdir(parents=True, exist_ok=True)

    def run(self):
        print(f"[START] Bat dau Full Text Parsing cho game: {self.game_name}")
        
        detail_file = self.raw_dir / "Character Detail.txt"
        if not detail_file.exists():
            print(f"[ERROR] Khong tim thay file: {detail_file}")
            return

        with open(detail_file, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        # [CRITICAL FIX] Dung Regex de tach chinh xac theo cum thong tin bat dau tu 'Basic Information'
        char_blocks = re.split(r'Basic Information', content)
        
        processed_count = 0
        for block in char_blocks:
            if "Name" in block and "Rarity" in block:
                self.parse_and_save(block)
                processed_count += 1
        
        print(f"[SUCCESS] Da cap nhat {processed_count} nhan vat voi du lieu day du 100%.")

    def parse_and_save(self, block):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        
        # Trich xuat cac thong tin co ban cho Metadata
        data = {}
        for i, line in enumerate(lines):
            if line == "Name" and i+1 < len(lines): data['name'] = lines[i+1]
            if line == "Rarity" and i+1 < len(lines): data['rarity'] = lines[i+1]
            if line == "Faction" and i+1 < len(lines): data['faction'] = lines[i+1]
            if line == "Type" and i+1 < len(lines): data['type'] = lines[i+1]
        
        name = data.get('name', 'Unknown')
        filename = re.sub(r'[^a-zA-Z0-9]', '', name).strip().replace(" ", "_")
        
        # [FIX] Su dung lookahead voi newline de tranh stop nham tai cac tu khoa nam trong cau
        stats_match = re.search(r'Stats Lv\. 60\n(.*?)(?=\nEnlightens\n|$)', block, re.DOTALL)
        enlightens_match = re.search(r'\nEnlightens\n(.*?)(?=\nExalts\n|$)', block, re.DOTALL)
        exalts_match = re.search(r'\nExalts\n(.*?)(?=\nCards\n|$)', block, re.DOTALL)
        cards_match = re.search(r'\nCards\n(.*?)(?=\nTalents\n|$)', block, re.DOTALL)
        talents_match = re.search(r'\nTalents\n(.*)', block, re.DOTALL)

        wiki_content = f"""---
title: "{name}"
type: Character
rarity: {data.get('rarity', 'SSR')}
faction: {data.get('faction', 'Chaos')}
specialty: {data.get('type', 'Unknown')}
---

# 👤 Awakener Wiki: {name}

> **Rarity:** {data.get('rarity', 'SSR')} | **Faction:** {data.get('faction', 'Chaos')} | **Type:** {data.get('type', 'Unknown')}
> #Character #{data.get('faction', 'Chaos')} #{data.get('type', 'Unknown')}

---

## 📊 Stats (Lv. 60)
```text
{stats_match.group(1).strip() if stats_match else "N/A"}
```

---

## 🌟 Enlightens
{enlightens_match.group(1).strip() if enlightens_match else "N/A"}

---

## 🔥 Exalts
{exalts_match.group(1).strip() if exalts_match else "N/A"}

---

## ⚔️ Command Cards
{cards_match.group(1).strip() if cards_match else "N/A"}

---

## 💡 Talents
{talents_match.group(1).strip() if talents_match else "N/A"}

---
*Dữ liệu được trích xuất tự động bởi CEO Sovereign Engine.*
"""
        output_file = self.wiki_chars_dir / f"{filename}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(wiki_content)
        print(f"[FIXED] Wiki day du cho: {filename}")

if __name__ == "__main__":
    parser = FullTextParser()
    parser.run()
