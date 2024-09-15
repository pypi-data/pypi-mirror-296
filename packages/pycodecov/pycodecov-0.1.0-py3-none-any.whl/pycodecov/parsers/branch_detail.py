from typing import Any

from ..schemas import BranchDetail
from .branch import parse_branch_data
from .commit_detail import parse_commit_detail_data

__all__ = ["parse_branch_detail_data"]


def parse_branch_detail_data(data: dict[str, Any]) -> BranchDetail:
    """
    Parse branch detail data.

    Args:
        data: branch detail json data.

    Returns:
        An `BranchDetail` schema.

    Examples:
    >>> data = {
    ...     "name": "string",
    ...     "updatestamp": "2024-03-25T16:38:25.747678Z",
    ...     "head_commit": {
    ...         "commitid": "string",
    ...         "message": "string",
    ...         "timestamp": "2024-04-08T06:59:47.329Z",
    ...         "ci_passed": true,
    ...         "author": {"service": "github", "username": "string", "name": "string"},
    ...         "branch": "string",
    ...         "totals": {
    ...             "files": 0,
    ...             "lines": 0,
    ...             "hits": 0,
    ...             "misses": 0,
    ...             "partials": 0,
    ...             "coverage": 0,
    ...             "branches": 0,
    ...             "methods": 0,
    ...             "sessions": 0,
    ...             "complexity": 0,
    ...             "complexity_total": 0,
    ...             "complexity_ratio": 0,
    ...             "diff": [],
    ...         },
    ...         "state": "complete",
    ...         "parent": "eb057a62519546830420a8ab2bb5e3bba03929fb",
    ...         "report": {
    ...             "totals": {
    ...                 "files": 0,
    ...                 "lines": 0,
    ...                 "hits": 0,
    ...                 "misses": 0,
    ...                 "partials": 0,
    ...                 "coverage": 0,
    ...                 "branches": 0,
    ...                 "methods": 0,
    ...                 "messages": 0,
    ...                 "sessions": 0,
    ...                 "complexity": 0,
    ...                 "complexity_total": 0,
    ...                 "complexity_ratio": 0,
    ...                 "diff": [],
    ...             },
    ...             "files": [
    ...                 {
    ...                     "name": "string",
    ...                     "totals": {
    ...                         "files": 0,
    ...                         "lines": 0,
    ...                         "hits": 0,
    ...                         "misses": 0,
    ...                         "partials": 0,
    ...                         "coverage": 0,
    ...                         "branches": 0,
    ...                         "methods": 0,
    ...                         "messages": 0,
    ...                         "sessions": 0,
    ...                         "complexity": 0,
    ...                         "complexity_total": 0,
    ...                         "complexity_ratio": 0,
    ...                         "diff": 0,
    ...                     },
    ...                 }
    ...             ],
    ...         },
    ...     },
    ... }
    >>> branch_detail = parse_branch_detail_data(data)
    >>> branch_detail
    BranchDetail(name='string', updatestamp=datetime.datetime(...), head_commit=CommitDetail(...))
    """  # noqa: E501
    branch = parse_branch_data(data)

    name = branch.name
    updatestamp = branch.updatestamp

    head_commit = data.get("head_commit")

    return BranchDetail(name, updatestamp, parse_commit_detail_data(head_commit))
