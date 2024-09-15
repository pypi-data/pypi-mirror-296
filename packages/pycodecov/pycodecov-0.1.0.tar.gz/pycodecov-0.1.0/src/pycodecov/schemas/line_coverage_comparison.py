from dataclasses import dataclass

from ..enums import Coverage

__all__ = ["LineCoverageComparison"]


@dataclass(slots=True)
class LineCoverageComparison:
    """
    A schema used to store info about line coverage comparison.

    Attributes:
        base: base line coverage status.
        head: head line coverage status.
    """

    base: Coverage | None
    head: Coverage | None
