import os
from pathlib import Path
import sys
import json
import re
import io

# Cuong che PYTHONPATH tu code
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Import Core bang duong dan tuyet doi
from src.base_agent import BaseAgent

import fitz  # PyMuPDF
from docx import Document

# Integration of Sub-Agents cho Crawler
try:
    from projects.universal_game_vault.src.scraper import GameWebScraper
except ImportError:
    GameWebScraper = None

class BatchImporter(BaseAgent):
    def __init__(self, game_name="morimens"):
        # Su dung fast (Llama-3.1-8b) de dam bao on dinh tren Windows Proxy
        super().__init__(name=f"BatchImporter_{game_name}", role="Game Vault Importer", agent_label="fast")
        self.game_name = game_name
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.raw_dir = self.project_root / "data" / game_name / "raw"
        self.wiki_dir = self.project_root / "data" / game_name / "wiki"
        self.wiki_chars_dir = self.wiki_dir / "characters"

    def _ai_handler(self, state: dict) -> dict:
        """Thuc thi logic AI bat buoc tu BaseAgent"""
        return state

    def _logic_handler(self, state: dict) -> dict:
        """Thuc thi logic Code bat buoc tu BaseAgent"""
        return state

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        try:
            with fitz.open(pdf_path) as doc:
                for page in doc:
                    text += page.get_text()
        except Exception as e:
            print(f"[ERROR] Loi doc PDF {pdf_path}: {e}")
        return text

    def extract_text_from_docx(self, docx_path):
        text = ""
        try:
            doc = Document(docx_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"[ERROR] Loi doc DOCX {docx_path}: {e}")
        return text

    def run_import(self):
        print(f"[START] Bat dau Batch Import V2 (AI-Powered) cho game: {self.game_name}")
        combined_content = ""

        if not self.raw_dir.exists():
            print(f"[ERROR] Thu muc raw khong ton tai: {self.raw_dir}")
            return

        # 0. Crawler Integration (Neu co file urls.txt)
        urls_file = self.raw_dir / "urls.txt"
        if urls_file.exists() and GameWebScraper:
            print("[SUB-AGENT] Kich hoat Crawler sub-agent...")
            scraper = GameWebScraper()
            with open(urls_file, "r", encoding="utf-8") as f:
                urls = [url.strip() for url in f.readlines() if url.strip()]
            for url in urls:
                scraped_text = scraper.scrape_url(url)
                if scraped_text:
                    combined_content += f"\n\n--- Du lieu cao tu: {url} ---\n{scraped_text}\n"
            # Doi ten de khong crawl lai nhieu lan
            try:
                urls_file.rename(self.raw_dir / "urls.txt.done")
            except:
                pass

        for file in os.listdir(self.raw_dir):
            file_path = self.raw_dir / file
            if file_path.is_dir():
                continue
            
            print(f"[READ] Dang doc: {file}...")
            if file.endswith(".pdf"):
                combined_content += self.extract_text_from_pdf(file_path)
            elif file.endswith(".docx"):
                combined_content += self.extract_text_from_docx(file_path)
            elif file.endswith(".txt") and not file.startswith("urls.txt"):
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    combined_content += f.read()
            # 0.5 OCR Integration cho anh
            elif file.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"[SUB-AGENT] Kich hoat Vision OCR sub-agent cho {file}...")
                try:
                    # Goi module jarvis_core vision bang cach sys.path
                    jarvis_path = str(BASE_DIR / "projects" / "jarvis-rpg-assistant")
                    if jarvis_path not in sys.path:
                        sys.path.insert(0, jarvis_path)
                    
                    from jarvis_core.vision_parser import parse_schedule_image
                    
                    ocr_results = parse_schedule_image(str(file_path))
                    if ocr_results:
                        combined_content += f"\n\n--- Du lieu OCR tu anh {file} ---\n{json.dumps(ocr_results, ensure_ascii=False, indent=2)}\n"
                except Exception as e:
                    print(f"[ERROR] Loi khi chay Vision OCR: {e}")

        if not combined_content.strip():
            print("[WARN] Khong co du lieu de xu ly.")
            return

        print("[AI] AI dang phan tich du lieu tong hop de nhan dien nhan vat...")
        
        # Tach theo khoi 'Basic Information' (Dua theo Character Detail.txt)
        char_blocks = re.split(r'Basic Information', combined_content)
        
        processed_count = 0
        for block in char_blocks:
            if "Name" in block and "Rarity" in block:
                self.process_character_block(block)
                processed_count += 1
                # Simulator mode: gioi han 3 nhan vat de tranh ton token va dam bao hieu qua
                if processed_count >= 3:
                    print("[INFO] Simulator mode: Da xu ly 3 nhan vat mau. Dung lai de Admin kiem tra.")
                    break
        
        print(f"[SUCCESS] Hoan tat dot phan tich mau. Da xu ly {processed_count} nhan vat.")

    def process_character_block(self, block):
        """Su dung LLM de sinh file Wiki Markdown chuan."""
        lines = block.splitlines()
        char_name = "Unknown"
        for i, line in enumerate(lines):
            if "Name" in line and i + 1 < len(lines):
                potential_name = lines[i+1].strip()
                if potential_name:
                    char_name = potential_name
                    break
        
        if char_name == "Unknown":
            return

        char_name_clean = re.sub(r'[^a-zA-Z0-9\s]', '', char_name).strip().replace(" ", "_")
        print(f"[AI-THINKING] Dang phan tich nhan vat: {char_name}...")

        prompt = f"""
        Ban la mot chuyen gia ve game Morimens. Hay chuyen doi du lieu tho duoi day thanh mot file Wiki Markdown chuyen nghiep.

        Yeu cau:
        1. Su dung YAML Frontmatter o dau file voi cac truong:
           - title: "{char_name}"
           - type: Character
           - rarity: (SSR/SR/R)
           - faction: (Chaos/Aequor/Caro/Ultra)
           - specialty: (Vd: Poison, Bleed, Tank, Assist, ...)
        2. Noi dung Markdown su dung cac Icon: 📊 (Stats), 🌟 (Enlightens), ⚔️ (Skills/Cards), 🔥 (Exalts), 💡 (Talents).
        3. Dinh dang bang bieu cho cac chi so neu can.
        4. Trinh bay sach dep, logic bang tieng Viet (cac thuat ngu game quan trong giu nguyen tieng Anh).

        Du lieu tho:
        {block[:3000]}
        """
        
        wiki_content = self._call_llm(prompt)
        
        if wiki_content:
            output_file = self.wiki_chars_dir / f"{char_name_clean}.md"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(wiki_content)
            print(f"[SAVED] Da tao Wiki thuc te cho: {char_name_clean}")
        else:
            print(f"[ERROR] LLM khong tra ve ket qua cho {char_name}")

if __name__ == "__main__":
    importer = BatchImporter()
    importer.run_import()