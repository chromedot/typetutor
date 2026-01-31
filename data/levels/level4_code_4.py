from abc import ABC, abstractmethod
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)

class CacheStrategy(ABC):
    @abstractmethod
    def get(self, key: str) -> Optional[any]:
        pass

    @abstractmethod
    def set(self, key: str, value: any, ttl: int = 3600) -> bool:
        pass

class LRUCache(CacheStrategy):
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._cache: Dict[str, any] = {}
        self._access_order: List[str] = []

    def get(self, key: str) -> Optional[any]:
        if key not in self._cache:
            return None
        self._access_order.remove(key)
        self._access_order.append(key)
        return self._cache[key]

    def set(self, key: str, value: any, ttl: int = 3600) -> bool:
        if len(self._cache) >= self._capacity:
            oldest = self._access_order.pop(0)
            del self._cache[oldest]
        self._cache[key] = value
        self._access_order.append(key)
        return True
