from typing import Any

from ..schemas import LineComparison
from .line_coverage_comparison import parse_line_coverage_comparison_data
from .line_number_comparison import parse_line_number_comparison_data

__all__ = ["parse_line_comparison_data"]


def parse_line_comparison_data(data: dict[str, Any]) -> LineComparison:
    """
    Parse line comparison data.

    Args:
        data: line comparison json data.

    Returns:
        A `LineComparison` schema.

    Examples:
    >>> data = {
    ...     "value": "string",
    ...     "number": {
    ...         "base": 0,
    ...         "head": 0,
    ...     },
    ...     "coverage": {
    ...         "base": 0,
    ...         "head": 0,
    ...     },
    ...     "is_diff": True,
    ...     "added": True,
    ...     "removed": False,
    ...     "sessions": 0,
    ... }
    >>> line_comparison = parse_line_comparison_data(data)
    >>> line_comparison
    LineComparison(value='string', number=LineNumberComparison(...), coverage=LineCoverageComparison(...), is_diff=True, added=True, removed=False, sessions=0)
    """  # noqa: E501
    value = data.get("value")
    number = data.get("number")
    coverage = data.get("coverage")
    is_diff = data.get("is_diff")
    added = data.get("added")
    removed = data.get("removed")
    sessions = data.get("sessions")

    return LineComparison(
        value,
        parse_line_number_comparison_data(number),
        parse_line_coverage_comparison_data(coverage),
        is_diff,
        added,
        removed,
        sessions,
    )
