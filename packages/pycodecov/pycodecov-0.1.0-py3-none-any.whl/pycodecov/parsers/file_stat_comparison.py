from typing import Any

from ..schemas import FileStatComparison

__all__ = ["parse_file_stat_comparison_data"]


def parse_file_stat_comparison_data(data: dict[str, Any]) -> FileStatComparison:
    """
    Parse file stat comparison data.

    Args:
        data: file stat comparison json data.

    Returns:
        A `FileStatComparison` schema.

    Examples:
    >>> data = {
    ...     "added": 0,
    ...     "removed": 0,
    ... }
    >>> file_stat_comparison = parse_file_stat_comparison_data(data)
    >>> file_stat_comparison
    FileStatComparison(added=0, removed=0)
    """
    added = data.get("added")
    removed = data.get("removed")

    return FileStatComparison(added, removed)
