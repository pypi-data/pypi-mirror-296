from dataclasses import dataclass

__all__ = ["BaseTotal"]


@dataclass(slots=True)
class BaseTotal:
    """
    A schema used to store info about base totals coverage information.

    Attributes:
        files: files count.
        lines: lines count.
        hits: hits count.
        misses: misses count.
        partials: partials count.
        coverage: coverage count.
        branches: branches count.
        methods: methods count.
    """

    files: int
    lines: int
    hits: int
    misses: int
    partials: int
    coverage: float
    branches: int
    methods: int
