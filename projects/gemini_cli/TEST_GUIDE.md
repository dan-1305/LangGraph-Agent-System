# 🧪 Unit Testing Guide for Gemini CLI

This guide explains how to write and run unit tests for the Gemini CLI project.

## 📚 Overview

The test suite uses:
- **pytest**: Modern Python testing framework
- **pytest-asyncio**: Async support for testing async functions
- **pytest-mock**: Mocking utilities

## 🚀 Setup

### Install Test Dependencies

```bash
cd projects/gemini_cli
uv sync --extra test
```

## 📁 Test Structure

```
tests/
├── __init__.py           # Package init
├── test_config.py        # Configuration tests
└── test_client.py        # Client tests (with mocking)
```

## 🧪 Running Tests

### Run All Tests

```bash
uv run pytest
```

### Run with Verbose Output

```bash
uv run pytest -v
```

### Run with Coverage

```bash
uv run pytest --cov=core --cov-report=html
```

View coverage report:
```bash
# On Windows
start htmlcov\index.html

# On Linux/Mac
open htmlcov/index.html
```

### Run Specific Test File

```bash
uv run pytest tests/test_config.py -v
```

### Run Specific Test Function

```bash
uv run pytest tests/test_config.py::test_config_loads_from_env -v
```

## 📝 Writing Tests

### Example: Testing Config Module

```python
import pytest
from core.config import Config, ConfigError
from pathlib import Path
import os


def test_config_loads_from_env():
    """Test that Config loads API key from environment."""
    # Set environment variable
    os.environ["GCLI_API_KEY"] = "test_key_123"
    
    # Load config
    config = Config()
    
    # Assert API key is loaded
    assert config.api_key == "test_key_123"
    assert config.base_url == "https://generativelanguage.googleapis.com/v1beta"
    
    # Cleanup
    del os.environ["GCLI_API_KEY"]


def test_config_raises_error_without_api_key():
    """Test that Config raises error when API key is missing."""
    # Ensure API key is not set
    if "GCLI_API_KEY" in os.environ:
        del os.environ["GCLI_API_KEY"]
    
    # Assert ConfigError is raised
    with pytest.raises(ConfigError, match="Missing required environment variables"):
        Config()


def test_config_custom_model():
    """Test that Config loads custom model from environment."""
    os.environ["GCLI_API_KEY"] = "test_key"
    os.environ["GCLI_MODEL"] = "gemini-1.5-pro"
    
    config = Config()
    
    assert config.model == "gemini-1.5-pro"
    
    del os.environ["GCLI_API_KEY"]
    del os.environ["GCLI_MODEL"]


def test_config_custom_timeout():
    """Test that Config loads custom timeout from environment."""
    os.environ["GCLI_API_KEY"] = "test_key"
    os.environ["GCLI_TIMEOUT"] = "120"
    
    config = Config()
    
    assert config.timeout == 120
    
    del os.environ["GCLI_API_KEY"]
    del os.environ["GCLI_TIMEOUT"]


def test_config_headers_hide_api_key():
    """Test that API key is exposed in headers but hidden in repr."""
    os.environ["GCLI_API_KEY"] = "secret_key"
    
    config = Config()
    headers = config.get_headers()
    
    # Headers should contain API key
    assert headers["x-goog-api-key"] == "secret_key"
    
    # Repr should hide it
    repr_str = repr(config)
    assert "secret_key" not in repr_str
    assert "***" in repr_str
    
    del os.environ["GCLI_API_KEY"]
```

### Example: Testing Client Module (with Mocking)

```python
import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, Response
from core.config import Config
from core.client import (
    GeminiClient,
    GeminiError,
    QuotaExceededError,
    NetworkError,
    InvalidResponseError,
)


@pytest.mark.asyncio
async def test_client_context_manager():
    """Test that GeminiClient works as async context manager."""
    os.environ["GCLI_API_KEY"] = "test_key"
    config = Config()
    
    async with GeminiClient(config) as client:
        assert client._client is not None
        assert isinstance(client._client, AsyncClient)
    
    del os.environ["GCLI_API_KEY"]


@pytest.mark.asyncio
async def test_stream_chat_success():
    """Test successful streaming chat response."""
    os.environ["GCLI_API_KEY"] = "test_key"
    config = Config()
    
    # Mock streaming response
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    
    # Simulate streaming lines
    mock_lines = [
        json.dumps({
            "candidates": [{
                "content": {
                    "parts": [{"text": "Hello"}]
                }
            }]
        }),
        json.dumps({
            "candidates": [{
                "content": {
                    "parts": [{"text": " world!"}]
                }
            }]
        }),
    ]
    
    async def mock_aiter_lines():
        for line in mock_lines:
            yield line
    
    mock_response.aiter_lines = mock_aiter_lines
    
    mock_stream_context = MagicMock()
    mock_stream_context.__aenter__ = AsyncMock(return_value=mock_response)
    mock_stream_context.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(GeminiClient, '_client', create=True):
        client = GeminiClient(config)
        client._client = MagicMock()
        client._client.stream = MagicMock(return_value=mock_stream_context)
        
        chunks = []
        async for chunk in client.stream_chat("Hello"):
            chunks.append(chunk)
        
        assert chunks == ["Hello", " world!"]
    
    del os.environ["GCLI_API_KEY"]


@pytest.mark.asyncio
async def test_stream_chat_quota_exceeded():
    """Test that QuotaExceededError is raised on 429 status."""
    os.environ["GCLI_API_KEY"] = "test_key"
    config = Config()
    
    from httpx import HTTPStatusError, Request, Response
    
    # Mock 429 response
    request = Request("POST", "https://api.example.com")
    response = Response(429, request=request)
    error = HTTPStatusError("Quota exceeded", request=request, response=response)
    
    mock_stream_context = MagicMock()
    mock_stream_context.__aenter__ = AsyncMock(side_effect=error)
    mock_stream_context.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(GeminiClient, '_client', create=True):
        client = GeminiClient(config)
        client._client = MagicMock()
        client._client.stream = MagicMock(return_value=mock_stream_context)
        
        with pytest.raises(QuotaExceededError, match="API quota exceeded"):
            async for _ in client.stream_chat("Hello"):
                pass
    
    del os.environ["GCLI_API_KEY"]


@pytest.mark.asyncio
async def test_stream_chat_invalid_api_key():
    """Test that GeminiError is raised on 401 status."""
    os.environ["GCLI_API_KEY"] = "test_key"
    config = Config()
    
    from httpx import HTTPStatusError, Request, Response
    
    # Mock 401 response
    request = Request("POST", "https://api.example.com")
    response = Response(401, request=request)
    error = HTTPStatusError("Unauthorized", request=request, response=response)
    
    mock_stream_context = MagicMock()
    mock_stream_context.__aenter__ = AsyncMock(side_effect=error)
    mock_stream_context.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(GeminiClient, '_client', create=True):
        client = GeminiClient(config)
        client._client = MagicMock()
        client._client.stream = MagicMock(return_value=mock_stream_context)
        
        with pytest.raises(GeminiError, match="Invalid API key"):
            async for _ in client.stream_chat("Hello"):
                pass
    
    del os.environ["GCLI_API_KEY"]


@pytest.mark.asyncio
async def test_chat_non_streaming():
    """Test non-streaming chat method."""
    os.environ["GCLI_API_KEY"] = "test_key"
    config = Config()
    
    # Mock streaming response
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    
    mock_lines = [
        json.dumps({
            "candidates": [{
                "content": {
                    "parts": [{"text": "Hello "}]
                }
            }]
        }),
        json.dumps({
            "candidates": [{
                "content": {
                    "parts": [{"text": "world!"}]
                }
            }]
        }),
    ]
    
    async def mock_aiter_lines():
        for line in mock_lines:
            yield line
    
    mock_response.aiter_lines = mock_aiter_lines
    
    mock_stream_context = MagicMock()
    mock_stream_context.__aenter__ = AsyncMock(return_value=mock_response)
    mock_stream_context.__aexit__ = AsyncMock(return_value=None)
    
    with patch.object(GeminiClient, '_client', create=True):
        client = GeminiClient(config)
        client._client = MagicMock()
        client._client.stream = MagicMock(return_value=mock_stream_context)
        
        result = await client.chat("Hello")
        
        assert result == "Hello world!"
    
    del os.environ["GCLI_API_KEY"]
```

## 🎯 Best Practices

### 1. Use Async Decorator

Always use `@pytest.mark.asyncio` for async test functions:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result is not None
```

### 2. Mock External Dependencies

Never make real API calls in tests. Use mocking:

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_with_mock():
    with patch('core.client.httpx.AsyncClient') as mock_client:
        mock_instance = MagicMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_client.return_value = mock_instance
        
        # Test code here
```

### 3. Test Error Cases

Test both success and failure scenarios:

```python
def test_success_case():
    # Test normal operation
    pass

def test_error_case():
    # Test error handling
    with pytest.raises(ExpectedException):
        # Code that should raise exception
        pass
```

### 4. Use Descriptive Test Names

Test names should describe what they test:

```python
# Good
def test_config_loads_api_key_from_environment():
    pass

# Bad
def test_config():
    pass
```

### 5. Clean Up Environment

Always clean up environment variables after tests:

```python
def test_with_env():
    os.environ["TEST_VAR"] = "test_value"
    
    # Test code
    
    del os.environ["TEST_VAR"]
```

## 🔍 Debugging Tests

### Run with pdb (Python Debugger)

```bash
uv run pytest --pdb
```

### Print Output

```bash
uv run pytest -s
```

### Stop at First Failure

```bash
uv run pytest -x
```

### Show Local Variables on Failure

```bash
uv run pytest -l
```

## 📊 Coverage Goals

Aim for:
- **Line Coverage**: > 80%
- **Branch Coverage**: > 70%
- **Critical Paths**: 100% (config loading, API calls)

## 🚦 CI/CD Integration

Tests should run automatically on:
- Every pull request
- Every merge to main
- Nightly builds

## 📚 Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Mocking in Python](https://docs.python.org/3/library/unittest.mock.html)