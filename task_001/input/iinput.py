from abc import ABC, abstractmethod
from typing import Callable

from ..models.task import TaskStatus


class IInput(ABC):
    def set_add_handler(self, callback: Callable[[str], None]) -> None: ...

    def set_list_handler(
        self, callback: Callable[[TaskStatus | None], None]
    ) -> None: ...

    def set_update_handler(self, callback: Callable[[int, str], None]) -> None: ...

    def set_status_handler(
        self, callback: Callable[[int, TaskStatus], None]
    ) -> None: ...

    def set_delete_handler(self, callback: Callable[[int], None]) -> None: ...

    def set_error_handler(self, callback: Callable[[str], None]) -> None: ...

    def start(self) -> None: ...
