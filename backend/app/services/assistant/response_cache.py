"""
AgroScan AI — Response Cache Service
Implements secure, question-and-context aware in-memory caching with TTL and dynamic invalidation.
Prevents serving identical answers to different questions by incorporating normalized question,
intent, language, and context hashes into the cache key.
"""

import hashlib
import time
from typing import Dict, Any, Optional

class ResponseCache:
    """In-memory cache keyed by question content, intent, language, and active context."""

    _cache: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def generate_cache_key(
        cls,
        user_id: Optional[str],
        normalized_question: str,
        intent: str,
        language: str,
        plant_name: Optional[str] = None,
        disease_name: Optional[str] = None,
        location_key: Optional[str] = None
    ) -> str:
        raw_key = (
            f"uid:{user_id or 'anon'}|"
            f"q:{normalized_question.lower().strip()}|"
            f"intent:{intent}|"
            f"lang:{language}|"
            f"plant:{plant_name or 'none'}|"
            f"disease:{disease_name or 'none'}|"
            f"loc:{location_key or 'none'}"
        )
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    @classmethod
    def get(cls, cache_key: str) -> Optional[Dict[str, Any]]:
        entry = cls._cache.get(cache_key)
        if not entry:
            return None
        # Check expiry
        if time.time() > entry["expires_at"]:
            cls._cache.pop(cache_key, None)
            return None
        return entry["payload"]

    @classmethod
    def set(
        cls,
        cache_key: str,
        payload: Dict[str, Any],
        ttl_seconds: int = 3600
    ) -> None:
        # Avoid caching if payload has error or is empty
        if not payload or not payload.get("answer"):
            return
        cls._cache[cache_key] = {
            "payload": payload,
            "expires_at": time.time() + ttl_seconds
        }

    @classmethod
    def clear(cls) -> None:
        cls._cache.clear()
