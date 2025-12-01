from collections import Counter
from ..models.user_events import EventType, UserEvent


class CLIOutput:
    def _format_event(self, event: UserEvent):
        formatted_message = f"Unknown event type {event.type}"

        match event.type:
            case EventType.CommitCommentEvent.value:
                formatted_message = f"Created commit comment in {event.repo}"

            case EventType.CreateEvent.value:
                formatted_message = f"Created {event.ref_type} in {event.repo}"

            case EventType.DeleteEvent.value:
                formatted_message = f"Deleted {event.ref_type} in {event.repo}"

            case EventType.DiscussionEvent.value:
                formatted_message = f"Created discussion in {event.repo}"

            case EventType.ForkEvent.value:
                formatted_message = f"Forked {event.repo}"

            case EventType.GollumEvent.value:
                actions = event.actions
                counted_actions = Counter(actions)
                formatted_message = f"{" and ".join([f"{item[1]} {item[0]} " for item in counted_actions.items()])}wiki page{"s" if len(actions) > 1 else ""} in {event.repo}"

            case EventType.IssueCommentEvent.value:
                formatted_message = f"Created comment in {event.repo}"

            case EventType.IssuesEvent.value:
                formatted_message = f"{event.action.title() if event.action else 'Unknown IssuesEvent action'} issue in {event.repo}"

            case EventType.MemberEvent.value:
                formatted_message = f"Accepted an invitation to a {event.repo}"

            case EventType.PublicEvent.value:
                formatted_message = f"Made public {event.repo}"

            case EventType.PullRequestEvent.value:
                formatted_message = f"{event.action.title() if event.action else 'Unknown PullRequestEvent action'} pull request in {event.repo}"

            case EventType.PullRequestReviewEvent.value:
                formatted_message = f"{event.action.title() if event.action else 'Unknown PullRequestReviewEvent action'} pull request review in {event.repo}"

            case EventType.PullRequestReviewCommentEvent.value:
                formatted_message = (
                    f"Created pull request review comment in {event.repo}"
                )

            case EventType.PushEvent.value:
                formatted_message = f"Pushed commit in {event.repo}"

            case EventType.ReleaseEvent.value:
                formatted_message = f"Made a release in {event.repo}"

            case EventType.WatchEvent.value:
                formatted_message = f"Starred {event.repo}"

        return formatted_message

    async def error(self, message: str):
        print(message)

    async def diplay_events(self, events: list[UserEvent]):
        counted_events = Counter(
            [self._format_event(event) for event in events]
        ).items()

        for message, count in counted_events:
            if count == 1:
                print(message)
            else:
                print(f"{message} ({count} activities)")
