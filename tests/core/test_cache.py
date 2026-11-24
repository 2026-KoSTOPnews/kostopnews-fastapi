import time

from app.core.cache import TTLCache


def test_cache_set_and_get():
    cache = TTLCache()

    cache.set("test", {"value": 100})

    assert cache.get("test") == {"value": 100}


def test_cache_expiration():
    cache = TTLCache()

    cache.set("test", {"value": 100}, ttl=1)

    time.sleep(1.1)

    assert cache.get("test") is None


def test_cache_clear():
    cache = TTLCache()

    cache.set("test", {"value": 100})
    cache.clear()

    assert cache.get("test") is None


def test_cache_returns_independent_copy():
    cache = TTLCache()

    original = {"words": ["news"]}
    cache.set("test", original)

    result = cache.get("test")
    result["words"].append("changed")

    assert cache.get("test") == {"words": ["news"]}