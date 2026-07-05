# Sovereign Business Roadmap 2026

> **LAST UPDATE:** 2026-07-20 | **CURRENT PHASE:** Q3-Q4 2026 (CEO DIRECTIVE)

---

## 🟢 PHASE HIỆN TẠI: Q3-Q4 2026 "THE CEO DIRECTIVE"

> 📄 **Chi tiết đầy đủ:** See `reports/Q3_STRATEGIC_PLAN.md` và `reports/Q4_STRATEGIC_PLAN.md`

### Chiến dịch Alpha – Nâng cấp Trading Agent
- [ ] Ép `ai_trading_agent` kế thừa `BaseAgent`.
- [ ] Chuyển sang `gemini-3.1-flash-lite` (vận hành 24/7, chi phí 0đ).
- [ ] Scraping tin tức Whale miễn phí → khôi phục "Whale Alert".

### Chiến dịch Stealth – Cứu viện Airdrop Bot
- [ ] Giải quyết timeout Cloudflare Turnstile (Iframe).
- [ ] Mã hóa toàn bộ Session trong `./chrome_profile`.
- [ ] Xoay Proxy tự động để tránh chặn IP.

### Chiến dịch Nền tảng – Unified Monorepo
- [x] Xóa folder rác, đóng gói project simulation vô giá trị.
- [x] Bắt buộc `pyproject.toml` + `.env.example` cho mọi dự án.
- [x] Documentation Accuracy Audit (hoàn thành).

### Quy trình Hậu vệ (Defensive Protocol)
- [x] Circuit Breaker (Abort sau 3 lỗi).
- [x] Sentinel Backup (Full Backup ổ D sau mỗi task lớn).
- [x] Cross-Role Debate (`context/DEBATE_ROOM.md`).

### Timeline
- Tuần 1: BaseAgent sync → Tuần 2: Fix Cloudflare → Tuần 3: Stress Test.

---

## 📦 ARCHIVE: Q2/2026 "Affiliate Take-off"

> Trạng thái: HOÀN THÀNH. Giữ lại làm tham khảo lịch sử.

### Objective 1: Build an influential TikTok channel on the theme of AI & Technology
*   **Key Result 1.1:** Reach 10,000 followers on the new TikTok channel.
*   **Key Result 1.2:** Produce and publish 30 engaging, high-quality short videos about AI tools, programming, and automation.
*   **Key Result 1.3:** Achieve 100,000 views across the entire channel.

### Objective 2: Generate initial revenue from Affiliate Marketing
*   **Key Result 2.1:** Successfully integrate 3 affiliate links for suitable AI products/services into the video content.
*   **Key Result 2.2:** Generate 100 clicks on affiliate links.
*   **Key Result 2.3:** Record the first affiliate revenue (minimum $1).

### Objective 3: Establish EdTech Infrastructure ("Lò Luyện Thi AI")
*   **Key Result 3.1:** Complete and maintain PDF processing and syllabus decoding tools.
*   **Key Result 3.2:** Develop and refine engaging exam prep solutions: "Sleep Podcasts" (TTS) and gamified Desktop Quiz Apps.
*   **Key Result 3.3:** Ensure stable deployment of EdTech applications like `qtkdcks_quiz_app` for exam seasons.

### Objective 4: Core Infrastructure Stabilization (V2 Survival Architecture) ✅ COMPLETED
*   **Key Result 4.1:** [x] Eliminate "Dependency Hell" by migrating to `uv workspace`.
*   **Key Result 4.2:** [x] Eliminate "Context Window Explosion" by implementing Disk-as-State Memory Trimming.
*   **Key Result 4.3:** [x] Eliminate "Blind File Operations" by implementing Git Pre-flight Hooks.
*   **Key Result 4.4:** [x] Implement Application Circuit Breaker (Non-AI Fallbacks) in BaseAgent.
*   **Key Result 4.5:** [x] Deploy Centralized API Gateway & Rate Limiter to prevent LLM 429 Errors and Cache Prompts.

### Objective 5: Affiliate Video Pipeline Optimization (Tech Debt) ✅ COMPLETED
*   **Key Result 5.1:** [x] Deprecate Playwright UI Automation for TikTok Upload due to high instability and maintenance cost.
*   **Key Result 5.2:** [x] Research and implement Hybrid Upload Strategy (Official API + Playwright Fallback).
*   **Key Result 5.3:** [x] Achieve 95% upload success rate without human intervention.

### Objective 6: AI Tooling & System Optimization
*   **Key Result 6.1:** [x] Resolve Documentation Debt by establishing an on-demand sync mechanism (`tools/system/sync_docs.py`).
*   **Key Result 6.2:** [x] Develop an automated Documentation Agent (Scribe) for the Daily Health Loop.

### Objective 7: Project Eden (Minecraft AI Simulation) ✅ COMPLETED
*   **Key Result 7.1:** [x] Establish Text-based Grid Simulator (Phase 1) with Tech Tree and Resources.
*   **Key Result 7.2:** [x] Implement Tri-Brain Architecture (Working, Episodic, Semantic Memory) for Player Agent.
*   **Key Result 7.3:** [x] Integrate Vector DB (ChromaDB) for Long-term Tech Tree Memory.
*   **Key Result 7.4:** [x] Transition to Phase 2: Mineflayer & Minecraft 1.16.5 Integration.

### Objective 8: Airdrop Guerrilla Multi-chain Automation ✅ COMPLETED
*   **Key Result 8.1:** [x] Implement dual execution modes (Full-Auto RPC and Semi-Auto UI).
*   **Key Result 8.2:** [x] Integrate Target Testnets (Monad, Soneium, Inco) via EVMBase.
*   **Key Result 8.3:** [x] Deploy Smart Scheduler V2 with Catch-up Mechanism & Persistent Logging.
*   **Key Result 8.4:** [x] Establish Moni Score (Airdrop Scoring Engine).

### Epics (Q2 Legacy)
- **Epic 1:** Build TikTok Channel. (see `projects/auto_affiliate_video/epic_1_build_tiktok_channel.md`)
- **Epic 2:** Initial Affiliate Revenue. (see `projects/auto_affiliate_video/epic_2_initial_affiliate_revenue.md`)
- **Epic 3:** EdTech & AI Tutoring Tools Development.
- **Epic 4:** AI Factory V2 Infrastructure Upgrade. (Completed)
- **Epic 5:** [ON HOLD] The Omniscient System Expansion. (see `docs/V3_EXPANSION_PLAN.md`)
- **Epic 6:** AI Trading Agent V2 Deployment (Paper Trade).
- **Epic 7:** Airdrop Guerrilla Grand Audit & Multi-chain Expansion. (Completed)
- **Epic 8:** The Autonomous Era - Multi-Agent Governance & Self-Reflection. (Completed)