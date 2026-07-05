import os
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
preset_dir = BASE_DIR / "data" / "templates" / "preset"

# 1. Clean up duplicate files ending with (1), (2), (3) etc.
print("Cleaning up duplicates...")
for f in os.listdir(preset_dir):
    if re.search(r'\(\d+\)\.json$', f):
        os.remove(preset_dir / f)
        print(f"Deleted duplicate: {f}")

# Clean up the test file
test_file = preset_dir / "【Dreammini】3.92-Ultra-Merged-Test.json"
if test_file.exists():
    os.remove(test_file)
    print(f"Deleted test file: {test_file.name}")

# 2. Define the mapping of regex file keywords to preset file keywords
regex_mapping = {
    "regex_dreammini.json": ["dreammini"],
    "regex_kemini.json": ["kemini"],
    "regex_MoM.json": ["mom"],
    "regex_psyche.json": ["psyche"],
    "regex_Izumi.json": ["izumi"]
}

# 3. Process and merge
for regex_filename, keywords in regex_mapping.items():
    regex_path = preset_dir / regex_filename
    if not regex_path.exists():
        continue
        
    print(f"\nProcessing {regex_filename}...")
    
    # Read the regex rules
    with open(regex_path, "r", encoding="utf-8") as f:
        regex_data = json.load(f)
    
    regex_rules = regex_data.get("rules", [])
    if not regex_rules:
        continue
        
    # Find all matching presets
    for preset_filename in os.listdir(preset_dir):
        if preset_filename == regex_filename:
            continue
            
        is_match = any(kw.lower() in preset_filename.lower() for kw in keywords)
        if is_match and preset_filename.endswith(".json") and not preset_filename.startswith("regex"):
            preset_path = preset_dir / preset_filename
            print(f"  -> Injecting into {preset_filename}...")
            
            # Read preset
            with open(preset_path, "r", encoding="utf-8") as f:
                preset_data = json.load(f)
                
            # Inject regex
            if "extensions" not in preset_data:
                preset_data["extensions"] = {}
                
            # Override or set regex_scripts
            preset_data["extensions"]["regex_scripts"] = regex_rules
            
            # Save back
            with open(preset_path, "w", encoding="utf-8") as f:
                json.dump(preset_data, f, ensure_ascii=False, indent=4)
                
    # Delete the regex file after successful injection
    os.remove(regex_path)
    print(f"Deleted {regex_filename}")

print("\nDone!")
