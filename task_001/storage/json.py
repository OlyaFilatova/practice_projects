"""
JSON file structure:

[
    task:
        description: str
        status: "Done" | "In progress" | "Planned"
        updatedAt: float
        createdAt: float
]
"""

from dataclasses import asdict
import json
import os
from pathlib import Path

from .in_memory import InMemoryStorage
from .istorage import IStorage
from ..models.task import Task


class JSONStorage(IStorage):
    def __init__(
        self, *, file_location: str = "data/uncategorized.json", cache=InMemoryStorage()
    ):
        self.failed_to_load = False
        self.file_path = (
            Path(os.path.dirname(os.path.realpath(__file__))) / "../" / file_location
        )

        self.cache = cache

    def _dump(self):
        self.store(self.cache.load())

    def load(self) -> list[Task]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return self.cache.load(
                    [
                        Task(
                            description=task["description"],
                            status=task["status"],
                            createdAt=task["createdAt"],
                            updatedAt=task["updatedAt"],
                        )
                        for task in (json.load(f) or [])
                    ]
                )
        except FileNotFoundError as exc:
            if not self.failed_to_load:
                self.failed_to_load = True
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)
                return self.load()
            else:
                raise exc

    def store(self, tasks: list[Task]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([asdict(task) for task in tasks], f, indent=2)

    def get_by_idx(self, idx: int) -> Task:
        self.load()
        return self.cache.get_by_idx(idx)

    def update_by_idx(self, idx: int, task: Task) -> None:
        self.cache.update_by_idx(idx, task)
        self._dump()

    def delete_by_idx(self, idx: int) -> None:
        self.load()
        self.cache.delete_by_idx(idx)
        self._dump()

    def add(self, task: Task) -> tuple[int, Task]:
        self.load()
        res = self.cache.add(task)
        self._dump()
        return res
