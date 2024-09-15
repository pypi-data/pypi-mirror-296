from dataclasses import dataclass

from .base_total import BaseTotal

__all__ = ["CommitTotal"]


@dataclass(slots=True)
class CommitTotal(BaseTotal):
    """
    A schema used to store info about totals coverage commit information.

    Attributes:
        sessions: sessions count.
        complexity: complexity count.
        complexity_total: complexity_total count.
        complexity_ratio: complexity_ratio count.
    """

    sessions: int
    complexity: float
    complexity_total: float
    complexity_ratio: float
