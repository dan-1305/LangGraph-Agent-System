import os
import sys
import sqlite3
import logging
from pathlib import Path
import easyocr
from typing import List, Dict, Any, Optional

# [ANTI-BOMB] Suppress EasyOCR progress bars / tqdm noise to prevent Token Amplification
logging.getLogger("easyocr").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)
try:
    logging.getLogger("filelock").setLevel(logging.WARNING)
except Exception:
    pass

# Setup sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.base_agent import BaseAgent
from projects.universal_game_vault.src.scraper import GameWebScraper
from projects.universal_game_vault.src.storage.db_manager import GameDBManager
from pydantic import BaseModel, Field

class IngestedCharacter(BaseModel):
    name: str
    rarity: str = "Unknown"
    faction: str = "Unknown"
    specialty: str = "Unknown"

class IngestedLore(BaseModel):
    title: str
    content: str
    category: str = "General"

class IngestedMechanic(BaseModel):
    name: str
    description: str
    faction: str = "Global"

class IngestedData(BaseModel):
    characters: List[IngestedCharacter] = Field(default_factory=list)
    lore: List[IngestedLore] = Field(default_factory=list)
    mechanics: List[IngestedMechanic] = Field(default_factory=list)

class LoreIngestionAgent(BaseAgent):
    def __init__(self, game_name="morimens"):
        super().__init__(
            name="LoreIngestionAgent",
            role="Data Ingestion Specialist",
            agent_label="tier-2"
        )
        self.game_name = game_name
        self.scraper = GameWebScraper()
        self.db_manager = GameDBManager(game_name)
        self.db_manager.init_db()
        
        # Initialize EasyOCR with Drive D model cache (save space on C:)
        ocr_model_path = os.getenv("STORAGE_DIR", "D:/Users/Admin/Downloads/LangGraphStorage") + "/models/easyocr"
        Path(ocr_model_path).mkdir(parents=True, exist_ok=True)
        print(f"[LoreIngest] Initializing OCR Engine (CPU) | Cache: {ocr_model_path}")
        # [ANTI-BOMB] verbose=False tắt progress bar khi tải model / chạy OCR
        self.ocr_reader = easyocr.Reader(
            ['en', 'vi'], gpu=False, verbose=False,
            model_storage_directory=ocr_model_path, download_enabled=True
        )

    def _ai_handler(self, *args, **kwargs):
        pass

    def _logic_handler(self, *args, **kwargs):
        pass

    def save_to_db(self, data: IngestedData):
        """Lưu dữ liệu đã trích xuất vào SQLite."""
        conn = sqlite3.connect(self.db_manager.db_path)
        cursor = conn.cursor()
        
        # Save characters
        for char in data.characters:
            cursor.execute('''
                INSERT OR REPLACE INTO characters (name, rarity, faction, specialty)
                VALUES (?, ?, ?, ?)
            ''', (char.name, char.rarity, char.faction, char.specialty))
            
        # Save lore
        for item in data.lore:
            cursor.execute('''
                INSERT OR REPLACE INTO lore (title, content, category)
                VALUES (?, ?, ?)
            ''', (item.title, item.content, item.category))
            
        # Save mechanics
        for mech in data.mechanics:
            cursor.execute('''
                INSERT OR REPLACE INTO mechanics (name, description, faction)
                VALUES (?, ?, ?)
            ''', (mech.name, mech.description, mech.faction))
            
        conn.commit()
        conn.close()
        print(f"✅ [DB] Da luu {len(data.characters)} chars, {len(data.lore)} lore, {len(data.mechanics)} mechanics.")

    def ingest_from_url(self, url: str):
        """Cào web và trích xuất dữ liệu."""
        print(f"🌐 [LoreIngest] Processing URL: {url}")
        content = self.scraper.scrape_url(url)
        if not content:
            return
        
        prompt = f"Phân tích nội dung sau về game {self.game_name} và trích xuất dữ liệu cấu trúc:\n\n{content[:8000]}"
        result = self._call_llm(prompt, schema=IngestedData)
        if result:
            data = IngestedData(**result)
            self.save_to_db(data)

    def ingest_from_images(self, folder_path: str):
        """Chạy OCR trên thư mục ảnh và trích xuất dữ liệu."""
        print(f"📸 [LoreIngest] Processing Images in: {folder_path}")
        path = Path(folder_path)
        if not path.exists():
            print(f"❌ [Error] Path not found: {folder_path}")
            return

        files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.webp', '.jpg', '.png'))])
        if not files:
            print("⚠️ [Warning] No images found.")
            return

        combined_text = ""
        for file in files[:15]: # Limit for token safety
            print(f"  🔍 OCR-ing {file}...")
            res = self.ocr_reader.readtext(str(path / file), detail=0)
            combined_text += f"\n--- Source: {file} ---\n" + " ".join(res)

        prompt = f"Dưới đây là kết quả OCR từ tài liệu game {self.game_name}. Hãy trích xuất dữ liệu cấu trúc:\n\n{combined_text[:8000]}"
        result = self._call_llm(prompt, schema=IngestedData)
        if result:
            data = IngestedData(**result)
            self.save_to_db(data)

if __name__ == "__main__":
    # Example usage
    agent = LoreIngestionAgent()
    
    # Test with a placeholder URL if needed, or local folder
    # agent.ingest_from_url("https://example.com/game-wiki")
    
    # Test with local OCR data if available
    test_folder = BASE_DIR / "data" / "morimens" / "raw" / "screenshots"
    if test_folder.exists():
        agent.ingest_from_images(str(test_folder))
    else:
        print(f"ℹ️ Create {test_folder} and add images to test OCR ingestion.")
