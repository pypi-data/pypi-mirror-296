from typing import Any, Protocol

from aiohttp import ClientSession

__all__ = [
    "ApiParser",
    "CodecovApiToken",
    "CodecovUrl",
]


CodecovApiToken = str
CodecovUrl = str


class ApiParser(Protocol):
    def __call__(
        self,
        schema: Any,
        token: CodecovApiToken | None,
        session: ClientSession | None,
        **kwargs: Any,
    ) -> Any: ...
