from functools import wraps
from dataclasses import dataclass


@dataclass
class HealthStats:
    success: int = 0
    failure: int = 0

    def total(self) -> int:
        return self.success + self.failure

    def reset(self) -> None:
        self.success = 0
        self.failure = 0

    def __len__(self) -> int:
        return self.total()


health_stats = HealthStats()


def track_health():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                health_stats.success += 1
                return result
            except Exception as e:
                health_stats.failure += 1
                raise e
        return wrapper
    return decorator
