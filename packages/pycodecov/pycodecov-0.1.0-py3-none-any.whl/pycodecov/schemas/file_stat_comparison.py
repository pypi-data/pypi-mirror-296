from dataclasses import dataclass

__all__ = ["FileStatComparison"]


@dataclass(slots=True)
class FileStatComparison:
    """
    A schema used to store info about file stat comparison.

    Attributes:
        added: added count.
        removed: removed count.
    """

    added: int
    removed: int
