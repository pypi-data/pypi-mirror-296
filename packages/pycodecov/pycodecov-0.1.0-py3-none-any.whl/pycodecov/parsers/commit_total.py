from typing import Any

from ..schemas import CommitTotal
from .base_total import parse_base_total_data

__all__ = ["parse_commit_total_data"]


def parse_commit_total_data(data: dict[str, Any]) -> CommitTotal:
    """
    Parse commit total data.

    Args:
        data: commit total json data.

    Returns:
        A `CommitTotal` schema.

    Examples:
    >>> data = {
    ...     "files": 123,
    ...     "lines": 123,
    ...     "hits": 123,
    ...     "misses": 123,
    ...     "partials": 123,
    ...     "coverage": 12.3,
    ...     "branches": 123,
    ...     "methods": 123,
    ...     "sessions": 123,
    ...     "complexity": 12.3,
    ...     "complexity_total": 12.3,
    ...     "complexity_ratio": 12.3,
    ... }
    >>> commit_total = parse_commit_total_data(data)
    >>> commit_total
    CommitTotal(files=123, lines=123, hits=123, misses=123, partials=123, coverage=12.3, branches=123, methods=123, sessions=123, complexity=12.3, complexity_total=12.3, complexity_ratio=12.3)
    """  # noqa: E501
    base_total = parse_base_total_data(data)

    files = base_total.files
    lines = base_total.lines
    hits = base_total.hits
    misses = base_total.misses
    partials = base_total.partials
    coverage = base_total.coverage
    branches = base_total.branches
    methods = base_total.methods

    sessions = data.get("sessions")
    complexity = data.get("complexity")
    complexity_total = data.get("complexity_total")
    complexity_ratio = data.get("complexity_ratio")

    return CommitTotal(
        files,
        lines,
        hits,
        misses,
        partials,
        coverage,
        branches,
        methods,
        sessions,
        complexity,
        complexity_total,
        complexity_ratio,
    )
