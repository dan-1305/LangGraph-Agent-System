import os
import sys
import httpx
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Force UTF-8 encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

# Load .env
base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / ".env")

async def test_gemini(api_key):
    if not api_key or len(api_key) < 10:
        return "❌ Thiếu hoặc sai định dạng Key"
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": "Reply 'OK'"}]}]
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.post(url, json=payload)
            if res.status_code == 200:
                return "✅ SUCCESS (Hoạt động tốt)"
            elif res.status_code == 429:
                return "⚠️ RATE LIMIT (Đã hết hạn mức sử dụng tạm thời)"
            elif res.status_code == 400:
                return f"❌ BAD REQUEST: {res.text[:50]}"
            elif res.status_code == 403:
                return "❌ FORBIDDEN (Key bị vô hiệu hóa hoặc sai vùng)"
            else:
                return f"❌ LỖI KHÁC: {res.status_code} - {res.text[:50]}"
        except Exception as e:
            return f"❌ LỖI MẠNG: {str(e)}"

async def test_openai_compatible(url, api_key, model):
    if not api_key or len(api_key) < 10:
        return "❌ Thiếu hoặc sai định dạng Key"
        
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Reply 'OK'"}]
    }
    
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            res = await client.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                return "✅ SUCCESS (Hoạt động tốt)"
            elif res.status_code == 429:
                return "⚠️ RATE LIMIT / OUT OF CREDITS (Đã hết tiền hoặc quá tải)"
            elif res.status_code == 401:
                return "❌ UNAUTHORIZED (Key sai hoặc bị khóa)"
            else:
                return f"❌ LỖI KHÁC: {res.status_code} - {res.text[:50]}"
        except Exception as e:
            return f"❌ LỖI MẠNG: {str(e)}"

async def main():
    print("="*60)
    print("🔍 KIỂM TRA TRẠNG THÁI CÁC API KEYS TRONG .ENV")
    print("="*60)
    
    # 1. Test Gemini
    gemini_key = os.getenv("GEMINI_API_KEY")
    print(f"\n[1] Đang test GEMINI_API_KEY ({str(gemini_key)[:6]}...)....")
    res = await test_gemini(gemini_key)
    print(f"    Kết quả: {res}")
    
    # 2. Test Groq (Model mới nhất)
    groq_key = os.getenv("GROQ_API_KEY")
    print(f"\n[2] Đang test GROQ_API_KEY ({str(groq_key)[:6]}...)....")
    res = await test_openai_compatible("https://api.groq.com/openai/v1/chat/completions", groq_key, "llama-3.3-70b-versatile")
    print(f"    Kết quả: {res}")
    
    # 3. Test OpenRouter (Model mới nhất)
    or_key = os.getenv("OPENROUTER_API_KEY")
    print(f"\n[3] Đang test OPENROUTER_API_KEY ({str(or_key)[:6]}...)....")
    res = await test_openai_compatible("https://openrouter.ai/api/v1/chat/completions", or_key, "google/gemini-2.5-flash")
    print(f"    Kết quả: {res}")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(main())