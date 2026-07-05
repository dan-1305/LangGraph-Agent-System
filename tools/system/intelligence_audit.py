import os
from pathlib import Path

def run_intelligence_audit():
    print("[INTELLIGENCE AUDIT] STARTING...")
    
    base_dir = Path.cwd()
    
    # 1. Measure total codebase size (filtered)
    total_size = 0
    total_files = 0
    for path in base_dir.rglob('*'):
        if any(part in str(path) for part in ['.git', '.venv', '__pycache__', 'node_modules', 'data', 'projects/_template']):
            continue
        if path.is_file():
            total_size += path.stat().st_size
            total_files += 1
            
    # 2. Measure Context Hub size (Wiki + Memories)
    context_size = 0
    context_paths = [
        base_dir / "openwiki",
        base_dir / "context"
    ]
    for cp in context_paths:
        if cp.exists():
            for f in cp.rglob('*.md'):
                context_size += f.stat().st_size

    # 3. Calculate Compression Ratio (Knowledge Density)
    compression = (context_size / total_size) * 100 if total_size > 0 else 0
    
    print("-" * 30)
    print(f"Total Codebase: {total_files} files | {total_size/1024:.2f} KB")
    print(f"Context Hub: {context_size/1024:.2f} KB")
    print(f"Knowledge Density: {compression:.2f}% (Target: < 10% for efficiency)")
    print("-" * 30)
    
    if compression < 10:
        print("SUCCESS: High Intelligence Density achieved. Efficient RAG retrieval expected.")
    else:
        print("WARNING: Context Bloat detected. Recommendation: Prune minor details.")

if __name__ == "__main__":
    run_intelligence_audit()
