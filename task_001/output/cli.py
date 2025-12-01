from .ioutput import IOutput
from ..models.task import TaskStatus, Task


class CLIOutput(IOutput):
    def _format_task_status(self, status: str) -> str:
        match status:
            case TaskStatus.done.value:
                return "Done"
            case TaskStatus.in_progress.value:
                return "In progress"
            case TaskStatus.planned.value:
                return "Planned"
            case _:
                return "Unknown status"

    def tasks_list(self, tasks_list: list[tuple[int, Task]]):
        print(
            "\n".join(
                [
                    f"{idx} - {self._format_task_status(task.status)} - {task.description}"
                    for idx, task in tasks_list
                ]
            )
        )

    def task_added_success(self, id: int):
        print(f"Task added successfully (ID: {id})")

    def task_updated_success(self, id: int):
        print(f"Task updated successfully (ID: {id})")

    def task_status_updated_success(self, id: int):
        print(f"Task status updated successfully (ID: {id})")

    def task_deleted_success(self, id: int):
        print(f"Task deleted successfully (ID: {id})")

    def error(self, text: str):
        print(f"Error: {text}")

    def error_task_status_not_found(self, key: str):
        self.error(f"Task status index '{key}' not found.")

    def error_index_type(self, index: str):
        self.error(f'Index must be an integer. Received "{index}" instead.')

    def error_storage_type(self, storage_type: str):
        self.error(f"Unknown storage type {storage_type}")

    def error_task_not_found(self, index: int):
        self.error(f'Task "{index}" not found.')
