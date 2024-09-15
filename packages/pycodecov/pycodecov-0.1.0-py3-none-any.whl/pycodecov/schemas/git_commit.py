from dataclasses import dataclass

from .base_commit import BaseCommit
from .git_author import GitAuthor

__all__ = ["GitCommit"]


@dataclass(slots=True)
class GitCommit(BaseCommit):
    """
    A schema used to store info about git commit.

    Attributes:
        author: commit author.
    """

    author: GitAuthor
