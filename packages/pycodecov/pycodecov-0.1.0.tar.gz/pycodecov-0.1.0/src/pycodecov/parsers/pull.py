from datetime import datetime
from typing import Any

from ..enums import PullState
from ..schemas import Pull
from .commit_total import parse_commit_total_data
from .owner import parse_owner_data

__all__ = ["parse_pull_data"]


def parse_pull_data(data: dict[str, Any]) -> Pull:
    """
    Parse pull data.

    Args:
        data: pull json data.

    Returns:
        A `Pull` schema.

    Examples:
    >>> data = {
    ...     "pullid": 123,
    ...     "title": "string",
    ...     "base_total": {
    ...         "files": 123,
    ...         "lines": 123,
    ...         "hits": 123,
    ...         "misses": 123,
    ...         "partials": 123,
    ...         "coverage": 12.3,
    ...         "branches": 123,
    ...         "methods": 123,
    ...         "sessions": 123,
    ...         "complexity": 12.3,
    ...         "complexity_total": 12.3,
    ...         "complexity_ratio": 12.3,
    ...     },
    ...     "head_total": {
    ...         "files": 123,
    ...         "lines": 123,
    ...         "hits": 123,
    ...         "misses": 123,
    ...         "partials": 123,
    ...         "coverage": 12.3,
    ...         "branches": 123,
    ...         "methods": 123,
    ...         "sessions": 123,
    ...         "complexity": 12.3,
    ...         "complexity_total": 12.3,
    ...         "complexity_ratio": 12.3,
    ...     },
    ...     "updatestamp": "2024-03-25T16:38:25.747678Z",
    ...     "state": "open",
    ...     "ci_passed": True,
    ...     "author": None,
    ... }
    >>> pull = parse_pull_data(data)
    >>> pull
    Pull(pullid=123, title='string', base_total=CommitTotal(...), head_total=CommitTotal(...), updatestamp=datetime.datetime(...), state=<PullState.OPEN: 'open'>, ci_passed=True, author=None)
    """  # noqa: E501
    pullid = data.get("pullid")
    title = data.get("title")
    base_total = data.get("base_total")
    head_total = data.get("head_total")
    updatestamp = data.get("updatestamp")
    state = data.get("state")
    ci_passed = data.get("ci_passed")
    author = data.get("author")

    return Pull(
        pullid,
        title,
        parse_commit_total_data(base_total),
        parse_commit_total_data(head_total),
        datetime.fromisoformat(updatestamp),
        PullState(state),
        ci_passed,
        parse_owner_data(author) if author is not None else author,
    )
