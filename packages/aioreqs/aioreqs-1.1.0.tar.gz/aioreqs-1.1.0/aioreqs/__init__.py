import typing
import requests
import asyncificate
import concurrent.futures

# Local imports
from . import sync


# ==------------------------------------------------------------== #
# Classes                                                          #
# ==------------------------------------------------------------== #
class AsyncSession():
    """Creates requests session for making async HTTP/HTTPS requests."""

    def __init__(self, thread_pool: concurrent.futures.ThreadPoolExecutor = None) -> None:
        self.thread_pool = thread_pool
        self.session = requests.Session()

    async def get(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a GET request."""

        @asyncificate.awaitable(thread_pool=self.thread_pool)
        def wrapper() -> requests.Response:
            return self.session.get(url, *args, **kwargs)

        return await wrapper()

    async def post(self, url: str, *args, **kwargs) -> requests.Response:
        """Sends a POST request."""

        @asyncificate.awaitable(thread_pool=self.thread_pool)
        def wrapper() -> requests.Response:
            return self.session.post(url, *args, **kwargs)

        return await wrapper()

    async def patch(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a PATCH request."""

        @asyncificate.awaitable(thread_pool=self.thread_pool)
        def wrapper() -> requests.Response:
            return self.session.patch(url, *args, **kwargs)

        return await wrapper()

    async def put(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a PUT request."""

        @asyncificate.awaitable(thread_pool=self.thread_pool)
        def wrapper() -> requests.Response:
            return self.session.put(url, *args, **kwargs)

        return await wrapper()

    async def delete(self, url: str, *args: typing.Any, **kwargs: typing.Any) -> requests.Response:
        """Sends a DELETE request."""

        @asyncificate.awaitable(thread_pool=self.thread_pool)
        def wrapper() -> requests.Response:
            return self.session.delete(url, *args, **kwargs)

        return await wrapper()


# ==------------------------------------------------------------== #
# Async functions                                                  #
# ==------------------------------------------------------------== #
async def get(url: str, *args: typing.Any, thread_pool: concurrent.futures.ThreadPoolExecutor = None, **kwargs: typing.Any) -> requests.Response:
    """Sends a GET request."""

    @asyncificate.awaitable(thread_pool=thread_pool)
    def wrapper() -> requests.Response:
        return requests.get(url, *args, **kwargs)

    return await wrapper()


async def post(url: str, *args: typing.Any, thread_pool: concurrent.futures.ThreadPoolExecutor = None, **kwargs: typing.Any) -> requests.Response:
    """Sends a POST request."""

    @asyncificate.awaitable(thread_pool=thread_pool)
    def wrapper() -> requests.Response:
        return requests.post(url, *args, **kwargs)

    return await wrapper()


async def patch(url: str, *args: typing.Any, thread_pool: concurrent.futures.ThreadPoolExecutor = None, **kwargs: typing.Any) -> requests.Response:
    """Sends a PATCH request."""

    @asyncificate.awaitable(thread_pool=thread_pool)
    def wrapper() -> requests.Response:
        return requests.patch(url, *args, **kwargs)

    return await wrapper()


async def put(url: str, *args: typing.Any, thread_pool: concurrent.futures.ThreadPoolExecutor = None, **kwargs: typing.Any) -> requests.Response:
    """Sends a PUT request."""

    @asyncificate.awaitable(thread_pool=thread_pool)
    def wrapper() -> requests.Response:
        return requests.put(url, *args, **kwargs)

    return await wrapper()


async def delete(url: str, *args: typing.Any, thread_pool: concurrent.futures.ThreadPoolExecutor = None, **kwargs: typing.Any) -> requests.Response:
    """Sends a DELETE request."""

    @asyncificate.awaitable(thread_pool=thread_pool)
    def wrapper() -> requests.Response:
        return requests.delete(url, *args, **kwargs)

    return await wrapper()
