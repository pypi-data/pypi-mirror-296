from dataclasses import dataclass

__all__ = ["LineNumberComparison"]


@dataclass(slots=True)
class LineNumberComparison:
    """
    A schema used to store info about line number comparison.

    Attributes:
        base: base line number.
        head: head line number.
    """

    base: int | None
    head: int | None
