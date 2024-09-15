from dataclasses import dataclass

__all__ = ["GitAuthor"]


@dataclass(slots=True)
class GitAuthor:
    """
    A schema used to store info about git author.

    Attributes:
        id: git author id.
        username: username of the git author.
        name: name of the git author.
        email: name of the git author.
    """

    id: int
    username: str | None
    name: str
    email: str
