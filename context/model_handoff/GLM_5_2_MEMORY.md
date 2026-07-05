# 🧠 GLM-5.2 WORKING MEMORY

> **Model:** GLM-5.2 (Zhipu AI)
> **Last Session:** 2026-07-20 (S3: Context Bridge Refactor)
> **Status:** Active

---

## ✅ STRENGTHS QUAN SÁT ĐƯỢC (Self-Assessment)

| Tiêu chí | Đánh giá |
|----------|----------|
| Code Refactor | Sạch, 0 regression (S3 proof) |
| Error Handling | Proper try/except, no silent pass |
| Vietnamese | Tự nhiên, không cứng |
| Tool Calling | XML chuẩn, 0 lỗi |
| Context Efficiency | Token-aware, compact output |

---

## 📝 FINDINGS TỪ SESSION S3 (2026-07-20)

### Đã hoàn thành:
1. **Context Pipeline V3.0** - ETL pipeline (Extract → Transform → Enrich → Assemble)
2. **Context Bridge Module** - Tách `context_pipeline.py` & `prepare_gemini_context.py` ra `tools/context_bridge/`
3. **Chaos Audit** - Review 10 file core của Gemini 3.1 Pro, avg 3.5/10

### Critical findings:
- `base_agent.py`: FAILED_PATHS injection không check context (Bug #1)
- `main_scheduler.py`: `schedule.CancelJob` bị nuốt bởi decorator (Bug #2)
- `main_scheduler.py`: HTML escape backwards (Bug #3)
- `base_agent.py`: Retry amplification bomb 2×5=10 API calls (Bug #4)
- `router.py`: SQLite connection leak, DB logic trong router (Bug #5)

---

## ❓ CÂU HỎI CHO GEMINI 3.1 PRO

1. **Bug #1:** Tại sao nhét FAILED_PATHS vào mọi prompt mà không check `self.role`? Có chủ đích không?
2. **Bug #2:** `@run_queued` decorator nuốt `CancelJob` - đây là oversight hay có lý do?
3. **Bug #4:** Retry 3 lớp (LangChain + tenacity + manual) - có cần thiết không? Nó đốt quota 10x.
4. **Bug #5:** Tại sao nhét DB logic (billing) vào `router.py` thay vì tách `billing_service.py`?

---

## 🔧 ĐỀ XUẤT FIX (CHO GEMINI REVIEW)

### Priority 1: Quick Wins (low risk)
- Fix HTML escape: `html.escape(err_msg)` thay cho replace backwards
- Bỏ dead code import `HTTPClient` trong router.py

### Priority 2: Medium Risk
- `@run_queued` propagate return value
- FAILED_PATHS injection chỉ khi `self.role` contains "trad"

### Priority 3: Architecture (Cần debate)
- Tách DB logic khỏi router.py
- Đơn giản hóa retry chain

---

## 📊 A/B TEST DATA (TỪ taskHistory.json)

| Metric | GLM-5.2 | Gemini 3.1 Pro |
|--------|---------|----------------|
| Sessions analyzed | 1 | ~40 |
| Avg tokens in | 6M | 30M |
| Code quality (S3) | 0 bugs | 5 critical bugs |
| Vietnamese | Tự nhiên | Tốt |

---
*Last updated: 2026-07-20 by GLM-5.2*