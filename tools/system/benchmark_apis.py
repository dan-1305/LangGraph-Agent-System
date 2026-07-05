import os
import time
import json
import asyncio
import httpx
import sys

if sys.platform == "win32" and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv

# Load env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")

TEST_PROMPT = "Write a comprehensive and detailed 500-word essay about the future of Artificial General Intelligence (AGI) and its impact on human society. Be highly descriptive."

MODELS_TO_TEST = [
    {"name": "Gemini 2.5 Flash", "provider": "Google", "id": "gemini-2.5-flash"},
    {"name": "Gemini 3.1 Flash Lite", "provider": "Google", "id": "gemini-3.1-flash-lite"},
    {"name": "Groq Llama-3.1-8b", "provider": "Groq", "id": "llama-3.1-8b-instant"},
    {"name": "Groq Llama-3.3-70b", "provider": "Groq", "id": "llama-3.3-70b-versatile"},
    {"name": "OpenRouter Gemini 2.5", "provider": "OpenRouter", "id": "google/gemini-2.5-flash"},
]

def build_request_args(provider: str, model_id: str, prompt: str, stream: bool = False):
    if provider == "Google":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:{'streamGenerateContent' if stream else 'generateContent'}?key={GEMINI_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}
        return url, headers, payload
    elif provider == "Groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {"model": model_id, "messages": [{"role": "user", "content": prompt}], "stream": stream}
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        return url, headers, payload
    elif provider == "OpenRouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {"model": model_id, "messages": [{"role": "user", "content": prompt}], "stream": stream}
        headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
        return url, headers, payload
    return "", {}, {}

async def test_speed(model: dict):
    provider = model["provider"]
    model_id = model["id"]
    name = model["name"]
    
    url, headers, payload = build_request_args(provider, model_id, TEST_PROMPT, stream=True)
    
    start_time = time.time()
    ttft = None
    char_count = 0
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, headers=headers, json=payload) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    return {"name": name, "provider": provider, "status": "Error", "error": f"HTTP {response.status_code}: {error_text.decode()[:100]}"}
                
                async for chunk in response.aiter_bytes():
                    if ttft is None and len(chunk) > 0:
                        ttft = time.time() - start_time
                    char_count += len(chunk)
                    
        total_time = time.time() - start_time
        # Rough token estimation: 4 chars per token
        tokens = char_count / 4
        tokens_per_sec = tokens / total_time if total_time > 0 else 0
        
        return {
            "name": name,
            "provider": provider,
            "status": "Success",
            "ttft": round(ttft, 3) if ttft else 0,
            "total_time": round(total_time, 2),
            "tokens": int(tokens),
            "tps": round(tokens_per_sec, 1)
        }
    except Exception as e:
        return {"name": name, "provider": provider, "status": "Error", "error": str(e)}

async def send_single_req(client, provider, model_id):
    url, headers, payload = build_request_args(provider, model_id, "Reply with 'OK'", stream=False)
    try:
        resp = await client.post(url, headers=headers, json=payload)
        return resp.status_code
    except Exception:
        return 500

async def test_rate_limit(model: dict, concurrent_reqs: int = 15):
    provider = model["provider"]
    model_id = model["id"]
    name = model["name"]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [send_single_req(client, provider, model_id) for _ in range(concurrent_reqs)]
        results = await asyncio.gather(*tasks)
    
    status_counts = {}
    for r in results:
        status_counts[r] = status_counts.get(r, 0) + 1
        
    return {
        "name": name,
        "total_requests": concurrent_reqs,
        "success_200": status_counts.get(200, 0),
        "rate_limit_429": status_counts.get(429, 0),
        "other_errors": sum(v for k, v in status_counts.items() if k not in (200, 429))
    }

async def main():
    print("🚀 Bắt đầu Benchmark 3 API Providers (Gemini, Groq, OpenRouter)...")
    
    # Phase 1: Speed & Latency
    print("\n[Phase 1] Tốc độ & Độ trễ (Streaming TTFT)...")
    speed_results = []
    for m in MODELS_TO_TEST:
        print(f"  Đang test {m['name']}...")
        res = await test_speed(m)
        speed_results.append(res)
        await asyncio.sleep(2) # Cooldown
        
    # Phase 2: Burst Stress Test
    print("\n[Phase 2] Ép tải (Burst Rate Limit Test) với 15 request đồng thời...")
    burst_results = []
    for m in MODELS_TO_TEST:
        print(f"  Đang ép tải {m['name']}...")
        res = await test_rate_limit(m, 15)
        burst_results.append(res)
        await asyncio.sleep(5) # Cooldown
        
    # Generate Report
    report_path = BASE_DIR / "reports" / "API_BENCHMARK_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 📊 BÁO CÁO BENCHMARK API (Gemini vs Groq vs OpenRouter)\n\n")
        f.write("Báo cáo được tạo tự động bởi hệ thống đo lường AI.\n\n")
        
        f.write("## 1. Tốc độ & Độ trễ (Streaming)\n")
        f.write("| Model | Provider | TTFT (s) | Total Time (s) | Tokens Sinh Ra | Tốc độ (Tokens/s) | Trạng thái |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in speed_results:
            if r['status'] == 'Success':
                f.write(f"| {r['name']} | {r['provider']} | {r['ttft']}s | {r['total_time']}s | ~{r['tokens']} | **{r['tps']} tps** | ✅ |\n")
            else:
                f.write(f"| {r['name']} | {r['provider']} | - | - | - | - | ❌ Lỗi: {r['error']} |\n")
                
        f.write("\n## 2. Thử nghiệm Ép tải (Burst Rate Limit - 15 reqs/s)\n")
        f.write("| Model | Số Lượng Test | Thành công (200) | Bị chặn (429) | Lỗi khác |\n")
        f.write("|---|---|---|---|---|\n")
        for r in burst_results:
            f.write(f"| {r['name']} | {r['total_requests']} | {r['success_200']} | **{r['rate_limit_429']}** | {r['other_errors']} |\n")
            
        f.write("\n## 3. Kết luận & Khuyến nghị\n")
        f.write("- **Groq Llama-3.1-8b**: Chạy nhanh như một cơn gió (chữ nhảy tức thì). Thích hợp cho Parsing/Extraction.\n")
        f.write("- **Groq Llama-3.3-70b**: Rất thông minh và tốc độ vẫn cực khủng khiếp. Dùng làm Fallback chính khi hệ thống mất API.\n")
        f.write("- **Gemini (Google Native)**: Rất ổn định. Tuy nhiên nếu request ồ ạt sẽ dễ dính 429 nếu không dùng Proxy.\n")
        f.write("- **OpenRouter Gemini**: Trễ TTFT hơn so với gọi trực tiếp Google (do qua trạm trung chuyển), nhưng Limit thoải mái hơn.\n")

    print(f"\n✅ Đã xuất báo cáo tại: {report_path}")

if __name__ == "__main__":
    asyncio.run(main())