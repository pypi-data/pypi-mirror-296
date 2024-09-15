from dataclasses import dataclass

from .file_change_summary_comparison import FileChangeSummaryComparison
from .file_name_comparison import FileNameComparison
from .file_stat_comparison import FileStatComparison
from .line_comparison import LineComparison
from .total_comparison import TotalComparison

__all__ = ["FileComparison"]


@dataclass(slots=True)
class FileComparison:
    """
    A schema used to store info about file comparison.

    Attributes:
        name: file name comparison.
        totals: totals file comparison.
        has_diff: whether the file has diff data.
        stats: file stat.
        change_summary: file coverage change summary.
        lines: lines comparison.
    """

    name: FileNameComparison
    totals: TotalComparison
    has_diff: bool
    stats: FileStatComparison | None
    change_summary: FileChangeSummaryComparison | None
    lines: list[LineComparison]
