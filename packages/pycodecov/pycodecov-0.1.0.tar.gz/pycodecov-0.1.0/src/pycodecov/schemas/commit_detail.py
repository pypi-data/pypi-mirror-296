from dataclasses import dataclass

from .commit import Commit
from .report import Report

__all__ = ["CommitDetail"]


@dataclass(slots=True)
class CommitDetail(Commit):
    """
    A schema used to store info about commit detail.

    Attributes:
        report: coverage report.
    """

    report: Report
