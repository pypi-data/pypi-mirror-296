from typing import Any

from ..enums import Coverage
from ..schemas import LineCoverageComparison

__all__ = ["parse_line_coverage_comparison_data"]


def parse_line_coverage_comparison_data(data: dict[str, Any]) -> LineCoverageComparison:
    """
    Parse line coverage comparison data.

    Args:
        data: line coverage comparison json data.

    Returns:
        A `LineCoverageComparison` schema.

    Examples:
    >>> data = {
    ...     "base": 0,
    ...     "head": 0,
    ... }
    >>> line_coverage_comparison = parse_line_coverage_comparison_data(data)
    >>> line_coverage_comparison
    LineCoverageComparison(base=<Coverage.HIT: 0>, head=<Coverage.HIT: 0>)
    """
    base = data.get("base")
    head = data.get("head")

    return LineCoverageComparison(Coverage(base), Coverage(head))
