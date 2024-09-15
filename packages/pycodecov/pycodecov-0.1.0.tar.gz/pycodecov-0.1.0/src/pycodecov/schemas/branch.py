from dataclasses import dataclass
from datetime import datetime

__all__ = ["Branch"]


@dataclass(slots=True)
class Branch:
    """
    A schema used to store info about branch.

    Attributes:
        name: branch name.
        updatestamp: last time the branch was updated.
    """

    name: str
    updatestamp: datetime
