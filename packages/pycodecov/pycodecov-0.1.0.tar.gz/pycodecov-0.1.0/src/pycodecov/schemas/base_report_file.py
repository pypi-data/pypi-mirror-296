from dataclasses import dataclass

from .report_total import ReportTotal

__all__ = ["BaseReportFile"]


@dataclass(slots=True)
class BaseReportFile:
    """
    A schema used to store info about base report file.

    Attributes:
        name: file path.
        totals: coverage totals.
    """

    name: str
    totals: ReportTotal
