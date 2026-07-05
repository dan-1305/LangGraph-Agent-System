import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory for the Factory
BASE_DIR = Path(__file__).resolve().parent
WORKSPACE_ROOT = BASE_DIR.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

class Config:
    """Central configuration for AI Software Factory."""
    WORKSPACE_ROOT = WORKSPACE_ROOT
    
    # Primary API (GCLI - Hệ thống xoay Key siêu tiết kiệm qua Local Proxy)
    GCLI_API_KEY = os.getenv("GCLI_API_KEY")
    GCLI_BASE_URL = os.getenv("GCLI_BASE_URL")
            
    # Reports Directory - giờ sẽ lưu ở root/reports hoặc trong từng project
    REPORTS_DIR = WORKSPACE_ROOT / "reports"
    LOG_DIR = WORKSPACE_ROOT / "logs"

    @classmethod
    def initialize(cls):
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_llm_credentials() -> list:
        """
        Returns a list of available API credentials, prioritized.
        """
        credentials = []
        # API 1: Local Proxy Server (Hệ thống xoay Key Free Tier siêu tiết kiệm)
        if Config.GCLI_BASE_URL and Config.GCLI_API_KEY:
            credentials.append({
                "base_url": Config.GCLI_BASE_URL,
                "api_key": Config.GCLI_API_KEY,
            })
            
        # API 2: Fallback qua OpenAI nếu có cấu hình
        if os.getenv("OPENAI_API_KEY"):
            credentials.append({
                "api_key": os.getenv("OPENAI_API_KEY"),
            })
            
        return credentials

def create_fallback_chain(model_list: list, temperature: float = 0.2, max_tokens: int = 4096):
    """
    Creates a chain of LLMs with fallbacks. Bọc thêm Retry để chống Rate Limit 429/403.
    """
    from langchain_openai import ChatOpenAI
    
    # Luôn chèn thêm model Flash vào cuối danh sách Fallback để lót ổ nếu các model xịn (Pro) hết quota
    safe_models = model_list.copy()
    if "gemini-3.1-flash-lite" not in safe_models:
        safe_models.append("gemini-3.1-flash-lite")

    credentials = Config.get_llm_credentials()
    if not credentials:
        raise ValueError("No API credentials found in config. Please check your .env file.")

    llm_chain = []
    for model_name in safe_models:
        for cred in credentials:
            llm_chain.append(
                ChatOpenAI(
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    max_retries=2, # Tự động retry 2 lần ở tầng OpenAI Client
                    **cred
                )
            )

    if not llm_chain:
        raise ValueError("Could not create any LLM instances. Check model names and credentials.")

    # Tạo Fallback Tree: LLM[0] -> LLM[1] -> LLM[2]
    # Khi LLM[0] văng lỗi (429/403), Langchain sẽ TỰ ĐỘNG gọi LLM[1]
    fallback_chain = llm_chain[0]
    if len(llm_chain) > 1:
        fallback_chain = fallback_chain.with_fallbacks(llm_chain[1:])
        
    return fallback_chain

Config.initialize()
