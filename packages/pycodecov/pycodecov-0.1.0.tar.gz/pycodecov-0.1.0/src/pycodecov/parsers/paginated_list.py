from typing import Any, Callable

from ..schemas import PaginatedList

__all__ = ["parse_paginated_list_data"]


def parse_paginated_list_data[T](
    data: dict[str, Any], parser: Callable[[dict[str, Any]], T]
) -> PaginatedList[T]:
    """
    Parse paginated list data.

    Args:
        data: a paginated list data.

    Returns:
        A `PaginatedList` schema.

    Examples:
    >>> from pycodecov.parsers import parse_owner_data
    >>> data = {
    ...     "count": 123,
    ...     "next": "http://api.codecov.io/api/v2/github/?page=4",
    ...     "previous": "http://api.codecov.io/api/v2/github/?page=2",
    ...     "results": [
    ...         {"service": "github", "username": "string", "name": "string"},
    ...     ],
    ...     "total_pages": 7,
    ... }
    >>> paginated_list = parse_paginated_list_data(data, parse_owner_data)
    >>> paginated_list
    PaginatedList(...)
    """
    count = data.get("count")

    next = data.get("next")
    if next is not None:
        next = next[21:]

    previous = data.get("previous")
    if previous is not None:
        previous = previous[21:]

    results = [parser(result) for result in data.get("results")]
    total_pages = data.get("total_pages")

    return PaginatedList(count, next, previous, results, total_pages)
