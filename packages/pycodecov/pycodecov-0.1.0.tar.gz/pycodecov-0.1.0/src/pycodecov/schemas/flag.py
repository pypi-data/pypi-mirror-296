from dataclasses import dataclass

__all__ = ["Flag"]


@dataclass(slots=True)
class Flag:
    """
    A schema used to store info about flag.

    Attributes:
        name: flag name.
    """

    name: str
