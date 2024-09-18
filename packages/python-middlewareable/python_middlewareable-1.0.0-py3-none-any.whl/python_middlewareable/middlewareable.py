from typing import Generic
from .middleware import Middleware, TRequest


class Middlewareable(Generic[TRequest]):
    middlewares: list[type[Middleware[TRequest]]] = []

    middleware_instances: list[Middleware[TRequest]] = []

    def __init__(self) -> None:
        self._instantiate_middlewares()

    def _instantiate_middlewares(self) -> None:
        self.middleware_instances = [
            middleware() for middleware in self.middlewares
        ]

    async def process_middlewares(
        self,
        request: TRequest,
        index: int = 0,
    ) -> TRequest:
        is_index_out_of_range = index >= len(self.middleware_instances)

        if is_index_out_of_range:
            return request

        middleware = self.middleware_instances[index]

        async def next_call(request: TRequest) -> None:
            await self.process_middlewares(request, index + 1)

        await middleware.handle(request, next_call)

        return request
