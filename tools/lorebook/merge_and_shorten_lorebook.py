import json

file1 = r"c:\Users\Admin\Downloads\main_Realistic Representation of Sex._world_info.json"
file2 = r"c:\Users\Admin\Downloads\main_Fetish list race play school_world_info.json"

print("Reading files...")
with open(file1, 'r', encoding='utf-8') as f:
    data1 = json.load(f)
with open(file2, 'r', encoding='utf-8') as f:
    data2 = json.load(f)

categories = {
    "Biology & Anatomy": {"keywords": ["vagina", "penis", "clitoris", "orgasm", "hormone", "anatomy", "genitalia", "breast", "dick", "pussy"], "entries": []},
    "Diseases & STI": {"keywords": ["disease", "sti", "std", "infection", "bacteria", "syphilis", "gonorrhea"], "entries": []},
    "BDSM & Torture": {"keywords": ["bdsm", "bondage", "torture", "pain", "whip", "collar", "leash", "sadism", "masochism", "humiliation", "restraint", "gag", "spank", "punish", "choke", "slave"], "entries": []},
    "Size Play & Inflation": {"keywords": ["macro", "micro", "giant", "tiny", "shrink", "growth", "inflation", "fat", "muscle", "belly"], "entries": []},
    "Fluids & Excretion": {"keywords": ["scat", "watersports", "piss", "cum", "semen", "precum", "lactation", "milk", "vomit", "saliva", "sweat", "squirt", "leak"], "entries": []},
    "Pregnancy & Breeding": {"keywords": ["pregnancy", "breed", "oviposition", "egg", "impregnation", "creampie"], "entries": []},
    "Fantasy & Sci-Fi": {"keywords": ["elf", "orc", "demon", "angel", "alien", "robot", "cyborg", "magic", "monster", "furry", "animal", "kemonomimi", "lycanthrope", "dragon", "vampire", "tentacle"], "entries": []},
    "Romance & Intimacy": {"keywords": ["romance", "kiss", "cuddle", "foreplay", "intimacy", "affection", "date"], "entries": []},
    "Roles & Dynamics": {"keywords": ["dom", "sub", "master", "pet", "daddy", "brat", "roleplay", "incest", "family", "mom", "mommy", "sister", "brother"], "entries": []},
    "Specific Sex Acts": {"keywords": ["anal", "oral", "blowjob", "cunnilingus", "rimming", "titfuck", "footjob", "handjob", "masturbation", "fingering", "facesitting"], "entries": []},
    "Miscellaneous Fetishes": {"keywords": [], "entries": []}
}

def get_category(name, keys, content):
    text = (name + " " + " ".join(keys)).lower()
    for cat, data in categories.items():
        if cat == "Miscellaneous Fetishes":
            continue
        for kw in data["keywords"]:
            if kw in text:
                return cat
    return "Miscellaneous Fetishes"

all_entries = list(data1.get("entries", {}).values()) + list(data2.get("entries", {}).values())

for entry in all_entries:
    if "name" not in entry or "content" not in entry:
        continue
    name = entry.get("name", "")
    if "DIEASES CAUSED" in name or "<---" in name:
        continue
        
    keys = entry.get("keys", [])
    content = entry.get("content", "").strip()
    
    # Get first sentence or up to 100 chars
    clean_content = content.replace("\n", " ").strip()
    if clean_content.startswith("[What"):
        # Pattern: [What "..." means: Text]
        parts = clean_content.split("means:", 1)
        if len(parts) > 1:
            clean_content = parts[1].strip().strip("]")
            
    first_sentence = clean_content.split('.')[0]
    if len(first_sentence) > 120:
        first_sentence = first_sentence[:117] + "..."
    elif len(first_sentence) < 10:
        # Fallback if split was too aggressive
        first_sentence = clean_content[:120] + ("..." if len(clean_content) > 120 else "")
        
    cat = get_category(name, keys, content)
    categories[cat]["entries"].append({
        "name": name,
        "keys": keys,
        "short_desc": first_sentence.strip()
    })

new_data = {
    "name": "Master NSFW & RP Lorebook",
    "description": "A highly condensed and categorized lorebook containing biology, BDSM, fetishes, and roleplay dynamics.",
    "is_creation": False,
    "scan_depth": 50,
    "token_budget": 2000,
    "recursive_scanning": False,
    "extensions": {},
    "entries": {}
}

uid = 1
chunk_size = 25

print("Grouping and summarizing...")
for cat, data in categories.items():
    entries_list = data["entries"]
    if not entries_list:
        continue
        
    chunks = [entries_list[i:i + chunk_size] for i in range(0, len(entries_list), chunk_size)]
    
    for i, chunk in enumerate(chunks):
        all_keys = []
        chunk_name = f"{cat} (Part {i+1})" if len(chunks) > 1 else cat
        content_lines = [f"=== {chunk_name} Concepts ==="]
        
        for e in chunk:
            all_keys.extend(e["keys"])
            content_lines.append(f"• {e['name']}: {e['short_desc']}")
            
        all_keys = list(set(all_keys)) # unique keys
        
        # Exclude empty keys
        all_keys = [k for k in all_keys if k.strip()]
        
        final_content = "\n".join(content_lines)
        
        new_data["entries"][str(uid)] = {
            "uid": uid,
            "key": all_keys,
            "keysecondary": [],
            "comment": chunk_name,
            "content": final_content,
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
            "extensions": {
                "depth": 4,
                "weight": 10,
                "addMemo": True,
                "probability": 100,
                "displayIndex": uid,
                "selectiveLogic": 0,
                "useProbability": True,
                "characterFilter": None,
                "excludeRecursion": False
            },
            "case_sensitive": False,
            "depth": 4,
            "characterFilter": None
        }
        uid += 1

output_file = r"c:\Users\Admin\Downloads\main_Merged_Short_Lorebook.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {output_file} with {uid-1} consolidated entries.")
