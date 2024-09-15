from datetime import datetime
from typing import Any

from ..schemas import BaseCommit

__all__ = ["parse_base_commit_data"]


def parse_base_commit_data(data: dict[str, Any]) -> BaseCommit:
    """
    Parse base commit data.

    Args:
        data: base commit json data.

    Returns:
        A `BaseCommit` schema.

    Examples:
    >>> data = {
    ...     "commitid": "string",
    ...     "message": "string",
    ...     "timestamp": "2024-03-25T16:38:25.747678Z",
    ... }
    >>> base_commit = parse_base_commit_data(data)
    >>> base_commit
    BaseCommit(commitid='string', message='string', timestamp=datetime.datetime(...)
    """
    commitid = data.get("commitid")
    message = data.get("message")
    timestamp = data.get("timestamp")

    return BaseCommit(commitid, message, datetime.fromisoformat(timestamp))
