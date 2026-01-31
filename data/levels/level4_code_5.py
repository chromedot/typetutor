from functools import wraps, lru_cache
from datetime import datetime, timedelta
import threading

def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

class RateLimiter:
    def __init__(self, max_requests: int, window: timedelta):
        self._max_requests = max_requests
        self._window = window
        self._requests: Dict[str, List[datetime]] = defaultdict(list)
        self._lock = threading.Lock()

    def is_allowed(self, identifier: str) -> bool:
        with self._lock:
            now = datetime.now()
            cutoff = now - self._window
            self._requests[identifier] = [
                ts for ts in self._requests[identifier] if ts > cutoff
            ]
            if len(self._requests[identifier]) < self._max_requests:
                self._requests[identifier].append(now)
                return True
            return False
