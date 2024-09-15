from typing import Any

from ..schemas import BaseReportFile
from .report_total import parse_report_total_data

__all__ = ["parse_base_report_file_data"]


def parse_base_report_file_data(data: dict[str, Any]) -> BaseReportFile:
    """
    Parse base report file data.

    Args:
        data: base report file json data.

    Returns:
        A `BaseReportFile` schema.

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
    ... }
    >>> base_report_file = parse_base_report_file_data(data)
    >>> base_report_file
    BaseReportFile(name='string', totals=ReportTotal(...))
    """
    name = data.get("name")
    totals = data.get("totals")

    return BaseReportFile(name, parse_report_total_data(totals))
