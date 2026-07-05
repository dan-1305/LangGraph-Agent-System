import sys
from pathlib import Path
from pydantic import BaseModel, Field

# Import BaseAgent (do monorepo, sys.path cần lấy đúng thư mục src)
root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.append(str(root_dir))
from src.base_agent import BaseAgent

from agents.memory_module import MemoryModule

class PlayerActionSchema(BaseModel):
    reflection: str = Field(description="Rút kinh nghiệm từ lượt trước hoặc suy luận logic cho hành động tiếp theo.")
    action: str = Field(description="Hành động muốn thực hiện. VD: 'mine_wood', 'craft_Wooden Plank', 'move_north'")

class EdenPlayer(BaseAgent):
    def __init__(self, name: str, memory_module: MemoryModule):
        super().__init__(model_name="label:tier-2", temperature=0.7)
        self.name = name
        self.memory = memory_module
        
    def _ai_handler(self, current_state: str) -> dict:
        """Luồng suy nghĩ của Agent"""
        
        # Rolling Window Buffer: Truy xuất ký ức dài hạn bằng HyDE để tránh tràn prompt
        # Ví dụ query: "Làm sao sinh tồn ở toạ độ này hoặc chế đồ cần thiết?"
        long_term_lore = self.memory.retrieve_memory(f"Tôi đang ở trạng thái: {current_state}. Tôi cần làm gì?", top_k=2)

        prompt = f"""
Bạn là {self.name}, một kỹ sư bị nhốt trong thế giới Grid hình vuông.
Thế giới này không có phép thuật, chỉ có logic cơ khí.

[SỔ TAY KÝ ỨC CỦA BẠN]:
{long_term_lore}

[TRẠNG THÁI HIỆN TẠI]:
{current_state}

NHIỆM VỤ:
Dựa vào trạng thái hiện tại và túi đồ, hãy quyết định hành động tiếp theo.
Luôn luôn tuân thủ cấu trúc JSON được yêu cầu (Sử dụng Pydantic Structured Output).
Bắt buộc phải điền field 'reflection' để rút kinh nghiệm.
"""
        
        # Gọi BaseAgent với Schema Enforcer (bọc giáp tự động retry nếu LLM trả JSON sai)
        try:
            result = self._call_llm(prompt, schema=PlayerActionSchema)
            
            # Trích xuất bài học và lưu vào bộ nhớ ngắn hạn
            if result and isinstance(result, dict) and "reflection" in result:
                self.memory.add_lesson(result["reflection"])
                
                # Kích hoạt nén ký ức nếu đủ 10 lượt
                if self.memory.should_compress():
                    self.memory.compress_memory()
                    
            return result
        except Exception as e:
            print(f"⚠️ [Player {self.name}] LLM bị lỗi: {e}")
            return None

    def _logic_handler(self, current_state: str) -> dict:
        """Fallback Sinh Tồn nếu AI sập: Tự động đi hái lượm"""
        print(f"[{self.name} - FALLBACK] Tự động đi nhặt tài nguyên...")
        return {
            "reflection": "Cảm thấy mơ hồ, tôi chỉ biết đấm vào cái cây gần nhất.",
            "action": "mine_wood"
        }

if __name__ == "__main__":
    # Test Player
    memory = MemoryModule("projects/minecraft_eden_simulation/data/lore_memory.md")
    player = EdenPlayer("Steve", memory)
    
    mock_state = "Bạn đang đứng ở bãi cỏ. Túi đồ: ['Wood', 'Wood']. Trời đang sáng."
    print("--- Lượt 1 ---")
    decision = player.execute(mock_state)
    print(f"Decisions: {decision}")