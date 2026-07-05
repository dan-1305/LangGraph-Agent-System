from typing import Dict, List, Optional, Tuple

class TechTree:
    """
    Cây công nghệ định nghĩa các công thức Crafting (Chế tạo) cho AI.
    Không có phép thuật, chỉ có cơ khí và logic vật lý.
    """
    def __init__(self):
        # Định nghĩa các nguyên liệu cơ bản có thể đào được
        self.raw_materials = ['Wood', 'Stone', 'Iron Ore', 'Coal', 'Water']
        
        # Dictionary chứa công thức: key là tên vật phẩm tạo ra, value là list nguyên liệu cần thiết
        self.recipes: Dict[str, List[str]] = {
            # Giai đoạn 1: Công cụ thô sơ
            'Wooden Plank': ['Wood', 'Wood'],
            'Stick': ['Wooden Plank', 'Wooden Plank'],
            'Wooden Pickaxe': ['Wooden Plank', 'Wooden Plank', 'Wooden Plank', 'Stick', 'Stick'],
            'Stone Pickaxe': ['Stone', 'Stone', 'Stone', 'Stick', 'Stick'],
            'Furnace': ['Stone', 'Stone', 'Stone', 'Stone', 'Stone', 'Stone', 'Stone', 'Stone'],
            
            # Giai đoạn 2: Luyện kim cơ bản
            'Iron Ingot': ['Iron Ore', 'Coal', 'Furnace'], # Cần Furnace để nung
            'Iron Pickaxe': ['Iron Ingot', 'Iron Ingot', 'Iron Ingot', 'Stick', 'Stick'],
            'Iron Block': ['Iron Ingot'] * 9,
            
            # Giai đoạn 3: Cơ khí sơ khai (Động lực học)
            'Wooden Cogwheel': ['Stick', 'Stick', 'Stick', 'Stick', 'Wooden Plank'], # Bánh răng gỗ
            'Shaft': ['Iron Ingot', 'Iron Ingot'], # Trục truyền động
            'Water Wheel': ['Wooden Plank', 'Wooden Plank', 'Wooden Plank', 'Wooden Plank', 'Wooden Cogwheel', 'Water'], # Bánh xe nước
            
            # Giai đoạn 4: Tự động hóa
            'Mechanical Press': ['Iron Block', 'Shaft', 'Wooden Cogwheel'],
            'Steam Engine': ['Iron Block', 'Iron Block', 'Furnace', 'Water', 'Mechanical Press']
        }
        
    def craft(self, inventory: List[str], target_item: str) -> Tuple[bool, str, List[str]]:
        """
        Kiểm tra xem AI có đủ nguyên liệu để chế tạo target_item không.
        Trả về: (Thành công?, Lời nhắn, Inventory còn lại)
        """
        if target_item not in self.recipes:
            return False, f"Không tồn tại công thức cho '{target_item}'.", inventory
            
        recipe = self.recipes[target_item]
        temp_inv = inventory.copy()
        
        # Kiểm tra từng nguyên liệu
        for item in recipe:
            if item in temp_inv:
                temp_inv.remove(item)
            else:
                return False, f"Thiếu nguyên liệu '{item}' để chế tạo '{target_item}'.", inventory
                
        # Nếu thành công, thêm vật phẩm mới vào túi
        temp_inv.append(target_item)
        return True, f"Chế tạo thành công: {target_item}!", temp_inv

if __name__ == "__main__":
    tree = TechTree()
    my_inventory = ['Wood', 'Wood', 'Stone']
    print(f"Túi đồ hiện tại: {my_inventory}")
    
    success, msg, new_inv = tree.craft(my_inventory, 'Wooden Plank')
    print(f"Hành động: Chế tạo Wooden Plank -> {msg}")
    print(f"Túi đồ sau khi chế: {new_inv}")
