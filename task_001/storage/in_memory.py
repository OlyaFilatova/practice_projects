from ..models.task import Task, TaskNotFound
from ..storage.istorage import IStorage


class InMemoryStorage(IStorage):
    def __init__(self):
        self.tasks = []

    async def load(self, tasks: list[Task] | None = None) -> list[Task]:
        if tasks != None:
            self.tasks = tasks

        return self.tasks

    async def update_by_idx(self, idx: int, task: Task) -> None:
        try:
            self.tasks[idx] = task
        except IndexError:
            raise TaskNotFound()

    async def delete_by_idx(self, idx: int) -> None:
        try:
            del self.tasks[idx]
        except IndexError:
            raise TaskNotFound()

    async def add(self, task: Task) -> tuple[int, Task]:
        self.tasks.append(task)
        return (len(self.tasks) - 1, self.tasks[-1])

    async def get_by_idx(self, idx: int) -> Task:
        try:
            return self.tasks[idx]
        except IndexError:
            raise TaskNotFound()
