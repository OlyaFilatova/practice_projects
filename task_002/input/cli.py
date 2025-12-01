import argparse
import asyncio
from types import CoroutineType
from typing import Any, Callable

from ..exceptions.http import ConnectivityError, UserNotFound


def create_default_handler(handler_fn_name: str):
    async def handler_not_set(*_):
        print(f"Wrong CLIOutput configuration, you need to call `{handler_fn_name}`.")

    return handler_not_set


class CLIInput:
    def __init__(self):
        self._setup_program()

        self.__show_activity_handler = create_default_handler(
            "set_show_activity_handler"
        )
        self.__error_handler = create_default_handler("set_error_handler")

    def set_show_activity_handler(
        self, callback: Callable[[str], CoroutineType[Any, Any, None]]
    ):
        self.__show_activity_handler = callback

    def set_error_handler(
        self, callback: Callable[[str], CoroutineType[Any, Any, None]]
    ):
        self.__error_handler = callback

    def _setup_program(self) -> None:
        self.parser = argparse.ArgumentParser(prog="List user's latest activity")
        self.parser.add_argument("username")

    async def start(self):
        args = self.parser.parse_args()
        try:
            handler_task = asyncio.create_task(
                self.__show_activity_handler(args.username)
            )
            await handler_task
        except UserNotFound as exc:
            await self.__error_handler(exc.args[0])
        except ConnectivityError as exc:
            await self.__error_handler(exc.args[0])


if __name__ == "__main__":
    asyncio.run(CLIInput().start())
