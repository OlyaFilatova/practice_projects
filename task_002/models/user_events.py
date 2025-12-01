"""
https://docs.github.com/en/rest/using-the-rest-api/github-event-types?apiVersion=2022-11-28
"""

from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    CommitCommentEvent = "CommitCommentEvent"
    """
    A commit comment is created.

    action: "created" """

    CreateEvent = "CreateEvent"
    """
    A Git branch or tag is created.
    
    ref_type: "branch", "tag", or "repository" """

    DeleteEvent = "DeleteEvent"
    """A Git branch or tag is deleted.
    
    ref_type: branch, tag"""

    DiscussionEvent = "DiscussionEvent"
    """A discussion is created in a repository.

    action: "created" """

    ForkEvent = "ForkEvent"
    """A user forks a repository.
    
    action: "forked" """

    GollumEvent = "GollumEvent"
    """A wiki page is created or updated.

    pages[][action]: "created" or "edited" """

    IssueCommentEvent = "IssueCommentEvent"
    """Activity related to an issue or pull request comment.

    action: "created" """

    IssuesEvent = "IssuesEvent"
    """Activity related to an issue.

    action: opened, closed, reopened """

    MemberEvent = "MemberEvent"
    """Activity related to repository collaborators.

    action: Can be "added" to indicate a user accepted an invitation to a repository."""

    PublicEvent = "PublicEvent"
    """When a private repository is made public."""

    PullRequestEvent = "PullRequestEvent"
    """Activity related to pull requests.

    action: opened, closed, reopened, assigned, unassigned, labeled, and unlabeled"""

    PullRequestReviewEvent = "PullRequestReviewEvent"
    """Activity related to pull request reviews.

    action: created, updated, or dismissed."""

    PullRequestReviewCommentEvent = "PullRequestReviewCommentEvent"
    """Activity related to pull request review comments in the pull request's unified diff.

    action: "created" """

    PushEvent = "PushEvent"
    """One or more commits are pushed to a repository branch or tag."""

    ReleaseEvent = "ReleaseEvent"
    """Activity related to a release.

    action: "published" """

    WatchEvent = "WatchEvent"
    """When someone stars a repository.

    action: "started" """


@dataclass
class UserEvent:
    type: str  # event.type
    repo: str  # event.repo.name
    action: str | None  # event.payload.action
    actions: list[str]  # event.payload.pages.action
    ref_type: str | None  # event.payload.ref_type
