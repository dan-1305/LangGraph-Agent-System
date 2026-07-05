"""
Adapter Module for Payload Conversion

This module handles conversion between OpenAI-compatible format and Gemini API format.
It converts request payloads from OpenAI to Gemini and transforms streaming responses
back to OpenAI-compatible Server-Sent Events (SSE) format.
"""
import json
from typing import AsyncGenerator, Dict


def _trim_messages_if_needed(messages: list) -> list:
    """
    Tiêu chuẩn 1: Zero Token Leakage.
    Đo độ dài payload bằng thuật toán cơ bản (tương đương tiktoken), 
    nếu quá dài thì tự động cắt tỉa các tin nhắn cũ nhất (trừ system message).
    Giữ lại khoảng 30,000 ký tự (~7000 tokens) để chống bị rate limit.
    """
    MAX_CHARS = 30000 
    
    # Tính tổng độ dài
    total_len = sum(len(str(m.get("content", ""))) for m in messages)
    if total_len <= MAX_CHARS:
        return messages
        
    print(f"[Tiktoken Tracker] Payload quá lớn ({total_len} chars). Đang tiến hành cắt tỉa context...")
    
    trimmed = []
    current_len = 0
    
    # Luôn giữ lại message đầu tiên (thường là System prompt hoặc Core instruction)
    if len(messages) > 0:
        trimmed.append(messages[0])
        current_len += len(str(messages[0].get("content", "")))
        
    # Duyệt từ dưới lên (giữ lại tin nhắn mới nhất)
    recent_messages = []
    for msg in reversed(messages[1:]):
        msg_len = len(str(msg.get("content", "")))
        if current_len + msg_len > MAX_CHARS:
            break
        recent_messages.append(msg)
        current_len += msg_len
        
    trimmed.extend(reversed(recent_messages))
    print(f"[Tiktoken Tracker] Đã cắt tỉa xuống còn {current_len} chars ({len(trimmed)}/{len(messages)} messages).")
    return trimmed

def to_gemini_payload(openai_payload: Dict) -> Dict:
    """
    Convert OpenAI-compatible chat completion payload to Gemini API format.
    
    Args:
        openai_payload: Dictionary containing OpenAI format request with 'messages'.
    
    Returns:
        Dictionary containing Gemini API format with 'contents'.
    
    Example:
        Input: {"messages": [{"role": "user", "content": "Hello"}]}
        Output: {"contents": [{"role": "user", "parts": [{"text": "Hello"}]}]}
    """
    # Extract messages from OpenAI payload
    messages = openai_payload.get("messages", [])
    
    # Zero Token Leakage: Trim context if too large
    messages = _trim_messages_if_needed(messages)
    
    # Convert OpenAI messages to Gemini contents
    contents = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        # Map OpenAI roles to Gemini roles
        if role == "user":
            gemini_role = "user"
        elif role == "assistant":
            gemini_role = "model"
        elif role == "system":
            gemini_role = "user"
            # Prepend system message for better context
            content = f"System: {content}"
        else:
            gemini_role = "user"
        
        # Create Gemini content structure
        gemini_content = {
            "role": gemini_role,
            "parts": [{"text": str(content)}]
        }
        contents.append(gemini_content)
    
    # Build Gemini payload
    gemini_payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": openai_payload.get("temperature", 0.7),
            "maxOutputTokens": openai_payload.get("max_tokens", 8192),
            "topK": openai_payload.get("top_k", 40),
            "topP": openai_payload.get("top_p", 0.95),
        }
    }
    
    return gemini_payload


def to_openai_stream(gemini_chunk: str) -> str:
    """
    Convert Gemini streaming response chunk to OpenAI SSE format.
    
    Args:
        gemini_chunk: Raw text chunk from Gemini streaming response.
    
    Returns:
        Server-Sent Events (SSE) formatted string compatible with OpenAI.
    
    Example:
        Input: "Hello world"
        Output: 'data: {"choices": [{"delta": {"content": "Hello world"}}]}\n\n'
    """
    # Create OpenAI-compatible SSE format
    openai_chunk = {
        "choices": [
            {
                "delta": {
                    "content": gemini_chunk
                },
                "finish_reason": None,
                "index": 0
            }
        ],
        "created": 0,
        "id": "chatcmpl-localproxy",
        "model": "gemini-2.0-flash-exp",
        "object": "chat.completion.chunk"
    }
    
    # Format as SSE
    return f"data: {json.dumps(openai_chunk)}\n\n"


def to_openai_final_chunk() -> str:
    """
    Create a final chunk to signal stream completion.
    
    Returns:
        SSE formatted string with finish_reason set to 'stop'.
    """
    final_chunk = {
        "choices": [
            {
                "delta": {},
                "finish_reason": "stop",
                "index": 0
            }
        ],
        "created": 0,
        "id": "chatcmpl-localproxy",
        "model": "gemini-2.0-flash-exp",
        "object": "chat.completion.chunk"
    }
    
    return f"data: {json.dumps(final_chunk)}\n\ndata: [DONE]\n\n"


def _extract_text_from_gemini_obj(obj: dict) -> str:
    """
    Extract output text from a single parsed Gemini stream object,
    skipping any thought tokens (Gemini 3.x / Gemma-4 reasoning).
    """
    candidates = obj.get("candidates", [])
    if not candidates:
        return ""
    content = candidates[0].get("content", {})
    parts_list = content.get("parts", [])
    texts = []
    for part in parts_list:
        # Skip thought tokens (internal reasoning, not final answer)
        if part.get("thought") is True:
            continue
        text = part.get("text", "")
        if text:
            texts.append(text)
    return "".join(texts)


async def stream_gemini_to_openai(
    gemini_stream: AsyncGenerator[bytes, None]
) -> AsyncGenerator[str, None]:
    """
    Transform Gemini streaming response to OpenAI SSE format.

    Robust brace-depth parser: accumulates bytes into a buffer, finds complete
    JSON objects by tracking `{`/`}` depth, parses each complete object and
    yields OpenAI-format SSE chunks. Skips thought tokens automatically.
    Handles both array format `[{...},{...}]` and single-object streaming.
    """
    buffer = ""
    try:
        async for chunk in gemini_stream:
            buffer += chunk.decode("utf-8", errors="ignore")

            # Strip leading array bracket on first iteration
            stripped = buffer.lstrip()
            if stripped.startswith("["):
                # Remove only the leading bracket, keep rest
                idx = buffer.find("[")
                buffer = buffer[idx + 1:]

            # Parse complete JSON objects using brace-depth tracking
            while True:
                # Find the next complete JSON object
                obj_str, remainder = _extract_next_json_object(buffer)
                if obj_str is None:
                    break  # No complete object yet, wait for more data

                buffer = remainder
                try:
                    gemini_data = json.loads(obj_str)
                except json.JSONDecodeError:
                    continue

                text = _extract_text_from_gemini_obj(gemini_data)
                if text:
                    print(f"[Stream] Extracted text: '{text[:50]}...'")
                    yield to_openai_stream(text)

        # After stream ends, try to parse any remaining buffered object
        remaining = buffer.strip().rstrip(",").strip()
        if remaining.startswith("]"):
            remaining = remaining[1:].strip()
        if remaining.endswith("]"):
            remaining = remaining[:-1].strip()
        if remaining and remaining != "}":
            if not remaining.endswith("}"):
                remaining += "}"
            try:
                gemini_data = json.loads(remaining)
                text = _extract_text_from_gemini_obj(gemini_data)
                if text:
                    print(f"[Stream] Extracted final text: '{text[:50]}...'")
                    yield to_openai_stream(text)
            except json.JSONDecodeError:
                pass

        # Send final completion signal
        yield to_openai_final_chunk()

    except Exception as e:
        error_chunk = {
            "choices": [],
            "error": {
                "message": f"Streaming error: {str(e)}",
                "type": "stream_error"
            }
        }
        yield f"data: {json.dumps(error_chunk)}\n\ndata: [DONE]\n\n"


def _extract_next_json_object(buffer: str) -> tuple:
    """
    Find the first complete top-level JSON object in buffer using brace-depth.

    Returns:
        Tuple of (object_string, remainder) or (None, buffer) if incomplete.
    """
    start_idx = -1
    depth = 0
    in_string = False
    escape = False

    for i, ch in enumerate(buffer):
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            if depth == 0:
                start_idx = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start_idx != -1:
                obj_str = buffer[start_idx : i + 1]
                remainder = buffer[i + 1 :]
                return obj_str, remainder

    return None, buffer
