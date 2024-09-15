from dataclasses import dataclass

from .base_report_file import BaseReportFile
from .report_total import ReportTotal

__all__ = ["Report"]


@dataclass(slots=True)
class Report:
    """
    A schema used to store info about report.

    Attributes:
        totals: coverage totals.
        files: file specific coverage totals.
    """

    totals: ReportTotal
    files: list[BaseReportFile]
