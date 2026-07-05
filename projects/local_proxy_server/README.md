# Local Proxy Server for Gemini API

A lightweight, OpenAI-compatible proxy server that acts as a bridge between Cline (VS Code) and Google Gemini Free API. This server converts OpenAI-format requests to Gemini format and transforms streaming responses back to OpenAI-compatible Server-Sent Events (SSE).

## 🚀 Features

- **OpenAI-Compatible API**: Implements the `/v1/chat/completions` endpoint compatible with OpenAI clients
- **Real-time Streaming**: Supports streaming responses with low latency
- **Payload Conversion**: Automatically converts OpenAI messages to Gemini format
- **SSE Transformation**: Transforms Gemini streaming responses to OpenAI SSE format
- **FastAPI & Uvicorn**: Built with modern async Python frameworks
- **Type Hints**: Fully typed code for better IDE support
- **Unit Tests**: Comprehensive test suite included

## 📋 Prerequisites

- Python 3.10 or higher
- `uv` package manager (for dependency management)
- A Google Gemini API key ([Get one here](https://ai.google.dev/))

## 🔧 Installation

1. **Navigate to the project directory**:
   ```bash
   cd projects/local_proxy_server
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Configure your API key**:
   ```bash
   # Copy the example .env file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

## 🎯 Usage

### Starting the Server

Run the server using uv:
```bash
uv run main.py
```

The server will start on `http://0.0.0.0:8000` by default.

### Using with Cline (VS Code)

Configure Cline to use your local proxy server:

1. Open Cline settings in VS Code
2. Set the API Provider to **OpenAI Compatible**
3. Set the API base URL to: `http://localhost:8000/v1`
4. Set your API key to any placeholder (e.g., `local-proxy-key`). The server will automatically use the real keys from your `.env` file.
5. Select the model: `gemini-2.0-flash-exp`

## 🔄 API Key Rotation & Failover

The server supports automatic Fail-on-Demand key rotation. This is extremely useful for the Gemini Free Tier to avoid interrupted sessions due to Rate Limits.

### How to configure multiple keys:
In your `.env` file, use the `GEMINI_API_KEYS` variable with a comma-separated list:

```env
GEMINI_API_KEYS=key1,key2,key3
```

### How it works:
1. The server starts using the first key.
2. If Gemini returns a **429 (Rate Limit)** or **403 (Quota Exceeded)** error, the proxy automatically rotates to the next key.
3. The request is **retried immediately** with the new key.
4. This happens transparently, so Cline never experiences a disconnection until all keys are exhausted.

### API Endpoints

#### `POST /v1/chat/completions`
OpenAI-compatible chat completions endpoint with streaming support.

**Request Example**:
```json
{
  "messages": [
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}
```

**Response**: Server-Sent Events (SSE) stream in OpenAI format.

#### `GET /health`
Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "local-proxy-server"
}
```

#### `GET /`
Root endpoint with service information.

**Response**:
```json
{
  "service": "Local Proxy Server for Gemini API",
  "version": "1.0.0",
  "model": "gemini-2.0-flash-exp",
  "endpoints": {
    "chat_completions": "/v1/chat/completions",
    "health": "/health"
  }
}
```

## 🧪 Testing

Run the unit tests:

```bash
# Make sure the server is running first
uv run main.py

# In another terminal, run tests
uv run tests/test_proxy_server.py
```

The test suite includes:
- Adapter function tests (payload conversion)
- Health check endpoint test
- Root endpoint test
- Streaming chat completions test

## 📁 Project Structure

```
local_proxy_server/
├── main.py                 # Application entry point
├── pyproject.toml          # Project configuration and dependencies
├── .env.example            # Environment variables template
├── README.md               # This file
├── core/
│   ├── __init__.py         # Core module initialization
│   ├── config.py           # Configuration and environment management
│   ├── adapter.py          # Payload conversion utilities
│   └── router.py           # FastAPI routes and endpoints
└── tests/
    ├── __init__.py         # Tests module initialization
    └── test_proxy_server.py # Unit tests
```

## 🔍 How It Works

### Architecture

1. **Request Flow**:
   - Cline sends OpenAI-format request to `/v1/chat/completions`
   - Server validates and converts payload to Gemini format
   - Server calls Gemini API with streaming enabled
   - Response streams back in real-time

2. **Response Flow**:
   - Gemini API returns streaming response chunks
   - Each chunk is parsed and converted to OpenAI SSE format
   - Server forwards transformed chunks to Cline
   - Process continues until stream completes

### Payload Conversion

**OpenAI Format** → **Gemini Format**:
```python
# OpenAI
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}

# Gemini
{
  "contents": [
    {"role": "user", "parts": [{"text": "Hello"}]}
  ]
}
```

### Streaming Transformation

**Gemini Chunk** → **OpenAI SSE**:
```python
# Gemini text
"Hello, World!"

# OpenAI SSE
"data: {\"choices\": [{\"delta\": {\"content\": \"Hello, World!\"}}]}\n\n"
```

## ⚙️ Configuration

Environment variables can be set in the `.env` file:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | Yes | - | Your Google Gemini API key |
| `HOST` | No | `0.0.0.0` | Server host address |
| `PORT` | No | `8000` | Server port number |

## 🛠️ Development

### Project Dependencies

The project uses modern Python packages:
- **FastAPI** (0.115.0+): Web framework for building APIs
- **Uvicorn** (0.32.0+): ASGI server for running FastAPI
- **HTTPX** (0.27.0+): Async HTTP client
- **python-dotenv** (1.0.0+): Environment variable management

### Code Standards

- Python 3.10+ with type hints
- PEP 8 compliant
- Async/await throughout
- Comprehensive docstrings

## 📝 License

This project is part of the LangGraph Agent System.

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows existing style
- Tests are added for new features
- Documentation is updated

## 📞 Support

For issues or questions:
1. Check the test suite for usage examples
2. Review the code documentation
3. Verify your API key is valid and active

---

**Built with ❤️ using FastAPI, Uvicorn, and HTTPX**