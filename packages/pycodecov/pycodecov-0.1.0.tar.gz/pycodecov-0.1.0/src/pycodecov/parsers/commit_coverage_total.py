from typing import Any

from ..schemas import CommitCoverageTotal
from .base_report import parse_base_report_file_data
from .commit_coverage import parse_commit_coverage_data

__all__ = ["parse_commit_coverage_total_data"]


def parse_commit_coverage_total_data(data: dict[str, Any]) -> CommitCoverageTotal:
    """
    Parse commit coverage total data.

    Args:
        data: commit coverage total json data.

    Returns:
        A `CommitCoverageTotal` schema.

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
    ...     "files": [],
    ... }
    >>> commit_coverage_total = parse_commit_coverage_total_data(data)
    >>> commit_coverage_total
    CommitCoverageTotal(totals=CommitTotal(...), commit_file_url='string', files=[])
    """
    commit_coverage = parse_commit_coverage_data(data)

    totals = commit_coverage.totals
    commit_file_url = commit_coverage.commit_file_url

    files = data.get("files")

    return CommitCoverageTotal(
        totals, commit_file_url, [parse_base_report_file_data(file) for file in files]
    )
