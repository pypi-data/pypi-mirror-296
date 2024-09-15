from dataclasses import dataclass

from .base_total import BaseTotal

__all__ = ["ReportTotal"]


@dataclass(slots=True)
class ReportTotal(BaseTotal):
    """
    A schema used to store info about totals coverage report information.

    Attributes:
        messages: messages count.
        sessions: sessions count.
        complexity: complexity count.
        complexity_total: complexity_total count.
        complexity_ratio: complexity_ratio count.
        diff: diff report.
    """

    messages: int
    sessions: int
    complexity: float
    complexity_total: float
    complexity_ratio: float
    diff: int | list[int | str | None]
