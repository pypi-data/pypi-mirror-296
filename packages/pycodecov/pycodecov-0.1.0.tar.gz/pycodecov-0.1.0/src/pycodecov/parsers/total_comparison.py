from typing import Any

from ..schemas import TotalComparison
from .report_total import parse_report_total_data

__all__ = ["parse_total_comparison_data"]


def parse_total_comparison_data(data: dict[str, Any]) -> TotalComparison:
    """
    Parse total comparison data.

    Args:
        data: total comparison json data.

    Returns:
        A `TotalComparison` schema.

    Examples:
    >>> data = {
    ...     "base": {
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
    ...     "head": {
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
    ...     "patch": None,
    ... }
    >>> total_comparison = parse_total_comparison_data(data)
    >>> total_comparison
    TotalComparison(base=ReportTotal(...), head=ReportTotal(...), patch=None)
    """
    base = data.get("base")
    head = data.get("head")
    patch = data.get("patch")

    return TotalComparison(
        parse_report_total_data(base),
        parse_report_total_data(head),
        parse_report_total_data(patch) if patch is not None else patch,
    )
