import os

DOCS_DIR = os.path.abspath('projects/sillytavern_world_card_generator/docs')

def delete_empty_docs():
    if not os.path.exists(DOCS_DIR):
        return
        
    count = 0
    for filename in os.listdir(DOCS_DIR):
        if filename.startswith('WORLDCARD_') and filename.endswith('.md'):
            path = os.path.join(DOCS_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "Không có thông tin" in content:
                        os.remove(path)
                        print(f"Deleted empty file: {filename.encode('ascii', 'ignore').decode('ascii')}")
                        count += 1
            except Exception as e:
                print(f"Error: {e}")
    print(f"Total deleted: {count}")

if __name__ == "__main__":
    delete_empty_docs()
