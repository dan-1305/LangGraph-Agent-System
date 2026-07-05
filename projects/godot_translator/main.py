import sys
from pathlib import Path
from rich.console import Console
import shutil
import io
import os

# Fix encoding cho Windows console
if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer') and 'pytest' not in sys.modules:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer') and 'pytest' not in sys.modules:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
# Thêm core vào path
sys.path.append(str(Path(__file__).resolve().parent))

from core.extractor import GodotExtractor
from core.translator import GodotTranslator
from core.injector import GodotInjector

console = Console()

def main():
    # Cấu hình đường dẫn cố định
    target_dir_str = r"d:\Users\Admin\Downloads\kimochi\Game\[Kimochi] [RJ01503291] さよならのチェックリスト\Output2"
    
    target_dir = Path(target_dir_str)
    if not target_dir.exists():
        console.print(f"[bold red]Path not found![/bold red]")
        return

    output_dir_str = "translated_project"
    output_dir = Path(output_dir_str)
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    extractor = GodotExtractor(target_dir_str)
    translator = GodotTranslator(model_name="gemini-3-flash-preview")
    injector = GodotInjector(target_root=target_dir, output_dir=output_dir_str)

    console.print(f"[bold green]Starting Translation (Smart Skip Mode)...[/bold green]")

    # Lấy danh sách TOÀN BỘ file
    all_files = [p for p in target_dir.rglob("*") if p.is_file()]
    
    if not all_files:
        return

    total = len(all_files)
    for i, file_path in enumerate(all_files):
        rel_p = file_path.relative_to(target_dir)
        target_path = output_dir / rel_p
        
        # CƠ CHẾ SMART SKIP: Nếu file đã tồn tại ở output thì bỏ qua (trừ file .gd/.tscn cần dịch)
        # Điều này giúp resume task nếu bị timeout
        if target_path.exists() and file_path.suffix not in [".gd", ".tscn"]:
            continue
            
        console.print(f"[{i+1}/{total}] Processing: {rel_p}")
        
        if file_path.suffix in [".gd", ".tscn"]:
            # Nếu file .gd/.tscn đã có ở đích, ta vẫn check xem có cần dịch không
            # (Hoặc có thể check dung lượng để skip nếu muốn nhanh hơn)
            texts = extractor.extract_from_file(file_path)
            if texts:
                console.print(f"  -> Translating {len(texts)} strings...")
                translations = translator.translate_batch(texts)
                injector.inject(file_path, translations)
            else:
                injector.inject(file_path, {})
        else:
            injector.inject(file_path, {})

    console.print(f"\n[bold green]Process Complete![/bold green]")

if __name__ == "__main__":
    main()
