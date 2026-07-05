import re
import os
from pathlib import Path
from typing import Dict
import shutil
from rich.console import Console

console = Console()

class GodotInjector:
    """Module to inject translated strings back into GDScript/TSCN files and maintain directory structure."""

    def __init__(self, target_root: Path, output_dir: str = "translated_project"):
        self.target_root = target_root
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def inject(self, file_path: Path, translations: Dict[str, str]):
        """Replace Japanese strings and save in the mirrored structure, while cleaning .remap/.gdc files."""
        
        # 1. Tính toán đường dẫn đích (Mirrored Structure)
        try:
            relative_path = file_path.relative_to(self.target_root)
        except ValueError:
            relative_path = Path(file_path.name)
            
        target_path = self.output_dir / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 2. Xử lý dọn dẹp các file .remap và .gdc gây nhiễu
        # Nếu ta đang ghi file .gd, phải đảm bảo không có .gd.remap hay .gdc ở thư mục đích
        if file_path.suffix == ".gd":
            remap_path = target_path.with_name(target_path.name + ".remap")
            gdc_path = target_path.with_suffix(".gdc")
            if remap_path.exists(): os.remove(remap_path)
            if gdc_path.exists(): os.remove(gdc_path)
            
        elif file_path.suffix == ".tscn":
            remap_path = target_path.with_name(target_path.name + ".remap")
            if remap_path.exists(): os.remove(remap_path)

        # 3. Nếu không có bản dịch, thực hiện copy nguyên bản
        if not translations:
            try:
                shutil.copy2(file_path, target_path)
            except Exception as e:
                console.print(f"[bold red]Failed to copy {file_path}: {e}[/bold red]")
            return

        # 4. Thực hiện thay thế bản dịch
        try:
            content = None
            for encoding in ['utf-8', 'cp932', 'shift_jis', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                shutil.copy2(file_path, target_path)
                return

            new_content = content
            sorted_keys = sorted(translations.keys(), key=len, reverse=True)

            for original in sorted_keys:
                translated = translations[original]
                # Sử dụng replace an toàn
                new_content = new_content.replace(f'"{original}"', f'"{translated}"')
                new_content = new_content.replace(f"'{original}'", f"'{translated}'")

            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            console.print(f"[bold green]Injected: {relative_path}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Failed to inject into {file_path}: {e}[/bold red]")

if __name__ == "__main__":
    # Test cleanup logic
    pass
