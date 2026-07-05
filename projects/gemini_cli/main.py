"""
Main entry point for Gemini CLI.

Accepts prompts from command line and streams responses from Gemini API.
"""

import asyncio
import argparse
import sys
from pathlib import Path

from core.config import Config, ConfigError
from core.client import (
    GeminiClient,
    GeminiError,
    QuotaExceededError,
    NetworkError,
    InvalidResponseError,
)


async def stream_response(
    config: Config,
    prompt: str,
    model: str,
) -> None:
    """
    Stream Gemini API response to stdout.
    
    Args:
        config: Configuration object.
        prompt: User's prompt text.
        model: Model name to use.
    """
    try:
        async with GeminiClient(config) as client:
            async for chunk in client.stream_chat(prompt, model):
                # Print chunk immediately as it arrives
                print(chunk, end="", flush=True)
            
            # Print newline at the end
            print()
    
    except QuotaExceededError as e:
        print(f"\n❌ Quota Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except NetworkError as e:
        print(f"\n❌ Network Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except InvalidResponseError as e:
        print(f"\n❌ Invalid Response: {e}", file=sys.stderr)
        sys.exit(1)
    
    except GeminiError as e:
        print(f"\n❌ Gemini API Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user.", file=sys.stderr)
        sys.exit(130)  # Standard exit code for SIGINT
    
    except Exception as e:
        print(f"\n❌ Unexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """
    Main entry point - parses arguments and runs async stream.
    """
    parser = argparse.ArgumentParser(
        description="Ultra-lightweight Custom CLI for Google Gemini API (Free Tier)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with prompt
  gemini "Explain quantum computing in simple terms"
  
  # Use specific model
  gemini "Write a haiku about coding" --model gemini-1.5-pro
  
  # Read prompt from file
  gemini "$(cat prompt.txt)"
  
  # Pipe input
  echo "What is Python?" | gemini
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Prompt text to send to Gemini API. If not provided, reads from stdin.",
    )
    
    parser.add_argument(
        "--model",
        "-m",
        default=None,
        help=(
            "Model name to use (default: gemini-1.5-flash). "
            "Available: gemini-1.5-flash, gemini-1.5-pro, gemini-2.5-flash"
        ),
    )
    
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="gemini-cli 1.0.0",
    )
    
    args = parser.parse_args()
    
    # Read prompt from stdin if not provided
    if args.prompt is None:
        if not sys.stdin.isatty():
            # Read from pipe or redirect
            args.prompt = sys.stdin.read().strip()
        else:
            # Interactive mode - read line
            try:
                args.prompt = input("Enter your prompt: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nNo prompt provided. Exiting.", file=sys.stderr)
                sys.exit(1)
    
    # Validate prompt
    if not args.prompt:
        print("❌ Error: Prompt cannot be empty.", file=sys.stderr)
        sys.exit(1)
    
    # Load configuration
    try:
        config = Config()
    except ConfigError as e:
        print(f"❌ Configuration Error: {e}", file=sys.stderr)
        print("\n💡 Setup instructions:", file=sys.stderr)
        print("1. Get API key from: https://aistudio.google.com/app/apikey", file=sys.stderr)
        print("2. Add to root .env file:", file=sys.stderr)
        print("   GCLI_API_KEY=your_api_key_here", file=sys.stderr)
        sys.exit(1)
    
    # Run async stream
    asyncio.run(stream_response(config, args.prompt, args.model))


if __name__ == "__main__":
    main()