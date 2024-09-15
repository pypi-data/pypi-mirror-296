from typing import Any

from ..schemas import Flag

__all__ = ["parse_flag_data"]


def parse_flag_data(data: dict[str, Any]) -> Flag:
    """
    Parse flag data.

    Args:
        data: flag json data.

    Returns:
        A `Flag` schema.

    Examples:
    >>> data = {
    ...     "name": "string",
    ... }
    >>> flag = parse_flag_data(data)
    >>> flag
    Flag(name='string')
    """
    name = data.get("name")

    return Flag(name)
