from dataclasses import dataclass

from ..enums import Coverage

__all__ = ["Line"]


@dataclass(slots=True)
class Line:
    """
    A schema used to store info about line.

    Attributes:
        number: line number.
        coverage: line coverage status.
    """

    number: int
    coverage: Coverage
