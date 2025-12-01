from abc import ABC, abstractmethod

from ..models.task import Task


class IStorage(ABC):
    @abstractmethod
    def load(self) -> list[Task]: ...

    @abstractmethod
    def get_by_idx(self, idx: int) -> Task: ...

    @abstractmethod
    def update_by_idx(self, idx: int, task: Task) -> None: ...

    @abstractmethod
    def delete_by_idx(self, idx: int) -> None: ...

    @abstractmethod
    def add(self, task: Task) -> tuple[int, Task]: ...
