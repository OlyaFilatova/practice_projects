"""
JSON file structure:

[
    task:
        description: str
        status: "Done" | "In progress" | "Planned"
]
"""

from dataclasses import asdict, dataclass
from enum import Enum
import json
from pathlib import Path


class TaskNotFound(Exception):
    """Task index out of bound."""


class JSONStorageCorrupted(Exception):
    """Not able to extract data from JSON storage."""


class TaskStatus(str, Enum):
    done = "Done"
    in_progress = "In progress"
    planned = "Planned"


task_statuses = {
    "done": TaskStatus.done,
    "todo": TaskStatus.planned,
    "in-progress": TaskStatus.in_progress,
}


def parse_task_status(key: str | None) -> TaskStatus | None:
    if key == None:
        return None

    if key not in task_statuses:
        raise ValueError(f"Task status index '{key}' not found.")

    return task_statuses[key]


@dataclass
class Task:
    description: str
    status: TaskStatus


class TaskManager:
    def __init__(self, file_path: Path):
        self.failed_to_load = False
        self.file_path = file_path

        self.load()

    def list_tasks(self, status: TaskStatus | None = None) -> list[tuple[int, Task]]:
        return [
            task
            for task in enumerate(self.tasks)
            if not status or task[1].status == status
        ]

    def create_task(self, description: str) -> tuple[int, Task]:
        self.tasks.append(Task(description, TaskStatus.planned))

        self.store()

        return len(self.tasks), self.tasks[-1]

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.tasks = [
                    Task(task["description"], task["status"])
                    for task in (json.load(f) or [])
                ]
        except FileNotFoundError as exc:
            if not self.failed_to_load:
                self.failed_to_load = True
                self.file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump([], f)
                self.load()
            else:
                raise exc

    def store(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([asdict(task) for task in self.tasks], f, indent=2)

    def change_status(self, task_idx: int, status: TaskStatus) -> None:
        if task_idx >= len(self.tasks):
            raise TaskNotFound(f"Task with index {task_idx} was not found.")

        self.tasks[task_idx].status = status

        self.store()

    def update_task(self, task_idx: int, description: str) -> None:
        if task_idx >= len(self.tasks):
            raise TaskNotFound(f"Task with index {task_idx} was not found.")

        self.tasks[task_idx].description = description

        self.store()

    def delete_task(self, task_idx: int) -> None:
        if task_idx >= len(self.tasks):
            raise TaskNotFound(f"Task with index {task_idx} was not found.")

        del self.tasks[task_idx]

        self.store()


if __name__ == "__main__":
    file_path = Path("tasks_storage.json")
    task_manager = TaskManager(file_path)
    print(task_manager.list_tasks())

    print(task_manager.create_task("First ever task"))
    print(task_manager.create_task("Second ever task"))
    print(task_manager.create_task("Thirs ever task"))

    print(task_manager.list_tasks())

    print(task_manager.change_status(0, TaskStatus.in_progress))
    print(task_manager.change_status(2, TaskStatus.done))

    print(task_manager.list_tasks())
    print(task_manager.list_tasks(TaskStatus.planned))
    print(task_manager.list_tasks(TaskStatus.in_progress))
    print(task_manager.list_tasks(TaskStatus.done))

    print(task_manager.update_task(1, "Stop procrastination: Second ever task"))
    print(task_manager.list_tasks())

    print(task_manager.delete_task(2))
    print(task_manager.list_tasks())
    print(task_manager.delete_task(1))
    print(task_manager.list_tasks())
    print(task_manager.delete_task(0))
    print(task_manager.list_tasks())
