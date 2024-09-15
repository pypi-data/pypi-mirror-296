from typing import Any

from ..schemas import FileNameComparison

__all__ = ["parse_file_name_comparison_data"]


def parse_file_name_comparison_data(data: dict[str, Any]) -> FileNameComparison:
    """
    Parse file name comparison data.

    Args:
        data: file name comparison json data.

    Returns:
        A `FileNameComparison` schema.

    Examples:
    >>> data = {
    ...     "base": "string",
    ...     "head": "string",
    ... }
    >>> file_name_comparison = parse_file_name_comparison_data(data)
    >>> file_name_comparison
    FileNameComparison(base='string', head='string')
    """
    base = data.get("base")
    head = data.get("head")

    return FileNameComparison(base, head)
