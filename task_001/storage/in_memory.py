from ..models.task import BaseTask, Task, TaskNotFound
from ..storage.istorage import IStorage


class InMemoryStorage(IStorage):
    def __init__(self):
        self.tasks: dict[str, Task] = {}

    async def load(self, counter: int = 0, tasks: dict[str, Task] | None = None) -> dict[str, Task]:
        if tasks != None:
            self.counter = counter
            self.tasks = tasks

        return self.tasks

    async def update_by_idx(self, idx: int, task: Task) -> None:
        try:
            self.tasks[str(idx)] = task
        except KeyError:
            raise TaskNotFound()

    async def delete_by_idx(self, idx: int) -> None:
        try:
            del self.tasks[str(idx)]
        except KeyError:
            raise TaskNotFound()

    async def add(self, task: BaseTask) -> tuple[int, Task]:
        self.counter += 1
        self.tasks[str(self.counter)] = Task(**task.__dict__, id=self.counter)
        return self.counter, self.tasks[str(self.counter)]

    async def get_by_idx(self, idx: int) -> Task:
        try:
            return self.tasks[str(idx)]
        except KeyError:
            raise TaskNotFound()
