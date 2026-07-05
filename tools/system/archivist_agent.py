import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import sys
import io

# Fix Unicode for Windows
if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if hasattr(sys.stderr, 'buffer') and 'pytest' not in sys.modules:
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
class ArchivistAgent:
    """
    Agent làm nhiệm vụ nén tri thức (Context Distillation).
    Chuyển các log cũ sang _archive và tạo Digest.
    """
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent.parent
        self.archive_dir = self.root_dir / "context" / "_archive"
        self.archive_dir.mkdir(exist_ok=True)

    def distill_debate_room(self):
        """Nén DEBATE_ROOM.md."""
        file_path = self.root_dir / "context" / "DEBATE_ROOM.md"
        if not file_path.exists(): return

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Giả lập nén: Chỉ giữ lại 2000 ký tự cuối và Final Decisions
        # Trong thực tế sẽ gọi LLM để tóm tắt
        sections = content.split("---")
        if len(sections) > 5:
            old_sections = sections[:-3]
            remaining_sections = sections[-3:]
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_file = self.archive_dir / f"DEBATE_ROOM_{timestamp}.md"
            
            with open(archive_file, "w", encoding="utf-8") as f:
                f.write("---".join(old_sections))
                
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("# 🏛️ DEBATE ROOM (Distilled)\n\n")
                f.write(f"> **Archivist Note:** Old debates moved to {archive_file.name}\n\n")
                f.write("---".join(remaining_sections))
            
            print(f"✅ DEBATE_ROOM.md distilled. Archive: {archive_file.name}")

    def run(self):
        print("--- [Archivist Agent] Starting Context Distillation ---")
        self.distill_debate_room()

if __name__ == "__main__":
    archivist = ArchivistAgent()
    archivist.run()
