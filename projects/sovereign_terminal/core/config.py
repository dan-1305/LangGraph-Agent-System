"""
Sovereign Terminal - Cấu hình API và Environment.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env từ root monorepo
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

class Config:
    """Cấu hình trung tâm cho Sovereign Terminal."""
    
    # API Settings - GGCHAN Gateway (OpenAI-compatible)
    API_KEY: str = os.getenv("GGCHAN_API_KEY", "")
    BASE_URL: str = os.getenv("GGCHAN_BASE_URL", "https://gcli.ggchan.dev/v1")
    
    # Model Settings
    DEFAULT_MODEL: str = "gemini-3.1-pro-preview"
    FALLBACK_MODEL: str = "gemini-3-flash-preview"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 8192
    
    # System Settings
    ROOT_DIR: Path = ROOT_DIR
    MAX_HISTORY: int = 20  # Giữ tối đa 20 tin nhắn gần nhất
    COMMAND_TIMEOUT: int = 60  # Timeout cho run_command (giây)
    
    # Protected files (không cho phép write)
    PROTECTED_FILES: list = [".env", "pyproject.toml", "uv.lock"]
    
    # Forbidden commands (không cho phép run)
    FORBIDDEN_COMMANDS: list = [
        "rm -rf", "del /f /s /q", "format", "shutdown", 
        "rmdir /s /q", "mkfs", "dd if=", ":(){:|:&};:"
    ]
    
    @classmethod
    def validate(cls) -> bool:
        """Kiểm tra xem API Key đã được cấu hình chưa."""
        if not cls.API_KEY:
            print("[ERROR] GGCHAN_API_KEY không tìm thấy trong .env!")
            print("Vui lòng thêm: GGCHAN_API_KEY=gg-gcli-xxx vào file .env")
            return False
        return True
    
    @classmethod
    def get_client_config(cls) -> dict:
        """Trả về config cho OpenAI client."""
        return {
            "api_key": cls.API_KEY,
            "base_url": cls.BASE_URL,
        }