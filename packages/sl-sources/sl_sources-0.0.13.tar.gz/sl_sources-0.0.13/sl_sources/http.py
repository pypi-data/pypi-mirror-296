import asyncio
import os
import re
import time
from typing import Optional, Any, Dict
from urllib.parse import urljoin, urlparse

import aiohttp


class ThrottledClientSession(aiohttp.ClientSession):
    """
    A rate-throttled client session class inherited from aiohttp.ClientSession.

    This class implements a leaky bucket algorithm to limit the rate of requests.

    Attributes
    ----------
    rate_limit : float, optional
        The maximum number of requests per second.
    MIN_SLEEP : float
        The minimum sleep time between requests.

    Methods
    -------
    close()
        Close the rate-limiter's "bucket filler" task.
    _filler(rate_limit: float = 1)
        Filler task to implement the leaky bucket algorithm.
    _allow()
        Check if a request is allowed based on the rate limit.
    _request(*args, **kwargs)
        Throttled version of the parent class's _request method.

    Usage
    -----
    Replace `session = aiohttp.ClientSession()`
    with `session = ThrottledClientSession(rate_limit=15)`

    Notes
    -----
    See https://stackoverflow.com/a/60357775/107049 for more details.
    """

    MIN_SLEEP: float = 0.1

    def __init__(
        self, rate_limit: Optional[float] = None, *args: Any, **kwargs: Any
    ) -> None:
        """
        Initialize the ThrottledClientSession.

        Parameters
        ----------
        rate_limit : float, optional
            The maximum number of requests per second.
        *args : Any
            Variable length argument list to be passed to the parent class.
        **kwargs : Any
            Arbitrary keyword arguments to be passed to the parent class.

        Raises
        ------
        ValueError
            If the rate_limit is not positive.
        """
        super().__init__(*args, **kwargs)
        self.rate_limit: Optional[float] = rate_limit
        self._fillerTask: Optional[asyncio.Task] = None
        self._queue: Optional[asyncio.Queue] = None
        self._start_time: float = time.time()
        if rate_limit is not None:
            if rate_limit <= 0:
                raise ValueError("rate_limit must be positive")
            self._queue = asyncio.Queue(min(2, int(rate_limit) + 1))
            self._fillerTask = asyncio.create_task(self._filler(rate_limit))

    def _get_sleep(self) -> Optional[float]:
        """
        Calculate the sleep time between requests based on the rate limit.

        Returns
        -------
        Optional[float]
            The sleep time in seconds, or None if no rate limit is set.
        """
        if self.rate_limit is not None:
            return max(1 / self.rate_limit, self.MIN_SLEEP)
        return None

    async def close(self) -> None:
        """
        Close the rate-limiter's "bucket filler" task.

        This method cancels the filler task and waits for it to complete
        before closing the session.
        """
        if self._fillerTask is not None:
            self._fillerTask.cancel()
        try:
            await asyncio.wait_for(self._fillerTask, timeout=0.5)
        except (asyncio.TimeoutError, asyncio.CancelledError) as err:
            print(str(err))
        await super().close()

    async def _filler(self, rate_limit: float = 1) -> None:
        """
        Filler task to implement the leaky bucket algorithm.

        This method continuously adds tokens to the bucket (queue) based on
        the specified rate limit.

        Parameters
        ----------
        rate_limit : float, optional
            The rate at which to add tokens to the bucket (default is 1).
        """
        try:
            if self._queue is None:
                return
            self.rate_limit = rate_limit
            sleep = self._get_sleep()
            updated_at = time.monotonic()
            fraction = 0
            extra_increment = 0
            for i in range(0, self._queue.maxsize):
                self._queue.put_nowait(i)
            while True:
                if not self._queue.full():
                    now = time.monotonic()
                    increment = rate_limit * (now - updated_at)
                    fraction += increment % 1
                    extra_increment = fraction // 1
                    items_2_add = int(
                        min(
                            self._queue.maxsize - self._queue.qsize(),
                            int(increment) + extra_increment,
                        )
                    )
                    fraction = fraction % 1
                    for i in range(0, items_2_add):
                        self._queue.put_nowait(i)
                    updated_at = now
                await asyncio.sleep(sleep)
        except asyncio.CancelledError:
            pass
        except Exception as err:
            print(str(err))

    async def _allow(self) -> None:
        """
        Check if a request is allowed based on the rate limit.

        This method waits for a token from the queue before allowing a request.
        """
        if self._queue is not None:
            await self._queue.get()
            self._queue.task_done()
        return None

    async def _request(self, *args: Any, **kwargs: Any) -> aiohttp.ClientResponse:
        """
        Throttled version of the parent class's _request method.

        This method ensures that requests are made according to the rate limit.

        Parameters
        ----------
        *args : Any
            Variable length argument list to be passed to the parent's _request method.
        **kwargs : Any
            Arbitrary keyword arguments to be passed to the parent's _request method.

        Returns
        -------
        aiohttp.ClientResponse
            The response from the server.
        """
        await self._allow()
        return await super()._request(*args, **kwargs)


async def cloud_function_request(
    request_type: str,
    params: Dict[str, Any],
    url: Optional[str] = os.getenv("CLOUD_FUNCTION_URL"),
) -> Optional[Dict[str, Any]]:
    """
    Make a request to a cloud function.

    This function sends a POST request to the specified cloud function URL
    with the given request type and parameters.

    Parameters
    ----------
    request_type : str
        The type of request to be made to the cloud function.
    params : Dict[str, Any]
        The parameters to be sent with the request.
    url : Optional[str], optional
        The URL of the cloud function (default is None, which will use the
        CLOUD_FUNCTION_URL environment variable).

    Returns
    -------
    Optional[Dict[str, Any]]
        The JSON response from the cloud function if successful, None otherwise.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            json={"request_type": request_type, **params},
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Error calling cloud function: {response.status}")
                print(await response.text())
                return None


def validate_url(url: str) -> str:
    """
    Validate and normalize a URL.

    This function checks if the given URL is valid and normalizes it by
    adding the appropriate scheme if missing.

    Parameters
    ----------
    url : str
        The URL to validate and normalize.

    Returns
    -------
    str
        The validated and normalized URL.

    Raises
    ------
    ValueError
        If the URL is invalid and cannot be normalized.
    """
    if url is None:
        raise ValueError("URL cannot be None")

    # Check if the URL already starts with a valid scheme
    if url.startswith(("http://", "https://")):
        return url

    # If it starts with ftp, throw error
    if url.startswith("ftp"):
        raise ValueError(f"FTP URLs are not supported: {url}")

    # If it starts with www, add https://
    if url.startswith("www."):
        url = f"https://{url}"

    # If it starts with anything 2-8 characters and then a ://, throw error
    if re.match(r"^[a-z]{2,8}://", url):
        raise ValueError(f"Invalid URL: {url}")

    # Check for a valid domain structure
    domain_pattern = r"^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}(/.*)?$"
    if re.match(domain_pattern, url, re.IGNORECASE):
        return f"https://{url}"

    # Try to parse the URL
    parsed = urlparse(url)
    if parsed.netloc:
        return f"https://{parsed.netloc}{parsed.path}"

    # If all else fails, raise an exception
    raise ValueError(f"Invalid URL: {url}")


def resolve_url(url: str, base_url: Optional[str] = None) -> str:
    """
    Resolve a URL to its absolute form, handling various edge cases.

    This function takes a URL (which may be relative) and resolves it to
    its absolute form, using a base URL if provided.

    Parameters
    ----------
    url : str
        The URL to resolve.
    base_url : Optional[str], optional
        The base URL to use for relative URLs (default is None).

    Returns
    -------
    str
        The resolved absolute URL.

    Raises
    ------
    ValueError
        If the URL cannot be resolved.
    """
    # Handle protocol-relative URLs
    if url.startswith("//"):
        return f"https:{url}"

    # Handle URLs starting with 'www.'
    if url.startswith("www."):
        url = f"https://{url}"

    # Handle relative URLs
    if (
        url.startswith("/")
        or url.startswith("./")
        or url.startswith("../")
        or not urlparse(url).netloc
    ):
        if not base_url:
            raise ValueError(f"Base URL is required to resolve relative URL: {url}")
        return urljoin(base_url, url)

    # Handle URLs without a scheme
    if not urlparse(url).scheme:
        url = f"https://{url}"

    # Validate the URL
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL: {url}")

        # Normalize the URL
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path or '/'}{f'?{parsed.query}' if parsed.query else ''}{f'#{parsed.fragment}' if parsed.fragment else ''}"
    except Exception as e:
        raise ValueError(f"Failed to parse URL {url}: {str(e)}")
