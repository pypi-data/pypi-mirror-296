from typing import Any

from ..schemas import LineNumberComparison

__all__ = ["parse_line_number_comparison_data"]


def parse_line_number_comparison_data(data: dict[str, Any]) -> LineNumberComparison:
    """
    Parse line number comparison data.

    Args:
        data: line number comparison json data.

    Returns:
        A `LineNumberComparison` schema.

    Examples:
    >>> data = {
    ...     "base": 0,
    ...     "head": 0,
    ... }
    >>> line_number_comparison = parse_line_number_comparison_data(data)
    >>> line_number_comparison
    LineNumberComparison(base=0, head=0)
    """
    base = data.get("base")
    head = data.get("head")

    return LineNumberComparison(base, head)
