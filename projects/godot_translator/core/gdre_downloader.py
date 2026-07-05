from core_utilities.http_client import HTTPClient
import os
import zipfile
import platform
from pathlib import Path
from rich.console import Console

import sys
if sys.platform == "win32":
    if hasattr(sys.stdout, 'reconfigure'):
        if 'pytest' not in sys.modules: sys.stdout.reconfigure(encoding='utf-8')

console = Console()

GDRE_API_URL = "https://api.github.com/repos/bruvzg/gdsdecomp/releases/latest"

def download_gdre_tools(target_dir: str = "tools/gdre_tools"):
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    sys_os = platform.system().lower()
    
    # Check if already downloaded
    exe_name = "gdre_tools.exe" if sys_os == "windows" else "gdre_tools"
    if (target_path / exe_name).exists():
        console.print(f"[bold green]GDRE Tools đã tồn tại tại {target_path}[/bold green]")
        return target_path / exe_name

    console.print("[bold yellow]Đang lấy thông tin bản GDRE Tools mới nhất...[/bold yellow]")
    try:
        response = HTTPClient.get(GDRE_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        download_url = None
        for asset in data.get("assets", []):
            name = asset["name"].lower()
            if sys_os == "windows" and "win" in name and "console" in name and name.endswith(".zip"):
                download_url = asset["browser_download_url"]
                break
                
        if not download_url:
            # Fallback
            for asset in data.get("assets", []):
                name = asset["name"].lower()
                if sys_os == "windows" and "win" in name and name.endswith(".zip"):
                    download_url = asset["browser_download_url"]
                    break

        if not download_url:
            raise Exception("Không tìm thấy link tải GDRE Tools cho hệ điều hành này.")

        console.print(f"Đang tải từ: {download_url}")
        zip_path = target_path / "gdre_download.zip"
        
        with HTTPClient.get(download_url, stream=True) as r:
            r.raise_for_status()
            with open(zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
        console.print("Đang giải nén GDRE Tools...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_path)
            
        zip_path.unlink() # Clean up zip
        
        # Rename the extracted exe to a standard name for easier access
        found_exe = None
        for file in target_path.iterdir():
            if file.suffix == ".exe":
                found_exe = file
                break
        
        if found_exe and found_exe.name != exe_name:
            final_path = target_path / exe_name
            if final_path.exists():
                final_path.unlink()
            found_exe.rename(final_path)
            console.print(f"[bold green]Đã cài đặt thành công tại: {final_path}[/bold green]")
            return final_path
            
        return target_path / exe_name

    except Exception as e:
        console.print(f"[bold red]Lỗi khi tải GDRE Tools: {e}[/bold red]")
        return None

if __name__ == "__main__":
    download_gdre_tools()
