"""Model data untuk TaskTracker."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    priority: str = "medium"
    done: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return asdict(self)
