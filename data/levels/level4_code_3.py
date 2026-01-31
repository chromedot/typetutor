import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Awaitable

class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    id: str
    priority: int
    status: Status = Status.PENDING

class TaskScheduler:
    def __init__(self, max_concurrent: int = 5):
        self._queue: List[Task] = []
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._results: Dict[str, any] = {}

    async def execute(self, task: Task, func: Callable[[], Awaitable]) -> None:
        async with self._semaphore:
            task.status = Status.RUNNING
            try:
                result = await func()
                self._results[task.id] = result
                task.status = Status.COMPLETED
            except Exception as e:
                task.status = Status.FAILED
                raise
