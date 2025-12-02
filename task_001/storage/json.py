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

import asyncio
from dataclasses import asdict
import json
import os
from pathlib import Path

from .in_memory import InMemoryStorage
from .istorage import IStorage
from ..models.task import BaseTask, Task


class JSONStorage(IStorage):
    def __init__(
        self, *, file_location: str = "data/uncategorized.json", cache=InMemoryStorage()
    ):
        self.failed_to_load = False
        self.file_path = (
            Path(os.path.dirname(os.path.realpath(__file__))) / "../" / file_location
        )

        self.cache = cache

    async def _dump(self):
        load_task = asyncio.create_task(self.cache.load())
        store_task = asyncio.create_task(self.store(await load_task))
        await store_task

    async def load(self) -> dict[str, Task]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f) or {
                    "counter": 0,
                    "tasks": {}
                }
                load_task = asyncio.create_task(
                    self.cache.load(
                        data["counter"],
                        {
                            str(task["id"]): Task(
                                id=task["id"],
                                description=task["description"],
                                status=task["status"],
                                createdAt=task["createdAt"],
                                updatedAt=task["updatedAt"],
                            )
                            for task in data["tasks"].values()
                        }
                    )
                )
                return await load_task
        except FileNotFoundError as exc:
            if not self.failed_to_load:
                self.failed_to_load = True
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)
                return await self.load()
            else:
                raise exc

    async def store(self, tasks: dict[str, Task]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump({
                "counter": self.cache.counter,
                "tasks": {task[0]: asdict(task[1]) for task in tasks.items()}
            }, f, indent=2)

    async def get_by_idx(self, idx: int) -> Task:
        load_task = asyncio.create_task(self.load())
        await load_task
        get_task = asyncio.create_task(self.cache.get_by_idx(idx))
        return await get_task

    async def update_by_idx(self, idx: int, task: Task) -> None:
        update_task = asyncio.create_task(self.cache.update_by_idx(idx, task))
        await update_task
        dump_task = asyncio.create_task(self._dump())
        await dump_task

    async def delete_by_idx(self, idx: int) -> None:
        load_task = asyncio.create_task(self.load())
        await load_task
        delete_task = asyncio.create_task(self.cache.delete_by_idx(idx))
        await delete_task
        store_task = asyncio.create_task(self._dump())
        await store_task

    async def add(self, task: BaseTask) -> tuple[int, Task]:
        load_task = asyncio.create_task(self.load())
        await load_task
        add_task = asyncio.create_task(self.cache.add(task))
        res = await add_task
        store_task = asyncio.create_task(self._dump())
        await store_task
        return res
