import os
from pathlib import Path
from .tasks import Task, TaskManager, TaskNotFound, parse_task_status

file_path = Path(
    Path(os.path.dirname(os.path.realpath(__file__))) / "../data/tasks_storage.json"
)


def _get_task_manager():
    task_manager = TaskManager(file_path)
    return task_manager


def _format_tasks_list(tasks_list: list[tuple[int, Task]]) -> str:
    return "\n".join(
        [f"{idx} - {task.status} - {task.description}" for idx, task in tasks_list]
    )


def add_task(description: str, **kwargs):
    task_manager = _get_task_manager()
    idx, _ = task_manager.create_task(description)

    print(
        f"Task added successfully (ID: {idx})\n\nList of tasks:\n{create_tasks_list()}"
    )


def update_task(index: str, description: str, **kwargs):
    idx = int(index)

    task_manager = TaskManager(file_path)
    try:
        task_manager.update_task(idx, description)
    except TaskNotFound as exc:
        print(exc.args[0])
    else:
        print(
            f"Task updated successfully (ID: {idx})\n\nList of tasks:\n{create_tasks_list()}"
        )


def change_task_status(index: str, status: str, **kwargs):
    try:
        idx = int(index)
    except ValueError:
        print(f'Index must be an integer. Received "{index}" instead.')
        return

    parsed_status = parse_task_status(status)

    if not parsed_status:
        raise ValueError("Failed to parse status.")

    task_manager = TaskManager(file_path)
    try:
        task_manager.change_status(idx, parsed_status)
    except TaskNotFound as exc:
        print(exc.args[0])
    else:
        print(
            f"Task status updated successfully (ID: {idx})\n\nList of tasks:\n{create_tasks_list()}"
        )


def delete_task(index: str, **kwargs):
    idx = int(index)

    task_manager = TaskManager(file_path)
    try:
        task_manager.delete_task(idx)
    except TaskNotFound as exc:
        print(exc.args[0])
    else:
        print(
            f"Task deleted successfully (ID: {idx})\n\nList of tasks:\n{create_tasks_list()}"
        )


def create_tasks_list(status: str | None = None):
    parsed_status = parse_task_status(status)

    task_manager = TaskManager(file_path)
    tasks_list = task_manager.list_tasks(parsed_status)

    return _format_tasks_list(tasks_list)


def list_tasks(status: str | None = None, **kwargs):
    print(create_tasks_list(status))
