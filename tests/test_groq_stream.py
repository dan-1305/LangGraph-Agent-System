import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv(".env")

async def test():
    key = os.getenv("GROQ_API_KEY")
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": "hi"}],
        "stream": True
    }
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload
        ) as response:
            print(f"STATUS: {response.status_code}")
            async for chunk in response.aiter_bytes():
                print(repr(chunk))

if __name__ == "__main__":
    asyncio.run(test())