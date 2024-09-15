from typing import Any

from ..schemas import FileChangeSummaryComparison

__all__ = ["parse_file_change_summary_comparison_data"]


def parse_file_change_summary_comparison_data(
    data: dict[str, Any],
) -> FileChangeSummaryComparison:
    """
    Parse file change summary comparison data.

    Args:
        data: file change summary comparison json data.

    Returns:
        A `FileChangeSummaryComparison` schema.

    Examples:
    >>> data = {
    ...     "hits": 0,
    ...     "misses": 0,
    ...     "partials": 0,
    ... }
    >>> file_change_summary_comparison = parse_file_change_summary_comparison_data(data)
    >>> file_change_summary_comparison
    FileChangeSummaryComparison(hits=0, misses=0, partials=0)
    """
    hits = data.get("hits")
    misses = data.get("misses")
    partials = data.get("partials")

    return FileChangeSummaryComparison(hits, misses, partials)
