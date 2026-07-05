import os
import re
import random
import string
from pathlib import Path

class CodeObfuscator:
    """
    He thong xao tron ma nguon (Obfuscation) lop sau.
    Bao ve cac thuat toan quan trong khoi viec doc trom.
    """
    def __init__(self):
        self.root_dir = Path(__file__).resolve().parent.parent
        self.output_dir = self.root_dir / "core" / "obfuscated"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _generate_random_name(self, length=12):
        """Tao ten bien/ham ngau nhien."""
        return "v_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def obfuscate_file(self, input_path: Path):
        """Xao tron mot file Python co ban."""
        if not input_path.exists(): return
        
        print(f"🛡️ Dang xao tron: {input_path.name}...")
        content = input_path.read_text(encoding="utf-8")
        
        # 1. Xoa bo comments
        content = re.sub(r'#.*', '', content)
        
        # 2. Xoa bo docstrings
        content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
        content = re.sub(r"'''.*?'''", '', content, flags=re.DOTALL)
        
        # 3. Nen code (xoa dong trong du thua)
        content = "\n".join([line for line in content.split("\n") if line.strip()])
        
        # Luu vao thu muc cach ly
        output_file = self.output_dir / f"obs_{input_path.name}"
        output_file.write_text(content, encoding="utf-8")
        print(f"✅ Da bao ve tai: {output_file}")

if __name__ == "__main__":
    obf = CodeObfuscator()
    # Test thu nghiem tren mot file technical
    target = Path("projects/ai_trading_agent/src/technical_engine.py")
    if target.exists():
        obf.obfuscate_file(target)
