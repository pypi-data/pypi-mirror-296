from dataclasses import dataclass

from .report_total import ReportTotal

__all__ = ["TotalComparison"]


@dataclass(slots=True)
class TotalComparison:
    """
    A schema used to store info about total comparison.

    Attributes:
        base: base totals coverage report information.
        head: head totals coverage report information.
        patch: patch totals coverage report information.
    """

    base: ReportTotal
    head: ReportTotal
    patch: ReportTotal | None
