from typing import Any

from ..schemas import ReportFile
from .base_report import parse_base_report_file_data
from .line import parse_line_data

__all__ = ["parse_report_file_data"]


def parse_report_file_data(data: dict[str, Any]) -> ReportFile:
    """
    Parse report file data.

    Args:
        data: report file json data.

    Returns:
        A `ReportFile` schema.

    Examples:
    >>> data = {
    ...     "name": "string",
    ...     "totals": {
    ...         "files": 123,
    ...         "lines": 123,
    ...         "hits": 123,
    ...         "misses": 123,
    ...         "partials": 123,
    ...         "coverage": 12.3,
    ...         "branches": 123,
    ...         "methods": 123,
    ...         "messages": 123,
    ...         "sessions": 123,
    ...         "complexity": 12.3,
    ...         "complexity_total": 12.3,
    ...         "complexity_ratio": 12.3,
    ...         "diff": 123,
    ...     },
    ...     "line_coverage": [],
    ... }
    >>> report_file = parse_report_file_data(data)
    >>> report_file
    ReportFile(name='string', totals=ReportTotal(...), line_coverage=[])
    """
    base_report_file = parse_base_report_file_data(data)

    name = base_report_file.name
    totals = base_report_file.totals

    line_coverage = data.get("line_coverage")

    return ReportFile(
        name,
        totals,
        [parse_line_data(line) for line in line_coverage],
    )
