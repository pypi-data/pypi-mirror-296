from typing import Any

from ..schemas import CommitComparison
from .commit import parse_commit_data
from .diff_comparison import parse_diff_comparison_data
from .file_comparison import parse_file_comparison_data
from .total_comparison import parse_total_comparison_data

__all__ = ["parse_commit_comparison_data"]


def parse_commit_comparison_data(data: dict[str, Any]) -> CommitComparison:
    """
    Parse commit comparison data.

    Args:
        data: commit comparison json data.

    Returns:
        A `CommitComparison` schema.

    Examples:
    >>> data = {
    ...     "base_commit": "string",
    ...     "head_commit": "string",
    ...     "totals": {
    ...         "base": {
    ...             "files": 123,
    ...             "lines": 123,
    ...             "hits": 123,
    ...             "misses": 123,
    ...             "partials": 123,
    ...             "coverage": 12.3,
    ...             "branches": 123,
    ...             "methods": 123,
    ...             "messages": 123,
    ...             "sessions": 123,
    ...             "complexity": 12.3,
    ...             "complexity_total": 12.3,
    ...             "complexity_ratio": 12.3,
    ...             "diff": 123,
    ...         },
    ...         "head": {
    ...             "files": 123,
    ...             "lines": 123,
    ...             "hits": 123,
    ...             "misses": 123,
    ...             "partials": 123,
    ...             "coverage": 12.3,
    ...             "branches": 123,
    ...             "methods": 123,
    ...             "messages": 123,
    ...             "sessions": 123,
    ...             "complexity": 12.3,
    ...             "complexity_total": 12.3,
    ...             "complexity_ratio": 12.3,
    ...             "diff": 123,
    ...         },
    ...         "patch": None,
    ...     },
    ...     "commit_uploads": [],
    ...     "diff": {
    ...         "git_commits": [],
    ...     },
    ...     "files": [],
    ...     "untracked": [],
    ...     "has_unmerged_base_commits": False,
    ... }
    >>> commit_comparison = parse_commit_comparison_data(data)
    >>> commit_comparison
    CommitComparison(base_commit='string', head_commit='string', totals=TotalComparison(...), commit_uploads=[], diff=DiffComparison(...), files=[], untracked=[], has_unmerged_base_commits=False)
    """  # noqa: E501
    base_commit = data.get("base_commit")
    head_commit = data.get("head_commit")
    totals = data.get("totals")
    commit_uploads = data.get("commit_uploads")
    diff = data.get("diff")
    files = data.get("files")
    untracked = data.get("untracked")
    has_unmerged_base_commits = data.get("has_unmerged_base_commits")

    return CommitComparison(
        base_commit,
        head_commit,
        parse_total_comparison_data(totals),
        [parse_commit_data(commit_upload) for commit_upload in commit_uploads],
        parse_diff_comparison_data(diff),
        [parse_file_comparison_data(file) for file in files],
        untracked,
        has_unmerged_base_commits,
    )
