from typing import Any

from ..schemas import CommitCoverage
from .report_total import parse_report_total_data

__all__ = ["parse_commit_coverage_data"]


def parse_commit_coverage_data(data: dict[str, Any]) -> CommitCoverage:
    """
    Parse commit coverage data.

    Args:
        data: commit coverage json data.

    Returns:
        A `CommitCoverage` schema.

    Examples:
    >>> data = {
    ...     "totals": {
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
    ...     "commit_file_url": "string",
    ... }
    >>> commit_coverage = parse_commit_coverage_data(data)
    >>> commit_coverage
    CommitCoverage(totals=CommitTotal(...), commit_file_url='string')
    """
    totals = data.get("totals")
    commit_file_url = data.get("commit_file_url")

    return CommitCoverage(parse_report_total_data(totals), commit_file_url)
