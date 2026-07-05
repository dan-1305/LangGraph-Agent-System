"""
Router Module for FastAPI Endpoints

This module defines the API routes for the Local Proxy Server,
including the streaming chat completions endpoint.
"""
from core_utilities.http_client import HTTPClient
import json
import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

from .config import get_settings
from .rotation_manager import get_rotation_manager
from .adapter import to_gemini_payload, stream_gemini_to_openai


router = APIRouter()


async def stream_fallback_generator(openai_payload: dict, requested_model: str) -> AsyncGenerator[str, None]:
    """Fallback generator using Groq or OpenRouter when Gemini is fully exhausted."""
    settings = get_settings()
    
    mapped_model = settings.map_model(requested_model)
    is_direct_routing = mapped_model.startswith("groq/") or mapped_model.startswith("openrouter/")
    
    # Choose fallback provider
    if is_direct_routing and mapped_model.startswith("openrouter/"):
        api_key = settings.openrouter_api_key
        base_url = "https://openrouter.ai/api/v1/chat/completions"
        fallback_model = mapped_model.replace("openrouter/", "")
        
        # [FIX] OpenRouter yêu cầu 'model' phải chính xác. Gemma free model thường có hậu tố :free
        if ":free" not in fallback_model and "gemma" in fallback_model.lower():
            fallback_model = f"{fallback_model}:free"
            
        provider = "OpenRouter"
    elif is_direct_routing and mapped_model.startswith("groq/"):
        api_key = settings.groq_api_key
        base_url = "https://api.groq.com/openai/v1/chat/completions"
        fallback_model = mapped_model.replace("groq/", "")
        provider = "Groq"
    elif settings.openrouter_api_key:
        api_key = settings.openrouter_api_key
        base_url = "https://openrouter.ai/api/v1/chat/completions"
        
        # OpenRouter supports Gemini directly. Just map the exact model!
        if requested_model and "gemini" in requested_model.lower():
            fallback_model = f"google/{requested_model}"
        else:
            fallback_model = "google/gemini-2.5-flash"
            
        provider = "OpenRouter"
    elif settings.groq_api_key:
        api_key = settings.groq_api_key
        base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Smart fallback for Groq based on speed requirements
        if requested_model and "lite" in requested_model.lower():
            fallback_model = "llama-3.1-8b-instant" # Fast parsing
        else:
            fallback_model = "llama-3.3-70b-versatile" # Complex reasoning
            
        provider = "Groq"
    else:
        raise HTTPException(
            status_code=429,
            detail="All Gemini credentials exhausted and no Fallback API (GROQ_API_KEY/OPENROUTER_API_KEY) configured."
        )

    print(f"[Fallback] (Switching) Switching to Backup Provider: {provider} | Model: {fallback_model}")
    
    # Modify payload for fallback provider
    fallback_payload = openai_payload.copy()
    fallback_payload["model"] = fallback_model
    # BẮT BUỘC dùng stream=True vì hàm parse bên ngoài (chat_completions) luôn tìm cú pháp "data: "
    fallback_payload["stream"] = True

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream(
                "POST",
                base_url,
                json=fallback_payload,
                headers=headers
            ) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    error_msg = error_text.decode("utf-8", errors="ignore")
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"{provider} API error: {error_msg}"
                    )

                async for chunk in response.aiter_bytes():
                    # Groq/OpenRouter are already OpenAI-compatible SSE
                    if chunk:
                        yield chunk.decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[!] STREAM FALLBACK ERROR: {e.__class__.__name__}: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"Failed to connect to Fallback API ({provider}): {str(e)}"
        )

async def stream_generator(gemini_payload: dict, requested_model: str = None, openai_payload: dict = None) -> AsyncGenerator[str, None]:
    """
    Async generator that streams responses from Gemini and converts to OpenAI format.
    Uses RotationManager for smart (key, model) dispatch with automatic fallback.

    Args:
        gemini_payload: The payload to send to Gemini API.
        requested_model: The model name requested by the client.

    Yields:
        OpenAI-compatible SSE formatted strings.
    """
    settings = get_settings()
    
    # Check if target model is explicitly routed to Groq or OpenRouter
    mapped_model = settings.map_model(requested_model)
    if mapped_model.startswith("groq/") or mapped_model.startswith("openrouter/"):
        if openai_payload:
            target_model = mapped_model.split("/", 1)[1]
            provider_prefix = mapped_model.split("/", 1)[0]
            print(f"[{provider_prefix.upper()} DIRECT ROUTING] -> Model: {target_model}")
            
            # Rewrite fallback_model logic for direct routing inside stream_fallback_generator
            openai_payload["model"] = target_model
            async for chunk in stream_fallback_generator(openai_payload, requested_model):
                yield chunk
            return
            
    rotation = get_rotation_manager()
    # Max retries = total (key, model) pairs available in fallback pool
    max_retries = len(settings.gemini_api_keys) * len(settings.model_rotation_pool)
    max_retries = max(max_retries, 1)

    for attempt in range(max_retries):
        try:
            current_key, target_model = rotation.get_valid_credential(requested_model)
        except RuntimeError as e:
            # Fallback to Groq/OpenRouter!
            if openai_payload:
                async for chunk in stream_fallback_generator(openai_payload, requested_model):
                    yield chunk
                return
            else:
                raise HTTPException(status_code=429, detail=str(e))

        # Handle manual block before calling API
        if target_model == "manual-block":
            print(f"[!] Manual block triggered for label: {requested_model}")
            raise HTTPException(
                status_code=403,
                detail="[MANUAL MODE] This Agent is restricted to manual operation to save API Quota."
            )

        gemini_url = settings.get_gemini_stream_url(target_model, current_key)
        masked_key = f"{current_key[:6]}...{current_key[-4:]}" if len(current_key) > 10 else "invalid"

        print(f"[Rotation] Attempt {attempt + 1}/{max_retries} → Model={target_model} | Key={masked_key}")

        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                async with client.stream(
                    "POST",
                    gemini_url,
                    json=gemini_payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    # If Rate Limited (429) or Quota issue (403), mark pair and retry
                    if response.status_code in (429, 403):
                        error_text = await response.aread()
                        error_msg = error_text.decode("utf-8", errors="ignore")
                        print(f"[-] ({target_model}, {masked_key}) → HTTP {response.status_code}: {error_msg[:120]}")
                        rotation.mark_exhausted(current_key, target_model)

                        if attempt < max_retries - 1:
                            continue  # RotationManager will dispatch next valid pair
                        else:
                            if openai_payload:
                                async for chunk in stream_fallback_generator(openai_payload, requested_model):
                                    yield chunk
                                return
                            else:
                                raise HTTPException(
                                    status_code=429,
                                    detail=f"All credentials exhausted. Last error: {error_msg}"
                                )

                    if response.status_code != 200:
                        error_text = await response.aread()
                        error_msg = error_text.decode("utf-8", errors="ignore")
                        raise HTTPException(
                            status_code=response.status_code,
                            detail=f"Gemini API error ({target_model}): {error_msg}"
                        )

                    # Stream response and convert to OpenAI format
                    print(f"[Stream] Starting response stream for {target_model}...")
                    async for openai_chunk in stream_gemini_to_openai(response.aiter_bytes()):
                        if openai_chunk:
                            yield openai_chunk
                    print(f"[Stream] Streaming complete for {target_model}")
                    return  # Success, exit generator

        except httpx.HTTPError as e:
            print(f"[-] HTTP error ({target_model}): {str(e)}")
            rotation.mark_exhausted(current_key, target_model)
            if attempt < max_retries - 1:
                continue
            raise HTTPException(
                status_code=502,
                detail=f"Failed to connect to Gemini API: {str(e)}"
            )

    # If we fall through the loop, all pairs failed
    if openai_payload:
        async for chunk in stream_fallback_generator(openai_payload, requested_model):
            yield chunk
        return
    else:
        raise HTTPException(
            status_code=429,
            detail="All configured (key, model) pairs are currently rate-limited or exhausted."
        )


@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    OpenAI-compatible chat completions endpoint with streaming support.
    
    This endpoint accepts OpenAI-format requests and proxies them to Gemini API,
    transforming the streaming response back to OpenAI-compatible SSE format.
    """
    try:
        # Parse JSON request
        openai_payload = await request.json()
        
        # Validate required fields
        if "messages" not in openai_payload:
            raise HTTPException(
                status_code=400,
                detail="Missing required field: 'messages'"
            )
        
        # Convert OpenAI payload to Gemini format
        gemini_payload = to_gemini_payload(openai_payload)
        
        # Extract model for mapping
        requested_model = openai_payload.get("model")
        is_streaming = openai_payload.get("stream", False)
        
        if is_streaming:
            # Return streaming response using the robust generator
            return StreamingResponse(
                stream_generator(gemini_payload, requested_model, openai_payload),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )
        else:
            # Handle non-streaming request
            full_content = ""
            buffer = ""
            async for chunk in stream_generator(gemini_payload, requested_model, openai_payload):
                # stream_generator already yields OpenAI SSE chunks
                if not chunk:
                    continue
                    
                buffer += chunk
                # Tích lũy buffer và tách chính xác theo \n\n để tránh lỗi cắt ngang JSON giữa chừng (Network Chunking)
                while "\n\n" in buffer:
                    event, buffer = buffer.split("\n\n", 1)
                    event = event.strip()
                    if event.startswith("data: ") and event != "data: [DONE]":
                        try:
                            json_str = event[6:].strip()
                            data = json.loads(json_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                # Standard OpenAI streaming chunk has delta
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                full_content += content
                        except Exception as e:
                            print(f"[DEBUG] Error parsing event: {e} | Data: {event[:100]}...")
                            continue
            
            print(f"[DEBUG] Non-streaming full content length: {len(full_content)}")
            if len(full_content) > 0:
                print(f"[DEBUG] Preview: {full_content[:100]}...")
            
            # If everything failed and content is still empty, throw error
            if not full_content:
                raise HTTPException(
                    status_code=500,
                    detail="Gemini returned an empty response. Possible model incompatibility or safety filter."
                )

            # Wrap in standard OpenAI response format
            return {
                "id": "chatcmpl-localproxy",
                "object": "chat.completion",
                "created": 0,
                "model": requested_model or "gemini-proxy",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": full_content
                        },
                        "finish_reason": "stop"
                    }
                ],
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }
    
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid JSON payload: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Validation error: {str(e)}"
        )


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Dictionary with health status.
    """
    return {"status": "healthy", "service": "local-proxy-server"}


import sqlite3
import os
import time

def _init_billing_db():
    from pathlib import Path
    db_path = Path(__file__).resolve().parent.parent / "data" / "billing.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30.0)
    # Luật Database Sinh tồn
    conn.execute('PRAGMA journal_mode=WAL;')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tx_history (
            tx_hash TEXT PRIMARY KEY,
            amount REAL,
            currency TEXT,
            timestamp REAL
        )
    """)
    conn.commit()
    conn.close()
    return db_path

# Initialize billing DB
BILLING_DB_PATH = _init_billing_db()

# Rate limit tracking for billing endpoint (in-memory, simple)
_billing_rate_limits = {}

@router.post("/v1/billing")
async def process_billing(request: Request):
    """
    Tiêu chuẩn 3: Crypto Payment Config Ready & Anti-Replay
    Endpoint nhận TxHash, kiểm tra trùng lặp và lưu vào billing.db
    """
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    # Rate Limit: 5 req/min
    if client_ip in _billing_rate_limits:
        reqs = _billing_rate_limits[client_ip]
        # remove old reqs
        reqs = [t for t in reqs if now - t < 60]
        if len(reqs) >= 5:
            raise HTTPException(status_code=429, detail="Too many billing requests. Please wait.")
        reqs.append(now)
        _billing_rate_limits[client_ip] = reqs
    else:
        _billing_rate_limits[client_ip] = [now]
        
    try:
        payload = await request.json()
        tx_hash = payload.get("tx_hash")
        amount = payload.get("amount", 0.0)
        currency = payload.get("currency", "USDT")
        
        if not tx_hash:
            raise HTTPException(status_code=400, detail="Missing tx_hash")
            
        # Fix Bug #5: Use try/finally to prevent connection leak
        conn = sqlite3.connect(BILLING_DB_PATH, timeout=30.0)
        try:
            cursor = conn.cursor()
            
            # Anti-Replay Attack Check
            cursor.execute("SELECT * FROM tx_history WHERE tx_hash = ?", (tx_hash,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Transaction Hash already processed (Anti-Replay Triggered).")
                
            cursor.execute("INSERT INTO tx_history (tx_hash, amount, currency, timestamp) VALUES (?, ?, ?, ?)",
                           (tx_hash, amount, currency, now))
            conn.commit()
        finally:
            conn.close()  # Fix Bug #5: Always close connection even on exception
        
        return {"status": "success", "message": "Transaction verified and recorded.", "tx_hash": tx_hash}
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/")
async def root() -> dict:
    """
    Root endpoint with service information.
    
    Returns:
        Dictionary with service information.
    """
    settings = get_settings()
    return {
        "service": "Local Proxy Server for Gemini API",
        "version": "1.0.0",
        "default_model": settings.default_model,
        "available_models": list(settings.model_mapping.keys()),
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "health": "/health"
        }
    }