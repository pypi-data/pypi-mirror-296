from dataclasses import dataclass
from datetime import datetime

from ..enums import PullState
from .commit_total import CommitTotal
from .owner import Owner

__all__ = ["Pull"]


@dataclass(slots=True)
class Pull:
    """
    A schema used to store info about pull.

    Attributes:
        pullid: pull id number.
        title: title of the pull.
        base_total: coverage totals of base commit.
        head_total: coverage totals of head commit.
        updatestamp: last time the pull was updated.
        state: pull state of the pull.
        ci_passed: whether pull pass ci.
        author: pull author.
    """

    pullid: int
    title: str | None
    base_total: CommitTotal
    head_total: CommitTotal
    updatestamp: datetime
    state: PullState
    ci_passed: bool
    author: Owner | None
