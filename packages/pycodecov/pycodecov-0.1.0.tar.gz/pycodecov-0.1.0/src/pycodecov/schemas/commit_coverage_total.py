from dataclasses import dataclass

from .base_report_file import BaseReportFile
from .commit_coverage import CommitCoverage

__all__ = ["CommitCoverageTotal"]


@dataclass(slots=True)
class CommitCoverageTotal(CommitCoverage):
    """
    A schema used to store info about commit coverage report.

    Attributes:
        files: file specific commit coverage totals.
    """

    files: list[BaseReportFile]
