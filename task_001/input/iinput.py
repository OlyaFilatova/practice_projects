from abc import ABC
from types import CoroutineType
from typing import Any, Callable

from ..models.task import TaskStatus


class IInput(ABC):
    def set_add_handler(self, callback: Callable[[str], CoroutineType[Any, Any, None]]) -> None: ...

    def set_list_handler(
        self, callback: Callable[[TaskStatus | None], CoroutineType[Any, Any, None]]
    ) -> None: ...

    def set_update_handler(self, callback: Callable[[int, str], CoroutineType[Any, Any, None]]) -> None: ...

    def set_status_handler(
        self, callback: Callable[[int, TaskStatus], CoroutineType[Any, Any, None]]
    ) -> None: ...

    def set_delete_handler(self, callback: Callable[[int], CoroutineType[Any, Any, None]]) -> None: ...

    def set_error_handler(self, callback: Callable[[str], CoroutineType[Any, Any, None]]) -> None: ...

    def start(self) -> CoroutineType[Any, Any, None]: ...
