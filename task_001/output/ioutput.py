from abc import ABC, abstractmethod
from ..models.task import Task


class IOutput(ABC):
    @abstractmethod
    async def tasks_list(self, tasks_list: list[tuple[int, Task]]): ...

    @abstractmethod
    async def task_added_success(self, id: int): ...

    @abstractmethod
    async def task_updated_success(self, id: int): ...

    @abstractmethod
    async def task_status_updated_success(self, id: int): ...

    @abstractmethod
    async def task_deleted_success(self, id: int): ...

    @abstractmethod
    async def error_task_not_found(self, index: int): ...

    @abstractmethod
    async def error_task_status_not_found(self, key: str): ...

    @abstractmethod
    async def error_index_type(self, index: str): ...

    @abstractmethod
    async def error_storage_type(self, storage_type: str): ...

    @abstractmethod
    async def error(self, text: str): ...
