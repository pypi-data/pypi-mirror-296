from typing import Any

from ..enums import Coverage
from ..schemas import Line

__all__ = ["parse_line_data"]


def parse_line_data(data: dict[str, Any]) -> Line:
    """
    Parse line data.

    Args:
        data: line json data.

    Returns:
        A `Line` schema.

    Examples:
    >>> data = {
    ...     "number": 123,
    ...     "coverage": 0,
    ... }
    >>> line = parse_line_data(data)
    >>> line
    Line(number=123, coverage=<Coverage.HIT: 0>)
    """
    number = data.get("number")
    coverage = data.get("coverage")

    return Line(number, Coverage(coverage))
