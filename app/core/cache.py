from copy import deepcopy
from threading import Lock
from time import monotonic

import logging

logger = logging.getLogger(__name__)

class TTLCache:
    def __init__(self, max_entries: int = 100):
        self._store = {}
        self._lock = Lock()
        self._max_entries = max_entries

    def get(self, key):
        with self._lock:
            item = self._store.get(key)

            if item is None:
                logger.debug("Cache MISS: %s", key)
                return None

            expires_at, value = item

            if monotonic() >= expires_at:
                del self._store[key]
                logger.debug("Cache EXPIRED: %s", key)
                return None

            logger.debug("Cache HIT: %s", key)
            return deepcopy(value)

    def set(self, key, value, ttl: int = 300):
        with self._lock:
            now = monotonic()

            # 만료된 캐시 정리
            expired_keys = [
                key for key, (expires_at, _) in self._store.items()
                if now >= expires_at
            ]

            for expired_key in expired_keys:
                del self._store[expired_key]

            # 기존 키가 아닌 새로운 키이고 최대 개수에 도달한 경우
            if key not in self._store and len(self._store) >= self._max_entries:
                oldest_key = next(iter(self._store))
                del self._store[oldest_key]
                logger.info("Cache EVICTED (FIFO): %s", oldest_key)

            self._store[key] = (
                now + ttl,
                deepcopy(value),
            )

            logger.debug("Cache SET: %s (TTL: %s)", key, ttl)

    def clear(self):
        with self._lock:
            self._store.clear()

    def invalidate(self, prefix: str):
        """특정 데이터 유형의 캐시만 초기화한다."""
        with self._lock:
            keys = [
                key
                for key in self._store
                if isinstance(key, tuple) and key[0] == prefix
            ]

            for key in keys:
                del self._store[key]

            logger.info(
                "Cache INVALIDATED: prefix=%s, count=%d",
                prefix,
                len(keys),
            )

cache = TTLCache(max_entries=100)