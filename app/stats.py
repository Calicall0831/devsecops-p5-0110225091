"""Fungsi statistik ringkas untuk daftar tugas."""
from typing import Iterable

from .models import Task, VALID_PRIORITIES


def summarize(tasks: Iterable[Task]) -> dict:
    tasks = list(tasks)
    total = len(tasks)
    done = sum(1 for t in tasks if t.done)
    by_priority = {p: 0 for p in VALID_PRIORITIES}
    for t in tasks:
        by_priority[t.priority] += 1
    completion = round(done / total * 100, 1) if total else 0.0
    return {
        "total": total,
        "done": done,
        "pending": total - done,
        "completion_rate": completion,
        "by_priority": by_priority,
    }
