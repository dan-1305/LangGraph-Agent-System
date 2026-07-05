"""
API Guard: Secure configuration management for Gemini API.

STRICT RULES (from .clinerules - The Death Rule):
1. ABSOLUTELY NO HARDCODED API Keys or Base URLs in source code.
2. API Key MUST be loaded from .env file using os.getenv().
3. DO NOT import requests to manually post data to LLM.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass


class Config:
    """
    Secure configuration manager for Gemini API.
    
    Loads all sensitive data from environment variables.
    Never hardcodes credentials.
    """
    
    def __init__(self, env_file: Optional[str] = None) -> None:
        """
        Initialize configuration by loading environment variables.
        
        Args:
            env_file: Path to .env file. If None, searches in parent directories.
        
        Raises:
            ConfigError: If required environment variables are missing.
        """
        # Load .env file
        if env_file:
            load_dotenv(env_file)
        else:
            # Auto-discover .env in parent directories (root workspace)
            project_root = Path(__file__).resolve().parent.parent.parent
            load_dotenv(project_root / '.env')
        
        # Validate required configuration
        self._validate()
    
    def _validate(self) -> None:
        """Validate that all required environment variables are set."""
        missing_vars = []
        
        if not self.api_key:
            missing_vars.append("GCLI_API_KEY")
        
        if missing_vars:
            raise ConfigError(
                f"Missing required environment variables: {', '.join(missing_vars)}\n"
                "Please create a .env file with your GCLI_API_KEY."
            )
    
    @property
    def api_key(self) -> Optional[str]:
        """
        Get Gemini API key from environment.
        
        Returns:
            API key string or None if not set.
        """
        return os.getenv("GCLI_API_KEY")
    
    @property
    def base_url(self) -> str:
        """
        Get Gemini API base URL from environment.
        
        Returns:
            Base URL string or default if not set.
        """
        return os.getenv(
            "GCLI_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta"
        )
    
    @property
    def model(self) -> str:
        """
        Get default model name.
        
        Returns:
            Model name string.
        """
        return os.getenv("GCLI_MODEL", "gemini-1.5-flash")
    
    @property
    def timeout(self) -> int:
        """
        Get request timeout in seconds.
        
        Returns:
            Timeout value in seconds.
        """
        return int(os.getenv("GCLI_TIMEOUT", "60"))
    
    def get_headers(self) -> dict[str, str]:
        """
        Get HTTP headers for API requests.
        
        Returns:
            Dictionary of HTTP headers.
        """
        return {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key or ""
        }
    
    def __repr__(self) -> str:
        """String representation (safe - hides API key)."""
        return (
            f"Config(api_key={'***' if self.api_key else None}, "
            f"base_url={self.base_url}, model={self.model})"
        )