from dataclasses import dataclass

from .commit_coverage import CommitCoverage
from .report_file import ReportFile

__all__ = ["CommitCoverageReport"]


@dataclass(slots=True)
class CommitCoverageReport(CommitCoverage):
    """
    A schema used to store info about commit coverage report.

    Attributes:
        files: file specific commit coverage totals.
    """

    files: list[ReportFile]
