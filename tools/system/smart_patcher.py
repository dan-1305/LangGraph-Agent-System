import os
import subprocess
from pathlib import Path

class SmartPatcher:
    """
    The Smart Patcher: A utility to automatically format and fix Python code.
    It runs `ruff check --fix` and `ruff format` to clean up tech debt.
    """
    def __init__(self, target_dir: str = "."):
        self.target_dir = Path(target_dir).resolve()

    def run_ruff(self):
        print(f"[*] Running Smart Patcher on {self.target_dir}...")
        try:
            print("[*] Running ruff format...")
            subprocess.run(["uv", "run", "ruff", "format", str(self.target_dir)], check=True)
            print("[*] Running ruff check --fix...")
            subprocess.run(["uv", "run", "ruff", "check", "--fix", str(self.target_dir)], check=True)
            print("[+] Smart Patching completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Smart Patcher encountered an error: {e}")

if __name__ == "__main__":
    patcher = SmartPatcher()
    patcher.run_ruff()
