"""
World Card Generator (Orchestrator):
Tập hợp các Agent (Storyteller, Lore Master, Coder) để sinh ra file World Card hoàn chỉnh.
"""

from typing import Dict, Any
from .models.world_card_v3 import WorldCardV3, UserIdeaInput
from .agents.storyteller_agent import StorytellerAgent
from .agents.lore_master_agent import LoreMasterAgent
from .agents.coder_agent import CoderAgent

class WorldCardGenerator:
    def __init__(self):
        self.storyteller = StorytellerAgent()
        self.lore_master = LoreMasterAgent()
        self.coder = CoderAgent()
        
    def generate(self, user_idea: UserIdeaInput) -> WorldCardV3:
        """
        Chạy quy trình sinh dữ liệu bằng AI thực.
        """
        print(f"🔄 Đang gọi Gemini API cho chủ đề: {user_idea.theme}...")
        
        idea_dict = user_idea.model_dump()
        
        # 1. Storyteller Step (Gọi LLM thật)
        print(">> Đang sinh System Prompt & First Message...")
        narrative_context = self.storyteller.generate_narrative_context(idea_dict)
        system_prompt = narrative_context.get("system_prompt", "Lỗi: Không sinh được System Prompt")
        first_message = narrative_context.get("first_message", "Lỗi: Không sinh được First Message")
        
        # 2. Lore Master Step (Gọi LLM thật)
        print(">> Đang sinh Lorebook...")
        lorebook = self.lore_master.generate_lorebook(idea_dict)
        
        # 3. Coder Step (Dùng Template tĩnh tạm thời)
        print(">> Đang chèn Regex / UI Extensions...")
        extensions = self.coder.generate_extensions(idea_dict)
        
        # 4. Gộp dữ liệu vào thẻ theo chuẩn SillyTavern V3
        from .models.world_card_v3 import CharacterData, CharacterBook, CharacterExtensions
        
        # Đóng gói Character Book
        char_book = CharacterBook(
            name=f"Lorebook - {user_idea.theme}",
            entries=lorebook
        )
        
        # Đóng gói Extensions
        char_ext = CharacterExtensions(
            regex_scripts=extensions
        )
        
        # Đóng gói Data
        char_data = CharacterData(
            name=f"World - {user_idea.theme}",
            description=system_prompt,
            first_mes=first_message,
            tags=user_idea.features,
            character_book=char_book,
            extensions=char_ext
        )
        
        # Đóng gói Root
        card = WorldCardV3(
            name=f"World - {user_idea.theme}",
            description=system_prompt,
            first_mes=first_message,
            tags=user_idea.features,
            data=char_data
        )
        
        print(f"✅ Đã sinh xong Lorebook ({len(lorebook)} entries).")
        print(f"✅ Đã sinh xong Extensions ({len(extensions)} files).")
        
        return card

    def export_to_json(self, card: WorldCardV3, filename: str = "generated_world_card.json"):
        """Xuất file JSON."""
        json_str = card.to_json()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"📁 Đã xuất file: {filename}")
        return filename
