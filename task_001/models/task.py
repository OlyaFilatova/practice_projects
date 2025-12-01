from dataclasses import dataclass
from enum import Enum


class TaskNotFound(Exception):
    """Task index out of bound."""


class TaskStatus(str, Enum):
    done = "done"
    in_progress = "in-progress"
    planned = "todo"


@dataclass
class Task:
    description: str
    status: TaskStatus
    createdAt: float
    updatedAt: float
