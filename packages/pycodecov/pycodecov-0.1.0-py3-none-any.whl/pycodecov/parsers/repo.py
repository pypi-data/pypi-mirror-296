from datetime import datetime
from typing import Any

from ..enums import Language
from ..schemas import Repo
from .commit_total import parse_commit_total_data
from .owner import parse_owner_data

__all__ = ["parse_repo_data"]


def parse_repo_data(data: dict[str, Any]) -> Repo:
    """
    Parse repo data.

    Args:
        data: repo json data.

    Returns:
        A `Repo` schema.

    Examples:
    >>> data = {
    ...     "name": "string",
    ...     "private": True,
    ...     "updatestamp": "2024-03-25T16:38:25.747678Z",
    ...     "author": {"service": "github", "username": "string", "name": "string"},
    ...     "language": "string",
    ...     "branch": "string",
    ...     "active": True,
    ...     "activated": True,
    ...     "totals": None,
    ... }
    >>> repo = parse_repo_data(data)
    >>> repo
    Repo(name='string', private=True, updatestamp=datetime.datetime(...), author=Owner(...), language='string', branch='string', active=True, activated=True, totals=None)
    """  # noqa: E501
    name = data.get("name")
    private = data.get("private")
    updatestamp = data.get("updatestamp")
    author = data.get("author")
    language = data.get("language")
    branch = data.get("branch")
    active = data.get("active")
    activated = data.get("activated")
    totals = data.get("totals")

    return Repo(
        name,
        private,
        datetime.fromisoformat(updatestamp) if updatestamp is not None else updatestamp,
        parse_owner_data(author),
        Language(language) if language is not None else language,
        branch,
        active,
        activated,
        parse_commit_total_data(totals) if totals is not None else totals,
    )
