from dataclasses import dataclass
from datetime import datetime

from ..enums import Language
from .commit_total import CommitTotal
from .owner import Owner

__all__ = ["Repo"]


@dataclass(slots=True)
class Repo:
    """
    A schema used to store info about repository.

    Attributes:
        name: repository name.
        private: whether private or public repository.
        updatestamp: last time the repository was updated.
        author: repository owner.
        language: primary programming language used.
        branch: default branch name.
        active: whether the repository has received a coverage upload.
        activated: whether the repository has been manually deactivated.
        totals: recent commit totals on the default branch.
    """

    name: str
    private: bool
    updatestamp: datetime | None
    author: Owner
    language: Language | None
    branch: str
    active: bool | None
    activated: bool | None
    totals: CommitTotal | None
