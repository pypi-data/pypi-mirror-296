from typing import Any

from ..schemas import GitCommit
from .base_commit import parse_base_commit_data
from .git_author import parse_git_author_data

__all__ = ["parse_git_commit_data"]


def parse_git_commit_data(data: dict[str, Any]) -> GitCommit:
    """
    Parse git commit data.

    Args:
        data: git commit json data.

    Returns:
        A `GitCommit` schema.

    Examples:
    >>> data = {
    ...     "commitid": "string",
    ...     "message": "string",
    ...     "timestamp": "2024-03-25T16:38:25.747678Z",
    ...     "author": {
    ...         "id": 123,
    ...         "username": "string",
    ...         "name": "string",
    ...         "email": "string",
    ...     },
    ... }
    >>> git_commit = parse_git_commit_data(data)
    >>> git_commit
    GitCommit(commitid='string', message='string', timestamp=datetime.datetime(...), author=GitAuthor(...))
    """  # noqa: E501
    base_commit = parse_base_commit_data(data)

    commitid = base_commit.commitid
    message = base_commit.message
    timestamp = base_commit.timestamp

    author = data.get("author")

    return GitCommit(commitid, message, timestamp, parse_git_author_data(author))
