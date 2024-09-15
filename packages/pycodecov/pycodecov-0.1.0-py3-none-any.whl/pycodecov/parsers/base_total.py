from typing import Any

from ..schemas import BaseTotal

__all__ = ["parse_base_total_data"]


def parse_base_total_data(data: dict[str, Any]) -> BaseTotal:
    """
    Parse base total data.

    Args:
        data: base total json data.

    Returns:
        A `BaseTotal` schema.

    Examples:
    >>> data = {
    ...     "files": 123,
    ...     "lines": 123,
    ...     "hits": 123,
    ...     "misses": 123,
    ...     "partials": 123,
    ...     "coverage": 12.3,
    ...     "branches": 123,
    ...     "methods": 123,
    ... }
    >>> base_total = parse_base_total_data(data)
    >>> base_total
    BaseTotal(files=123, lines=123, hits=123, misses=123, partials=123, coverage=12.3, branches=123, methods=123)
    """  # noqa: E501
    files = data.get("files")
    lines = data.get("lines")
    hits = data.get("hits")
    misses = data.get("misses")
    partials = data.get("partials")
    coverage = data.get("coverage")
    branches = data.get("branches")
    methods = data.get("methods")

    return BaseTotal(files, lines, hits, misses, partials, coverage, branches, methods)
