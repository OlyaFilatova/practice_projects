from abc import ABC, abstractmethod
from ..models.task import Task


class IOutput(ABC):
    @abstractmethod
    def tasks_list(self, tasks_list: list[tuple[int, Task]]): ...

    @abstractmethod
    def task_added_success(self, id: int): ...

    @abstractmethod
    def task_updated_success(self, id: int): ...

    @abstractmethod
    def task_status_updated_success(self, id: int): ...

    @abstractmethod
    def task_deleted_success(self, id: int): ...

    @abstractmethod
    def error_task_not_found(self, index: int): ...

    @abstractmethod
    def error_task_status_not_found(self, key: str): ...

    @abstractmethod
    def error_index_type(self, index: str): ...

    @abstractmethod
    def error_storage_type(self, storage_type: str): ...

    @abstractmethod
    def error(self, text: str): ...
