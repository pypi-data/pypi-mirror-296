from dataclasses import dataclass
from datetime import datetime

__all__ = ["BaseCommit"]


@dataclass(slots=True)
class BaseCommit:
    """
    A schema used to store info about base commit.

    Attributes:
        commitid: commit SHA.
        message: commit message.
        timestamp: timestamp when commit was made.
    """

    commitid: str
    message: str | None
    timestamp: datetime
