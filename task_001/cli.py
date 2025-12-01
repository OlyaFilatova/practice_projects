import asyncio
from enum import Enum
import configparser
import os
from pathlib import Path

from .input.iinput import IInput
from .output.ioutput import IOutput
from .storage.istorage import IStorage

from .input.cli import CLIInput
from .storage.json import JSONStorage
from .storage.in_memory import InMemoryStorage
from .output.cli import CLIOutput
from .core.tasks import TaskManager


config = configparser.ConfigParser()


class StorageType(Enum):
    json = "json"
    in_memory = "in-memory"


class InputType(Enum):
    cli = "cli"


class OutputType(Enum):
    cli = "cli"


get_output_type = lambda: config["DEFAULT"]["output-type"]


def _get_output_manager() -> IOutput | None:
    output_type = get_output_type()
    match output_type:
        case OutputType.cli.value:
            return CLIOutput()


get_input_type = lambda: config["DEFAULT"]["input-type"]


def _get_input_manager() -> IInput | None:
    input_type = get_input_type()
    match input_type:
        case InputType.cli.value:
            return CLIInput()


get_storage_type = lambda: config["DEFAULT"]["storage-type"]


def _get_storage_manager() -> IStorage | None:
    storage_type = get_storage_type()
    match storage_type:
        case StorageType.json.value:
            return JSONStorage(file_location=config["DEFAULT"]["file-location"])
        case StorageType.in_memory.value:
            return InMemoryStorage()


async def main():
    config.read(Path(os.path.dirname(os.path.realpath(__file__))) / "config.ini")

    output_manager = _get_output_manager()
    input_manager = _get_input_manager()
    storage_manager = _get_storage_manager()

    if not output_manager:
        print("Failed to load output manager. Closing application")
        exit()

    if not input_manager:
        output_task = asyncio.create_task(
            output_manager.error("Failed to load input manager. Closing application")
        )
        await output_task
        exit()

    if not storage_manager:
        output_task = asyncio.create_task(
            output_manager.error("Failed to load storage manager. Closing application")
        )
        await output_task
        exit()

    TaskManager(
        storage_manager=storage_manager,
        input_manager=input_manager,
        output_manager=output_manager,
    )

    start_task = asyncio.create_task(input_manager.start())
    await start_task


asyncio.run(main())
