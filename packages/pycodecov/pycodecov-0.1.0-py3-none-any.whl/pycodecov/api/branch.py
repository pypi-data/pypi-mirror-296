from .. import schemas
from ..enums import Service
from ..exceptions import CodecovError
from ..parsers import (
    parse_branch_data,
    parse_branch_detail_data,
    parse_paginated_list_data,
)
from .api import API
from .paginated_list import PaginatedList

__all__ = ["Branch"]


class Branch(API):
    """
    Branch API Wrapper from Codecov API.
    """

    async def get_branch_list(
        self,
        service: Service,
        owner_username: str,
        repo_name: str,
        author: bool | None = None,
        ordering: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
    ) -> PaginatedList[schemas.Branch]:
        """
        Get a paginated list of branches for the specified repository.

        Args:
            service: git hosting service provider.
            owner_username: username from service provider.
            repo_name: repository name.
            author: .
            ordering: which field to use when ordering the results.
            page: a page number within the paginated result set.
            page_size: number of results to return per page.

        Returns:
            Paginated list of `Branch`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         branches = await codecov.branches.get_branch_list(
            ...             Service.GITHUB, "jazzband", "django-silk"
            ...         )
            ...         print(branches)
            >>> asyncio.run(main())
            PaginatedList(...)
        """
        params = {}
        optional_params = {
            "author": str(author).lower() if author is not None else author,
            "ordering": ordering,
            "page": str(page) if page is not None else page,
            "page_size": str(page_size) if page_size is not None else page_size,
        }

        params.update({k: v for k, v in optional_params.items() if v is not None})

        async with self._session.get(
            f"{self.api_url}/{service}/{owner_username}/repos/{repo_name}/branches/",
            params=params,
        ) as response:
            data = await response.json()

            if response.ok:
                paginated_list = parse_paginated_list_data(data, parse_branch_data)

                return PaginatedList(
                    paginated_list.count,
                    paginated_list.results,
                    paginated_list.total_pages,
                    parse_branch_data,
                    paginated_list.next,
                    paginated_list.previous,
                    self._token,
                    self._session,
                )

            raise CodecovError(data)

    async def get_branch_detail(
        self, service: Service, owner_username: str, repo_name: str, name: str
    ) -> schemas.BranchDetail:
        """
        Get a single branch by name. Includes head commit information embedded in the
        response.

        Args:
            service: git hosting service provider.
            owner_username: username from service provider.
            repo_name: repository name.
            name: branch name.

        Returns:
            A `BranchDetail`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         branch = await codecov.branches.get_branch_detail(
            ...             Service.GITHUB,
            ...             "jazzband",
            ...             "django-silk",
            ...             "add_multipart_support",
            ...         )
            ...         print(branch)
            >>> asyncio.run(main())
            BranchDetail(...)
        """
        async with self._session.get(
            f"{self.api_url}/{service}/{owner_username}/repos/{repo_name}/branches/{name}/"
        ) as response:
            data = await response.json()

            if response.ok:
                return parse_branch_detail_data(data)

            raise CodecovError(data)
