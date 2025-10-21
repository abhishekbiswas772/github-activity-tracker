from models import GitHubModel
from typing import Dict, Callable


def format_push_event(event: GitHubModel) -> str:
    ref = event.payload.ref or ""
    branch = ref.split("/")[-1] if ref else "unknown"
    return f"Pushed to {branch}"


def format_create_event(event: GitHubModel) -> str:
    ref = event.payload.ref
    if ref:
        return f"Created branch {ref}"
    return "Created repository"


def format_delete_event(event: GitHubModel) -> str:
    ref = event.payload.ref or "branch"
    return f"Deleted {ref}"


def format_fork_event(event: GitHubModel) -> str:
    return "Forked repository"


def format_watch_event(event: GitHubModel) -> str:
    return "Starred repository"


def format_issues_event(event: GitHubModel) -> str:
    return event.payload.description or "Issue event"


def format_issue_comment_event(event: GitHubModel) -> str:
    return "Commented on issue"


def format_pull_request_event(event: GitHubModel) -> str:
    return event.payload.description or "Pull request event"


def format_pull_request_review_event(event: GitHubModel) -> str:
    return "Reviewed pull request"


def format_pull_request_review_comment_event(event: GitHubModel) -> str:
    return "Commented on pull request"


def format_release_event(event: GitHubModel) -> str:
    return event.payload.description or "Published release"


def format_member_event(event: GitHubModel) -> str:
    return "Added collaborator"


def format_public_event(event: GitHubModel) -> str:
    return "Made repository public"


def format_gollum_event(event: GitHubModel) -> str:
    return "Updated wiki"


def format_commit_comment_event(event: GitHubModel) -> str:
    return "Commented on commit"


def format_default_event(event: GitHubModel) -> str:
    return event.payload.description or "Activity"


EVENT_FORMATTERS: Dict[str, Callable[[GitHubModel], str]] = {
    "PushEvent": format_push_event,
    "CreateEvent": format_create_event,
    "DeleteEvent": format_delete_event,
    "ForkEvent": format_fork_event,
    "WatchEvent": format_watch_event,
    "IssuesEvent": format_issues_event,
    "IssueCommentEvent": format_issue_comment_event,
    "PullRequestEvent": format_pull_request_event,
    "PullRequestReviewEvent": format_pull_request_review_event,
    "PullRequestReviewCommentEvent": format_pull_request_review_comment_event,
    "ReleaseEvent": format_release_event,
    "MemberEvent": format_member_event,
    "PublicEvent": format_public_event,
    "GollumEvent": format_gollum_event,
    "CommitCommentEvent": format_commit_comment_event,
}


def get_event_description(event: GitHubModel) -> str:
    formatter = EVENT_FORMATTERS.get(event.type, format_default_event)
    return formatter(event)


def get_event_icon(event_type: str) -> str:
    icons = {
        "PushEvent": "📤",
        "CreateEvent": "✨",
        "DeleteEvent": "🗑️",
        "ForkEvent": "🍴",
        "WatchEvent": "⭐",
        "IssuesEvent": "📋",
        "IssueCommentEvent": "💬",
        "PullRequestEvent": "🔀",
        "PullRequestReviewEvent": "👀",
        "PullRequestReviewCommentEvent": "💭",
        "ReleaseEvent": "🚀",
        "MemberEvent": "👥",
        "PublicEvent": "🌐",
        "GollumEvent": "📖",
        "CommitCommentEvent": "💬",
    }
    return icons.get(event_type, "📌")
