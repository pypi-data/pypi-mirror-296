"""
Module to store an int enum class representation coverage status.
"""

from enum import IntEnum

__all__ = ["Coverage"]


class Coverage(IntEnum):
    """
    An int enum class that define valid coverage status.

    Attributes:
        HIT: `0`
        MISS: `1`
        PARTIAL: `2`

    Examples:
        >>> Coverage(0)
        <Coverage.HIT: 0>
        >>> Coverage["HIT"]
        <Coverage.HIT: 0>
        >>> Coverage.HIT
        <Coverage.HIT: 0>
        >>> Coverage.HIT == 0
        True
        >>> print(Coverage.HIT)
        0
    """

    HIT: int = 0
    MISS: int = 1
    PARTIAL: int = 2
