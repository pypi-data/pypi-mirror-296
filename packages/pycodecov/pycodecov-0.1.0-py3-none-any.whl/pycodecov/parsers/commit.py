from typing import Any

from ..enums import CommitState
from ..schemas import Commit
from .base_commit import parse_base_commit_data
from .commit_total import parse_commit_total_data
from .owner import parse_owner_data

__all__ = ["parse_commit_data"]


def parse_commit_data(data: dict[str, Any]) -> Commit:
    """
    Parse commit data.

    Args:
        data: commit json data.

    Returns:
        A `Commit` schema.

    Examples:
    >>> data = {
    ...     "commitid": "string",
    ...     "message": "string",
    ...     "timestamp": "2024-03-25T16:38:25.747678Z",
    ...     "ci_passed": True,
    ...     "author": None,
    ...     "branch": "string",
    ...     "totals": None,
    ...     "state": None,
    ...     "parent": "string",
    ... }
    >>> commit = parse_commit_data(data)
    >>> commit
    Commit(commitid='string', message='string', timestamp=datetime.datetime(...), ci_passed=True, author=None, branch='string', totals=None, state=None, parent='string')
    """  # noqa: E501
    base_commit = parse_base_commit_data(data)

    commitid = base_commit.commitid
    message = base_commit.message
    timestamp = base_commit.timestamp

    ci_passed = data.get("ci_passed")
    author = data.get("author")
    branch = data.get("branch")
    totals = data.get("totals")
    state = data.get("state")
    parent = data.get("parent")

    return Commit(
        commitid,
        message,
        timestamp,
        ci_passed,
        parse_owner_data(author) if author is not None else author,
        branch,
        parse_commit_total_data(totals) if totals is not None else totals,
        CommitState(state) if state is not None else state,
        parent,
    )
