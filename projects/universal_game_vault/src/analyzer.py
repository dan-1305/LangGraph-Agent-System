import sqlite3
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

class GameAnalyzer:
    def __init__(self, game_name="morimens"):
        self.game_name = game_name
        self.project_root = Path(__file__).resolve().parent.parent
        self.db_path = self.project_root / "data" / game_name / "database" / "game_vault.db"

    def get_character_info(self, name):
        """Lay thong tin chi tiet nhan vat tu DB."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM characters WHERE name LIKE ?", (f"%{name}%",))
        result = cursor.fetchone()
        conn.close()
        return result

    def suggest_team(self, archetype="Poison"):
        """Goi y doi hinh dua tren loi choi."""
        print(f"[ANALYZING] Doi hinh cho loi choi: {archetype}...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        suggestions = []
        if archetype.lower() == "poison":
            cursor.execute("SELECT name, rarity, faction FROM characters WHERE faction = 'Aequor' OR specialty LIKE '%Poison%'")
            suggestions = cursor.fetchall()
        elif archetype.lower() == "bleed":
            cursor.execute("SELECT name, rarity, faction FROM characters WHERE faction = 'Caro' OR specialty LIKE '%Bleed%'")
            suggestions = cursor.fetchall()
            
        conn.close()
        return suggestions

    def run_cli_test(self):
        print(f"=== MORIMENS TACTICAL ANALYZER ===")
        
        # Test 1: Info
        char = self.get_character_info("Faros")
        if char:
            print(f"[INFO] Nhan vat: {char[1]} | He: {char[3]} | Vai tro: {char[4]}")
        
        # Test 2: Team suggestion
        print("\n[SUGGESTION] Doi hinh Poison:")
        team = self.suggest_team("Poison")
        for member in team:
            print(f"- {member[0]} ({member[1]}) [{member[2]}]")

if __name__ == "__main__":
    analyzer = GameAnalyzer()
    analyzer.run_cli_test()
