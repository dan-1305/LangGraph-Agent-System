# 🔥 CHAOS OVERLORD CODE AUDIT - 2026-07-20

> **Reviewer:** GLM-5.2 (acting as Chaos Overlord / CEO)
> **Subject:** Codebase viết bởi Gemini 3.1 Pro Preview (100+ sessions)
> **Mode:** Tàn nhẫn, trực diện, không nương tay
> **Verdict:** Average **3.5/10** - Tech debt khổng lồ, 5 critical bugs

---

## 📊 BẢNG ĐIỂM TỔNG HỢP

| File | Score | Verdict |
|------|-------|---------|
| `src/base_agent.py` | 4/10 | 🔴 NEEDS_REFACTOR |
| `src/factory/config.py` | 3/10 | 🔴 NEEDS_REFACTOR |
| `projects/local_proxy_server/core/router.py` | 3/10 | 🔴 CRITICAL |
| `projects/local_proxy_server/core/config.py` | 2.5/10 | 🔴 CRITICAL |
| `scheduler/main_scheduler.py` | 3.5/10 | 🔴 NEEDS_REFACTOR |
| `core/process_watchdog.py` | 4/10 | 🔴 NEEDS_REFACTOR |
| `projects/ai_trading_agent/src/langgraph_agent.py` | 4/10 | 🔴 NEEDS_REFACTOR |
| `projects/ai_trading_agent/src/binance_executor.py` | 3/10 | 🔴 CRITICAL |

---

## 💀 TOP 5 CRITICAL BUGS

### 🔴 Bug #1: Self-Healing Memory Injection (`src/base_agent.py`)

**Severity:** CRITICAL (Security + Correctness)

Hàm `_call_llm_with_retry` đọc `logs/FAILED_PATHS.json` rồi **prepend trực tiếp vào MỌI prompt** mà không check bối cảnh. Comment nói "nếu prompt có từ khóa liên quan giao dịch/rủi ro" — nhưng CODE KHÔNG HỀ CHECK.

```python
# Mọi agent (QA, Coder, BA...) đều bị nhét ký ức thất bại vào prompt
# → Context pollution + data leak
except Exception: pass  # Im lặng nuốt lỗi nếu file hỏng
```

**Fix:** Chỉ inject FAILED_PATHS khi `self.role` chứa "trader" hoặc "trading".

---

### 🔴 Bug #2: Scheduler Dead Code (`scheduler/main_scheduler.py`)

**Severity:** CRITICAL (Resource Leak)

```python
@run_queued
def scrape_job():
    # ...
    return schedule.CancelJob  # BỊ NUỐT bởi @run_queued decorator!
```

Decorator `@run_queued` wrap hàm trong `wrapper()` gọi `executor.submit(func)` và return `None`. Nên `return schedule.CancelJob` bị ăn mất — job "stop after 10 runs" **KHÔNG BAO GIỜ cancel**. Scheduler chạy vô hạn, đốt RAM.

**Fix:** `wrapper()` phải propagate return value của `func()`.

---

### 🔴 Bug #3: HTML Escape BACKWARDS (`scheduler/main_scheduler.py`)

**Severity:** HIGH (Security + UX)

```python
err_msg.replace('<', '<').replace('>', '>')  # IDENTITY - KHÔNG LÀM GÌ CẢ!
```

Phải là `.replace('<', '<').replace('>', '>')`. Hiện tại Telegram `<pre>` blocks bị break, error trace leak raw HTML.

**Fix:** Dùng `html.escape(err_msg)`.

---

### 🔴 Bug #4: Retry Amplification Bomb (`src/base_agent.py`)

**Severity:** HIGH (Cost + Quota Burn)

```python
ChatOpenAI(max_retries=2)     # Layer 1: LangChain retry
+ @retry(stop=stop_after_attempt(5))  # Layer 2: tenacity retry
+ try/except in _call_llm     # Layer 3: manual retry
# = 2 × 5 = 10 lần gọi API cho 1 request khi lỗi
```

Đốt quota Gemini 10x nhanh hơn dự kiến. Logic `_call_llm` check `"429" in error_msg` để re-raise — nhưng lỗi đã bị retry 5 lần rồi, re-raise lúc này vô nghĩa.

**Fix:** Bỏ 1 layer retry. Giữ chỉ `@retry(stop=stop_after_attempt(3))`.

---

### 🔴 Bug #5: Resource Leak (`projects/local_proxy_server/core/router.py`)

**Severity:** HIGH (Stability)

```python
conn = sqlite3.connect(BILLING_DB_PATH, timeout=30.0)
cursor = conn.cursor()
# Nếu exception → LEAK CONNECTION
conn.close()  # KHÔNG trong finally block
```

+ Rate limit dict grow vô hạn (no cleanup)
+ `HTTPClient` import dead code (không bao giờ dùng)
+ API key expose trong URL query param
+ `/v1/billing` endpoint không auth
+ DB logic nhét giữa router (vi phạm SRP)

**Fix:** Tách DB ra `billing_service.py`, dùng context manager cho connection.

---

## 📋 FULL FILE-BY-FILE DETAILS

### `src/base_agent.py` — 4/10

| Issue | Severity | Line |
|-------|----------|------|
| FAILED_PATHS injection không check context | CRITICAL | 95-108 |
| Retry bọc retry bọc retry | HIGH | 238-240 |
| `except Exception: pass` im lặng | MEDIUM | Multiple |

**Verdict:** NEEDS_REFACTOR - Foundation class ảnh hưởng toàn bộ agent.

### `projects/local_proxy_server/core/router.py` — 3/10

| Issue | Severity |
|-------|----------|
| DB logic nhét trong router (SRP violation) | CRITICAL |
| SQLite connection không trong finally | HIGH |
| Rate limit dict grow vô hạn | HIGH |
| Dead code import (HTTPClient) | LOW |
| API key trong URL query param | MEDIUM |
| `/v1/billing` không auth | MEDIUM |

**Verdict:** CRITICAL - Cần tách module ngay.

### `projects/local_proxy_server/core/config.py` — 2.5/10

| Issue | Severity |
|-------|----------|
| Model name hardcode khắp nơi | HIGH |
| Không có validation cho API key | MEDIUM |
| Rotation logic fragile | HIGH |

**Verdict:** CRITICAL - Config mess.

### `scheduler/main_scheduler.py` — 3.5/10

| Issue | Severity |
|-------|----------|
| `schedule.CancelJob` bị nuốt | CRITICAL |
| HTML escape backwards | HIGH |
| ThreadPoolExecutor(max_workers=1) = single point of self-DoS | HIGH |

**Verdict:** NEEDS_REFACTOR - Scheduler chạy vô hạn.

---

## 🎯 KẾT LUẬN CHAOS OVERLORD

> **Gemini 3.1 Pro Preview viết code NHANH nhưng BỀN.** Ưu tiên "make it work" hơn "make it right". Kết quả: tech debt tích tụ, security holes, resource leaks.

> **Điểm sáng:** Logic business đúng, architecture concept tốt (fallback chain, circuit breaker). Nhưng implementation sloppy.

> **Action Plan:**
> 1. Fix 5 critical bugs (Priority 1)
> 2. Refactor `base_agent.py` FAILED_PATHS injection (Priority 2)
> 3. Tách DB logic khỏi `router.py` (Priority 3)

---
*Generated by GLM-5.2 Chaos Overlord Mode | 2026-07-20*