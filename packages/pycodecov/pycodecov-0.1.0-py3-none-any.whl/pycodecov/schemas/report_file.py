from dataclasses import dataclass

from .base_report_file import BaseReportFile
from .line import Line

__all__ = ["ReportFile"]


@dataclass(slots=True)
class ReportFile(BaseReportFile):
    """
    A schema used to store info about report file.

    Attributes:
        line_coverage: line-by-line coverage values.
    """

    line_coverage: list[Line]
