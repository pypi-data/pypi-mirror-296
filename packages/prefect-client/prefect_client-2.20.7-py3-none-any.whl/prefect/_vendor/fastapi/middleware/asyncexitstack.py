from typing import Optional

from prefect._vendor.fastapi.concurrency import AsyncExitStack
from prefect._vendor.starlette.types import ASGIApp, Receive, Scope, Send


class AsyncExitStackMiddleware:
    def __init__(self, app: ASGIApp, context_name: str = "fastapi_astack") -> None:
        self.app = app
        self.context_name = context_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        dependency_exception: Optional[Exception] = None
        async with AsyncExitStack() as stack:
            scope[self.context_name] = stack
            try:
                await self.app(scope, receive, send)
            except Exception as e:
                dependency_exception = e
                raise e
        if dependency_exception:
            # This exception was possibly handled by the dependency but it should
            # still bubble up so that the ServerErrorMiddleware can return a 500
            # or the ExceptionMiddleware can catch and handle any other exceptions
            raise dependency_exception
