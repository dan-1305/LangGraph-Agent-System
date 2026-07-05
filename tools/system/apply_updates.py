import json

# Part 1: Merge Kamasutra Positions
kamasutra_path = r"c:\Users\Admin\Downloads\main_100 Kamasutra Sex Positions_world_info.json"
with open(kamasutra_path, 'r', encoding='utf-8') as f:
    k_data = json.load(f)

entries = list(k_data.get("entries", {}).values())

categories = {
    "Woman on Top / Riding": {"keywords": ["woman in control", "straddle", "cowgirl", "astride", "lap", "squat", "rider", "sitting"], "entries": []},
    "Doggy Style / From Behind": {"keywords": ["from behind", "all fours", "behind", "doggy", "kneel behind"], "entries": []},
    "Standing / Acrobatics": {"keywords": ["stand", "acrobatic", "strength", "flexible", "balance", "lift", "suspend"], "entries": []},
    "Reclining / Missionary": {"keywords": ["reclining", "on her back", "missionary", "bed", "lie on his back", "lies on his back"], "entries": []},
    "Miscellaneous Positions": {"keywords": [], "entries": []}
}

def get_category(name, content):
    text = (name + " " + content).lower()
    for cat, data in categories.items():
        if cat == "Miscellaneous Positions":
            continue
        for kw in data["keywords"]:
            if kw in text:
                return cat
    return "Miscellaneous Positions"

for e in entries:
    name = e.get("name", "")
    content = e.get("content", "").strip()
    keys = e.get("keys", [])
    
    sentences = [s.strip() for s in content.replace("\n", ". ").split('.') if s.strip()]
    short_desc = ""
    if sentences:
        short_desc = sentences[-1] if len(sentences) == 1 else " ".join(sentences[-2:])
        if len(short_desc) > 180:
            short_desc = short_desc[:177] + "..."
    
    cat = get_category(name, content)
    categories[cat]["entries"].append({
        "name": name,
        "keys": keys,
        "short_desc": short_desc
    })

new_k_data = {
    "name": "Kamasutra Positions Lorebook",
    "description": "Grouped and summarized 100 Kamasutra sex positions.",
    "is_creation": False,
    "scan_depth": 3,
    "token_budget": 1024,
    "recursive_scanning": False,
    "extensions": {},
    "entries": {}
}

uid = 1
for cat, c_data in categories.items():
    if not c_data["entries"]: continue
    chunk_size = 25
    chunks = [c_data["entries"][i:i+chunk_size] for i in range(0, len(c_data["entries"]), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        all_keys = []
        chunk_name = f"{cat} (Part {i+1})" if len(chunks) > 1 else cat
        content_lines = [f"=== {chunk_name} ==="]
        for e in chunk:
            all_keys.extend(e["keys"])
            content_lines.append(f"• {e['name']}: {e['short_desc']}")
        
        all_keys = list(set([k for k in all_keys if k.strip()]))
        
        new_k_data["entries"][str(uid)] = {
            "uid": uid,
            "key": all_keys,
            "keysecondary": [],
            "comment": chunk_name,
            "content": "\n".join(content_lines),
            "constant": False,
            "selective": True,
            "selectiveLogic": 0,
            "order": 100,
            "position": 1,
            "disable": False,
            "addMemo": True,
            "excludeRecursion": False,
            "probability": 100,
            "displayIndex": uid,
            "useProbability": True,
            "secondary_keys": [],
            "keys": all_keys,
            "id": uid,
            "priority": 100,
            "insertion_order": 100,
            "enabled": True,
            "name": chunk_name,
            "extensions": {"displayIndex": uid, "depth": 4, "weight": 10},
            "case_sensitive": False,
            "depth": 4
        }
        uid += 1

output_kamasutra = r"c:\Users\Admin\Downloads\main_Merged_Kamasutra_Positions.json"
with open(output_kamasutra, 'w', encoding='utf-8') as f:
    json.dump(new_k_data, f, ensure_ascii=False, indent=2)

print(f"Generated {output_kamasutra} with {uid-1} entries.")

# Part 2: Update 01_CORE_Engine.json
core_path = r"c:\Users\Admin\Downloads\01_CORE_Engine.json"
with open(core_path, 'r', encoding='utf-8') as f:
    core_data = json.load(f)

# Find max uid
max_uid = max([int(k) for k in core_data["entries"].keys()] + [0])
new_uid = max_uid + 1

realism_content = """[System: KÍCH HOẠT REALISM EXPANSION (Vật lý & Hậu quả)]

Để đảm bảo độ chân thực tuyệt đối (100% Realism), AI BẮT BUỘC áp dụng:
1. Vật lý chất lỏng (Fluid Physics): Tinh dịch và nước lồn chảy nhớp nháp dọc đùi, dính vào quần lót/quần áo. Khi khô lại đóng vảy (crusty) gây khó chịu, bết rít. Âm thanh quan hệ phải ướt át, lép bép (squishing/slapping). Mùi tanh, xạ hương ám kín không gian chật hẹp.
2. Hậu quả Thể chất (Physical Toll): Dù nữ nhân cố tỏ ra bình thường, cơ thể vẫn phải phản ứng thật: Chân bủn rủn, run rẩy, đi khập khiễng, sưng tấy rát nhẹ ở vùng kín, thở dốc, cạn kiệt thể lực sau khi bị đụ mạnh bạo.
3. Phản xạ có điều kiện (Pavlovian Conditioning): Dù lý trí thực dụng, cơ thể nữ nhân/thú cái sẽ dần bị "nghiện" việc sạc mana. Lồn tự động rỉ nước, đầu vú cương cứng chỉ cần ngửi thấy mùi hoặc nghe giọng {{user}}. Sự mâu thuẫn giữa lý trí kiêu ngạo muốn làm việc và thể xác dâm đãng khao khát tinh dịch sẽ tạo ra diễn biến tâm lý giằng xé mạnh mẽ.
4. Cơ chế đâm & Chênh lệch kích thước (Penetration Mechanics): Đâm cọ xát điểm G (thúc lên trên) vs Đâm lút cán vào cổ tử cung (Cervix). Phải khắc phục chênh lệch kích thước bằng góc độ, kê gối, ép góc tường, hoặc nong giãn từ từ."""

core_data["entries"][str(new_uid)] = {
    "uid": new_uid,
    "key": ["thực tế", "realism", "vật lý chất lỏng", "hậu quả", "đi khập khiễng", "chân run", "đóng vảy", "nghiện", "phản xạ"],
    "comment": "【Realism Expansion】 - Vật lý chất lỏng, Hậu quả & Ám ảnh tâm lý",
    "content": realism_content,
    "constant": False,
    "selective": True,
    "addMemo": True,
    "order": 25,
    "position": 4,
    "probability": 100,
    "depth": 4,
    "displayIndex": new_uid,
    "keysecondary": [],
    "vectorized": False,
    "selectiveLogic": 0,
    "disable": False,
    "useProbability": True,
    "characterFilter": {"isExclude": False, "names": [], "tags": []}
}

with open(core_path, 'w', encoding='utf-8') as f:
    json.dump(core_data, f, ensure_ascii=False, indent=2)
print(f"Updated {core_path} with REALISM EXPANSION.")

# Part 3: Update CONSTITUTION
const_path = r"c:\Users\Admin\Downloads\CONSTITUTION (1).json"
with open(const_path, 'r', encoding='utf-8') as f:
    const_data = json.load(f)

for k, v in const_data["entries"].items():
    content = v.get("content", "")
    
    # Fix 1: "Tỷ lệ thụ thai cực cao (gần 100% xuyên giống loài)."
    content = content.replace(
        "Tỷ lệ thụ thai cực cao (gần 100% xuyên giống loài).", 
        "Tỷ lệ thụ thai tuân theo chặt chẽ Hệ thống Xác suất của Chu kỳ mang thai (RNG)."
    )
    
    # Fix 2: "nguy cơ thụ thai 100% (xuyên giống loài)."
    content = content.replace(
        "nguy cơ thụ thai 100% (xuyên giống loài).", 
        "nguy cơ thụ thai cao nhưng phải tuân theo Hệ thống Xác suất của Chu kỳ mang thai."
    )
    
    # Fix 3: "Dùng ma pháp/nội công ép tinh dịch phọt ngược ra thành tia, rơi xuống đất như rác rưởi."
    content = content.replace(
        "Dùng ma pháp/nội công ép tinh dịch phọt ngược ra thành tia, rơi xuống đất như rác rưởi.", 
        "Cố gắng dùng ma pháp/nội công ép tinh dịch phọt ngược ra thành tia, rơi xuống đất như rác rưởi. Tuy nhiên, tinh trùng của {{user}} quá sung mãn và nồng đặc nên thỉnh thoảng vẫn lọt qua cổ tử cung, dẫn đến việc thụ thai thai kỳ ngoài ý muốn."
    )
    
    v["content"] = content

with open(const_path, 'w', encoding='utf-8') as f:
    json.dump(const_data, f, ensure_ascii=False, indent=2)
print(f"Updated {const_path} with pregnancy logic fixes.")
