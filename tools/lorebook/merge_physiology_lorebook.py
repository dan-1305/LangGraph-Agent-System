import json

file1 = r"c:\Users\Admin\Downloads\main_Accurate Human Pregnancy_world_info.json"
file2 = r"c:\Users\Admin\Downloads\main_Womb simulator turned into a lorebook_world_info.json"
file3 = r"c:\Users\Admin\Downloads\main_Lactation_Breast Expansion_Pregnancy items_world_info.json"

print("Reading files...")
with open(file1, 'r', encoding='utf-8') as f:
    data1 = json.load(f)
with open(file2, 'r', encoding='utf-8') as f:
    data2 = json.load(f)
with open(file3, 'r', encoding='utf-8') as f:
    data3 = json.load(f)

# Extract entries
entries1 = list(data1.get("entries", {}).values())
entries2 = list(data2.get("entries", {}).values())
entries3 = list(data3.get("entries", {}).values())

# Filter entries3 to only keep "Breast Sizes"
filtered_entries3 = []
for e in entries3:
    if "Breast Sizes" in e.get("name", ""):
        filtered_entries3.append(e)

all_entries = entries1 + entries2 + filtered_entries3

# Initialize new structure
new_data = {
    "name": "Physiology & Pregnancy Lorebook",
    "description": "A comprehensive lorebook focusing entirely on female physiology, pregnancy stages, womb mechanics, and breast sizes. No magic items included.",
    "is_creation": False,
    "scan_depth": 3,
    "token_budget": 2048,
    "recursive_scanning": False,
    "extensions": {},
    "entries": {}
}

uid = 1
for e in all_entries:
    # copy entry
    new_e = dict(e)
    # update IDs
    new_e["uid"] = uid
    new_e["id"] = uid
    new_e["displayIndex"] = uid
    new_e["order"] = 10
    new_e["position"] = 1
    new_e["insertion_order"] = 10
    
    if "extensions" in new_e and isinstance(new_e["extensions"], dict):
        new_e["extensions"]["displayIndex"] = uid
        
    new_data["entries"][str(uid)] = new_e
    uid += 1

output_file = r"c:\Users\Admin\Downloads\main_Merged_Physiology_Pregnancy.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {output_file} with {uid-1} consolidated entries.")