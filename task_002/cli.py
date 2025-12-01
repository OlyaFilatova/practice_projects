import asyncio

from .storage.data import UserController

from .output.cli import CLIOutput
from .input.cli import CLIInput


class AppController:
    def __init__(
        self,
        storage_controller: UserController,
        input_controller: CLIInput,
        output_controller: CLIOutput,
    ):
        self.storage_controller = storage_controller
        self.input_controller = input_controller
        self.output_controller = output_controller

        self.input_controller.set_show_activity_handler(self.on_get_user_activity)
        self.input_controller.set_error_handler(self.on_error)

    async def on_get_user_activity(self, username: str) -> None:
        request_task = asyncio.create_task(
            self.storage_controller.retrieve_events(username)
        )
        events = await request_task

        output_task = asyncio.create_task(self.output_controller.diplay_events(events))
        await output_task

    async def on_error(self, message: str) -> None:
        output_task = asyncio.create_task(self.output_controller.error(message))
        await output_task

    async def start(self):
        input_task = asyncio.create_task(self.input_controller.start())
        await input_task


controller = AppController(UserController(), CLIInput(), CLIOutput())
asyncio.run(controller.start())
