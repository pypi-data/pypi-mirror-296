from typing import Any

from ..schemas import DiffComparison
from .git_commit import parse_git_commit_data

__all__ = ["parse_diff_comparison_data"]


def parse_diff_comparison_data(data: dict[str, Any]) -> DiffComparison:
    """
    Parse diff comparison data.

    Args:
        data: diff comparison json data.

    Returns:
        A `DiffComparison` schema.

    Examples:
    >>> data = {
    ...     "git_commits": [],
    ... }
    >>> diff_comparison = parse_diff_comparison_data(data)
    >>> diff_comparison
    DiffComparison(git_commits=[])
    """
    git_commits = data.get("git_commits")

    return DiffComparison(
        [parse_git_commit_data(git_commit) for git_commit in git_commits]
    )
