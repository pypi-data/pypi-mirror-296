"""
Module to store a str enum class representation commit state.
"""

from enum import StrEnum

__all__ = ["CommitState"]


class CommitState(StrEnum):
    """
    A str enum class that define valid commit state.

    Attributes:
        COMPLETE: `"complete"`
        PENDING: `"pending"`
        ERROR: `"error"`
        SKIPPED: `"skipped"`

    Examples:
        >>> CommitState("complete")
        <CommitState.COMPLETE: 'complete'>
        >>> CommitState["COMPLETE"]
        <CommitState.COMPLETE: 'complete'>
        >>> CommitState.COMPLETE
        <CommitState.COMPLETE: 'complete'>
        >>> CommitState.COMPLETE == "complete"
        True
        >>> print(CommitState.COMPLETE)
        complete
    """

    COMPLETE: str = "complete"
    PENDING: str = "pending"
    ERROR: str = "error"
    SKIPPED: str = "skipped"
