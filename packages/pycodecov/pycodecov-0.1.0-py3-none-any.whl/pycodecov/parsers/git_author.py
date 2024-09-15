from typing import Any

from ..schemas import GitAuthor

__all__ = ["parse_git_author_data"]


def parse_git_author_data(data: dict[str, Any]) -> GitAuthor:
    """
    Parse git author data.

    Args:
        data: git author json data.

    Returns:
        A `GitAuthor` schema.

    Examples:
    >>> data = {
    ...     "id": 123,
    ...     "username": "string",
    ...     "name": "string",
    ...     "email": "string",
    ... }
    >>> git_author = parse_git_author_data(data)
    >>> git_author
    GitAuthor(id=123, username='string', name='string', email='string')
    """
    id = data.get("id")
    username = data.get("username")
    name = data.get("name")
    email = data.get("email")

    return GitAuthor(id, username, name, email)
