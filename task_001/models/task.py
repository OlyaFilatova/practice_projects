from dataclasses import dataclass
from enum import Enum


class TaskNotFound(Exception):
    """Task index out of bound."""


class TaskStatus(Enum):
    done = "done"
    in_progress = "in-progress"
    planned = "todo"


@dataclass
class BaseTask:
    description: str
    status: str
    createdAt: float
    updatedAt: float

@dataclass
class Task(BaseTask):
    id: int
