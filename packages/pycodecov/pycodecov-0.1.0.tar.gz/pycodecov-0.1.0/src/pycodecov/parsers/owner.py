from typing import Any

from ..enums import Service
from ..schemas import Owner

__all__ = ["parse_owner_data"]


def parse_owner_data(data: dict[str, Any]) -> Owner:
    """
    Parse owner data.

    Args:
        data: owner json data.

    Returns:
        An `Owner` schema.

    Examples:
    >>> data = {
    ...     "service": "github",
    ...     "username": "string",
    ...     "name": "string",
    ... }
    >>> owner = parse_owner_data(data)
    >>> owner
    Owner(service=<Service.GITHUB: 'github'>, username='string', name='string')
    """
    service = data.get("service")
    username = data.get("username")
    name = data.get("name")

    return Owner(Service(service), username, name)
