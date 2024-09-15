from dataclasses import dataclass

from ..enums import Service

__all__ = ["Owner"]


@dataclass(slots=True)
class Owner:
    """
    A schema used to store info about owner.

    Attributes:
        service: Git hosting service provider of the owner.
        username: username of the owner.
        name: name of the owner.
    """

    service: Service
    username: str | None
    name: str | None
