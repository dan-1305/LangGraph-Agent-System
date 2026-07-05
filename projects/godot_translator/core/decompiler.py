import subprocess
import os
from pathlib import Path
from rich.console import Console

console = Console()

class GodotDecompiler:
    """
    Wrapper for external Godot decompile tools (like GDRE Tools CLI).
    Usage:
        decompiler = GodotDecompiler(tool_path="path/to/gdre_tools.exe")
        decompiler.decompile_pck("game.pck", "output_dir")
    """

    def __init__(self, tool_path: str = "gdre_tools"):
        self.tool_path = tool_path

    def decompile_pck(self, pck_path: str, output_dir: str):
        """Decompile a .pck file using GDRE Tools CLI."""
        console.print(f"[bold yellow]Executing decompile for {pck_path}...[/bold yellow]")
        
        # Example command for GDRE Tools: gdre_tools --headless --recover=path/to/pck --output-dir=path/to/output
        command = [
            self.tool_path,
            "--headless",
            f"--recover={pck_path}",
            f"--output-dir={output_dir}"
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                console.print("[bold green]Decompile successful![/bold green]")
                return True
            else:
                console.print(f"[bold red]Decompile failed: {result.stderr}[/bold red]")
                return False
        except FileNotFoundError:
            console.print(f"[bold red]Error: Decompile tool not found at {self.tool_path}[/bold red]")
            console.print("[cyan]Please install GDRE Tools and provide the correct path.[/cyan]")
            return False

if __name__ == "__main__":
    # Example usage
    # decompiler = GodotDecompiler()
    # decompiler.decompile_pck("Game.pck", "extracted_source")
    pass
