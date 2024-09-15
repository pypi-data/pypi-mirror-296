from typing import Any

from ..schemas import User
from .owner import parse_owner_data

__all__ = ["parse_user_data"]


def parse_user_data(data: dict[str, Any]) -> User:
    """
    Parse user data.

    Args:
        data: user json data.

    Returns:
        A `User` schema.

    Examples:
    >>> data = {
    ...     "service": "github",
    ...     "username": "string",
    ...     "name": "string",
    ...     "activated": True,
    ...     "is_admin": True,
    ...     "email": "string",
    ... }
    >>> user = parse_user_data(data)
    >>> user
    User(service=<Service.GITHUB: 'github'>, username='string', name='string', activated=True, is_admin=True, email='string')
    """  # noqa: E501
    owner = parse_owner_data(data)

    service = owner.service
    username = owner.username
    name = owner.name

    activated = data.get("activated")
    is_admin = data.get("is_admin")
    email = data.get("email")

    return User(service, username, name, activated, is_admin, email)
