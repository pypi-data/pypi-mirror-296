from typing import Any

from aiohttp import ClientSession

from .. import schemas
from ..enums import Service
from ..exceptions import CodecovError
from ..parsers import parse_owner_data, parse_paginated_list_data, parse_user_data
from ..types import CodecovApiToken
from .api import API
from .paginated_list import PaginatedList, PaginatedListApi, parse_paginated_list_api
from .user import User, parse_user_api

__all__ = [
    "Owner",
    "parse_owner_api",
]


class Owner(API, schemas.Owner):
    """
    Owner API Wrapper from Codecov API.
    """

    def __init__(
        self,
        service: Service,
        owner_username: str,
        name: str | None = None,
        token: CodecovApiToken | None = None,
        session: ClientSession | None = None,
    ) -> None:
        API.__init__(self, token, session)
        schemas.Owner.__init__(self, service, owner_username, name)

    async def get_detail(self) -> schemas.Owner:
        """
        Get a single owner by name.

        Returns:
            An `Owner`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         service_owners = await codecov.get_service_owners(Service.GITHUB)
            ...         for service_owner in service_owners:
            ...             print(await service_owner.get_detail())
            >>> asyncio.run(main())
            Owner(...)
            ...
        """  # noqa: E501
        async with self._session.get(
            f"{self.api_url}/{self.service}/{self.username}"
        ) as response:
            data = await response.json()

            if response.ok:
                return parse_owner_data(data)

            raise CodecovError(data)

    async def get_users(
        self,
        activated: bool | None = None,
        is_admin: bool | None = None,
        page: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
    ) -> PaginatedListApi[User]:
        """
        Get a paginated list of users for the specified owner (org).

        Args:
            activated: whether the user has been manually deactivated.
            is_admin: whether the user is admin.
            page: a page number within the paginated result set.
            page_size: number of results to return per page.
            search: a search term.

        Returns:
            Paginated list of `User`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         service_owners = await codecov.get_service_owners(Service.GITHUB)
            ...         for service_owner in service_owners:
            ...             print(await service_owner.get_users())
            >>> asyncio.run(main())
            PaginatedListApi(...)
        """  # noqa: E501
        params = {}
        optional_params = {
            "activated": str(activated).lower() if activated is not None else activated,
            "is_admin": str(is_admin).lower() if is_admin is not None else is_admin,
            "page": str(page) if page is not None else page,
            "page_size": str(page_size) if page_size is not None else page_size,
            "search": search,
        }

        params.update({k: v for k, v in optional_params.items() if v is not None})

        async with self._session.get(
            f"{self.api_url}/{self.service}/{self.username}/users", params=params
        ) as response:
            data = await response.json()

            if response.ok:
                paginated_list_data = parse_paginated_list_data(data, parse_user_data)
                paginated_list = PaginatedList(
                    paginated_list_data.count,
                    paginated_list_data.results,
                    paginated_list_data.total_pages,
                    parse_user_data,
                    paginated_list_data.next,
                    paginated_list_data.previous,
                    self._token,
                    self._session,
                )

                return parse_paginated_list_api(
                    paginated_list,
                    parse_user_api,
                    owner_username=self.username,
                )

            raise CodecovError(data)


def parse_owner_api(
    schema: schemas.Owner,
    token: CodecovApiToken | None = None,
    session: ClientSession | None = None,
    **kwargs: Any,
) -> Owner:
    """
    Turn Owner schema into Owner API.

    Args:
        schema: owner data.
        token: Codecov API Token.
        session: client session.

    Returns:
        An `Owner` API.

    Examples:
    >>> import asyncio
    >>> async def main():
    ...     data = {
    ...         "service": "github",
    ...         "username": "string",
    ...         "name": "string",
    ...     }
    ...     owner = parse_owner_data(data)
    ...     owner_api = parse_owner_api(owner)
    ...     print(owner_api)
    >>> asyncio.run(main())
    Owner(service=<Service.GITHUB: 'github'>, username='string', name='string')
    """
    return Owner(schema.service, schema.username, schema.name, token, session)
