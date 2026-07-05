import random
from typing import List, Tuple, Dict, Optional

class Tile:
    def __init__(self, x: int, y: int, type_name: str, symbol: str):
        self.x = x
        self.y = y
        self.type_name = type_name  # e.g., 'Grass', 'Tree', 'Stone', 'Water'
        self.symbol = symbol        # e.g., '.', 'T', 'S', '~'
        
    def __repr__(self):
        return self.symbol

class GridMap:
    def __init__(self, width: int = 20, height: int = 20):
        self.width = width
        self.height = height
        self.grid: List[List[Tile]] = []
        self.mobs: List[Tuple[int, int]] = []
        self._generate_world()
        
    def _generate_world(self):
        """Sinh thế giới đơn giản với tỉ lệ xuất hiện nhất định."""
        # Tỉ lệ: 60% Đất, 20% Cây, 15% Đá, 5% Nước
        types = [
            ('Grass', '.'),
            ('Tree', 'T'),
            ('Stone', 'S'),
            ('Water', '~')
        ]
        weights = [0.60, 0.20, 0.15, 0.05]
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Simple random choice based on weights
                choice = random.choices(types, weights=weights, k=1)[0]
                row.append(Tile(x, y, choice[0], choice[1]))
            self.grid.append(row)
            
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Lấy thông tin của một ô tại tọa độ x, y."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
        
    def set_tile(self, x: int, y: int, type_name: str, symbol: str) -> bool:
        """Cập nhật một ô (vd: khi AI đập cây, ô thành đất trống)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x].type_name = type_name
            self.grid[y][x].symbol = symbol
            return True
        return False

    def update(self, tick: int, player_x: int, player_y: int) -> int:
        """Cập nhật thế giới mỗi tick. Trả về lượng sát thương Player phải chịu."""
        damage = 0
        is_night = (tick % 24) >= 12
        
        # Sinh quái ngẫu nhiên vào ban đêm (Max 3 con)
        if is_night and len(self.mobs) < 3 and random.random() < 0.3:
            spawn_x = random.randint(0, self.width - 1)
            spawn_y = random.randint(0, self.height - 1)
            # Tránh sinh ngay trên đầu Player
            if abs(spawn_x - player_x) > 2 and abs(spawn_y - player_y) > 2:
                self.mobs.append((spawn_x, spawn_y))
                
        # Xóa quái khi trời sáng
        if not is_night:
            self.mobs.clear()
            
        # Di chuyển quái và tính sát thương
        new_mobs = []
        for mx, my in self.mobs:
            # Quái di chuyển về phía Player
            if mx < player_x: mx += 1
            elif mx > player_x: mx -= 1
            elif my < player_y: my += 1
            elif my > player_y: my -= 1
            
            if mx == player_x and my == player_y:
                damage += 5 # Bị cắn mất 5 HP
            else:
                new_mobs.append((mx, my))
                
        self.mobs = new_mobs
        return damage

    def render(self, player_x: Optional[int] = None, player_y: Optional[int] = None) -> str:
        """Trả về chuỗi hiển thị bản đồ."""
        output = []
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                if x == player_x and y == player_y:
                    row_str += "P " # Player
                elif (x, y) in self.mobs:
                    row_str += "M " # Mob
                else:
                    row_str += f"{self.grid[y][x].symbol} "
            output.append(row_str.strip())
        return "\n".join(output)

if __name__ == "__main__":
    world = GridMap(15, 10)
    print("🌍 BẢN ĐỒ EDEN (Phase 1):\n")
    print(world.render(player_x=7, player_y=5))
