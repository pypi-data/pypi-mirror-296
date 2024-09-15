from typing import Any

from aiohttp import ClientSession

from .. import schemas
from ..enums import Service
from ..exceptions import CodecovError
from ..parsers import parse_user_data
from ..types import CodecovApiToken
from .api import API

__all__ = [
    "User",
    "parse_user_api",
]


class User(API, schemas.User):
    """
    User API Wrapper from Codecov API.
    """

    def __init__(
        self,
        service: Service,
        owner_username: str,
        user_username_or_ownerid: str,
        name: str | None = None,
        activated: bool | None = None,
        is_admin: bool | None = None,
        email: str | None = None,
        token: CodecovApiToken | None = None,
        session: ClientSession | None = None,
    ) -> None:
        API.__init__(self, token, session)
        schemas.User.__init__(
            self, service, user_username_or_ownerid, name, activated, is_admin, email
        )

        self.owner_username = owner_username

    async def get_detail(self) -> schemas.User:
        """
        Get a user for the specified owner_username or ownerid.

        Returns:
            A `User`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         service_owners = await codecov.get_service_owners(Service.GITHUB)
            ...         for service_owner in service_owners:
            ...             users = await service_owner.get_users()
            ...             for user in users:
            ...                 print(await user.get_detail())
            >>> asyncio.run(main())
            User(...)
            ...
        """  # noqa: E501
        async with self._session.get(
            f"{self.api_url}/{self.service}/{self.owner_username}/users/{self.username}"
        ) as response:
            data = await response.json()

            if response.ok:
                return parse_user_data(data)

            raise CodecovError(data)


def parse_user_api(
    schema: schemas.User,
    token: CodecovApiToken | None = None,
    session: ClientSession | None = None,
    **kwargs: Any,
) -> User:
    """
    Turn User schema into User API.

    Args:
        schema: user data.
        token: Codecov API Token.
        session: client session.

    Returns:
        An `User` API.

    Examples:
    >>> import asyncio
    >>> async def main():
    ...     data = {
    ...         "service": "github",
    ...         "username": "string",
    ...         "name": "string",
    ...         "activated": True,
    ...         "is_admin": True,
    ...         "email": "string",
    ...     }
    ...     user = parse_user_data(data)
    ...     user_api = parse_user_api(user, owner_username="string")
    ...     print(user_api)
    >>> asyncio.run(main())
    User(service=<Service.GITHUB: 'github'>, username='string', name='string', activated=True, is_admin=True, email='string')
    """  # noqa: E501
    return User(
        schema.service,
        kwargs["owner_username"],
        schema.username,
        schema.name,
        schema.activated,
        schema.is_admin,
        schema.email,
        token,
        session,
    )
