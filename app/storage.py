"""Penyimpanan in-memory untuk Task."""
from typing import Dict, List, Optional

from .models import Task


class TaskStorage:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add(self, title, description="", priority="medium") -> Task:
        task = Task(id=self._next_id, title=title.strip(),
                    description=description, priority=priority)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list(self, done: Optional[bool] = None, priority: Optional[str] = None) -> List[Task]:
        items = list(self._tasks.values())
        if done is not None:
            items = [t for t in items if t.done == done]
        if priority is not None:
            items = [t for t in items if t.priority == priority]
        return items

    def update(self, task_id: int, **fields) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        for key, value in fields.items():
            if hasattr(task, key) and key not in ("id", "created_at"):
                setattr(task, key, value.strip() if key == "title" else value)
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None
