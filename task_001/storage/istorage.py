from abc import ABC, abstractmethod

from ..models.task import Task


class IStorage(ABC):
    @abstractmethod
    async def load(self) -> list[Task]: ...

    @abstractmethod
    async def get_by_idx(self, idx: int) -> Task: ...

    @abstractmethod
    async def update_by_idx(self, idx: int, task: Task) -> None: ...

    @abstractmethod
    async def delete_by_idx(self, idx: int) -> None: ...

    @abstractmethod
    async def add(self, task: Task) -> tuple[int, Task]: ...
