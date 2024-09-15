from datetime import datetime
from typing import Any

from ..schemas import Branch

__all__ = ["parse_branch_data"]


def parse_branch_data(data: dict[str, Any]) -> Branch:
    """
    Parse branch data.

    Args:
        data: branch json data.

    Returns:
        A `Branch` schema.

    Examples:
    >>> data = {
    ...     "name": "string",
    ...     "updatestamp": "2024-03-25T16:38:25.747678Z",
    ... }
    >>> branch = parse_branch_data(data)
    >>> branch
    Branch(name='string', updatestamp=datetime.datetime(...))
    """
    name = data.get("name")
    updatestamp = data.get("updatestamp")

    return Branch(name, datetime.fromisoformat(updatestamp))
