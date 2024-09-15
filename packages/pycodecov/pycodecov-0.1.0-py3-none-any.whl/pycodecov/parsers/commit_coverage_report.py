from typing import Any

from ..schemas import CommitCoverageReport
from .commit_coverage import parse_commit_coverage_data
from .report_file import parse_report_file_data

__all__ = ["parse_commit_coverage_report_data"]


def parse_commit_coverage_report_data(data: dict[str, Any]) -> CommitCoverageReport:
    """
    Parse commit coverage report data.

    Args:
        data: commit coverage report json data.

    Returns:
        A `CommitCoverageReport` schema.

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
    >>> commit_coverage_report = parse_commit_coverage_report_data(data)
    >>> commit_coverage_report
    CommitCoverageReport(totals=CommitTotal(...), commit_file_url='string', files=[])
    """
    commit_coverage = parse_commit_coverage_data(data)

    totals = commit_coverage.totals
    commit_file_url = commit_coverage.commit_file_url

    files = data.get("files")

    return CommitCoverageReport(
        totals, commit_file_url, [parse_report_file_data(file) for file in files]
    )
