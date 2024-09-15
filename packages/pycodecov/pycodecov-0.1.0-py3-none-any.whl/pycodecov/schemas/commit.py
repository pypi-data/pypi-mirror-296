from dataclasses import dataclass

from ..enums import CommitState
from .base_commit import BaseCommit
from .commit_total import CommitTotal
from .owner import Owner

__all__ = ["Commit"]


@dataclass(slots=True)
class Commit(BaseCommit):
    """
    A schema used to store info about commit.

    Attributes:
        ci_passed: whether the CI process passed for this commit.
        author: commit author.
        branch: branch name on which this commit currently lives.
        totals: commit totals coverage information.
        state: codecov processing state for this commit.
        parent: commit SHA of first ancestor commit with coverage.
    """

    ci_passed: bool | None
    author: Owner | None
    branch: str | None
    totals: CommitTotal | None
    state: CommitState | None
    parent: str | None
