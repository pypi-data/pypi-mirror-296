from dataclasses import dataclass

__all__ = ["FileChangeSummaryComparison"]


@dataclass(slots=True)
class FileChangeSummaryComparison:
    """
    A schema used to store info about file coverage change summary comparison.

    Attributes:
        hits: line coverage hits count summary.
        misses: line coverage misses count summary.
        partials: line coverage partials count summary.
    """

    hits: int | None
    misses: int | None
    partials: int | None
