# Gemini CLI 🚀

Ultra-lightweight Custom CLI for Google Gemini API (Free Tier) built with Python.

## ✨ Features

- **🎯 Ultra-Lightweight**: Minimal dependencies (`httpx`, `python-dotenv`)
- **🚀 Async Performance**: Built with `httpx` for non-blocking I/O
- **🌊 Streaming Support**: Real-time response streaming - text appears as it's generated
- **🔒 Secure**: API keys loaded from `.env` only - NEVER hardcoded
- **🧪 Clean Code**: PEP-8 compliant with full type hinting
- **📦 UV Ready**: Managed with `uv` for fast dependency resolution

## 📋 Requirements

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key (Free Tier)

## 🚀 Quick Start

### 1. Get API Key

Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and create your free API key.

### 2. Configure Environment

Add your API key to the root `.env` file:

```bash
# In root .env file (LangGraph_Agent_System/.env)
GCLI_API_KEY=your_actual_api_key_here
```

Or create a local `.env` in the project directory:

```bash
cd projects/gemini_cli
cp .env.example .env
# Edit .env and add your API key
```

### 3. Install Dependencies

```bash
cd projects/gemini_cli
uv sync
```

### 4. Run CLI

```bash
uv run python main.py "Explain quantum computing in simple terms"
```

Or install as a CLI tool:

```bash
uv pip install -e .
gemini "Write a haiku about coding"
```

## 💻 Usage Examples

### Basic Usage

```bash
# Direct prompt
uv run python main.py "What is machine learning?"

# Using the installed CLI
gemini "Explain async/await in Python"
```

### Model Selection

```bash
# Use default model (gemini-1.5-flash)
uv run python main.py "Hello, world!"

# Use gemini-1.5-pro for complex tasks
uv run python main.py "Analyze this code" --model gemini-1.5-pro

# Use gemini-2.5-flash (latest)
uv run python main.py "Write a poem" -m gemini-2.5-flash
```

### Pipe Input

```bash
# Pipe from echo
echo "What is Python?" | uv run python main.py

# Pipe from file
cat prompt.txt | uv run python main.py

# Chain with other commands
ls -la | uv run python main.py "Analyze this file listing"
```

### Interactive Mode

```bash
# Run without prompt to enter interactive mode
uv run python main.py
# Then type your prompt when prompted
```

## 📁 Project Structure

```
gemini_cli/
├── main.py              # Entry point with argparse
├── core/
│   ├── __init__.py      # Package init
│   ├── config.py        # API Guard - secure config management
│   └── client.py        # Async HTTPX client with streaming
├── tests/
│   └── test_client.py   # Unit tests
├── pyproject.toml       # UV project configuration
├── .env.example         # Environment template
└── README.md           # This file
```

## 🧪 Running Tests

### Install Test Dependencies

```bash
uv sync --extra test
```

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=core --cov-report=html

# Run specific test file
uv run pytest tests/test_client.py -v
```

## 🔧 Configuration Options

Environment variables (optional):

```bash
# API Key (required)
GCLI_API_KEY=your_key_here

# Custom Base URL (optional)
GCLI_BASE_URL=https://generativelanguage.googleapis.com/v1beta

# Model Name (optional, default: gemini-1.5-flash)
GCLI_MODEL=gemini-1.5-flash

# Request Timeout in seconds (optional, default: 60)
GCLI_TIMEOUT=60
```

## 📚 API Models

Available models:

- `gemini-1.5-flash` - Fast, efficient, good for quick tasks
- `gemini-1.5-pro` - More capable, better for complex reasoning
- `gemini-2.5-flash` - Latest version (if available)

## 🛡️ Security

✅ **NO HARDCODED API KEYS** - All credentials loaded from `.env`

✅ **NO REQUESTS IMPORT** - Uses `httpx` for async I/O

✅ **SAFE CONFIGURATION** - API Guard validates environment variables

✅ **ERROR HANDLING** - Comprehensive exception handling for quotas, network errors

## 🐛 Error Handling

The CLI provides clear error messages:

- **Quota Exceeded**: "API quota exceeded. Please try again later."
- **Invalid Key**: "Invalid API key. Please check your GCLI_API_KEY."
- **Network Error**: "Failed to connect to API. Check your internet connection."
- **Timeout**: "Request timed out after X seconds."

## 📝 License

Part of LangGraph Agent System project.

## 🤝 Contributing

Follow PEP-8 guidelines and add type hints for all new code.

## 🔗 Links

- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [UV Package Manager](https://github.com/astral-sh/uv)