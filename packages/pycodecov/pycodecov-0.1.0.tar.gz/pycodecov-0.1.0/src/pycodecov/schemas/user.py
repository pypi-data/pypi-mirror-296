from dataclasses import dataclass

from .owner import Owner

__all__ = ["User"]


@dataclass(slots=True)
class User(Owner):
    """
    A schema used to store info about user.

    Attributes:
        activated: whether the user has been manually deactivated.
        is_admin: whether the user is an admin.
        email: email of the user.

    Note:
        It is actually impossible for the fields `activated` and `is_admin` to have the
        value `None` based on the API documentation, however, to make it easier to use
        the API wrapper so that it is more flexible, these fields are made so that they
        can contain the value `None`.
    """

    activated: bool | None
    is_admin: bool | None
    email: str | None
