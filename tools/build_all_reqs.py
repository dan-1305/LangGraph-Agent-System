import os

root_reqs = "requirements.in"
out_reqs = "all_requirements.in"

req_files = [root_reqs]
for root, dirs, files in os.walk("projects"):
    if "requirements.txt" in files:
        req_files.append(os.path.join(root, "requirements.txt"))

with open(out_reqs, 'w', encoding='utf-8') as out_f:
    for req in req_files:
        # replace backslashes with forward slashes for cross-platform compatibility
        normalized_path = req.replace('\\', '/')
        out_f.write(f"-r {normalized_path}\n")

print(f"Generated {out_reqs} containing {len(req_files)} files.")