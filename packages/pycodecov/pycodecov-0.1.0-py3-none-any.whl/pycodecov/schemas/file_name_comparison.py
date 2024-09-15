from dataclasses import dataclass

__all__ = ["FileNameComparison"]


@dataclass(slots=True)
class FileNameComparison:
    """
    A schema used to store info about file name comparison.

    Attributes:
        base: base file name.
        head: head file name.
    """

    base: str | None
    head: str | None
