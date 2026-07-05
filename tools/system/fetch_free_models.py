import os
import httpx
import json
from pathlib import Path
from dotenv import load_dotenv

def fetch_free_models():
    load_dotenv()
    print("Hunting for FREE models on OpenRouter and Groq...")
    
    catalog_content = "# 🆓 FREE MODELS CATALOG\n\n"
    catalog_content += f"Last updated: {Path('docs/PROJECT_TRACKER.md').stat().st_mtime}\n\n"

    # 1. Fetch OpenRouter Free Models
    try:
        response = httpx.get("https://openrouter.ai/api/v1/models")
        response.raise_for_status()
        models = response.json().get('data', [])
        
        catalog_content += "## 🚀 OpenRouter (Miễn phí 100%)\n"
        catalog_content += "| Model ID | Context Window | Description |\n"
        catalog_content += "| :--- | :--- | :--- |\n"
        
        free_count = 0
        for m in models:
            pricing = m.get('pricing', {})
            # Check if prompt and completion are both 0
            if pricing.get('prompt') == "0" and pricing.get('completion') == "0":
                cid = m.get('id')
                context = m.get('context_length', 'N/A')
                desc = m.get('description', 'No description').split('.')[0]
                catalog_content += f"| `{cid}` | {context} | {desc} |\n"
                free_count += 1
        
        print(f"Found {free_count} free models on OpenRouter.")
    except Exception as e:
        print(f"Error fetching OpenRouter models: {e}")

    # 2. Groq Models (Current Free/Beta)
    catalog_content += "\n## ⚡ Groq (Beta/Free Usage)\n"
    catalog_content += "| Model ID | Max Tokens | Provider |\n"
    catalog_content += "| :--- | :--- | :--- |\n"
    groq_models = [
        ("llama3-70b-8192", "8192", "Meta"),
        ("llama3-8b-8192", "8192", "Meta"),
        ("mixtral-8x7b-32768", "32768", "Mistral"),
        ("gemma-7b-it", "8192", "Google"),
        ("whisper-large-v3", "N/A", "OpenAI")
    ]
    for mid, tokens, provider in groq_models:
        catalog_content += f"| `{mid}` | {tokens} | {provider} |\n"

    # Save to Markdown
    output_path = Path("docs/FREE_MODELS_CATALOG.md")
    output_path.write_text(catalog_content, encoding="utf-8")
    print(f"Catalog saved to {output_path}")

if __name__ == "__main__":
    fetch_free_models()
