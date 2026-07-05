"""
Lightweight Unit Test for RotationManager logic.

Run: uv run --directory projects/local_proxy_server python tests/test_proxy.py

Tests:
1. Basic credential dispatch (key, model) pair
2. Mark exhausted + verify skip
3. Fallback to alternative model when requested model's keys are depleted
4. Full exhaustion -> RuntimeError
"""
import sys
from pathlib import Path

# Add core to path so we can import directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.rotation_manager import RotationManager
from core.config import Settings


def make_manager(num_keys: int = 4) -> RotationManager:
    """Build a RotationManager with a fake Settings containing N keys."""
    settings = Settings.__new__(Settings)
    settings.gemini_api_keys = [f"FAKE_KEY_{i:02d}" for i in range(num_keys)]
    settings.default_model = "gemini-3.1-flash-lite"
    settings.model_mapping = {
        "gemini-3.5-flash": "gemini-3.5-flash",
        "gemini-3.1-flash-lite": "gemini-3.1-flash-lite",
        "gemma-4-26b-a4b-it": "gemma-4-26b-a4b-it",
        "default": "gemini-3.1-flash-lite",
    }
    settings.label_mapping = {"manual": "manual-block"}
    settings.high_quota_models = ["gemini-3.1-flash-lite", "gemma-4-26b-a4b-it"]
    settings.standard_models = ["gemini-3.5-flash"]
    settings.model_rotation_pool = settings.high_quota_models + settings.standard_models

    mgr = RotationManager.__new__(RotationManager)
    mgr.settings = settings
    mgr.model_key_indices = {}
    mgr.exhausted_pairs = set()
    mgr._last_reset_day = 0
    return mgr


def test_basic_dispatch():
    """Test 1: Basic credential dispatch returns a valid pair."""
    print("\n=== TEST 1: Basic Credential Dispatch ===")
    mgr = make_manager(num_keys=4)
    key, model = mgr.get_valid_credential("gemini-3.1-flash-lite")
    assert model == "gemini-3.1-flash-lite", f"Expected gemini-3.1-flash-lite, got {model}"
    assert key.startswith("FAKE_KEY_"), f"Expected FAKE_KEY_*, got {key}"
    print(f"  [OK] Dispatched: Model={model} | Key={key}")
    print("  PASSED")


def test_mark_exhausted_skip():
    """Test 2: Marked pair is skipped on next dispatch."""
    print("\n=== TEST 2: Mark Exhausted + Skip ===")
    mgr = make_manager(num_keys=4)
    key0, model0 = mgr.get_valid_credential("gemini-3.1-flash-lite")
    mgr.mark_exhausted(key0, model0)
    print(f"  Marked exhausted: ({key0}, {model0})")

    key1, model1 = mgr.get_valid_credential("gemini-3.1-flash-lite")
    assert key1 != key0, f"Expected different key after exhaustion, got same {key0}"
    print(f"  [OK] Next dispatch skipped exhausted: New Key={key1}")
    print("  PASSED")


def test_fallback_to_alternative_model():
    """Test 3: When all keys of requested model die, fallback to alternative model."""
    print("\n=== TEST 3: Fallback to Alternative Model ===")
    mgr = make_manager(num_keys=2)

    # Exhaust all keys for the requested model
    for i in range(2):
        key, model = mgr.get_valid_credential("gemini-3.1-flash-lite")
        assert model == "gemini-3.1-flash-lite"
        mgr.mark_exhausted(key, model)
        print(f"  Exhausted: ({key}, {model})")

    # Next dispatch should fallback to another model
    key, model = mgr.get_valid_credential("gemini-3.1-flash-lite")
    assert model != "gemini-3.1-flash-lite", f"Expected fallback model, got {model}"
    print(f"  [OK] Fell back to alternative: Model={model} | Key={key}")
    print("  PASSED")


def test_full_exhaustion():
    """Test 4: All pairs exhausted -> RuntimeError."""
    print("\n=== TEST 4: Full Exhaustion ===")
    mgr = make_manager(num_keys=2)

    total_pairs = 2 * len(mgr.settings.model_rotation_pool)  # 2 keys x 3 models = 6
    print(f"  Total pairs available: {total_pairs}")

    for i in range(total_pairs):
        key, model = mgr.get_valid_credential("gemini-3.1-flash-lite")
        mgr.mark_exhausted(key, model)

    try:
        mgr.get_valid_credential("gemini-3.1-flash-lite")
        print("  [FAIL] Should have raised RuntimeError")
        assert False, "RuntimeError not raised"
    except RuntimeError as e:
        print(f"  [OK] Correctly raised RuntimeError: {str(e)[:60]}...")
        print("  PASSED")


def test_stats():
    """Test 5: get_stats returns accurate counts."""
    print("\n=== TEST 5: Stats Accuracy ===")
    mgr = make_manager(num_keys=4)
    stats = mgr.get_stats()
    print(f"  Initial: {stats['remaining_pairs']}/{stats['total_available_pairs']} remaining")

    key, model = mgr.get_valid_credential("gemini-3.1-flash-lite")
    mgr.mark_exhausted(key, model)

    stats2 = mgr.get_stats()
    assert stats2["exhausted_pairs_count"] == 1, f"Expected 1 exhausted, got {stats2['exhausted_pairs_count']}"
    print(f"  [OK] After 1 exhaustion: {stats2['exhausted_pairs_count']} exhausted")
    print("  PASSED")


if __name__ == "__main__":
    print("=" * 60)
    print("ROTATION MANAGER UNIT TESTS")
    print("=" * 60)

    passed = 0
    failed = 0

    for test_func in [test_basic_dispatch, test_mark_exhausted_skip,
                      test_fallback_to_alternative_model, test_full_exhaustion, test_stats]:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {e}")
            failed += 1
        except Exception as e:
            print(f"  [ERROR] {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)