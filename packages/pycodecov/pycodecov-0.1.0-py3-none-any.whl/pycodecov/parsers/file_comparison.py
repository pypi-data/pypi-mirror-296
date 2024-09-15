from typing import Any

from ..schemas import FileComparison
from .file_change_summary_comparison import parse_file_change_summary_comparison_data
from .file_name_comparison import parse_file_name_comparison_data
from .file_stat_comparison import parse_file_stat_comparison_data
from .line_comparison import parse_line_comparison_data
from .total_comparison import parse_total_comparison_data

__all__ = ["parse_file_comparison_data"]


def parse_file_comparison_data(data: dict[str, Any]) -> FileComparison:
    """
    Parse file comparison data.

    Args:
        data: file comparison json data.

    Returns:
        A `FileComparison` schema.

    Examples:
    >>> data = {
    ...     "name": {
    ...         "base": "string",
    ...         "head": "string",
    ...     },
    ...     "totals": {
    ...         "base": {
    ...             "files": 123,
    ...             "lines": 123,
    ...             "hits": 123,
    ...             "misses": 123,
    ...             "partials": 123,
    ...             "coverage": 12.3,
    ...             "branches": 123,
    ...             "methods": 123,
    ...             "messages": 123,
    ...             "sessions": 123,
    ...             "complexity": 12.3,
    ...             "complexity_total": 12.3,
    ...             "complexity_ratio": 12.3,
    ...             "diff": 123,
    ...         },
    ...         "head": {
    ...             "files": 123,
    ...             "lines": 123,
    ...             "hits": 123,
    ...             "misses": 123,
    ...             "partials": 123,
    ...             "coverage": 12.3,
    ...             "branches": 123,
    ...             "methods": 123,
    ...             "messages": 123,
    ...             "sessions": 123,
    ...             "complexity": 12.3,
    ...             "complexity_total": 12.3,
    ...             "complexity_ratio": 12.3,
    ...             "diff": 123,
    ...         },
    ...         "patch": None,
    ...     },
    ...     "has_diff": True,
    ...     "stats": None,
    ...     "change_summary": None,
    ...     "lines": [],
    ... }
    >>> file_comparison = parse_file_comparison_data(data)
    >>> file_comparison
    FileComparison(name=FileNameComparison(...), totals=TotalComparison(...), has_diff=True, stats=None, change_summary=None, lines=[])
    """  # noqa: E501
    name = data.get("name")
    totals = data.get("totals")
    has_diff = data.get("has_diff")
    stats = data.get("stats")
    change_summary = data.get("change_summary")
    lines = data.get("lines")

    return FileComparison(
        parse_file_name_comparison_data(name),
        parse_total_comparison_data(totals),
        has_diff,
        parse_file_stat_comparison_data(stats) if stats is not None else stats,
        parse_file_change_summary_comparison_data(change_summary)
        if change_summary is not None
        else change_summary,
        [parse_line_comparison_data(line) for line in lines],
    )
