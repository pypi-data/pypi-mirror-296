from dataclasses import dataclass

from .report_total import ReportTotal

__all__ = ["CommitCoverage"]


@dataclass(slots=True)
class CommitCoverage:
    """
    A schema used to store info about commit coverage.

    Attributes:
        totals: totals coverage report information.
        commit_file_url: Codecov URL to see file coverage on commit.
    """

    totals: ReportTotal
    commit_file_url: str
