import time
import asyncio

from ..input.cli import CLIInput
from ..input.iinput import IInput


from ..models.task import TaskNotFound, TaskStatus, Task
from ..output.cli import CLIOutput
from ..output.ioutput import IOutput
from ..storage.istorage import IStorage
from ..storage.in_memory import InMemoryStorage


class TaskManager:
    def __init__(
        self,
        *,
        storage_manager: IStorage,
        output_manager: IOutput,
        input_manager: IInput
    ):
        self.storage_manager = storage_manager
        self.output_manager = output_manager
        self.input_manager = input_manager

        self.input_manager.set_list_handler(self.list_tasks)
        self.input_manager.set_add_handler(self.create_task)
        self.input_manager.set_status_handler(self.change_status)
        self.input_manager.set_update_handler(self.update_task)
        self.input_manager.set_delete_handler(self.delete_task)

    async def list_tasks(self, status: TaskStatus | None = None) -> None:
        storage_task = asyncio.create_task(self.storage_manager.load())
        tasks = await storage_task
        tasks_list = [
            task for task in enumerate(tasks) if not status or task[1].status == status
        ]

        output_task = asyncio.create_task(self.output_manager.tasks_list(tasks_list))
        await output_task

    async def create_task(self, description: str):
        storage_task = asyncio.create_task(
            self.storage_manager.add(
                Task(
                    description=description,
                    status=TaskStatus.planned,
                    createdAt=time.time(),
                    updatedAt=time.time(),
                )
            )
        )
        idx, _ = await storage_task

        output_task = asyncio.create_task(self.output_manager.task_added_success(idx))
        await output_task

    async def change_status(self, idx: int, status: TaskStatus) -> None:
        try:
            storage_task = asyncio.create_task(self.storage_manager.get_by_idx(idx))
            task = await storage_task
        except TaskNotFound:
            output_task = asyncio.create_task(
                self.output_manager.error_task_not_found(idx)
            )
            await output_task
        else:
            output_task = asyncio.create_task(
                self.output_manager.task_status_updated_success(idx)
            )
            await output_task

            task.status = status
            task.updatedAt = time.time()

            storage_task = asyncio.create_task(
                self.storage_manager.update_by_idx(idx, task)
            )
            await storage_task

    async def update_task(self, idx: int, description: str) -> None:
        try:
            storage_task = asyncio.create_task(self.storage_manager.get_by_idx(idx))
            task = await storage_task
        except TaskNotFound:
            output_task = asyncio.create_task(
                self.output_manager.error_task_not_found(idx)
            )
            await output_task
        else:
            task.description = description
            task.updatedAt = time.time()

            storage_task = asyncio.create_task(
                self.storage_manager.update_by_idx(idx, task)
            )
            await storage_task
            output_task = asyncio.create_task(
                self.output_manager.task_updated_success(idx)
            )
            await output_task

    async def delete_task(self, idx: int) -> None:
        try:
            storage_task = asyncio.create_task(self.storage_manager.delete_by_idx(idx))
            await storage_task
        except TaskNotFound:
            output_task = asyncio.create_task(
                self.output_manager.error_task_not_found(idx)
            )
            await output_task
        else:
            output_task = asyncio.create_task(
                self.output_manager.task_deleted_success(idx)
            )
            await output_task


if __name__ == "__main__":

    async def test():
        task_manager = TaskManager(
            storage_manager=InMemoryStorage(),
            output_manager=CLIOutput(),
            input_manager=CLIInput(),
        )
        test_tasks = [
            task_manager.list_tasks(),
            task_manager.create_task("First ever task"),
            task_manager.create_task("Second ever task"),
            task_manager.create_task("Thirs ever task"),
            task_manager.list_tasks(),
            task_manager.change_status(0, TaskStatus.in_progress),
            task_manager.change_status(2, TaskStatus.done),
            task_manager.list_tasks(),
            task_manager.list_tasks(TaskStatus.planned),
            task_manager.list_tasks(TaskStatus.in_progress),
            task_manager.list_tasks(TaskStatus.done),
            task_manager.update_task(1, "Stop procrastination: Second ever task"),
            task_manager.list_tasks(),
            task_manager.delete_task(2),
            task_manager.list_tasks(),
            task_manager.delete_task(1),
            task_manager.list_tasks(),
            task_manager.delete_task(0),
            task_manager.list_tasks(),
        ]

        for task in test_tasks:
            await task

    asyncio.run(test())
