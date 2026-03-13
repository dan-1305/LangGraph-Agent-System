import json
import uuid

input_file = r'data\[System] Universal Battle Sex.json'
output_file = r'data\[System] Universal Battle Sex (Grouped).json'

with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract entries
entries_dict = data.get('entries', {})
if not entries_dict and 'data' in data and 'entries' in data['data']:
    entries_dict = data['data']['entries']

# Group mappings
groups = {
    "1_Initiation": {"ids": ['0', '1', '52'], "name": "[System] Giai đoạn 1: Khởi nguồn & Gặp gỡ", "keys": ['đối thủ nữ', 'thách đấu', 'gặp mặt', 'khiêu chiến', 'khinh thường', 'pokémon', 'gái', 'trainer', 'bắt đầu', 'ghét', 'nam trainer']},
    "2_Combat": {"ids": ['2', '3', '51', '55', '56', '57', '58', '60', '66'], "name": "[System] Giai đoạn 2: Lĩnh vực Tà thần & Đấu trường", "keys": ['battle', 'chiến đấu', 'thách đấu', 'tấn công', 'đâm', 'hp', 'sát thương', 'k.o', 'creampie', 'đánh', 'combat', 'thi đấu', 'khán giả', 'shota']},
    "3_Resistance": {"ids": ['4', '35', '40', '62', '63', '64', '65'], "name": "[System] Giai đoạn 3: Kháng cự & Tsundere", "keys": ['kháng cự', 'vùng vẫy', 'điểm g', 'thở dốc', 'chống cự', 'mind break', 'thôi miên', 'nghiện', 'phản công', 'chịu đựng', 'vắt kiệt', 'độc', 'pheromone']},
    "4_Aftermath": {"ids": ['53', '54', '61'], "name": "[System] Giai đoạn 4: Hậu quả & Báo thù", "keys": ['thua cuộc', 'k.o', 'bắn tinh', 'mang thai', 'trả thù', 'tái đấu', 'rematch', 'hậu quả', 'kết thúc', 'phục thù']}
}

new_entries = {}
uid_counter = 1

for group_key, group_info in groups.items():
    combined_content = f"--- {group_info['name']} ---\n"
    
    for eid in group_info['ids']:
        if eid in entries_dict:
            entry = entries_dict[eid]
            content = entry.get('content', '').strip()
            if content:
                combined_content += f"\n{content}\n"
    
    # Create new entry
    new_uid = str(uid_counter)
    new_entries[new_uid] = {
        "uid": int(new_uid),
        "key": group_info['keys'],
        "keysecondary": [],
        "comment": group_info['name'],
        "content": combined_content.strip(),
        "constant": False,
        "vectorized": False,
        "selective": True,
        "insertionorder": 50, # High priority
        "enabled": True,
        "position": "before_char",
        "usecase": "System",
        "name": group_info['name'],
        "priority": 10
    }
    uid_counter += 1

# Reconstruct the Lorebook object
new_lorebook = {
    "name": "[System] Universal Battle Sex (Grouped)",
    "description": "Hệ thống chiến đấu Hardcore Tsundere đã được gộp gọn thành 4 giai đoạn kích hoạt theo từ khóa để tối ưu token.",
    "entries": new_entries,
    "version": 2
}

# Write out the new file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_lorebook, f, ensure_ascii=False, indent=2)

print(f"Successfully grouped 22 entries into 4 categories.")
print(f"Saved to: {output_file}")
