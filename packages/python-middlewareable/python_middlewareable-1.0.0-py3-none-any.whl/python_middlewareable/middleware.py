from abc import ABC, abstractmethod
from typing import Awaitable, Callable, Generic, TypeVar
from .request import Request

TRequest = TypeVar("TRequest", bound=Request)

MiddlewareNextCall = Callable[[TRequest], Awaitable[None]]


class Middleware(Generic[TRequest], ABC):
    @abstractmethod
    async def handle(
        self,
        request: TRequest,
        next_call: MiddlewareNextCall[TRequest],
    ) -> None:
        pass
