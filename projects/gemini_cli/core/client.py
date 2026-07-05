"""
Async HTTPX client for Gemini API communication.

Handles streaming responses and comprehensive error management.
"""

import asyncio
import json
from typing import AsyncGenerator, Optional
import importlib

httpx = importlib.import_module("httpx")
AsyncClient = httpx.AsyncClient
HTTPStatusError = httpx.HTTPStatusError
TimeoutException = httpx.TimeoutException
ConnectError = httpx.ConnectError
StreamConsumed = httpx.StreamConsumed
HttpxNetworkError = httpx.NetworkError

from core.config import Config


class GeminiError(Exception):
    """Base exception for Gemini API errors."""
    pass


class QuotaExceededError(GeminiError):
    """Raised when API quota is exhausted."""
    pass


class NetworkError(GeminiError):
    """Raised when network issues occur."""
    pass


class InvalidResponseError(GeminiError):
    """Raised when API returns invalid response."""
    pass


class GeminiClient:
    """
    Async HTTPX client for Gemini API with streaming support.
    
    Features:
    - Async HTTPX for non-blocking I/O
    - Streaming response support
    - Comprehensive error handling
    - Timeout management
    """
    
    def __init__(self, config: Config) -> None:
        """
        Initialize Gemini client.
        
        Args:
            config: Configuration object with API credentials.
        """
        self.config = config
        self._client: Optional[AsyncClient] = None
    
    async def __aenter__(self) -> "GeminiClient":
        """Async context manager entry."""
        self._client = AsyncClient(
            timeout=self.config.timeout,
            base_url=self.config.base_url,
            headers=self.config.get_headers(),
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
    
    async def stream_chat(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Send a chat prompt and stream the response.
        
        Args:
            prompt: User's prompt text.
            model: Model name (uses config default if None).
        
        Yields:
            Chunks of the response text as they arrive.
        
        Raises:
            QuotaExceededError: When API quota is exhausted.
            NetworkError: When network issues occur.
            InvalidResponseError: When API returns malformed response.
            GeminiError: For other API-related errors.
        """
        if not self._client:
            raise GeminiError("Client not initialized. Use async with statement.")
        
        model_name = model or self.config.model
        
        # Construct request payload
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}],
                    "role": "user",
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            },
        }
        
        # API endpoint for streaming
        endpoint = f"models/{model_name}:streamGenerateContent"
        
        try:
            async with self._client.stream(
                "POST",
                endpoint,
                json=payload,
            ) as response:
                # Raise for HTTP errors (4xx, 5xx)
                response.raise_for_status()
                
                # Parse streaming response
                async for line in response.aiter_lines():
                    if not line.strip():
                        continue
                    
                    try:
                        # Each line is a JSON object
                        chunk = json.loads(line)
                        
                        # Extract text from response
                        if "candidates" in chunk and chunk["candidates"]:
                            candidate = chunk["candidates"][0]
                            if "content" in candidate and "parts" in candidate["content"]:
                                for part in candidate["content"]["parts"]:
                                    if "text" in part:
                                        yield part["text"]
                    
                    except json.JSONDecodeError as e:
                        # Skip invalid JSON lines
                        continue
                    
                    except KeyError as e:
                        raise InvalidResponseError(
                            f"Malformed response from API: missing key {e}"
                        ) from e
                    
        except HTTPStatusError as e:
            status_code = e.response.status_code
            
            if status_code == 429:
                raise QuotaExceededError(
                    "API quota exceeded. Please try again later."
                ) from e
            elif status_code == 401:
                raise GeminiError(
                    "Invalid API key. Please check your GCLI_API_KEY."
                ) from e
            elif status_code == 403:
                raise GeminiError(
                    "Access forbidden. Check API permissions."
                ) from e
            else:
                raise GeminiError(
                    f"HTTP error {status_code}: {e.response.text}"
                ) from e
        
        except TimeoutException as e:
            raise NetworkError(
                f"Request timed out after {self.config.timeout} seconds."
            ) from e
        
        except ConnectError as e:
            raise NetworkError(
                "Failed to connect to API. Check your internet connection."
            ) from e
        
        except NetworkError as e:
            raise NetworkError(
                f"Network error occurred: {str(e)}"
            ) from e
        
        except StreamConsumed as e:
            raise InvalidResponseError(
                "Response stream was already consumed."
            ) from e
        
        except Exception as e:
            raise GeminiError(
                f"Unexpected error: {type(e).__name__}: {str(e)}"
            ) from e
    
    async def chat(
        self,
        prompt: str,
        model: Optional[str] = None,
    ) -> str:
        """
        Send a chat prompt and return complete response (non-streaming).
        
        Args:
            prompt: User's prompt text.
            model: Model name (uses config default if None).
        
        Returns:
            Complete response text.
        
        Raises:
            Same exceptions as stream_chat().
        """
        response_chunks = []
        
        async for chunk in self.stream_chat(prompt, model):
            response_chunks.append(chunk)
        
        return "".join(response_chunks)