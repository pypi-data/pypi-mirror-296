from aiohttp import ClientSession

from ..enums import Service
from ..exceptions import CodecovError
from ..parsers import parse_owner_data, parse_paginated_list_data
from ..types import CodecovApiToken
from .api import API
from .owner import Owner, parse_owner_api
from .paginated_list import PaginatedList, PaginatedListApi, parse_paginated_list_api

__all__ = ["Codecov"]


class Codecov(API):
    """
    Base Codecov API wrapper.
    """

    def __init__(
        self,
        token: CodecovApiToken | None = None,
        session: ClientSession | None = None,
    ) -> None:
        API.__init__(self, token, session)

    async def get_service_owners(
        self, service: Service, page: int | None = None, page_size: int | None = None
    ) -> PaginatedListApi[Owner]:
        """
        Get a paginated list of owners to which the currently authenticated user has
        access.

        Args:
            service: git hosting service provider.
            page: a page number within the paginated result set.
            page_size: number of results to return per page.

        Returns:
            Paginated list of `Owner`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         service_owners = await codecov.get_service_owners(Service.GITHUB)
            ...         print(service_owners)
            >>> asyncio.run(main())
            PaginatedListApi(...)
        """  # noqa: E501
        params = {}
        optional_params = {
            "page": str(page) if page is not None else page,
            "page_size": str(page_size) if page_size is not None else page_size,
        }

        params.update({k: v for k, v in optional_params.items() if v is not None})

        async with self._session.get(
            f"{self.api_url}/{service}", params=params
        ) as response:
            data = await response.json()

            if response.ok:
                paginated_list_data = parse_paginated_list_data(data, parse_owner_data)
                paginated_list = PaginatedList(
                    paginated_list_data.count,
                    paginated_list_data.results,
                    paginated_list_data.total_pages,
                    parse_owner_data,
                    paginated_list_data.next,
                    paginated_list_data.previous,
                    self._token,
                    self._session,
                )

                return parse_paginated_list_api(paginated_list, parse_owner_api)

            raise CodecovError(data)
