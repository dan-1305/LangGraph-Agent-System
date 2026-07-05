"""
Unit Tests for Local Proxy Server

This module contains tests for the proxy server's adapter functions and endpoint.
"""
import asyncio
import json
import os

import httpx


# Test server configuration
SERVER_URL = "http://localhost:8000"
API_KEY = os.getenv("GEMINI_API_KEY", "")


def test_adapter_to_gemini_payload():
    """Test conversion from OpenAI to Gemini payload format."""
    from core.adapter import to_gemini_payload
    
    # Test input: OpenAI format
    openai_payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, how are you?"},
            {"role": "assistant", "content": "I'm doing well, thanks!"},
            {"role": "user", "content": "What can you do?"}
        ],
        "temperature": 0.8,
        "max_tokens": 1000
    }
    
    # Convert to Gemini format
    gemini_payload = to_gemini_payload(openai_payload)
    
    # Verify structure
    assert "contents" in gemini_payload
    assert "generationConfig" in gemini_payload
    assert len(gemini_payload["contents"]) == 4
    
    # Verify role mapping
    assert gemini_payload["contents"][0]["role"] == "user"  # system -> user
    assert "System:" in gemini_payload["contents"][0]["parts"][0]["text"]
    assert gemini_payload["contents"][1]["role"] == "user"
    assert gemini_payload["contents"][2]["role"] == "model"  # assistant -> model
    assert gemini_payload["contents"][3]["role"] == "user"
    
    # Verify generation config
    assert gemini_payload["generationConfig"]["temperature"] == 0.8
    assert gemini_payload["generationConfig"]["maxOutputTokens"] == 1000
    
    print("[+] test_adapter_to_gemini_payload passed")


def test_adapter_to_openai_stream():
    """Test conversion from Gemini chunk to OpenAI SSE format."""
    from core.adapter import to_openai_stream
    
    # Test input: Gemini text chunk
    gemini_chunk = "Hello, this is a response from Gemini!"
    
    # Convert to OpenAI format
    openai_sse = to_openai_stream(gemini_chunk)
    
    # Verify SSE format
    assert openai_sse.startswith("data: {")
    assert openai_sse.endswith("}\n\n")
    
    # Parse and verify JSON structure
    json_start = openai_sse.find("{")
    json_end = openai_sse.rfind("}") + 1
    json_str = openai_sse[json_start:json_end]
    openai_data = json.loads(json_str)
    
    assert "choices" in openai_data
    assert len(openai_data["choices"]) == 1
    assert "delta" in openai_data["choices"][0]
    assert "content" in openai_data["choices"][0]["delta"]
    assert openai_data["choices"][0]["delta"]["content"] == gemini_chunk
    assert openai_data["object"] == "chat.completion.chunk"
    
    print("[+] test_adapter_to_openai_stream passed")


def test_api_key_rotation_logic():
    """Test the configuration loading and rotation mechanism of API Keys."""
    from core.config import get_settings
    
    # Get configuration settings
    settings = get_settings()
    
    # Ensure there is at least one key loaded
    assert len(settings.gemini_api_keys) >= 1
    
    # Check rotation logic
    initial_key = settings.get_current_key()
    initial_index = settings.current_key_index
    
    # If there are multiple keys, rotate and test sequence
    if len(settings.gemini_api_keys) > 1:
        next_key = settings.rotate_key()
        assert next_key != initial_key
        assert settings.current_key_index == (initial_index + 1) % len(settings.gemini_api_keys)
        
        # Reset back to initial index for consistent state in other tests
        while settings.current_key_index != initial_index:
            settings.rotate_key()
            
        assert settings.get_current_key() == initial_key
    else:
        # If single key, rotation yields same key and keeps index at 0
        rotated_key = settings.rotate_key()
        assert rotated_key == initial_key
        assert settings.current_key_index == 0
        
    print(f"[+] test_api_key_rotation_logic passed (Total loaded keys: {len(settings.gemini_api_keys)})")


async def test_health_endpoint():
    """Test the health check endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVER_URL}/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        
        print("[+] test_health_endpoint passed")


async def test_root_endpoint():
    """Test the root endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{SERVER_URL}/")
        
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "endpoints" in data
        
        print("[+] test_root_endpoint passed")


async def test_chat_completions_stream():
    """Test the chat completions endpoint with streaming."""
    if not API_KEY:
        print("[-] test_chat_completions_stream skipped (no GEMINI_API_KEY)")
        return
    
    # Prepare request payload
    payload = {
        "messages": [
            {"role": "user", "content": "Say 'Hello, World!' in exactly these words."}
        ],
        "temperature": 0.7,
        "max_tokens": 100
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream(
            "POST",
            f"{SERVER_URL}/v1/chat/completions",
            json=payload,
            headers={"Content-Type": "application/json"}
        ) as response:
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
            
            # Collect streaming chunks
            chunks_received = 0
            has_content = False
            has_done_signal = False
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix
                    
                    if data_str == "[DONE]":
                        has_done_signal = True
                        break
                    
                    try:
                        data = json.loads(data_str)
                        
                        # Check for content in delta
                        if "choices" in data and data["choices"]:
                            delta = data["choices"][0].get("delta", {})
                            if "content" in delta:
                                has_content = True
                                chunks_received += 1
                    
                    except json.JSONDecodeError:
                        # Skip invalid JSON
                        continue
            
            assert has_content, "No content received in stream"
            assert has_done_signal, "Stream didn't end with [DONE]"
            assert chunks_received > 0, "No chunks received"
            
            print(f"[+] test_chat_completions_stream passed (received {chunks_received} chunks)")


def run_tests():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("RUNNING UNIT TESTS FOR LOCAL PROXY SERVER")
    print("=" * 60 + "\n")
    
    # Test adapter functions (sync tests)
    print("Testing adapter functions...")
    test_adapter_to_gemini_payload()
    test_adapter_to_openai_stream()
    test_api_key_rotation_logic()
    
    # Check if server is running
    try:
        httpx.get(f"{SERVER_URL}/health", timeout=2.0)
        print("\n[+] Server is running, proceeding with endpoint tests...")
    except Exception:
        print("\n[!] Server is not running. Start the server with: uv run main.py")
        print("  Only adapter tests were executed.\n")
        return
    
    # Test endpoints (async tests)
    print("\nTesting endpoints...")
    asyncio.run(test_health_endpoint())
    asyncio.run(test_root_endpoint())
    asyncio.run(test_chat_completions_stream())
    
    print("\n" + "=" * 60)
    print("[+] ALL TESTS PASSED!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_tests()