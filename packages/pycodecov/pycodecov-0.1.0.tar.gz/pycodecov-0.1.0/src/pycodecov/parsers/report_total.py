from typing import Any

from ..schemas import ReportTotal
from .base_total import parse_base_total_data

__all__ = ["parse_report_total_data"]


def parse_report_total_data(data: dict[str, Any]) -> ReportTotal:
    """
    Parse report total data.

    Args:
        data: report total json data.

    Returns:
        A `ReportTotal` schema.

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
    ...     "messages": 123,
    ...     "sessions": 123,
    ...     "complexity": 12.3,
    ...     "complexity_total": 12.3,
    ...     "complexity_ratio": 12.3,
    ...     "diff": 123,
    ... }
    >>> report_total = parse_report_total_data(data)
    >>> report_total
    ReportTotal(files=123, lines=123, hits=123, misses=123, partials=123, coverage=12.3, branches=123, methods=123, messages=123, sessions=123, complexity=12.3, complexity_total=12.3, complexity_ratio=12.3, diff=123)
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

    messages = data.get("messages")
    sessions = data.get("sessions")
    complexity = data.get("complexity")
    complexity_total = data.get("complexity_total")
    complexity_ratio = data.get("complexity_ratio")
    diff = data.get("diff")

    return ReportTotal(
        files,
        lines,
        hits,
        misses,
        partials,
        coverage,
        branches,
        methods,
        messages,
        sessions,
        complexity,
        complexity_total,
        complexity_ratio,
        diff,
    )
