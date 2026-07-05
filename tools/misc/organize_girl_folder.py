import os
import shutil
from collections import defaultdict
import re

TARGET_DIR = r"d:\Users\Admin\Downloads\Girl"

def get_common_prefix(name1, name2):
    # Find the longest common string prefix between two strings
    prefix = []
    for c1, c2 in zip(name1, name2):
        if c1 == c2:
            prefix.append(c1)
        else:
            break
    return "".join(prefix)

def clean_common_prefix(prefix):
    # Clean up trailing spaces, underscores, numbers if they are partial
    prefix = re.sub(r'[\s_\-\.]+$', '', prefix)
    return prefix

def main():
    if not os.path.exists(TARGET_DIR):
        print(f"Directory not found: {TARGET_DIR}")
        return

    # 1. Get all files and existing directories
    items = os.listdir(TARGET_DIR)
    files = [f for f in items if os.path.isfile(os.path.join(TARGET_DIR, f)) and f != 'organize_files.py']
    directories = [d for d in items if os.path.isdir(os.path.join(TARGET_DIR, d))]
    
    dir_map = {d.lower(): d for d in directories}
    
    # 2. Extract base names
    base_files = {f: os.path.splitext(f)[0] for f in files}
    
    # 3. Find pairwise common prefixes
    # We group files if their base names share a common prefix of at least 4 characters
    # that starts at the beginning of the filename.
    matched_files = set()
    
    # First, try to match files with existing directories exactly or partially
    moved_count = 0
    
    for f in files:
        if f in matched_files: continue
        base_name = base_files[f]
        
        # Try to match with existing dirs
        for d_lower, d_actual in dir_map.items():
            if base_name.lower().startswith(d_lower) or d_lower in base_name.lower().split('_')[0]:
                src = os.path.join(TARGET_DIR, f)
                dst = os.path.join(TARGET_DIR, d_actual, f)
                shutil.move(src, dst)
                moved_count += 1
                matched_files.add(f)
                print(f"Moved {f} -> {d_actual}/")
                break
                
    files = [f for f in files if f not in matched_files]
    
    # Now group remaining files by common prefix
    groups = defaultdict(list)
    processed = set()
    
    for i in range(len(files)):
        f1 = files[i]
        if f1 in processed: continue
        base1 = base_files[f1]
        
        # Look for files that share a prefix with f1
        current_group = [f1]
        best_prefix = base1
        
        for j in range(i + 1, len(files)):
            f2 = files[j]
            if f2 in processed: continue
            base2 = base_files[f2]
            
            common = get_common_prefix(base1.lower(), base2.lower())
            clean_common = clean_common_prefix(common)
            
            # If the common prefix is long enough and contains letters
            if len(clean_common) >= 4 and re.search(r'[a-zA-Z]', clean_common):
                current_group.append(f2)
                best_prefix = common # use original case or lower common
        
        if len(current_group) > 1:
            # We found a group!
            final_prefix = clean_common_prefix(get_common_prefix(base_files[current_group[0]], base_files[current_group[1]]))
            for f in current_group:
                final_prefix = clean_common_prefix(get_common_prefix(final_prefix.lower(), base_files[f].lower()))
            
            if len(final_prefix) >= 3:
                for f in current_group:
                    processed.add(f)
                    groups[final_prefix].append(f)
                    
    # Move the grouped files
    for prefix, file_list in groups.items():
        if len(file_list) < 2: continue
        
        # Create folder named after the common prefix
        folder_name = prefix.strip()
        new_dir_path = os.path.join(TARGET_DIR, folder_name)
        os.makedirs(new_dir_path, exist_ok=True)
        print(f"Created new directory: {folder_name}")
        
        for f in file_list:
            src = os.path.join(TARGET_DIR, f)
            dst = os.path.join(TARGET_DIR, folder_name, f)
            shutil.move(src, dst)
            moved_count += 1
            print(f"Moved {f} -> {folder_name}/")

    print(f"\nTotal files moved: {moved_count}")

if __name__ == "__main__":
    main()
