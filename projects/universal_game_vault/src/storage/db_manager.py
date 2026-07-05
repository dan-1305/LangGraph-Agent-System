import sqlite3
import os
from pathlib import Path
import sys
import yaml
import re

# Setup sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

class GameDBManager:
    def __init__(self, game_name="morimens"):
        self.game_name = game_name
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.db_dir = self.project_root / "data" / game_name / "database"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.db_dir / "game_vault.db"
        self.wiki_chars_dir = self.project_root / "data" / game_name / "wiki" / "characters"

    def init_db(self):
        """Khoi tao cau truc bang du lieu."""
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA journal_mode=WAL;')
        cursor = conn.cursor()
        
        # Bang nhan vat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                rarity TEXT,
                faction TEXT,
                specialty TEXT,
                wiki_path TEXT
            )
        ''')

        # Bang Lore
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lore (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT UNIQUE,
                content TEXT,
                category TEXT
            )
        ''')

        # Bang Mechanic
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mechanics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                description TEXT,
                faction TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"[DB] Da khoi tao Database tai: {self.db_path}")

    def sync_from_wiki(self):
        """Doc file Markdown va dong bo vao SQLite."""
        self.init_db()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        count = 0
        if not self.wiki_chars_dir.exists():
            print(f"[ERROR] Thu muc wiki khong ton tai: {self.wiki_chars_dir}")
            return

        for md_file in os.listdir(self.wiki_chars_dir):
            if not md_file.endswith(".md"): continue
            
            file_path = self.wiki_chars_dir / md_file
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Trich xuat YAML Frontmatter
            match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                try:
                    metadata = yaml.safe_load(match.group(1))
                    name = metadata.get('title', md_file.replace(".md", ""))
                    rarity = metadata.get('rarity', 'Unknown')
                    faction = metadata.get('faction', 'Unknown')
                    specialty = metadata.get('specialty', 'Unknown')
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO characters (name, rarity, faction, specialty, wiki_path)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, rarity, faction, specialty, str(file_path)))
                    count += 1
                except Exception as e:
                    print(f"[ERROR] Loi parse YAML trong {md_file}: {e}")

        conn.commit()
        conn.close()
        print(f"[SUCCESS] Da dong bo {count} nhan vat vao Database.")

    def query_characters(self, faction=None, rarity=None):
        """Truy van nhan vat theo tieu chi."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT name, rarity, faction, specialty FROM characters WHERE 1=1"
        params = []
        
        if faction:
            query += " AND faction = ?"
            params.append(faction)
        if rarity:
            query += " AND rarity = ?"
            params.append(rarity)
            
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

if __name__ == "__main__":
    db_manager = GameDBManager()
    db_manager.sync_from_wiki()
    
    # Test query
    print("\n[TEST] Nhan vat he Aequor:")
    for char in db_manager.query_characters(faction="Aequor"):
        print(f"- {char[0]} ({char[1]})")
