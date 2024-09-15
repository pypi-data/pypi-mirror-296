from typing import Any

from ..schemas import CommitDetail
from .commit import parse_commit_data
from .report import parse_report_data

__all__ = ["parse_commit_detail_data"]


def parse_commit_detail_data(data: dict[str, Any]) -> CommitDetail:
    """
    Parse commit detail data.

    Args:
        data: commit detail json data.

    Returns:
        A `CommitDetail` schema.

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
    ...     "report": {
    ...         "totals": {
    ...             "files": 0,
    ...             "lines": 0,
    ...             "hits": 0,
    ...             "misses": 0,
    ...             "partials": 0,
    ...             "coverage": 0,
    ...             "branches": 0,
    ...             "methods": 0,
    ...             "messages": 0,
    ...             "sessions": 0,
    ...             "complexity": 0,
    ...             "complexity_total": 0,
    ...             "complexity_ratio": 0,
    ...             "diff": [],
    ...         },
    ...         "files": [
    ...             {
    ...                 "name": "string",
    ...                 "totals": {
    ...                     "files": 0,
    ...                     "lines": 0,
    ...                     "hits": 0,
    ...                     "misses": 0,
    ...                     "partials": 0,
    ...                     "coverage": 0,
    ...                     "branches": 0,
    ...                     "methods": 0,
    ...                     "messages": 0,
    ...                     "sessions": 0,
    ...                     "complexity": 0,
    ...                     "complexity_total": 0,
    ...                     "complexity_ratio": 0,
    ...                     "diff": 0,
    ...                 },
    ...             }
    ...         ],
    ...     },
    ... }
    >>> commit_detail = parse_commit_detail_data(data)
    >>> commit_detail
    CommitDetail(commitid='string', message='string', timestamp=datetime.datetime(...), ci_passed=True, author=None, branch='string', totals=None, state=None, parent='string', report=Report(...))
    """  # noqa: E501
    commit = parse_commit_data(data)

    commitid = commit.commitid
    message = commit.message
    timestamp = commit.timestamp
    ci_passed = commit.ci_passed
    author = commit.author
    branch = commit.branch
    totals = commit.totals
    state = commit.state
    parent = commit.parent

    report = data.get("report")

    return CommitDetail(
        commitid,
        message,
        timestamp,
        ci_passed,
        author,
        branch,
        totals,
        state,
        parent,
        parse_report_data(report),
    )
