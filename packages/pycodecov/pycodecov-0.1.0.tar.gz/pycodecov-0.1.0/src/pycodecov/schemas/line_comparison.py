from dataclasses import dataclass

from .line_coverage_comparison import LineCoverageComparison
from .line_number_comparison import LineNumberComparison

__all__ = ["LineComparison"]


@dataclass(slots=True)
class LineComparison:
    """
    A schema used to store info about line comparison.

    Attributes:
        value: text contained in the line.
        number: line number comparison.
        coverage: line coverage status comparison.
        is_diff: whether the line is in diff.
        added: whether the line was added.
        removed: whether the line was removed.
        sessions: sessions count.
    """

    value: str
    number: LineNumberComparison
    coverage: LineCoverageComparison
    is_diff: bool
    added: bool
    removed: bool
    sessions: int
