import hashlib
import json
from pathlib import Path
from typing import Any, Optional
from app.config import settings

class DiskCache:
    """Deterministic JSON file-based cache for API requests and LLM completions."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or settings.cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _generate_key(self, namespace: str, payload: Any) -> str:
        """Create deterministic SHA256 cache key."""
        serialized = json.dumps(payload, sort_keys=True, default=str)
        digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return f"{namespace}_{digest}"

    def get(self, namespace: str, payload: Any) -> Optional[Any]:
        """Retrieve cached value if cache_enabled and item exists."""
        if not settings.cache_enabled:
            return None
        key = self._generate_key(namespace, payload)
        cache_file = self.cache_dir / f"{key}.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    def set(self, namespace: str, payload: Any, value: Any) -> None:
        """Persist result in disk cache."""
        if not settings.cache_enabled:
            return
        key = self._generate_key(namespace, payload)
        cache_file = self.cache_dir / f"{key}.json"
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(value, f, indent=2, ensure_ascii=False, default=str)
        except Exception:
            pass

cache = DiskCache()
