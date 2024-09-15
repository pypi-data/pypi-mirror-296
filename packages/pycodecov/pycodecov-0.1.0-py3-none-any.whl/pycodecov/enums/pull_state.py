"""
Module to store a str enum class representation pull state.
"""

from enum import StrEnum

__all__ = ["PullState"]


class PullState(StrEnum):
    """
    A str enum class that define valid pull state.

    Attributes:
        OPEN: `"open"`
        MERGED: `"merged"`
        CLOSED: `"closed"`

    Examples:
        >>> PullState("open")
        <PullState.OPEN: 'open'>
        >>> PullState["OPEN"]
        <PullState.OPEN: 'open'>
        >>> PullState.OPEN
        <PullState.OPEN: 'open'>
        >>> PullState.OPEN == "open"
        True
        >>> print(PullState.OPEN)
        open
    """

    OPEN: str = "open"
    MERGED: str = "merged"
    CLOSED: str = "closed"
