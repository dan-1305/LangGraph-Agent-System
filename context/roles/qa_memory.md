# 🧪 QA MEMORY - Edge Case Registry

## 🚨 Active Bugs
- None

## 📉 Failed Test Cases
- **Gemini Direct API (httpx):** Always return 404 for `v1beta` models in direct script. Use `local_proxy_server` instead.

## 🧠 Learned Lessons
- When testing Windows Console, always remove Emojis to avoid `UnicodeEncodeError` (gbk).
- OpenWiki npm is hardcoded to OpenRouter, do not try to wrap it for local proxy via environment variables.

---
*QA is the watchdog of stability.*
