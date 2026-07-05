"""
Local Proxy Server - Main Entry Point

This server acts as a bridge between Cline (VS Code) and Gemini Free API,
converting OpenAI-compatible requests to Gemini format and back.

Usage:
    uv run main.py
"""
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from projects.local_proxy_server.core.config import get_settings
from projects.local_proxy_server.core.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events.
    """
    # Startup: Validate configuration
    try:
        settings = get_settings()
        print(f"[+] Configuration loaded successfully")
        print(f"[+] Default Gemini Model: {settings.default_model}")
        print(f"[+] Total API Keys: {len(settings.gemini_api_keys)}")
    except ValueError as e:
        print(f"[-] Configuration error: {e}", file=sys.stderr)
        print("Please ensure GEMINI_API_KEY is set in your .env file.", file=sys.stderr)
        sys.exit(1)
    
    yield
    
    # Shutdown: Cleanup if needed
    print("Shutting down Local Proxy Server...")


# Create FastAPI application
app = FastAPI(
    title="Local Proxy Server for Gemini API",
    description="OpenAI-compatible proxy server for Google Gemini API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Include API router
app.include_router(router)


def main() -> None:
    """
    Main entry point for the Local Proxy Server.
    
    Starts the Uvicorn server with configuration from environment variables.
    """
    try:
        settings = get_settings()
        
        print("\n" + "=" * 60)
        print("LOCAL PROXY SERVER FOR GEMINI API")
        print("=" * 60)
        print(f"Server running at: http://{settings.host}:{settings.port}")
        print(f"API Documentation: http://{settings.host}:{settings.port}/docs")
        print(f"Chat Completions: http://{settings.host}:{settings.port}/v1/chat/completions")
        print("=" * 60 + "\n")
        
        # Run Uvicorn server
        uvicorn.run(
            "projects.local_proxy_server.main:app",
            host=settings.host,
            port=settings.port,
            reload=False,  # Disable reload for production
            log_level="info",
            access_log=True,
        )
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()