import os

DOCS_DIR = os.path.abspath('projects/sillytavern_world_card_generator/docs')

def find_empty_files():
    if not os.path.exists(DOCS_DIR):
        return
        
    for filename in os.listdir(DOCS_DIR):
        if filename.startswith('WORLDCARD_') and filename.endswith('.md'):
            path = os.path.join(DOCS_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "Không có thông tin" in content:
                        # Safely print for windows
                        safe_name = filename.encode('ascii', 'ignore').decode('ascii')
                        print(f"EMPTY: {safe_name}")
            except Exception:
                pass

if __name__ == "__main__":
    find_empty_files()
