"""
Module to store a str enum class representation Git hosting service provider.
"""

from enum import StrEnum

__all__ = ["Service"]


class Service(StrEnum):
    """
    A str enum class that define valid Git hosting service provider.

    Attributes:
        BITBUCKET: `"bitbucket"`
        BITBUCKET_SERVER: `"bitbucket_server"`
        GITHUB: `"github"`
        GITHUB_ENTERPRISE: `"github_enterprise"`
        GITLAB: `"gitlab"`
        GITLAB_ENTERPRISE: `"gitlab_enterprise"`

    Examples:
        >>> Service("bitbucket")
        <Service.BITBUCKET: 'bitbucket'>
        >>> Service["BITBUCKET"]
        <Service.BITBUCKET: 'bitbucket'>
        >>> Service.BITBUCKET
        <Service.BITBUCKET: 'bitbucket'>
        >>> Service.BITBUCKET == "bitbucket"
        True
        >>> print(Service.BITBUCKET)
        bitbucket
    """

    BITBUCKET: str = "bitbucket"
    BITBUCKET_SERVER: str = "bitbucket_server"
    GITHUB: str = "github"
    GITHUB_ENTERPRISE: str = "github_enterprise"
    GITLAB: str = "gitlab"
    GITLAB_ENTERPRISE: str = "gitlab_enterprise"
