from traceback import TracebackException
from types import TracebackType
from typing import Self

from aiohttp import ClientSession

from ..types import CodecovApiToken

__all__ = ["API"]


class API:
    """
    Base API class.
    """

    base_url = "https://api.codecov.io"
    api_url = "/api/v2"

    def __init__(
        self,
        token: CodecovApiToken | None = None,
        session: ClientSession | None = None,
    ) -> None:
        headers = {
            "Accept": "application/json",
        }

        if token is not None:
            headers["Authorization"] = f"Bearer {token}"

        self._token = token
        self._session = (
            session
            if session is not None
            else ClientSession(self.base_url, headers=headers)
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Exception,
        exc_val: TracebackException,
        traceback: TracebackType,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.close()
