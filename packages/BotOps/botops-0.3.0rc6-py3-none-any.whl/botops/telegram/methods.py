from abc import ABC
from typing import Self, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from .enums import ParseModeEnum, UpdateTypeEnum
from .types import Message, Update, User

__all__ = ("TelegramMethod", "Close", "GetMe", "LogOut", "GetUpdates", "SetWebhook", "SendMessage")

T = TypeVar("T")

R = TypeVar("R")


class TelegramMethod[T](BaseModel, ABC):
    __content_type__: str = "application/json"
    __type__: type[T]

    model_config = ConfigDict(use_enum_values=True, revalidate_instances="never")

    def __call__(self) -> Self:
        return self


class Close(TelegramMethod[bool]):
    __type__ = bool


class GetMe(TelegramMethod[User]):
    __type__ = User


class LogOut(TelegramMethod[bool]):
    __type__ = bool


class GetUpdates(TelegramMethod[list[Update]]):
    __type__ = list[Update]

    offset: int = Field(...)
    limit: int = Field(...)
    timeout: int = Field(...)
    allowed_updates: list[UpdateTypeEnum] | None = Field(None)


class SetWebhook(TelegramMethod[bool]):
    __type__ = bool

    url: str = Field()
    certificate: str | None = Field(None)
    ip_address: str | None = Field(None)
    max_connections: int | None = Field(None)
    allowed_updates: list[UpdateTypeEnum] | None = Field(None)
    drop_pending_updates: bool | None = Field(None)
    secret_token: str | None = Field(None)


class SendMessage(TelegramMethod[Message]):
    __type__ = Message

    chat_id: int | str = Field()
    text: str = Field()
    message_thread_id: int | None = Field(None)
    parse_mode: ParseModeEnum | None = Field(None)
    disable_notification: bool | None = Field(None)
    business_connection_id: str | None = Field(None)
