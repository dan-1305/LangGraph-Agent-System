import os
import re
import argparse
import shutil

DOCS_DIR = r'c:\Users\Admin\Desktop\WorkSpace\Project\LangGraph_Agent_System\projects\sillytavern_world_card_generator\docs'

def get_core_sig(filename):
    s = filename.replace('WORLDCARD_', '').replace('.md', '')
    sig = "".join(re.findall(r'[\u4e00-\u9fffA-Za-z0-9]', s))
    return sig

def clean_docs(aggressive=False, silent=False):
    if not os.path.exists(DOCS_DIR):
        return

    files = [f for f in os.listdir(DOCS_DIR) if f.startswith('WORLDCARD_') and f.endswith('.md')]
    sig_map = {}
    
    for filename in files:
        path = os.path.join(DOCS_DIR, filename)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                is_empty = "Không có thông tin" in content
                
                sig = get_core_sig(filename)
                if not sig: sig = filename
                
                if sig not in sig_map:
                    sig_map[sig] = []
                
                sig_map[sig].append({
                    'filename': filename,
                    'path': path,
                    'is_empty': is_empty,
                    'size': len(content)
                })
        except:
            continue

    deleted = 0
    for sig, instances in sig_map.items():
        if len(instances) > 1:
            instances.sort(key=lambda x: (x['is_empty'], -x['size']))
            for i in range(1, len(instances)):
                try:
                    os.remove(instances[i]['path'])
                    deleted += 1
                except:
                    pass
        elif aggressive and instances[0]['is_empty']:
            try:
                os.remove(instances[0]['path'])
                deleted += 1
            except:
                pass

    if not silent:
        print(f"Cleanup completed. Deleted {deleted} files from docs.")

def clean_comfy():
    root = 'c:/Users/Admin/Desktop/WorkSpace/Project/LangGraph_Agent_System'
    dest = 'c:/Users/Admin/Desktop/WorkSpace/Project/ComfyUI'
    
    files_to_move = [
        'alembic.ini', 'CODEOWNERS', 'comfyui_version.py', 'cuda_malloc.py', 
        'execution.py', 'extra_model_paths.yaml.example', 'folder_paths.py', 
        'hook_breaker_ac10a0.py', 'latent_preview.py', 'LICENSE', 'main.py', 
        'manager_requirements.txt', 'new_updater.py', 'node_helpers.py', 
        'nodes.py', 'openapi.yaml', 'protocol.py', 'pyproject.toml', 
        'pytest.ini', 'QUANTIZATION.md', 'server.py'
    ]
    
    dirs_to_move = [
        '.ci', 'alembic_db', 'api_server', 'app', 'blueprints', 'comfy', 
        'comfy_api', 'comfy_api_nodes', 'comfy_config', 'comfy_execution', 
        'comfy_extras', 'script_examples', 'tests-unit', 'utils'
    ]
    
    for f in files_to_move:
        p = os.path.join(root, f)
        d = os.path.join(dest, f)
        if os.path.exists(p):
            if not os.path.exists(d):
                shutil.move(p, d)
            else:
                os.remove(p)
                
    for d_name in dirs_to_move:
        p = os.path.join(root, d_name)
        dest_d = os.path.join(dest, d_name)
        if os.path.exists(p):
            if not os.path.exists(dest_d):
                shutil.move(p, dest_d)
            else:
                shutil.rmtree(p)
    print("Comfy cleanup done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="System Cleaner")
    parser.add_argument("--aggressive", action="store_true", help="Aggressively delete empty docs")
    parser.add_argument("--silent", action="store_true", help="Run silently without output")
    parser.add_argument("--comfy", action="store_true", help="Clean up comfyui files from root")
    
    args = parser.parse_args()
    
    if args.comfy:
        clean_comfy()
    else:
        clean_docs(aggressive=args.aggressive, silent=args.silent)
