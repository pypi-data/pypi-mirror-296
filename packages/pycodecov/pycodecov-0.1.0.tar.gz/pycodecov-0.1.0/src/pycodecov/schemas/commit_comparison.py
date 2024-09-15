from dataclasses import dataclass

from .commit import Commit
from .diff_comparison import DiffComparison
from .file_comparison import FileComparison
from .total_comparison import TotalComparison

__all__ = ["CommitComparison"]


@dataclass(slots=True)
class CommitComparison:
    """
    A schema used to store info about commit comparison.

    Attributes:
        base_commit: base commit SHA.
        head_commit: head commit SHA.
        totals: total comparison.
        commit_uploads: list of commits.
        diff: diff comparison.
        files: list of files comparison.
        untracked: list of untracked files name.
        has_unmerged_base_commits: whether if any commits exist in the base reference
            but not in the head reference.
    """

    base_commit: str
    head_commit: str
    totals: TotalComparison
    commit_uploads: list[Commit]
    diff: DiffComparison
    files: list[FileComparison]
    untracked: list[str]
    has_unmerged_base_commits: bool
