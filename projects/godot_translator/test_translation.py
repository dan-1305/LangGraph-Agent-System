import sys
import os
from pathlib import Path
from rich.console import Console

# Thêm root dự án vào path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from projects.godot_translator.core.extractor import GodotExtractor
from projects.godot_translator.core.translator import GodotTranslator
from projects.godot_translator.core.injector import GodotInjector
from projects.godot_translator.core.pack_manager import PackManager

if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

console = Console()

def test_single_file_translation():
    target_dir = Path("temp_workspace/test_output")
    target_file = target_dir / "scripts" / "levels" / "level_at_principal_witness_1.gd"
    
    if not target_file.exists():
        console.print(f"[bold red]File không tồn tại: {target_file}[/bold red]")
        return
        
    console.print(f"[bold yellow]1. Extracting từ {target_file.name}...[/bold yellow]")
    extractor = GodotExtractor(str(target_dir))
    texts = extractor.extract_from_file(target_file)
    
    if not texts:
        console.print("[bold red]Không tìm thấy chuỗi nào để dịch.[/bold red]")
        return
        
    console.print(f"Đã trích xuất {len(texts)} chuỗi: {texts}")
    
    console.print(f"[bold yellow]2. Dịch thuật bằng GodotTranslator...[/bold yellow]")
    # Dùng model free nhanh nhất hiện tại
    translator = GodotTranslator(model_name="gemini-3.1-flash-lite", api_key="")
    
    # Ép nó dịch tiếng Anh sang tiếng Việt bằng cách ghi đè _logic_handler nếu cần,
    # Tuy nhiên GodotTranslator mặc định có thể tự nhận diện tiếng Anh -> Việt nếu prompt tốt.
    # Thử dịch:
    translations = translator.translate_batch(texts)
    console.print(f"Kết quả dịch: {translations}")
    
    console.print(f"[bold yellow]3. Injecting kết quả vào file...[/bold yellow]")
    injector = GodotInjector(target_root=target_dir, output_dir=str(target_dir))
    injector.inject(target_file, translations)
    console.print("[bold green]Inject thành công![/bold green]")
    
    console.print(f"[bold yellow]4. Repacking file .pck mới...[/bold yellow]")
    pm = PackManager()
    original_exe_path = "D:/Users/Admin/Downloads/Game/the-last-node-windows/the-last-node.exe"
    out_path = pm.repack(original_exe_path, target_dir)
    console.print(f"[bold green]Repack thành công tại: {out_path}[/bold green]")
    
    console.print(f"[bold yellow]5. Khởi chạy Game Test...[/bold yellow]")
    pm.test_run(str(out_path), Path("temp_workspace/test_run_dir"))

if __name__ == "__main__":
    test_single_file_translation()
