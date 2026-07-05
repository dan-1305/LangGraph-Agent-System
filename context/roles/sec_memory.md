# 🛡️ SEC MEMORY - Vulnerability & API Registry

## ⚠️ Security Vulnerabilities
- **Leaked API Keys:** Google detected `GEMINI_API_KEY` ending in `cEeA` as leaked.

## 🔑 Protected Assets
- `.env` (Strictly excluded by `.gitignore`)
- `~/.openwiki/.env` (Stored in user profile, safe from Git)

## 🧠 Learned Lessons
- Never include API keys in prompt examples or documentation.
- Use `local_proxy_server` to mask real API keys and manage rotations.

---
*Security is the armor of the system.*
