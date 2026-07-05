from pathlib import Path
import subprocess

def create_template(base_dir: Path):
    template_dir = base_dir / "projects" / "_template"
    
    # Create directories
    dirs = ["src", "tests", "config", "data", "docs"]
    for d in dirs:
        (template_dir / d).mkdir(parents=True, exist_ok=True)
        
    # Create standard files
    (template_dir / "README.md").write_text("# Project Name\n\n## Description\n\n## Setup\n", encoding='utf-8')
    (template_dir / "requirements.txt").write_text("# Add dependencies here\n", encoding='utf-8')
    (template_dir / ".env.example").write_text("# Example env variables\nAPI_KEY=your_key_here\n", encoding='utf-8')
    (template_dir / "config" / "settings.py").write_text('import os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\n# Define config vars\n', encoding='utf-8')
    (template_dir / "tests" / "__init__.py").touch()
    (template_dir / "src" / "__init__.py").touch()
    
    print(f"✅ Created standardized project template at {template_dir}")

def generate_missing_files(base_dir: Path):
    projects_dir = base_dir / "projects"
    
    for p in projects_dir.iterdir():
        if p.is_dir() and not p.name.startswith('_') and p.name not in ['data', 'docs']:
            readme_path = p / "README.md"
            req_path = p / "requirements.txt"
            
            if not readme_path.exists():
                readme_path.write_text(f"# {p.name}\n\n## Overview\nAuto-generated README for {p.name}.\n", encoding='utf-8')
                print(f"📝 Created README.md for {p.name}")
                
            if not req_path.exists():
                # Call pipreqs or just touch
                try:
                    subprocess.run(["pipreqs", str(p), "--force", "--savepath", str(req_path)], capture_output=True)
                    print(f"📦 Generated requirements.txt for {p.name} using pipreqs")
                except Exception:
                    req_path.write_text("# Add dependencies here\n", encoding='utf-8')
                    print(f"📦 Created empty requirements.txt for {p.name}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    create_template(base_dir)
    generate_missing_files(base_dir)
