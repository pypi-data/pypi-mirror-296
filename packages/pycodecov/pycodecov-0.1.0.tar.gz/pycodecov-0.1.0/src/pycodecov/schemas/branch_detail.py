from dataclasses import dataclass

from .branch import Branch
from .commit_detail import CommitDetail

__all__ = ["BranchDetail"]


@dataclass(slots=True)
class BranchDetail(Branch):
    """
    A schema used to store info about branch detail.

    Attributes:
        head_commit: branch's current head commit.
    """

    head_commit: CommitDetail
