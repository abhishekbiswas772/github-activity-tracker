from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class GithubActor:
    id: int
    login: str
    display_login: str
    gravatar_id: Optional[str]
    url: str
    avatar_url: str



@dataclass
class GithubRepo:
    id: int
    name: str
    url: str


@dataclass
class GithubPayload:
    repository_id: Optional[int] = None
    push_id: Optional[int] = None
    ref: Optional[str] = None
    head: Optional[str] = None
    before: Optional[str] = None
    description: Optional[str] = None


@dataclass
class GitHubModel:
    id: str
    type: str
    actor: GithubActor
    repo: GithubRepo
    payload: GithubPayload
    created_at: datetime
    public: bool
