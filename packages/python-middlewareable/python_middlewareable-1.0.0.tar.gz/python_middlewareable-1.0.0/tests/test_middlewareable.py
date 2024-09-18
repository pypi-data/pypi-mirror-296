import pytest
from _pytest.capture import CaptureFixture
from python_middlewareable import MiddlewareableBase
from tests.stubs.fake_basic_middlewares import (
    Request,
    OneMiddleware,
    TwoMiddleware,
)
from tests.stubs.fake_http_middlewares import (
    AddHeaderMiddleware,
    HttpMiddlewareable,
    HttpRequest,
    ModifyMethodMiddleware,
)


@pytest.mark.asyncio
async def test_basic_usage_instructions():
    class App(MiddlewareableBase[Request]):
        middlewares = [OneMiddleware, TwoMiddleware]

    app = App()
    result = await app.process_middlewares(Request(name="John"))
    assert (
        result.response == "Hello, John from OneMiddleware from TwoMiddleware"
    )


@pytest.mark.asyncio
async def test_middleware_print_output(capsys: CaptureFixture[str]) -> None:
    class App(MiddlewareableBase[Request]):
        middlewares = [OneMiddleware, TwoMiddleware]

    # Create the app instance with the middleware
    app = App()

    # Process the request
    request = Request(name="John")
    await app.process_middlewares(request)

    # Capture the output
    captured = capsys.readouterr()

    # Expected output lines in order
    expected_output = [
        "OneMiddleware before",
        "TwoMiddleware before",
        "TwoMiddleware after",
        "OneMiddleware after",
    ]

    # Split the captured output into lines and compare with the expected
    # sequence
    output_lines = captured.out.strip().splitlines()

    assert output_lines == expected_output


@pytest.mark.asyncio
async def test_basic_middleware_chain():
    class HttpMiddlewareableWithMiddlewares(HttpMiddlewareable):
        middlewares = [AddHeaderMiddleware, ModifyMethodMiddleware]

    app = HttpMiddlewareableWithMiddlewares()

    initial_request = HttpRequest(method="GET", headers={})
    processed_request = await app.process_middlewares(initial_request)

    assert processed_request.method == "POST"
    assert "X-Test" in processed_request.headers
    assert processed_request.headers["X-Test"] == "True"


@pytest.mark.asyncio
async def test_append_middlewares_at_runtime():
    app = HttpMiddlewareable()
    app.middleware_instances.append(AddHeaderMiddleware())
    app.middleware_instances.append(ModifyMethodMiddleware())

    initial_request = HttpRequest(method="GET", headers={})
    processed_request = await app.process_middlewares(initial_request)

    assert processed_request.method == "POST"
    assert "X-Test" in processed_request.headers
    assert processed_request.headers["X-Test"] == "True"
