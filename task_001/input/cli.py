import argparse
from typing import Callable

from .iinput import IInput

from ..models.task import TaskStatus


task_statuses = {
    "done": TaskStatus.done,
    "todo": TaskStatus.planned,
    "in-progress": TaskStatus.in_progress,
}


class CLIInput(IInput):
    def __init__(self):
        self._setup_program()

    def _parse_task_status(self, key: str | None) -> TaskStatus | None:
        if key == None:
            return None

        if key not in task_statuses:
            raise ValueError(self.__error_handler(f"Task status not found {key}"))

        return task_statuses[key]

    def _parse_index(self, index: str) -> int | None:
        try:
            return int(index)
        except ValueError:
            self.__error_handler(f"Failed to parse index {index}")
            return

    def set_add_handler(self, callback: Callable[[str], None]) -> None:
        self.__add_handler = callback

    def __setup_add_command(self) -> None:
        subparser = self.subparsers.add_parser("add", help="Create task.")
        subparser.add_argument("description")
        subparser.set_defaults(
            func=lambda description, **kwargs: self.__add_handler(description)
        )

    def set_list_handler(self, callback: Callable[[TaskStatus | None], None]) -> None:
        self.__list_handler = callback

    def __setup_list_command(self) -> None:
        subparser = self.subparsers.add_parser("list", help="List tasks.")
        subparser.add_argument(
            "status", choices=["done", "todo", "in-progress"], nargs="?", default=None
        )
        subparser.set_defaults(func=lambda status, **kwargs: self._list_tasks(status))

    def _list_tasks(self, status: str | None = None):
        parsed_status = self._parse_task_status(status)

        self.__list_handler(parsed_status)

    def set_update_handler(self, callback: Callable[[int, str], None]) -> None:
        self.__update_handler = callback

    def __setup_update_command(self) -> None:
        subparser = self.subparsers.add_parser("update", help="Update task.")
        subparser.add_argument("index")
        subparser.add_argument("description")
        subparser.set_defaults(
            func=lambda index, description, **kwargs: self._update_task(
                index, description
            )
        )

    def _update_task(self, index: str, description: str):
        idx = self._parse_index(index)

        if idx != None:
            self.__update_handler(idx, description)

    def set_status_handler(self, callback: Callable[[int, TaskStatus], None]) -> None:
        self.__status_handler = callback

    def __setup_mark_todo_command(self) -> None:
        subparser = self.subparsers.add_parser("mark-todo", help="Change task status.")
        subparser.add_argument("index")
        subparser.set_defaults(
            func=lambda index, **kwargs: self._change_task_status(
                index, TaskStatus.planned
            )
        )

    def _change_task_status(self, index: str, status: TaskStatus):
        idx = self._parse_index(index)

        if idx != None:
            self.__status_handler(idx, status)

    def __setup_mark_in_progress_command(self) -> None:
        subparser = self.subparsers.add_parser(
            "mark-in-progress", help="Change task status."
        )
        subparser.add_argument("index")
        subparser.set_defaults(
            func=lambda index, **kwargs: self._change_task_status(
                index, TaskStatus.in_progress
            )
        )

    def __setup_mark_done_command(self) -> None:
        subparser = self.subparsers.add_parser("mark-done", help="Change task status.")
        subparser.add_argument("index")
        subparser.set_defaults(
            func=lambda index, **kwargs: self._change_task_status(
                index, TaskStatus.done
            )
        )

    def set_delete_handler(self, callback: Callable[[int], None]) -> None:
        self.__delete_handler = callback

    def __setup_delete_command(self) -> None:
        subparser = self.subparsers.add_parser("delete", help="Delete task.")
        subparser.add_argument("index")
        subparser.set_defaults(func=lambda index, **kwargs: self._delete_task(index))

    def _delete_task(self, index: str, **kwargs):
        idx = self._parse_index(index)

        if idx != None:
            self.__delete_handler(idx)

    def set_error_handler(self, callback: Callable[[str], None]) -> None:
        self.__error_handler = callback

    def _setup_program(self) -> None:
        self.parser = argparse.ArgumentParser(
            prog="Task manager.",
            description="A simple TODO list.",
        )

        self.subparsers = self.parser.add_subparsers(help="Task actions.")

        self.__setup_add_command()
        self.__setup_delete_command()
        self.__setup_list_command()
        self.__setup_mark_done_command()
        self.__setup_mark_in_progress_command()
        self.__setup_mark_todo_command()
        self.__setup_update_command()

    def start(self):
        args = self.parser.parse_args()
        if "func" in args:
            args.func(**args.__dict__)
        else:
            self.parser.print_help()
