import asyncio
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

    async def tasks_list(self, tasks_list: list[tuple[int, Task]]):
        print(
            "\n".join(
                [
                    f"{idx} - {self._format_task_status(task.status)} - {task.description}"
                    for idx, task in tasks_list
                ]
            )
        )

    async def task_added_success(self, id: int):
        print(f"Task added successfully (ID: {id})")

    async def task_updated_success(self, id: int):
        print(f"Task updated successfully (ID: {id})")

    async def task_status_updated_success(self, id: int):
        print(f"Task status updated successfully (ID: {id})")

    async def task_deleted_success(self, id: int):
        print(f"Task deleted successfully (ID: {id})")

    async def error(self, text: str):
        print(f"Error: {text}")

    async def error_task_status_not_found(self, key: str):
        output_task = asyncio.create_task(self.error(f"Task status index '{key}' not found."))
        await output_task

    async def error_index_type(self, index: str):
        output_task = asyncio.create_task(self.error(f'Index must be an integer. Received "{index}" instead.'))
        await output_task

    async def error_storage_type(self, storage_type: str):
        output_task = asyncio.create_task(self.error(f"Unknown storage type {storage_type}"))
        await output_task

    async def error_task_not_found(self, index: int):
        output_task = asyncio.create_task(self.error(f'Task "{index}" not found.'))
        await output_task
