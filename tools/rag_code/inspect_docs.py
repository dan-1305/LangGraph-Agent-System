import os
import sys
import io

# Force stdout to be UTF-8
if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
DOCS_DIR = r'c:\Users\Admin\Desktop\WorkSpace\Project\LangGraph_Agent_System\projects\sillytavern_world_card_generator\docs'

def inspect_docs():
    if not os.path.exists(DOCS_DIR):
        return

    files = [f for f in os.listdir(DOCS_DIR) if f.startswith('WORLDCARD_') and f.endswith('.md')]
    
    for filename in files:
        path = os.path.join(DOCS_DIR, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                # Use a safe way to print or just check logic
                if "Naruto" in first_line or "-海贼王-" in first_line:
                    print(f"FILE: {filename.encode('ascii', 'ignore').decode('ascii')}")
                    print(f"  H1: {first_line.encode('ascii', 'ignore').decode('ascii')}")
        except:
            continue

if __name__ == "__main__":
    inspect_docs()
