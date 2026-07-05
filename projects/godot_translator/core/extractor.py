import re
from pathlib import Path
from rich.console import Console

console = Console()

class GodotExtractor:
    """Module to extract Japanese strings from Godot GDScript (.gd) and Scene (.tscn) files."""
    
    # Regex nhận diện ký tự tiếng Nhật (Kanji, Kana)
    JP_TEXT_PATTERN = re.compile(r'["\']([^"\']*(?:[ぁ-んァ-ヶー一-龠]|[\xe4-\xef][\x80-\xbf][\x80-\xbf])+[^"\']*)["\']')
    
    # Regex chung cho file .tscn: Bắt mọi chuỗi gán vào thuộc tính text="..." hoặc tooltip_text="..."
    TSCN_TEXT_PATTERN = re.compile(r'(?:text|tooltip_text)\s*=\s*["\']([^"\']+)["\']')
    
    # Regex chung cho file .gd: Bắt hàm tr("..."), dialogue = "...", text = "...", prompt_dialog("...")
    GD_TEXT_PATTERN = re.compile(r'(?:text|dialogue|message|body)\s*[:=]\s*"([^"]+)"|tr\("([^"]+)"\)|prompt_dialog\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*\)')

    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)

    def scan_files(self):
        """Recursively scan for .gd and .tscn files."""
        files = list(self.target_dir.rglob("*.gd")) + list(self.target_dir.rglob("*.tscn"))
        console.print(f"[bold blue]Found {len(files)} potential source files (.gd/.tscn).[/bold blue]")
        return files

    def extract_from_file(self, file_path: Path):
        """Extract Japanese strings from a single file based on its type."""
        try:
            content = None
            # Prioritize UTF-8
            for encoding in ['utf-8', 'euc-jp', 'cp932', 'shift_jis', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        temp_content = f.read()
                    
                    if encoding == 'latin-1':
                        try:
                            temp_content = temp_content.encode('latin-1').decode('utf-8')
                        except:
                            pass
                    
                    if re.search(r'[ぁ-んァ-ヶー一-龠]+', temp_content):
                        content = temp_content
                        break
                    
                    if content is None:
                        content = temp_content
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                with open(file_path, 'rb') as f:
                    content = f.read().decode('utf-8', errors='ignore')

            # Quét đa ngôn ngữ (Universal Extract)
            matches = []
            if file_path.suffix == ".tscn":
                matches.extend(self.TSCN_TEXT_PATTERN.findall(content))
                matches.extend(self.JP_TEXT_PATTERN.findall(content))
            else:
                gd_matches = self.GD_TEXT_PATTERN.findall(content)
                # GD_TEXT_PATTERN có nhiều group, lấy các group có nội dung
                for m in gd_matches:
                    for group_content in m:
                        if group_content and len(group_content.strip()) > 1:
                            matches.append(group_content)
                matches.extend(self.JP_TEXT_PATTERN.findall(content))
                
            # Lọc bỏ các chuỗi rỗng hoặc quá ngắn (tránh rác)
            matches = [m.strip() for m in matches if m and len(m.strip()) > 1]
                
            # Remove duplicates while preserving order
            unique_matches = list(dict.fromkeys(matches))
            
            return unique_matches
        except Exception as e:
            console.print(f"[bold red]Error reading {file_path}: {e}[/bold red]")
            return []

if __name__ == "__main__":
    target = r"d:\Users\Admin\Downloads\kimochi\Game\[Kimochi] [RJ01503291] さよならのチェックリスト\Output2"
    extractor = GodotExtractor(target)
    
    # Fix console output for Windows
    import sys
    import io
    if sys.platform == "win32":
        if hasattr(sys.stdout, 'reconfigure'):
            if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')
    
    # Test on a .tscn file if possible
    found_any = False
    for p in Path(target).rglob("*.tscn"):
        texts = extractor.extract_from_file(p)
        if texts:
            console.print(f"[bold green]Found JP content in TSCN: {p.name}[/bold green]")
            for t in texts[:5]:
                console.print(f"  - {t}")
            found_any = True
            break
            
    if not found_any:
        console.print("[yellow]No JP content found in .tscn files.[/yellow]")
