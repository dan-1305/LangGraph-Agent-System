import os
import httpx
import json
from pathlib import Path
from dotenv import load_dotenv

def generate_docs_and_map_models():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return

    # 1. Parse APIKEYFREE.md to JSON
    models_list = []
    apikey_free_path = Path("projects/local_proxy_server/APIKEYFREE.md")
    if apikey_free_path.exists():
        content = apikey_free_path.read_text(encoding="utf-8")
        # Simple extraction logic for demonstration
        for line in content.split("\n"):
            if "Gemini" in line or "Gemma" in line:
                models_list.append(line.strip())
    
    with open("data/free_models_map.json", "w", encoding="utf-8") as f:
        json.dump(models_list, f, indent=4)
    print("Free models mapped to data/free_models_map.json")

    # 2. Generate Documentation via Direct HTTP Request
    base_dir = Path.cwd()
    project_map = ""
    for path in sorted(base_dir.rglob('*')):
        if any(part in str(path) for part in ['.git', '.venv', '__pycache__', 'node_modules', 'data']):
            continue
        if path.is_file():
            project_map += f"- {path.relative_to(base_dir)}\n"

    # Use Local Proxy Server (Gemini Free)
    url = "http://localhost:8001/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer local-proxy-key'
    }
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [{
            "role": "user",
            "content": f"You are a technical architect. Based on this file structure, write a HIGH-LEVEL documentation for this system (OpenWiki format). Focus on Architecture and Workflow. Skip minor details to save context:\n\n{project_map[:12000]}"
        }]
    }

    print("Generating OpenWiki documentation via Local Proxy (Gemini Free)...")
    try:
        response = httpx.post(url, headers=headers, json=payload, timeout=120.0)
        response.raise_for_status()
        data = response.json()
        doc_content = data['choices'][0]['message']['content']
        
        # 3. Save as OpenWiki format
        wiki_dir = Path("openwiki")
        wiki_dir.mkdir(exist_ok=True)
        with open(wiki_dir / "CODEBASE_WIKI.md", "w", encoding="utf-8") as f:
            f.write(doc_content)
        
        # 4. Create CLAUDE.md for Agent optimization
        claude_content = f"# 🤖 CLAUDE.md (Agent Context)\n\nRefer to `openwiki/CODEBASE_WIKI.md` for full context.\n\n{doc_content[:2000]}"
        with open("CLAUDE.md", "w", encoding="utf-8") as f:
            f.write(claude_content)

        print("OpenWiki Documentation generated successfully at openwiki/CODEBASE_WIKI.md")
        print("CLAUDE.md updated for AI Agent optimization.")
    except Exception as e:
        print(f"Failed to generate documentation: {e}")

if __name__ == "__main__":
    generate_docs_and_map_models()
