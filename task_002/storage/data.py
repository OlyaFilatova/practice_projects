import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from ..exceptions.http import ConnectivityError, UserNotFound

from .examples.test_url import name
from ..models.response import Response
from ..models.user_events import UserEvent


class ResponseParseError(Exception):
    """Not able to parse response."""


async def _fetch(url):
    def _get():
        with urlopen(url) as response:
            status = response.status
            headers = response.headers.items()

            try:
                body = json.load(response)
            except json.JSONDecodeError:
                raise ResponseParseError(f"Failed to parse response: {response.read()}")

            return Response(status=status, headers=headers, body=body)

    return await asyncio.to_thread(_get)


class UserController:
    async def retrieve_events(self, username: str):
        url = f"https://api.github.com/users/{username}/events"
        try:
            request_task = asyncio.create_task(_fetch(url))
            response = await request_task
        except HTTPError as exc:
            if exc.code == 404:
                raise UserNotFound(f"Unable to find user {username}")
            else:
                raise exc
        except URLError:
            raise ConnectivityError(
                "Unable to connect to the API. Please check you connection."
            )

        events_raw = response.body

        return [
            UserEvent(
                type=event["type"],
                repo=event["repo"]["name"],
                action=event["payload"].get("action", None),
                ref_type=event["payload"].get("ref_type", None),
                actions=(
                    [page["action"] for page in event["payload"]["pages"]]
                    if "pages" in event["payload"]
                    else []
                ),
            )
            for event in events_raw
        ]


if __name__ == "__main__":

    async def main():
        # request_task = asyncio.create_task(_fetch(url))
        # response = await request_task
        # print(response.status)
        # print(response.headers)
        # print(json.dumps(response.body))
        request_task = asyncio.create_task(UserController().retrieve_events(name))
        events = await request_task
        print(events)

    asyncio.run(main())
