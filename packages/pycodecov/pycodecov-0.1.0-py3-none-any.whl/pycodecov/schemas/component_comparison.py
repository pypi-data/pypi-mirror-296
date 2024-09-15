from dataclasses import dataclass

from .component import Component
from .report_total import ReportTotal

__all__ = ["ComponentComparison"]


@dataclass(slots=True)
class ComponentComparison(Component):
    """
    A schema used to store info about component comparison.

    Attributes:
        base_report_totals: base totals coverage report information.
        head_report_totals: head totals coverage report information.
        diff_totals: diff totals coverage report information.
    """

    base_report_totals: ReportTotal
    head_report_totals: ReportTotal
    diff_totals: ReportTotal | None
