"""
Module to store a str enum class representation interval.
"""

from enum import StrEnum

__all__ = ["Interval"]


class Interval(StrEnum):
    """
    A str enum class that define valid interval.

    Attributes:
        ONE_DAY: `"1d"`, one day
        ONE_WEEK: `"7d"`, one week
        ONE_MONTH: `"30d"`, one month

    Examples:
        >>> Interval("1d")
        <Interval.ONE_DAY: '1d'>
        >>> Interval["ONE_DAY"]
        <Interval.ONE_DAY: '1d'>
        >>> Interval.ONE_DAY
        <Interval.ONE_DAY: '1d'>
        >>> Interval.ONE_DAY == "1d"
        True
        >>> print(Interval.ONE_DAY)
        1d
    """

    ONE_DAY: str = "1d"
    ONE_WEEK: str = "7d"
    ONE_MONTH: str = "30d"
