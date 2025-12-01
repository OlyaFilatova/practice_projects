import asyncio
import json
from urllib.request import urlopen

from .examples.test_url import url, name
from ..models.response import Response
from ..models.user_events import EventType, UserEvent, event_enum_values


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
    async def _format_event(self, event):
        default_event_formatting = UserEvent(
            type=event["type"],
            repo=event["repo"]["name"],
            formatted_message=f"Unknown event type {event["type"]}",
            action=event["payload"].get("action", None),
            ref_type=event["payload"].get("ref_type", None),
        )
        formatted_event = default_event_formatting
        if event["type"] not in event_enum_values:
            return formatted_event

        match event["type"]:
            case EventType.CommitCommentEvent.value:
                formatted_event.formatted_message = (
                    f"Created commit comment in {formatted_event.repo}"
                )

            case EventType.CreateEvent.value:
                formatted_event.formatted_message = (
                    f"Created {formatted_event.ref_type} in {formatted_event.repo}"
                )

            case EventType.DeleteEvent.value:
                formatted_event.formatted_message = (
                    f"Deleted {formatted_event.ref_type} in {formatted_event.repo}"
                )

            case EventType.DiscussionEvent.value:
                formatted_event.formatted_message = (
                    f"Created discussion in {formatted_event.repo}"
                )

            case EventType.ForkEvent.value:
                formatted_event.formatted_message = f"Forked {formatted_event.repo}"

            case EventType.GollumEvent.value:
                formatted_event.formatted_message = f" in {formatted_event.repo}"

            case EventType.IssueCommentEvent.value:
                formatted_event.formatted_message = (
                    f"Created comment in {formatted_event.repo}"
                )

            case EventType.IssuesEvent.value:
                formatted_event.formatted_message = f"{formatted_event.action.title() if formatted_event.action else 'Unknown IssuesEvent action'} in {formatted_event.repo}"

            case EventType.MemberEvent.value:
                formatted_event.formatted_message = (
                    f"Accepted an invitation to a {formatted_event.repo}"
                )

            case EventType.PublicEvent.value:
                formatted_event.formatted_message = (
                    f"Made public {formatted_event.repo}"
                )

            case EventType.PullRequestEvent.value:
                formatted_event.formatted_message = f"{formatted_event.action.title() if formatted_event.action else 'Unknown PullRequestEvent action'} pull request in {formatted_event.repo}"

            case EventType.PullRequestReviewEvent.value:
                formatted_event.formatted_message = f"{formatted_event.action.title() if formatted_event.action else 'Unknown PullRequestReviewEvent action'} pull request review in {formatted_event.repo}"

            case EventType.PullRequestReviewCommentEvent.value:
                formatted_event.formatted_message = (
                    f"Created pull request review comment in {formatted_event.repo}"
                )

            case EventType.PushEvent.value:
                formatted_event.formatted_message = (
                    f"Push comments in {formatted_event.repo}"
                )

            case EventType.ReleaseEvent.value:
                formatted_event.formatted_message = (
                    f"Made a release in {formatted_event.repo}"
                )

            case EventType.WatchEvent.value:
                formatted_event.formatted_message = f"Starred {formatted_event.repo}"

        return formatted_event

    async def retrieve_events(self, user_name: str):
        url = f"https://api.github.com/users/{user_name}/events"
        request_task = asyncio.create_task(_fetch(url))
        response = await request_task

        events_raw = response.body

        return await asyncio.gather(
            *[self._format_event(event) for event in events_raw]
        )


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
