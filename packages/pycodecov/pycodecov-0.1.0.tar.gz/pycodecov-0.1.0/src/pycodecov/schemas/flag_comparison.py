from dataclasses import dataclass

from .flag import Flag
from .report_total import ReportTotal

__all__ = ["FlagComparison"]


@dataclass(slots=True)
class FlagComparison(Flag):
    """
    A schema used to store info about flag comparison.

    Attributes:
        base_report_totals: base totals coverage report information.
        head_report_totals: head totals coverage report information.
        diff_totals: diff totals coverage report information.
    """

    base_report_totals: ReportTotal
    head_report_totals: ReportTotal
    diff_totals: ReportTotal | None
