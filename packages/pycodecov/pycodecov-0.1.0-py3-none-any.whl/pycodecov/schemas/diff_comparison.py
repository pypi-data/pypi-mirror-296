from dataclasses import dataclass

from .git_commit import GitCommit

__all__ = ["DiffComparison"]


@dataclass(slots=True)
class DiffComparison:
    """
    A schema used to store info about diff comparison.

    Attributes:
        git_commits: list of git commit.
    """

    git_commits: list[GitCommit]
