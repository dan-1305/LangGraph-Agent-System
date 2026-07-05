import os, httpx, asyncio  
from dotenv import load_dotenv  
load_dotenv()  
async def main():  
    api_key = os.getenv("GEMINI_API_KEY")  
    r = await httpx.AsyncClient().post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}", json={"contents": [{"parts": [{"text": "hi"}]}]})  
    print(r.status_code, r.text[:100])  
asyncio.run(main())  
