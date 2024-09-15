from .. import schemas
from ..enums import Service
from ..exceptions import CodecovError
from ..parsers import parse_paginated_list_data, parse_repo_config_data, parse_repo_data
from .api import API
from .paginated_list import PaginatedList

__all__ = ["Repo"]


class Repo(API):
    """
    Repo API Wrapper from Codecov API.
    """

    async def get_repo_list(
        self,
        service: Service,
        owner_username: str,
        active: bool | None = None,
        names: str | None = None,
        page: int | None = None,
        page_size: int | None = None,
        search: str | None = None,
    ) -> PaginatedList[schemas.Repo]:
        """
        Get a paginated list of repositories for the specified provider service and
        owner username.

        Args:
            service: git hosting service provider.
            owner_username: username from service provider.
            active: whether the repository has received an upload.
            names: list of repository names.
            page: a page number within the paginated result set.
            page_size: number of results to return per page.
            search: a search term.

        Returns:
            Paginated list of `Repo`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         repos = await codecov.repos.get_repo_list(
            ...             Service.GITHUB, "jazzband"
            ...         )
            ...         print(repos)
            >>> asyncio.run(main())
            PaginatedList(...)
        """
        params = {}
        optional_params = {
            "active": str(active).lower() if active is not None else active,
            "names": names,
            "page": str(page) if page is not None else page,
            "page_size": str(page_size) if page_size is not None else page_size,
            "search": search,
        }

        params.update({k: v for k, v in optional_params.items() if v is not None})

        async with self._session.get(
            f"{self.api_url}/{service}/{owner_username}/repos/", params=params
        ) as response:
            data = await response.json()

            if response.ok:
                paginated_list = parse_paginated_list_data(data, parse_repo_data)

                return PaginatedList(
                    paginated_list.count,
                    paginated_list.results,
                    paginated_list.total_pages,
                    parse_repo_data,
                    paginated_list.next,
                    paginated_list.previous,
                    self._token,
                    self._session,
                )

            raise CodecovError(data)

    async def get_repo_detail(
        self, service: Service, owner_username: str, repo_name: str
    ) -> schemas.Repo:
        """
        Get a single repository by name.

        Args:
            service: git hosting service provider.
            owner_username: username from service provider.
            repo_name: repository name.

        Returns:
            A `Repo`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         repo = await codecov.repos.get_repo_detail(
            ...             Service.GITHUB, "jazzband", "django-silk"
            ...         )
            ...         print(repo)
            >>> asyncio.run(main())
            Repo(...)
        """
        async with self._session.get(
            f"{self.api_url}/{service}/{owner_username}/repos/{repo_name}/"
        ) as response:
            data = await response.json()

            if response.ok:
                return parse_repo_data(data)

            raise CodecovError(data)

    async def get_repo_config(
        self,
        service: Service,
        owner_username: str,
        repo_name: str,
    ) -> schemas.RepoConfig:
        """
        Returns a repository config by name.

        Args:
            service: git hosting service provider.
            owner_username: username from service provider.
            repo_name: repository name.

        Returns:
            A `RepoConfig`.

        Examples:
            >>> import asyncio
            >>> import os
            >>> from pycodecov import Codecov
            >>> from pycodecov.enums import Service
            >>> async def main():
            ...     async with Codecov(os.environ["CODECOV_API_TOKEN"]) as codecov:
            ...         repo_config = await codecov.repos.get_repo_config(
            ...             Service.GITHUB, "jazzband", "django-silk"
            ...         )
            ...         print(repo_config)
            >>> asyncio.run(main())
            RepoConfig(...)
        """
        async with self._session.get(
            f"{self.api_url}/{service}/{owner_username}/repos/{repo_name}/config/"
        ) as response:
            data = await response.json()

            if response.ok:
                return parse_repo_config_data(data)

            raise CodecovError(data)
