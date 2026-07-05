"""
Core Configuration Module for Local Proxy Server

This module handles environment variable loading and configuration management.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Search for .env in parent directories (up to 4 levels)
current_dir = Path(__file__).parent.parent.parent
for _ in range(4):
    env_path = current_dir / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
        break
    current_dir = current_dir.parent


class Settings:
    """Application settings and configuration."""
    
    def __init__(self) -> None:
        """Initialize settings and validate required environment variables."""
        # Read GEMINI_API_KEYS (comma separated list) first
        api_keys_str = os.getenv("GEMINI_API_KEYS", "")
        if api_keys_str:
            # Parse, strip and filter empty keys
            self.gemini_api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]
        else:
            self.gemini_api_keys = []
            
        # Add single key to the list if it's not already there
        single_key = os.getenv("GEMINI_API_KEY", "")
        if single_key and single_key.strip() not in self.gemini_api_keys:
            self.gemini_api_keys.append(single_key.strip())
            
        # Keep gemini_api_key for backwards compatibility (defaults to first key)
        self.gemini_api_key = self.gemini_api_keys[0] if self.gemini_api_keys else ""
        
        # Validate that we have at least one key
        if not self.gemini_api_keys:
            raise ValueError(
                "GEMINI_API_KEY or GEMINI_API_KEYS is not set in environment variables. "
                "Please add at least one valid Gemini API key to your .env file."
            )
            
        # Fallback API keys (Task 1.3: Groq / OpenRouter Backup)
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
            
        # Keep track of active key index
        self.current_key_index = 0
        
        # Server configuration
        self.host = os.getenv("HOST", "0.0.0.0")
        self.port = int(os.getenv("PORT", "8000"))
        
        # Gemini API configuration
        self.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.default_model = "gemini-2.5-flash"  # Standard safe model
        
        # MAXIMIZING FREE TIER - Model Pool Rotation
        # Strategy: Prioritize by quota and capability
        # With 4 keys: Multiply each RPD by 4
        
        # HIGH PRIORITY (Best quota/speed balance)
        self.high_quota_models = [
            "gemini-3.1-flash-lite",  # 500 RPD/key = 2000 total ⭐ HIGHEST
            "gemma-4-26b-a4b-it",     # 1500 RPD/key = 6000 total 🏆 MAX
            "gemma-4-31b-it",         # 1500 RPD/key = 6000 total 🏆 MAX
        ]
        
        # MEDIUM PRIORITY (Standard chat models)
        self.standard_models = [
            "gemini-3.5-flash",       # 20 RPD/key = 80 total (Latest)
            "gemini-2.5-flash",       # 20 RPD/key = 80 total (Stable)
            "gemini-2.5-flash-lite",  # 20 RPD/key = 80 total (Faster)
            "gemini-3-flash",         # 20 RPD/key = 80 total (Newer)
        ]
        
        # BACKUP (Legacy mapping)
        self.model_mapping = {
            # Future/Advanced models → Prioritize correctly
            "gemini-3.5-flash": "gemini-3.5-flash",        # Keep as-is (20 RPD)
            "gemini-3.1-flash-lite": "gemini-3.1-flash-lite", # Keep as-is (500 RPD)
            "gemini-3-flash": "gemini-3-flash",            # Keep as-is (20 RPD)
            
            # Stable models
            "gemini-2.5-flash": "gemini-2.5-flash",        # Keep as-is (20 RPD)
            "gemini-2.5-flash-lite": "gemini-2.5-flash-lite", # Keep as-is (20 RPD)
            "gemini-2.5-pro": "gemini-2.5-flash",          # Map to Flash
            "gemini-2.5-pro-002": "gemini-2.5-flash",
            
            # Legacy → Map to available models
            "gemini-2.0-flash": "gemini-2.5-flash",
            "gemini-2.0-flash-001": "gemini-2.5-flash",
            "gemini-2.0-flash-lite": "gemini-2.5-flash-lite",
            "gemini-2.0-flash-lite-001": "gemini-2.5-flash-lite",
            "gemini-2.0-flash-exp": "gemini-2.5-flash",
            "gemini-1.5-flash": "gemini-2.5-flash",
            "gemini-1.5-pro": "gemini-2.5-flash",
            "gemini-pro": "gemini-2.5-flash",
            "gemini-flash": "gemini-3.1-flash-lite",      # Use high-quota model
            
            # Special models
            "gemini-flash-latest": "gemini-3.1-flash-lite", # Use high-quota
            "gemini-pro-latest": "gemini-3.1-flash-lite",
            "gemma-4": "gemma-4-26b-a4b-it",               # Use exact model
            "gemma-4-26b": "gemma-4-26b-a4b-it",
            "gemma-4-26b-a4b-it": "gemma-4-26b-a4b-it",    # Keep as-is (1500 RPD)
            "gemma-4-31b-it": "gemma-4-31b-it",            # Keep as-is (1500 RPD)
            
            # Default strategy: Start with highest quota model
            "default": "gemini-3.1-flash-lite"  # 500 RPD/key = 2000 total
        }

        # AGENT LABEL MAPPING (Tier-based strategy)
        self.label_mapping = {
            # Giữ cho các task suy luận siêu phức tạp (RAG, Trading, Code)
            "tier-1": "gemini-2.5-flash",        
            
        # Thư ký nội dung (Đã sửa lỗi chết model Gemma trên OpenRouter)
        "tier-2": "groq/llama-3.3-70b-versatile",
        
        # [TEST] Trực tiếp dùng Gemini qua OpenRouter để xem có bị 400 không
        "test": "openrouter/google/gemini-2.5-flash",
            
            # Khẩn cấp / siêu tốc (Groq Llama-3 8b)
            "fast": "groq/llama-3.1-8b-instant",
            
            # Routing thông minh / Reasoning cơ bản (Groq Llama-3 70b)
            "tier-3": "groq/llama-3.3-70b-versatile",
            
            "manual": "manual-block"             # Special flag to block API
        }
        
        # Model rotation pool (for load balancing)
        self.model_rotation_pool = (
            self.high_quota_models +  # Priority #1
            self.standard_models      # Priority #2
        )
        self.current_model_index = 0
        
        # Standardize mapping to use the target API strings
        self.default_model = self.model_mapping["default"]
        
    def map_model(self, requested_model: str) -> str:
        """Map requested model name or label to actual Google API model string."""
        if not requested_model:
            return self.default_model

        # Handle label format (e.g., "label:tier-1")
        if requested_model.startswith("label:"):
            label = requested_model.replace("label:", "").strip().lower()
            return self.label_mapping.get(label, self.default_model)

        # Handle standard model name mapping
        key = requested_model.lower().replace(" ", "-")
        return self.model_mapping.get(key, self.default_model)

    def get_gemini_stream_url(self, model_name: str, api_key: str) -> str:
        """
        Build the Gemini streaming endpoint URL for a specific (model, key) pair.

        Args:
            model_name: The exact target model name (already mapped).
            api_key: The API key to embed in the URL.

        Returns:
            str: Full URL with API key query param.
        """
        model_path = model_name
        if not model_path.startswith("models/"):
            model_path = f"models/{model_path}"

        return (
            f"{self.gemini_base_url}/{model_path}:"
            f"streamGenerateContent?key={api_key}"
        )


# Global settings instance (initialized once)
_settings: Settings | None = None


def get_settings() -> Settings:
    """
    Get the global settings instance.
    
    Returns:
        Settings: The application settings instance.
    
    Raises:
        ValueError: If GEMINI_API_KEY is not configured.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings