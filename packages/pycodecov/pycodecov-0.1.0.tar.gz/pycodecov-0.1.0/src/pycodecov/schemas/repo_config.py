from dataclasses import dataclass

__all__ = ["RepoConfig"]


@dataclass(slots=True)
class RepoConfig:
    """
    A schema used to store info about repository config.

    Attributes:
        upload_token: token used for uploading coverage reports for repository.
        graph_token: token used for repository graphs.
    """

    upload_token: str
    graph_token: str
