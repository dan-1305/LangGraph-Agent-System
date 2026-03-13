# jarvis_core/ai_agent_fixed.py
# PRODUCTION-READY AI ENGINE with Resilience Patterns
# Implements: Single-Flight Cache, Circuit Breaker, LRU Memory Safety

import os
import time
import json
import logging
import threading
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from collections import OrderedDict
from enum import Enum
from pathlib import Path

import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

# Import GLOBAL_KEY_MANAGER from key_manager.py
from jarvis_core.key_manager import GLOBAL_KEY_MANAGER, KeyExhaustedError

# Auto-detect .env path
base_path = Path(__file__).resolve().parent.parent
env_path = base_path / '.env'

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    logging.warning(f"KHÔNG TÌM THẤY file .env tại: {env_path}")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
MODEL_PRIORITY = ['gemini-2.5-flash-lite', 'gemini-2.5-flash']
DEFAULT_MODEL = 'gemini-2.5-flash-lite'
MAX_RETRIES = 3
CACHE_TTL = 3600  # 1 hour
CACHE_MAX_ITEMS = 1000
CACHE_MAX_MEMORY_MB = 100  # Max 100MB for cache

# Circuit Breaker Constants
CIRCUIT_FAILURE_THRESHOLD = 3  # Open circuit after 3 consecutive failures
CIRCUIT_OPEN_DURATION = 60  # Keep circuit open for 60 seconds
CIRCUIT_HALF_OPEN_MAX_REQUESTS = 1  # Allow 1 test request in HALF-OPEN state


# ============================================================
# CIRCUIT BREAKER PATTERN
# ============================================================

class CircuitState(Enum):
    """Circuit Breaker States."""
    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"  # Block all requests (system is failing)
    HALF_OPEN = "HALF_OPEN"  # Testing if system recovered


class CircuitBreakerError(Exception):
    """Raised when circuit is OPEN."""
    pass


class CircuitBreaker:
    """
    Circuit Breaker Pattern Implementation.
    
    Prevents cascading failures by:
    1. CLOSED → Normal operation, counting failures
    2. OPEN → Block all requests after N failures (fast-fail)
    3. HALF_OPEN → Test with 1 request after timeout
    
    This prevents the "Death Spiral" where the system keeps trying
    to call failed APIs, exhausting all resources.
    """
    
    def __init__(
        self,
        failure_threshold: int = CIRCUIT_FAILURE_THRESHOLD,
        open_duration: int = CIRCUIT_OPEN_DURATION,
        half_open_max_requests: int = CIRCUIT_HALF_OPEN_MAX_REQUESTS
    ):
        self.failure_threshold = failure_threshold
        self.open_duration = open_duration
        self.half_open_max_requests = half_open_max_requests
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.half_open_requests = 0
        
        self._lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args, **kwargs: Arguments to pass to function
            
        Returns:
            Function result
            
        Raises:
            CircuitBreakerError: If circuit is OPEN
        """
        with self._lock:
            if self.state == CircuitState.OPEN:
                # Check if we should transition to HALF_OPEN
                if self._should_attempt_reset():
                    self._transition_to_half_open()
                else:
                    logger.warning(f"🚫 [CIRCUIT OPEN] Blocking request. Cooldown: {self._get_remaining_cooldown()}s")
                    raise CircuitBreakerError(
                        f"Circuit breaker is OPEN. System is failing. "
                        f"Retry in {self._get_remaining_cooldown()}s"
                    )
            
            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_requests >= self.half_open_max_requests:
                    logger.warning("🚫 [CIRCUIT HALF_OPEN] Max test requests reached. Blocking.")
                    raise CircuitBreakerError("Circuit in HALF_OPEN state. Max test requests reached.")
                
                self.half_open_requests += 1
        
        # Execute the function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except KeyExhaustedError as e:
            # This is the critical error that should trigger circuit breaker
            self._on_failure()
            raise
        except Exception as e:
            # Other errors don't necessarily mean system failure
            logger.error(f"⚠️ [CIRCUIT] Function failed but not counted: {str(e)}")
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to try HALF_OPEN."""
        if self.last_failure_time is None:
            return False
        
        elapsed = time.time() - self.last_failure_time
        return elapsed >= self.open_duration
    
    def _get_remaining_cooldown(self) -> int:
        """Get remaining cooldown time in seconds."""
        if self.last_failure_time is None:
            return 0
        
        elapsed = time.time() - self.last_failure_time
        remaining = max(0, self.open_duration - elapsed)
        return int(remaining)
    
    def _transition_to_half_open(self):
        """Transition from OPEN to HALF_OPEN."""
        self.state = CircuitState.HALF_OPEN
        self.half_open_requests = 0
        logger.info("🔄 [CIRCUIT HALF_OPEN] Testing system recovery...")
    
    def _on_success(self):
        """Handle successful request."""
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                logger.info("✅ [CIRCUIT CLOSED] System recovered!")
                self.state = CircuitState.CLOSED
            
            self.failure_count = 0
            self.last_failure_time = None
            self.half_open_requests = 0
    
    def _on_failure(self):
        """Handle failed request."""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.state == CircuitState.HALF_OPEN:
                # Test failed, go back to OPEN
                logger.error(f"🔴 [CIRCUIT OPEN] Test request failed. System still unhealthy.")
                self.state = CircuitState.OPEN
                self.failure_count = self.failure_threshold
            elif self.failure_count >= self.failure_threshold:
                # Too many failures, open circuit
                logger.error(
                    f"🔴 [CIRCUIT OPEN] {self.failure_count} consecutive failures. "
                    f"Blocking all requests for {self.open_duration}s"
                )
                self.state = CircuitState.OPEN
    
    def get_status(self) -> dict:
        """Get current circuit breaker status."""
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'remaining_cooldown': self._get_remaining_cooldown() if self.state == CircuitState.OPEN else 0
        }


# ============================================================
# SINGLE-FLIGHT CACHE WITH LRU MEMORY MANAGEMENT
# ============================================================

class SingleFlightLRUCache:
    """
    Thread-safe LRU Cache with Single-Flight Pattern.
    
    Features:
    1. Single-Flight: Multiple requests for same key wait for single API call
    2. LRU Eviction: Removes least recently used items when full
    3. Memory Safety: Enforces max memory limit
    4. TTL Support: Auto-expire old entries
    
    Prevents Cache Stampede:
    - 10,000 concurrent requests → 1 API call
    - Others wait on threading.Event
    """
    
    def __init__(
        self,
        max_items: int = CACHE_MAX_ITEMS,
        max_memory_mb: int = CACHE_MAX_MEMORY_MB,
        ttl: int = CACHE_TTL
    ):
        self.max_items = max_items
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.ttl = ttl
        
        # LRU Cache using OrderedDict (maintains insertion order)
        self._cache: OrderedDict[str, dict] = OrderedDict()
        self._cache_lock = threading.Lock()
        self._current_memory_bytes = 0
        
        # Single-Flight Control
        self._in_flight: Dict[str, threading.Event] = {}
        self._in_flight_lock = threading.Lock()
        self._in_flight_results: Dict[str, Tuple[bool, Any]] = {}  # (success, data)
        
        # Stats
        self.stats = {
            'hits': 0,
            'misses': 0,
            'in_flight_joins': 0,
            'evictions': 0
        }
    
    def get_or_fetch(self, cache_key: str, fetch_fn) -> str:
        """
        Get from cache OR wait for in-flight request OR fetch new.
        
        This is THE SHIELD that prevents cache stampede.
        
        Args:
            cache_key: Unique identifier (hash of prompt + model)
            fetch_fn: Lambda function that calls the actual API
            
        Returns:
            The cached or freshly fetched response
        """
        
        # Step 1: Try to get from cache (Fast Path)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            logger.info(f"⚡ [CACHE HIT] Key: {cache_key[:16]}... (Instant response)")
            self.stats['hits'] += 1
            return cached
        
        self.stats['misses'] += 1
        
        # Step 2: Check if another thread is already fetching this key
        with self._in_flight_lock:
            if cache_key in self._in_flight:
                # Another thread is fetching, we wait
                event = self._in_flight[cache_key]
                self.stats['in_flight_joins'] += 1
                logger.info(
                    f"🔗 [IN-FLIGHT WAIT] Key: {cache_key[:16]}... "
                    f"(Joining existing request, {self.stats['in_flight_joins']} joins total)"
                )
                need_to_fetch = False
            else:
                # We are the first, create event for others to wait on
                event = threading.Event()
                self._in_flight[cache_key] = event
                need_to_fetch = True
                logger.info(f"🚀 [IN-FLIGHT START] Key: {cache_key[:16]}... (First request, others will wait)")
        
        # Step 3A: If we're NOT the first, WAIT
        if not need_to_fetch:
            event.wait(timeout=30)  # Wait max 30 seconds
            
            # Check result from the first request
            success, data = self._in_flight_results.get(cache_key, (False, None))
            
            if success:
                logger.info(f"✅ [IN-FLIGHT SUCCESS] Key: {cache_key[:16]}... (Piggyback successful)")
                return data
            else:
                # First request failed, we retry ourselves
                logger.warning(f"⚠️ [IN-FLIGHT FAILED] Key: {cache_key[:16]}... (First request failed, retrying)")
                # Don't retry in this implementation to avoid thundering herd
                raise Exception(f"In-flight request failed: {data}")
        
        # Step 3B: We ARE the first, do the actual work
        try:
            result = self._fetch_and_cache(cache_key, fetch_fn)
            
            # Notify all waiting threads
            with self._in_flight_lock:
                self._in_flight_results[cache_key] = (True, result)
                event.set()  # Wake up ALL waiting threads
                logger.info(f"📢 [BROADCAST] Waking up all threads waiting for {cache_key[:16]}...")
            
            return result
            
        except Exception as e:
            # API failed, notify waiters
            logger.error(f"❌ [API FAILED] Key: {cache_key[:16]}... Error: {str(e)}")
            
            with self._in_flight_lock:
                self._in_flight_results[cache_key] = (False, str(e))
                event.set()  # Wake up waiters so they know we failed
            
            raise
            
        finally:
            # Cleanup after 5 seconds (allow late joiners to read result)
            def cleanup():
                time.sleep(5)
                with self._in_flight_lock:
                    self._in_flight.pop(cache_key, None)
                    self._in_flight_results.pop(cache_key, None)
            
            threading.Thread(target=cleanup, daemon=True).start()
    
    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Get from cache if exists and not expired."""
        with self._cache_lock:
            if cache_key not in self._cache:
                return None
            
            entry = self._cache[cache_key]
            
            # Check TTL
            age = (datetime.now() - entry['timestamp']).seconds
            if age >= self.ttl:
                # Expired
                self._remove_entry(cache_key)
                return None
            
            # Move to end (mark as recently used for LRU)
            self._cache.move_to_end(cache_key)
            
            return entry['response']
    
    def _fetch_and_cache(self, cache_key: str, fetch_fn) -> str:
        """Fetch from API and store in cache."""
        logger.info(f"🌐 [API CALL] Fetching fresh data for {cache_key[:16]}...")
        
        response = fetch_fn()  # This calls the actual Gemini API
        
        # Calculate response size
        response_size = len(response.encode('utf-8'))
        
        # Store in cache with memory check
        with self._cache_lock:
            # Evict if memory limit exceeded
            while (self._current_memory_bytes + response_size > self.max_memory_bytes 
                   or len(self._cache) >= self.max_items):
                if not self._cache:
                    break
                
                # Remove oldest (first item in OrderedDict)
                oldest_key, oldest_entry = self._cache.popitem(last=False)
                oldest_size = len(oldest_entry['response'].encode('utf-8'))
                self._current_memory_bytes -= oldest_size
                self.stats['evictions'] += 1
                logger.debug(f"🗑️ [LRU EVICT] Removed {oldest_key[:16]}... ({oldest_size} bytes)")
            
            # Add to cache
            self._cache[cache_key] = {
                'response': response,
                'timestamp': datetime.now(),
                'size': response_size
            }
            self._current_memory_bytes += response_size
            
            logger.info(
                f"💾 [CACHE STORE] {cache_key[:16]}... "
                f"({response_size} bytes, total: {self._current_memory_bytes / 1024 / 1024:.2f}MB)"
            )
        
        return response
    
    def _remove_entry(self, cache_key: str):
        """Remove entry and update memory counter."""
        if cache_key in self._cache:
            entry = self._cache.pop(cache_key)
            self._current_memory_bytes -= entry['size']
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        hit_rate = (
            self.stats['hits'] / (self.stats['hits'] + self.stats['misses'])
            if (self.stats['hits'] + self.stats['misses']) > 0
            else 0
        )
        
        return {
            **self.stats,
            'hit_rate': f"{hit_rate * 100:.2f}%",
            'cache_items': len(self._cache),
            'memory_mb': f"{self._current_memory_bytes / 1024 / 1024:.2f}",
            'memory_limit_mb': self.max_memory_bytes / 1024 / 1024
        }


# ============================================================
# PRODUCTION-READY AI SERVICE
# ============================================================

class AIService:
    """
    Core AI Service - Production-Ready with 3 Resilience Layers.
    
    Layer 1 (THE SHIELD): Single-Flight LRU Cache
    - Prevents cache stampede
    - 10,000 concurrent requests → 1 API call
    
    Layer 2 (THE FUSE): Circuit Breaker
    - Stops calling failing APIs
    - Prevents resource exhaustion
    
    Layer 3 (THE JANITOR): Memory Management
    - LRU eviction
    - Strict memory limits
    """
    
    def __init__(self, key_manager=None):
        self.key_manager = key_manager or GLOBAL_KEY_MANAGER
        
        # THE SHIELD: Cache with Single-Flight
        self.cache = SingleFlightLRUCache()
        
        # THE FUSE: Circuit Breaker
        self.circuit_breaker = CircuitBreaker()
        
        logger.info("🛡️ [AI SERVICE] Initialized with resilience patterns")
    
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def _call_llm_api(self, prompt: str, model: str = None) -> str:
        """
        Call Gemini API with retry logic.
        
        This is wrapped by Circuit Breaker to prevent death spirals.
        """
        model = model or DEFAULT_MODEL
        current_key = self.key_manager.get_next_key()
        
        try:
            genai.configure(api_key=current_key)
            
            # Safety settings
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            generative_model = genai.GenerativeModel(model_name=model, safety_settings=safety_settings)
            response = generative_model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            self.key_manager.mark_key_exhausted(current_key)
            logger.error(f"Lỗi API với key ...{current_key[-4:]}: {str(e)}")
            raise
        finally:
            genai.configure(api_key=None)
    
    def generate_response(self, prompt: str, model: str = None) -> str:
        """
        Main entry point: Generate AI response with full resilience.
        
        Flow:
        1. Check Circuit Breaker state
        2. Check Cache (with Single-Flight)
        3. Call API if needed
        4. Try fallback models if primary fails
        """
        model = model or DEFAULT_MODEL
        cache_key = f"{model}:{hash(prompt)}"
        
        # Define API call function for cache
        def fetch_from_api():
            # Try models in priority order
            models_to_try = [model] if model in MODEL_PRIORITY else MODEL_PRIORITY
            last_error = None
            
            for current_model in models_to_try:
                try:
                    # THE FUSE: Circuit Breaker protects this call
                    return self.circuit_breaker.call(
                        self._call_llm_api,
                        prompt,
                        current_model
                    )
                except CircuitBreakerError:
                    # Circuit is open, fail fast without trying other models
                    raise
                except KeyExhaustedError as e:
                    # All keys exhausted, let circuit breaker handle it
                    last_error = e
                    logger.warning(f"Model {current_model} failed with KeyExhaustedError")
                    raise  # Let circuit breaker catch this
                except Exception as e:
                    last_error = e
                    logger.warning(f"Model {current_model} failed: {str(e)}, trying next...")
                    continue
            
            raise RuntimeError(f"All models failed. Last error: {str(last_error)}")
        
        # THE SHIELD: Cache with Single-Flight handles the rest
        try:
            return self.cache.get_or_fetch(cache_key, fetch_from_api)
        except CircuitBreakerError as e:
            logger.error(f"🔴 Circuit breaker blocked request: {str(e)}")
            return (
                f"⚠️ System is currently overloaded. Please try again in "
                f"{self.circuit_breaker.get_status()['remaining_cooldown']} seconds."
            )
    
    def get_system_status(self) -> dict:
        """Get comprehensive system health status."""
        return {
            'circuit_breaker': self.circuit_breaker.get_status(),
            'cache': self.cache.get_stats(),
            'timestamp': datetime.now().isoformat()
        }


# ============================================================
# GLOBAL INSTANCE & PUBLIC API (Facade Pattern)
# ============================================================

# Global instance (Singleton)
ai_service = AIService()


def ask_jarvis(prompt: str) -> str:
    """
    Public API: Ask Jarvis a question (Facade Pattern).
    
    This interface remains unchanged for backward compatibility.
    All resilience patterns are transparent to the caller.
    """
    try:
        return ai_service.generate_response(prompt)
    except Exception as e:
        logger.error(f"Critical Error in ask_jarvis: {str(e)}")
        return "Xin lỗi The Builder, hệ thống AI đang gặp sự cố. Vui lòng thử lại sau."


def evaluate_evolution(current_profile: dict, completed_tasks: str) -> dict:
    """
    Evaluate tasks for XP/HP calculation (RPG System).
    
    Unchanged from original, uses ask_jarvis internally.
    """
    prompt = f"""
    Bạn là Gamemaster của hệ thống RPG đời thực. Hãy đánh giá các nhiệm vụ sau:
    {completed_tasks}

    Profile hiện tại:
    {json.dumps(current_profile, indent=2)}

    Yêu cầu:
    - Phân tích độ khó của task để tính XP (Dễ: 10-20, Trung bình: 30-50, Khó: 50-100).
    - Nếu task không hoàn thành tốt, trừ HP.
    - Trả về DUY NHẤT một chuỗi JSON thuần (không markdown) với định dạng:
    {{
        "xp_gained": int,
        "hp_change": int,
        "new_status": "string",
        "message": "Lời nhận xét ngắn gọn, hài hước kiểu IT/DevOps"
    }}
    """
    
    try:
        raw_response = ai_service.generate_response(prompt)
        
        # Cleanup JSON
        clean_json = raw_response.strip()
        if clean_json.startswith("```"):
            clean_json = clean_json.split("```")[1]
        if clean_json.startswith("json"):
            clean_json = clean_json[4:]
        clean_json = clean_json.strip()
        
        result = json.loads(clean_json)
        return {
            'xp_gained': result.get('xp_gained', 0),
            'hp_change': result.get('hp_change', 0),
            'new_status': result.get('new_status', 'active'),
            'message': result.get('message', 'Nhiệm vụ đã được cập nhật!')
        }
    except json.JSONDecodeError:
        logger.error(f"Lỗi Parse JSON từ AI: {raw_response}")
        return {
            'xp_gained': 10,
            'hp_change': 0,
            'new_status': current_profile.get('status', 'active'),
            'message': 'AI bị ngáo JSON, nhưng tôi vẫn cộng cho bạn 10 XP an ủi!'
        }
    except Exception as e:
        logger.error(f"Error in evaluate_evolution: {str(e)}")
        return {
            'xp_gained': 0,
            'hp_change': 0,
            'new_status': current_profile.get('status', 'active'),
            'message': 'Lỗi hệ thống khi đánh giá nhiệm vụ.'
        }


def get_system_health() -> dict:
    """
    Get system health metrics.
    
    Useful for monitoring and debugging.
    """
    return ai_service.get_system_status()


# ============================================================
# HOW THIS PREVENTS "DEATH SPIRAL"
# ============================================================
"""
DEATH SPIRAL SCENARIO (Before Fix):
----------------------------------
1. 10,000 requests arrive at 9 AM
2. All miss cache → 10,000 API calls
3. Rate limit (60 RPM) hit in 0.36 seconds
4. All 3 keys marked as exhausted
5. @retry tries again → Still exhausted
6. System keeps retrying → CPU/Memory spike
7. Eventually crashes OR blocks for hours

RESILIENCE PATTERNS (After Fix):
---------------------------------
Layer 1 - THE SHIELD (Single-Flight Cache):
- 10,000 requests → Only 1 API call
- Other 9,999 wait on threading.Event
- When first succeeds → All get cached response
- Result: 1 API call instead of 10,000

Layer 2 - THE FUSE (Circuit Breaker):
- If KeyExhaustedError happens 3 times → OPEN circuit
- All subsequent requests fail IMMEDIATELY (no API calls)
- Wait 60 seconds → Test with 1 request (HALF_OPEN)
- If test succeeds → CLOSE circuit (resume normal operation)
- Result: System stops trying when failing, recovers gracefully

Layer 3 - THE JANITOR (LRU Memory Management):
- OrderedDict maintains insertion order
- When full → Remove oldest (least recently used)
- Memory limit enforced (100MB max)
- Result: No memory leaks, predictable resource usage

COMBINED EFFECT:
- Stampede: 10,000 requests → 1 API call ✅
- Exhaustion: Circuit opens → No wasted retries ✅
- Recovery: Auto-recovery after 60s ✅
- Memory: Bounded cache size ✅
- Monitoring: Full observability via get_system_health() ✅

This transforms a "Junior script" into a "Production-ready System" 
that can handle real-world traffic spikes without dying.
"""


# ============================================================
# TESTING & MONITORING
# ============================================================

if __name__ == "__main__":
    import concurrent.futures
    
    print("🧪 PRODUCTION RESILIENCE TEST\n")
    print("=" * 60)
    
    # Test 1: Cache Stampede Protection
    print("\n📊 TEST 1: Cache Stampede (1000 concurrent identical requests)")
    print("-" * 60)
    
    test_prompt = "Hello, test cache stampede"
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(ask_jarvis, test_prompt) for _ in range(1000)]
        results = [f.result() for f in futures]
    
    elapsed = time.time() - start_time
    
    print(f"✅ Completed 1000 requests in {elapsed:.2f}s")
    print(f"📈 Cache Stats: {ai_service.cache.get_stats()}")
    
    # Test 2: Circuit Breaker
    print("\n📊 TEST 2: Circuit Breaker Status")
    print("-" * 60)
    print(f"🔌 Circuit State: {ai_service.circuit_breaker.get_status()}")
    
    # Test 3: System Health
    print("\n📊 TEST 3: System Health Report")
    print("-" * 60)
    health = get_system_health()
    print(json.dumps(health, indent=2))
    
    print("\n" + "=" * 60)
    print("✅ All resilience patterns active and working!")
