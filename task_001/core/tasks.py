import time

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

    def list_tasks(self, status: TaskStatus | None = None) -> None:
        tasks_list = [
            task
            for task in enumerate(self.storage_manager.load())
            if not status or task[1].status == status
        ]
        self.output_manager.tasks_list(tasks_list)

    def create_task(self, description: str):
        idx, _ = self.storage_manager.add(
            Task(
                description=description,
                status=TaskStatus.planned,
                createdAt=time.time(),
                updatedAt=time.time(),
            )
        )

        self.output_manager.task_added_success(idx)

    def change_status(self, idx: int, status: TaskStatus) -> None:
        try:
            task = self.storage_manager.get_by_idx(idx)
        except TaskNotFound:
            self.output_manager.error_task_not_found(idx)
        else:
            self.output_manager.task_status_updated_success(idx)

            task.status = status
            task.updatedAt = time.time()

            self.storage_manager.update_by_idx(idx, task)

    def update_task(self, idx: int, description: str) -> None:
        try:
            task = self.storage_manager.get_by_idx(idx)
        except TaskNotFound:
            self.output_manager.error_task_not_found(idx)
        else:
            task.description = description
            task.updatedAt = time.time()

            self.storage_manager.update_by_idx(idx, task)
            self.output_manager.task_updated_success(idx)

    def delete_task(self, idx: int) -> None:
        try:
            self.storage_manager.delete_by_idx(idx)
        except TaskNotFound:
            self.output_manager.error_task_not_found(idx)
        else:
            self.output_manager.task_deleted_success(idx)


if __name__ == "__main__":
    task_manager = TaskManager(
        storage_manager=InMemoryStorage(),
        output_manager=CLIOutput(),
        input_manager=CLIInput(),
    )
    task_manager.list_tasks()

    task_manager.create_task("First ever task")
    task_manager.create_task("Second ever task")
    task_manager.create_task("Thirs ever task")

    task_manager.list_tasks()

    task_manager.change_status(0, TaskStatus.in_progress)
    task_manager.change_status(2, TaskStatus.done)

    task_manager.list_tasks()
    task_manager.list_tasks(TaskStatus.planned)
    task_manager.list_tasks(TaskStatus.in_progress)
    task_manager.list_tasks(TaskStatus.done)

    task_manager.update_task(1, "Stop procrastination: Second ever task")
    task_manager.list_tasks()

    task_manager.delete_task(2)
    task_manager.list_tasks()
    task_manager.delete_task(1)
    task_manager.list_tasks()
    task_manager.delete_task(0)
    task_manager.list_tasks()
