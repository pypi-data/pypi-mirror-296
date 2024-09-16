from typing import TypeVar, Self

import orjson
from aiohttp import ClientSession, hdrs

from .erros import TelegramError
from .methods import TelegramMethod, GetUpdates
from .types import TelegramResponse

__all__ = ("Bot",)

T = TypeVar("T")


class Bot:
    def __init__(self, token: str, base_url: str = "https://api.telegram.org") -> None:
        self._token = token
        self._base_url = base_url
        self._id = int(token.split(":")[0])
        self._session: ClientSession | None = None

    def _construct_url(self, method_url: str) -> str:
        return f"/bot{self._token}/{method_url}"

    async def _request(self, telegram_method: TelegramMethod[T], /) -> TelegramResponse[T]:
        request = self._session.post(
            url=self._construct_url(telegram_method.__class__.__name__),
            data=orjson.dumps(
                telegram_method.model_dump(
                    mode="json",
                    exclude_unset=True,
                )
            ),
            headers={hdrs.CONTENT_TYPE: telegram_method.__content_type__},
        )

        async with request as response:
            raw_data = await response.json(loads=orjson.loads)
            return TelegramResponse[telegram_method.__type__](**raw_data)

    @property
    def id(self) -> int:
        return self._id

    async def startup(self) -> None:
        self._session = ClientSession(self._base_url)

    async def shutdown(self) -> None:
        await self._session.close()

    async def exec(self, method: TelegramMethod[T] | type[TelegramMethod[T]], /) -> T:
        response = await self._request(method())

        if not response.ok:
            raise TelegramError(response.error_code, response.description)

        return response.result
