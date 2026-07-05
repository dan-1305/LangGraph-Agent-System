import os
import sys
import time
from pathlib import Path
from colorama import init, Fore, Back, Style

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from world_engine.grid_map import GridMap
from world_engine.tech_tree import TechTree
from agents.memory_module import MemoryModule
from agents.eden_player import EdenPlayer
from telemetry import EdenTelemetry

init(autoreset=True)

class SimulationRunner:
    def __init__(self):
        self.world = GridMap(15, 10)
        self.tech_tree = TechTree()
        
        memory_path = Path(__file__).resolve().parent.parent / "data" / "lore_memory.md"
        self.memory = MemoryModule(str(memory_path))
        self.player = EdenPlayer("Steve", self.memory)
        self.telemetry = EdenTelemetry(run_id="TEST_001")
        
        self.player_x = 7
        self.player_y = 5
        self.inventory = []
        self.hp = 20
        self.tick = 0
        self.action_log = []
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def draw_tui(self):
        self.clear_screen()
        print(f"{Fore.CYAN}{Style.BRIGHT}=== 🌍 EDEN SIMULATION TUI ==={Style.RESET_ALL}")
        print(f"Tick: {self.tick} | Time: {'Day' if self.tick % 24 < 12 else 'Night'}")
        print("-" * 50)
        
        # 1. Vẽ Map
        map_str = self.world.render(self.player_x, self.player_y)
        # Colorize map simple
        map_str = map_str.replace('P', f"{Fore.YELLOW}P{Fore.RESET}")
        map_str = map_str.replace('M', f"{Fore.RED}M{Fore.RESET}")
        map_str = map_str.replace('T', f"{Fore.GREEN}T{Fore.RESET}")
        map_str = map_str.replace('S', f"{Fore.WHITE}S{Fore.RESET}")
        map_str = map_str.replace('~', f"{Fore.BLUE}~{Fore.RESET}")
        print(map_str)
        print("-" * 50)
        
        # 2. Vẽ Status
        print(f"{Fore.MAGENTA}--- STATUS ---{Style.RESET_ALL}")
        print(f"HP: {'❤️' * (self.hp//2)}")
        print(f"Inventory: {self.inventory}")
        print("-" * 50)
        
        # 3. Vẽ Logs
        print(f"{Fore.YELLOW}--- RECENT LOGS ---{Style.RESET_ALL}")
        for log in self.action_log[-5:]:
            print(log)
            
    def _log(self, msg: str, color=""):
        self.action_log.append(f"{color}{msg}{Style.RESET_ALL}")
        
    def execute_action(self, action_str: str):
        action_str = action_str.lower().strip()
        
        if action_str == 'move_north' and self.player_y > 0:
            self.player_y -= 1
            self._log("Di chuyển lên Bắc.")
            self.telemetry.record_action("move_north", True)
        elif action_str == 'move_south' and self.player_y < self.world.height - 1:
            self.player_y += 1
            self._log("Di chuyển xuống Nam.")
            self.telemetry.record_action("move_south", True)
        elif action_str == 'move_west' and self.player_x > 0:
            self.player_x -= 1
            self._log("Di chuyển sang Tây.")
            self.telemetry.record_action("move_west", True)
        elif action_str == 'move_east' and self.player_x < self.world.width - 1:
            self.player_x += 1
            self._log("Di chuyển sang Đông.")
            self.telemetry.record_action("move_east", True)
        elif action_str.startswith('mine'):
            target_tile = self.world.get_tile(self.player_x, self.player_y)
            if target_tile.type_name == 'Tree':
                self.inventory.append('Wood')
                self.world.set_tile(self.player_x, self.player_y, 'Grass', '.')
                self._log("Đập cây! Nhận được +1 Wood.", Fore.GREEN)
                self.telemetry.record_action("mine_wood", True)
            elif target_tile.type_name == 'Stone':
                self.inventory.append('Stone')
                self.world.set_tile(self.player_x, self.player_y, 'Grass', '.')
                self._log("Đập đá! Nhận được +1 Stone.", Fore.WHITE)
                self.telemetry.record_action("mine_stone", True)
            else:
                self._log(f"Đào đất trống... Chẳng được gì.", Fore.LIGHTBLACK_EX)
                self.telemetry.record_action("mine_empty", False)
        elif action_str.startswith('craft'):
            parts = action_str.split('_', 1)
            if len(parts) > 1:
                item = parts[1].title()
                success, msg, self.inventory = self.tech_tree.craft(self.inventory, item)
                if success:
                    self._log(f"Craft Thành Công: {item}!", Fore.CYAN)
                    self.telemetry.record_action(f"craft_{item}", True)
                else:
                    self._log(f"Craft Lỗi: {msg}", Fore.RED)
                    self.telemetry.record_action(f"craft_{item}", False)
            else:
                self.telemetry.record_action("craft_unknown", False)
        else:
            self._log(f"Hành động không hợp lệ: {action_str}", Fore.RED)
            self.telemetry.record_action("invalid", False)

    def step(self):
        self.tick += 1
        self.telemetry.record_tick()
        
        # Cập nhật Quái vật và lấy sát thương
        damage = self.world.update(self.tick, self.player_x, self.player_y)
        if damage > 0:
            self.hp -= damage
            self._log(f"💥 Bị quái vật tấn công! Mất {damage} HP.", Fore.RED)
            self.telemetry.record_damage(damage)
            
        if self.hp <= 0:
            return False # Player chết
            
        current_tile = self.world.get_tile(self.player_x, self.player_y)
        
        state_desc = f"""
- Tọa độ hiện tại: ({self.player_x}, {self.player_y})
- Ô đang đứng: {current_tile.type_name}
- Túi đồ: {self.inventory}
- HP: {self.hp}
- Thời gian: Tick {self.tick}
- Quái vật xung quanh: {'Có' if damage > 0 else 'Không'}
- Các ô xung quanh: Cố gắng di chuyển (move_north, move_south, move_west, move_east) để tìm tài nguyên. Nếu đứng trên Tree/Stone thì gọi 'mine'. Nếu có nguyên liệu thì gọi 'craft_TênĐồVật'.
        """
        self.draw_tui()
        print(f"\n{Fore.LIGHTBLACK_EX}[Agent đang suy nghĩ...]{Style.RESET_ALL}")
        
        self.telemetry.record_api_call()
        decision = self.player.execute(state_desc)
        
        if decision and isinstance(decision, dict):
            reflection = decision.get("reflection", "...")
            action = decision.get("action", "wait")
            
            self._log(f"💭 {reflection}", Fore.LIGHTBLUE_EX)
            self.execute_action(action)
            
            # Ghi nhận Nén Ký ức nếu Memory module đã nén (ở đây giả lập tăng counter)
            # Tuy nhiên memory_module xử lý độc lập, ta có thể tạm record_reflection.
        else:
            self._log("Agent bị ngơ ngác, không làm gì cả.", Fore.RED)
            
        return True # Còn sống
            
    def run(self, max_ticks=20):
        death_reason = "Sống sót tới lúc hết giờ."
        for _ in range(max_ticks):
            if not self.step():
                death_reason = "Tử vong do quái vật tấn công."
                self.draw_tui()
                print(f"\n{Fore.RED}💀 GAME OVER: PLAYER HAS DIED.{Style.RESET_ALL}")
                break
            self.draw_tui()
            # Tạm dừng để dễ quan sát
            time.sleep(2)
            
        self.telemetry.finalize_report(death_reason=death_reason)

if __name__ == "__main__":
    app = SimulationRunner()
    app.run(max_ticks=15)