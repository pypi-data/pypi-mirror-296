from typing import Any

from ..schemas import Report
from .base_report import parse_base_report_file_data
from .report_total import parse_report_total_data

__all__ = ["parse_report_data"]


def parse_report_data(data: dict[str, Any]) -> Report:
    """
    Parse report data.

    Args:
        data: report json data.

    Returns:
        A `Report` schema.

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
    ...         "messages": 123,
    ...         "sessions": 123,
    ...         "complexity": 12.3,
    ...         "complexity_total": 12.3,
    ...         "complexity_ratio": 12.3,
    ...         "diff": 123,
    ...     },
    ...     "files": [],
    ... }
    >>> report = parse_report_data(data)
    >>> report
    Report(totals=ReportTotal(...), files=[])
    """
    totals = data.get("totals")
    files = data.get("files")

    return Report(
        parse_report_total_data(totals),
        [parse_base_report_file_data(file) for file in files],
    )
