import os
import shutil
import glob

def clean_root_directory():
    archive_dir = "_archive_old_files"
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Created directory: {archive_dir}")

    # List of specific known temporary/junk files in root
    known_junk = [
        "censor_18plus_v3.py",
        "extract_recent_chats.py",
        "AI_Trading_Agent_Infrastructure.py",
        "core_engine_v1.py",
        "create_dirs.py",
        "fundamental_fetcher.py",
        "resource_scout.py",
        "run_hoc_sau.py",
        "test_gateway.py",
        "trading_agent.py",
        "world_state_sync.py",
        "ml_output.txt"
    ]

    moved_count = 0

    # Move known junk files
    for file in known_junk:
        if os.path.exists(file):
            shutil.move(file, os.path.join(archive_dir, file))
            print(f"Moved {file} to {archive_dir}/")
            moved_count += 1

    # Move all .bak files in root
    bak_files = glob.glob("*.bak")
    for bak in bak_files:
        shutil.move(bak, os.path.join(archive_dir, bak))
        print(f"Moved {bak} to {archive_dir}/")
        moved_count += 1
        
    print(f"\n[SUCCESS] Garbage Collection complete. Moved {moved_count} temporary files to Tier 4 storage.")

if __name__ == "__main__":
    clean_root_directory()
