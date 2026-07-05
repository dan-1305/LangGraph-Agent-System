"""
Rotation Manager Module - Smart State Manager for API Key & Model Rotation.

This module tracks which (key, model) pairs have been exhausted (429/503),
and intelligently dispatches the next valid credential pair. When a specific
model runs out of keys, it automatically falls back to other models in the
global fallback pool to maximize Free Tier utilization.
"""
from typing import Dict, Tuple, Set, List
from .config import get_settings


class RotationManager:
    """
    Smart dispatcher: rotates API Keys per-model and falls back to alternative
    models when the requested model is completely exhausted.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

        # Tracks the current key index for each model independently to avoid
        # cross-model conflicts. Format: { "model_name": current_key_index }
        self.model_key_indices: Dict[str, int] = {}

        # Dict tracking exhaustion: { (key, model): {"count": int, "exhaust_time": float} }
        self.exhausted_records: Dict[Tuple[str, str], Dict] = {}

        # Optional: track last reset day to auto-reset pool at UTC midnight.
        self._last_reset_day: int = 0

    def _is_exhausted(self, key: str, model: str) -> bool:
        import time
        record = self.exhausted_records.get((key, model))
        if not record:
            return False
            
        now = time.time()
        count = record["count"]
        exhaust_time = record["exhaust_time"]
        
        # Exponential Backoff: 60s -> 5m (300s) -> 1h (3600s)
        if count == 1:
            cooldown = 60
        elif count == 2:
            cooldown = 300
        else:
            cooldown = 3600
            
        if now - exhaust_time > cooldown:
            # Time has passed, we can try this key again.
            # But we don't clear the count yet, if it fails again it will increment.
            # If it succeeds, ideally it should be reset, but router currently doesn't call a success method.
            # For now, just allow it.
            return False
            
        return True

    def get_valid_credential(self, requested_model: str) -> Tuple[str, str]:
        """
        Find a valid (Key, Model) pair that still has quota.

        If the requested model has exhausted all its keys, automatically
        fall back to other models in the global fallback pool.

        Args:
            requested_model: The model name requested by the client.

        Returns:
            Tuple of (api_key, model_name).

        Raises:
            RuntimeError: If all keys and all models are exhausted.
        """
        self._maybe_auto_reset()

        target_model: str = self.settings.map_model(requested_model)
        available_keys: List[str] = self.settings.gemini_api_keys

        # Build candidate list: requested model first, then fallback pool
        model_candidates: List[str] = [target_model]
        for m in self.settings.model_rotation_pool:
            if m not in model_candidates:
                model_candidates.append(m)

        for model in model_candidates:
            if model not in self.model_key_indices:
                self.model_key_indices[model] = 0

            start_index: int = self.model_key_indices[model]
            num_keys: int = len(available_keys)

            for i in range(num_keys):
                current_idx: int = (start_index + i) % num_keys
                potential_key: str = available_keys[current_idx]

                if not self._is_exhausted(potential_key, model):
                    self.model_key_indices[model] = current_idx
                    return potential_key, model

        raise RuntimeError(
            "All credentials exhausted: every (key, model) pair is rate-limited and in cooldown. "
            "Please wait for Exponential Backoff (60s -> 5m -> 1h) or UTC 00:00 reset."
        )

    def mark_exhausted(self, key: str, model: str) -> None:
        """
        Mark a (key, model) pair as quota-exhausted so it is skipped in
        subsequent dispatches. Also advances the model's key index.
        Applies Exponential Backoff count tracking.
        """
        import time
        record = self.exhausted_records.get((key, model))
        if not record:
            self.exhausted_records[(key, model)] = {"count": 1, "exhaust_time": time.time()}
        else:
            # Increment count, max out at 3 (1 hour cooldown)
            new_count = min(3, record["count"] + 1)
            self.exhausted_records[(key, model)] = {"count": new_count, "exhaust_time": time.time()}
            
        print(f"[RotationManager] Mark exhausted: Model={model}, Key={key[:6]}... Count={self.exhausted_records[(key, model)]['count']}")
        
        if model in self.model_key_indices:
            num_keys: int = len(self.settings.gemini_api_keys)
            self.model_key_indices[model] = (
                self.model_key_indices[model] + 1
            ) % num_keys

    def reset_quota_pool(self) -> None:
        """Clear all exhausted records. Call at UTC midnight or manually."""
        self.exhausted_records.clear()
        self.model_key_indices.clear()
        print("[RotationManager] Quota pool reset - all pairs available again.")

    def _maybe_auto_reset(self) -> None:
        """Auto-reset pool when the calendar day changes (UTC)."""
        import time
        current_day: int = int(time.time() // 86400)
        if self._last_reset_day == 0:
            self._last_reset_day = current_day
        elif current_day > self._last_reset_day:
            print("[RotationManager] New UTC day detected - auto-resetting quota pool.")
            self.reset_quota_pool()
            self._last_reset_day = current_day

    def get_stats(self) -> Dict:
        """Return current rotation statistics for monitoring."""
        total_pairs: int = len(self.settings.gemini_api_keys) * len(
            self.settings.model_rotation_pool
        )
        active_exhausted = [
            (k, m) for (k, m) in self.exhausted_records.keys()
            if self._is_exhausted(k, m)
        ]
        return {
            "total_available_pairs": total_pairs,
            "exhausted_pairs_count": len(active_exhausted),
            "remaining_pairs": total_pairs - len(active_exhausted),
            "exhausted_pairs": [
                {"key": k[:10] + "...", "model": m, "count": self.exhausted_records[(k, m)]["count"]}
                for k, m in active_exhausted
            ],
        }


# Global singleton instance
_rotation_manager: RotationManager | None = None


def get_rotation_manager() -> RotationManager:
    """Get the global RotationManager singleton."""
    global _rotation_manager
    if _rotation_manager is None:
        _rotation_manager = RotationManager()
    return _rotation_manager