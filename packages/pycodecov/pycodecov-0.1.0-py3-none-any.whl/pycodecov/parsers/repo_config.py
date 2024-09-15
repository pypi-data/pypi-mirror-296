from typing import Any

from ..schemas import RepoConfig

__all__ = ["parse_repo_config_data"]


def parse_repo_config_data(data: dict[str, Any]) -> RepoConfig:
    """
    Parse repo config data.

    Args:
        data: repo config json data.

    Returns:
        A `RepoConfig` schema.

    Examples:
    >>> data = {
    ...     "upload_token": "string",
    ...     "graph_token": "string",
    ... }
    >>> repo_config = parse_repo_config_data(data)
    >>> repo_config
    RepoConfig(upload_token='string', graph_token='string')
    """
    upload_token = data.get("upload_token")
    graph_token = data.get("graph_token")

    return RepoConfig(upload_token, graph_token)
