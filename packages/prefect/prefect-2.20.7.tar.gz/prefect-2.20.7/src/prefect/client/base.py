import copy
import sys
import threading
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import (
    Any,
    AsyncGenerator,
    Awaitable,
    Callable,
    Dict,
    MutableMapping,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    runtime_checkable,
)

import anyio
import httpx
from asgi_lifespan import LifespanManager
from httpx import HTTPStatusError, Request, Response
from prefect._vendor.starlette import status
from prefect._vendor.starlette.testclient import TestClient
from typing_extensions import Self

import prefect
from prefect.client import constants
from prefect.client.schemas.objects import CsrfToken
from prefect.exceptions import PrefectHTTPStatusError
from prefect.logging import get_logger
from prefect.settings import (
    PREFECT_CLIENT_MAX_RETRIES,
    PREFECT_CLIENT_RETRY_EXTRA_CODES,
    PREFECT_CLIENT_RETRY_JITTER_FACTOR,
)
from prefect.utilities.math import bounded_poisson_interval, clamped_poisson_interval

# Datastores for lifespan management, keys should be a tuple of thread and app
# identities.
APP_LIFESPANS: Dict[Tuple[int, int], LifespanManager] = {}
APP_LIFESPANS_REF_COUNTS: Dict[Tuple[int, int], int] = {}
# Blocks concurrent access to the above dicts per thread. The index should be the thread
# identity.
APP_LIFESPANS_LOCKS: Dict[int, anyio.Lock] = defaultdict(anyio.Lock)


logger = get_logger("client")


# Define ASGI application types for type checking
Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]

Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]


@runtime_checkable
class ASGIApp(Protocol):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...


@asynccontextmanager
async def app_lifespan_context(app: ASGIApp) -> AsyncGenerator[None, None]:
    """
    A context manager that calls startup/shutdown hooks for the given application.

    Lifespan contexts are cached per application to avoid calling the lifespan hooks
    more than once if the context is entered in nested code. A no-op context will be
    returned if the context for the given application is already being managed.

    This manager is robust to concurrent access within the event loop. For example,
    if you have concurrent contexts for the same application, it is guaranteed that
    startup hooks will be called before their context starts and shutdown hooks will
    only be called after their context exits.

    A reference count is used to support nested use of clients without running
    lifespan hooks excessively. The first client context entered will create and enter
    a lifespan context. Each subsequent client will increment a reference count but will
    not create a new lifespan context. When each client context exits, the reference
    count is decremented. When the last client context exits, the lifespan will be
    closed.

    In simple nested cases, the first client context will be the one to exit the
    lifespan. However, if client contexts are entered concurrently they may not exit
    in a consistent order. If the first client context was responsible for closing
    the lifespan, it would have to wait until all other client contexts to exit to
    avoid firing shutdown hooks while the application is in use. Waiting for the other
    clients to exit can introduce deadlocks, so, instead, the first client will exit
    without closing the lifespan context and reference counts will be used to ensure
    the lifespan is closed once all of the clients are done.
    """
    # TODO: A deadlock has been observed during multithreaded use of clients while this
    #       lifespan context is being used. This has only been reproduced on Python 3.7
    #       and while we hope to discourage using multiple event loops in threads, this
    #       bug may emerge again.
    #       See https://github.com/PrefectHQ/orion/pull/1696
    thread_id = threading.get_ident()

    # The id of the application is used instead of the hash so each application instance
    # is managed independently even if they share the same settings. We include the
    # thread id since applications are managed separately per thread.
    key = (thread_id, id(app))

    # On exception, this will be populated with exception details
    exc_info = (None, None, None)

    # Get a lock unique to this thread since anyio locks are not threadsafe
    lock = APP_LIFESPANS_LOCKS[thread_id]

    async with lock:
        if key in APP_LIFESPANS:
            # The lifespan is already being managed, just increment the reference count
            APP_LIFESPANS_REF_COUNTS[key] += 1
        else:
            # Create a new lifespan manager
            APP_LIFESPANS[key] = context = LifespanManager(
                app, startup_timeout=30, shutdown_timeout=30
            )
            APP_LIFESPANS_REF_COUNTS[key] = 1

            # Ensure we enter the context before releasing the lock so startup hooks
            # are complete before another client can be used
            await context.__aenter__()

    try:
        yield
    except BaseException:
        exc_info = sys.exc_info()
        raise
    finally:
        # If we do not shield against anyio cancellation, the lock will return
        # immediately and the code in its context will not run, leaving the lifespan
        # open
        with anyio.CancelScope(shield=True):
            async with lock:
                # After the consumer exits the context, decrement the reference count
                APP_LIFESPANS_REF_COUNTS[key] -= 1

                # If this the last context to exit, close the lifespan
                if APP_LIFESPANS_REF_COUNTS[key] <= 0:
                    APP_LIFESPANS_REF_COUNTS.pop(key)
                    context = APP_LIFESPANS.pop(key)
                    await context.__aexit__(*exc_info)


class PrefectResponse(httpx.Response):
    """
    A Prefect wrapper for the `httpx.Response` class.

    Provides more informative error messages.
    """

    def raise_for_status(self) -> None:
        """
        Raise an exception if the response contains an HTTPStatusError.

        The `PrefectHTTPStatusError` contains useful additional information that
        is not contained in the `HTTPStatusError`.
        """
        try:
            return super().raise_for_status()
        except HTTPStatusError as exc:
            raise PrefectHTTPStatusError.from_httpx_error(exc) from exc.__cause__

    @classmethod
    def from_httpx_response(cls: Type[Self], response: httpx.Response) -> Self:
        """
        Create a `PrefectReponse` from an `httpx.Response`.

        By changing the `__class__` attribute of the Response, we change the method
        resolution order to look for methods defined in PrefectResponse, while leaving
        everything else about the original Response instance intact.
        """
        new_response = copy.copy(response)
        new_response.__class__ = cls
        return new_response


class PrefectHttpxAsyncClient(httpx.AsyncClient):
    """
    A Prefect wrapper for the async httpx client with support for retry-after headers
    for the provided status codes (typically 429, 502 and 503).

    Additionally, this client will always call `raise_for_status` on responses.

    For more details on rate limit headers, see:
    [Configuring Cloudflare Rate Limiting](https://support.cloudflare.com/hc/en-us/articles/115001635128-Configuring-Rate-Limiting-from-UI)
    """

    def __init__(
        self,
        *args,
        enable_csrf_support: bool = False,
        raise_on_all_errors: bool = True,
        **kwargs,
    ):
        self.enable_csrf_support: bool = enable_csrf_support
        self.csrf_token: Optional[str] = None
        self.csrf_token_expiration: Optional[datetime] = None
        self.csrf_client_id: uuid.UUID = uuid.uuid4()
        self.raise_on_all_errors: bool = raise_on_all_errors

        super().__init__(*args, **kwargs)

        user_agent = (
            f"prefect/{prefect.__version__} (API {constants.SERVER_API_VERSION})"
        )
        self.headers["User-Agent"] = user_agent

    async def _send_with_retry(
        self,
        request: Request,
        send: Callable[[Request], Awaitable[Response]],
        send_args: Tuple,
        send_kwargs: Dict,
        retry_codes: Set[int] = set(),
        retry_exceptions: Tuple[Exception, ...] = tuple(),
    ):
        """
        Send a request and retry it if it fails.

        Sends the provided request and retries it up to PREFECT_CLIENT_MAX_RETRIES times
        if the request either raises an exception listed in `retry_exceptions` or
        receives a response with a status code listed in `retry_codes`.

        Retries will be delayed based on either the retry header (preferred) or
        exponential backoff if a retry header is not provided.
        """
        try_count = 0
        response = None

        is_change_request = request.method.lower() in {"post", "put", "patch", "delete"}

        if self.enable_csrf_support and is_change_request:
            await self._add_csrf_headers(request=request)

        while try_count <= PREFECT_CLIENT_MAX_RETRIES.value():
            try_count += 1
            retry_seconds = None
            exc_info = None

            try:
                response = await send(request, *send_args, **send_kwargs)
            except retry_exceptions:  # type: ignore
                if try_count > PREFECT_CLIENT_MAX_RETRIES.value():
                    raise
                # Otherwise, we will ignore this error but capture the info for logging
                exc_info = sys.exc_info()
            else:
                # We got a response; check if it's a CSRF error, otherwise
                # return immediately if it is not retryable
                if (
                    response.status_code == status.HTTP_403_FORBIDDEN
                    and "Invalid CSRF token" in response.text
                ):
                    # We got a CSRF error, clear the token and try again
                    self.csrf_token = None
                    await self._add_csrf_headers(request)
                elif response.status_code not in retry_codes:
                    return response

                if "Retry-After" in response.headers:
                    retry_seconds = float(response.headers["Retry-After"])

            # Use an exponential back-off if not set in a header
            if retry_seconds is None:
                retry_seconds = 2**try_count

            # Add jitter
            jitter_factor = PREFECT_CLIENT_RETRY_JITTER_FACTOR.value()
            if retry_seconds > 0 and jitter_factor > 0:
                if response is not None and "Retry-After" in response.headers:
                    # Always wait for _at least_ retry seconds if requested by the API
                    retry_seconds = bounded_poisson_interval(
                        retry_seconds, retry_seconds * (1 + jitter_factor)
                    )
                else:
                    # Otherwise, use a symmetrical jitter
                    retry_seconds = clamped_poisson_interval(
                        retry_seconds, jitter_factor
                    )

            logger.debug(
                (
                    "Encountered retryable exception during request. "
                    if exc_info
                    else (
                        "Received response with retryable status code"
                        f" {response.status_code}. "
                    )
                )
                + f"Another attempt will be made in {retry_seconds}s. "
                "This is attempt"
                f" {try_count}/{PREFECT_CLIENT_MAX_RETRIES.value() + 1}.",
                exc_info=exc_info,
            )
            await anyio.sleep(retry_seconds)

        assert (
            response is not None
        ), "Retry handling ended without response or exception"

        # We ran out of retries, return the failed response
        return response

    async def send(self, request: Request, *args, **kwargs) -> Response:
        """
        Send a request with automatic retry behavior for the following status codes:

        - 403 Forbidden, if the request failed due to CSRF protection
        - 408 Request Timeout
        - 429 CloudFlare-style rate limiting
        - 502 Bad Gateway
        - 503 Service unavailable
        - Any additional status codes provided in `PREFECT_CLIENT_RETRY_EXTRA_CODES`
        """

        super_send = super().send
        response = await self._send_with_retry(
            request=request,
            send=super_send,
            send_args=args,
            send_kwargs=kwargs,
            retry_codes={
                status.HTTP_429_TOO_MANY_REQUESTS,
                status.HTTP_503_SERVICE_UNAVAILABLE,
                status.HTTP_502_BAD_GATEWAY,
                status.HTTP_408_REQUEST_TIMEOUT,
                *PREFECT_CLIENT_RETRY_EXTRA_CODES.value(),
            },
            retry_exceptions=(
                httpx.ReadTimeout,
                httpx.PoolTimeout,
                httpx.ConnectTimeout,
                # `ConnectionResetError` when reading socket raises as a `ReadError`
                httpx.ReadError,
                # Sockets can be closed during writes resulting in a `WriteError`
                httpx.WriteError,
                # Uvicorn bug, see https://github.com/PrefectHQ/prefect/issues/7512
                httpx.RemoteProtocolError,
                # HTTP2 bug, see https://github.com/PrefectHQ/prefect/issues/7442
                httpx.LocalProtocolError,
            ),
        )

        # Convert to a Prefect response to add nicer errors messages
        response = PrefectResponse.from_httpx_response(response)

        if self.raise_on_all_errors:
            response.raise_for_status()

        return response

    async def _add_csrf_headers(self, request: Request):
        now = datetime.now(timezone.utc)

        if not self.enable_csrf_support:
            return

        if not self.csrf_token or (
            self.csrf_token_expiration and now > self.csrf_token_expiration
        ):
            token_request = self.build_request(
                "GET", f"/csrf-token?client={self.csrf_client_id}"
            )

            try:
                token_response = await self.send(token_request)
            except PrefectHTTPStatusError as exc:
                old_server = exc.response.status_code == status.HTTP_404_NOT_FOUND
                unconfigured_server = (
                    exc.response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
                    and "CSRF protection is disabled." in exc.response.text
                )

                if old_server or unconfigured_server:
                    # The token endpoint is either unavailable, suggesting an
                    # older server, or CSRF protection is disabled. In either
                    # case we should disable CSRF support.
                    self.enable_csrf_support = False
                    return

                raise

            token: CsrfToken = CsrfToken.parse_obj(token_response.json())
            self.csrf_token = token.token
            self.csrf_token_expiration = token.expiration

        request.headers["Prefect-Csrf-Token"] = self.csrf_token
        request.headers["Prefect-Csrf-Client"] = str(self.csrf_client_id)


class PrefectHttpxSyncClient(httpx.Client):
    """
    A Prefect wrapper for the async httpx client with support for retry-after headers
    for the provided status codes (typically 429, 502 and 503).

    Additionally, this client will always call `raise_for_status` on responses.

    For more details on rate limit headers, see:
    [Configuring Cloudflare Rate Limiting](https://support.cloudflare.com/hc/en-us/articles/115001635128-Configuring-Rate-Limiting-from-UI)
    """

    def __init__(
        self,
        *args,
        enable_csrf_support: bool = False,
        raise_on_all_errors: bool = True,
        **kwargs,
    ):
        self.enable_csrf_support: bool = enable_csrf_support
        self.csrf_token: Optional[str] = None
        self.csrf_token_expiration: Optional[datetime] = None
        self.csrf_client_id: uuid.UUID = uuid.uuid4()
        self.raise_on_all_errors: bool = raise_on_all_errors

        super().__init__(*args, **kwargs)

        user_agent = (
            f"prefect/{prefect.__version__} (API {constants.SERVER_API_VERSION})"
        )
        self.headers["User-Agent"] = user_agent

    def _send_with_retry(
        self,
        request: Request,
        send: Callable[[Request], Response],
        send_args: Tuple,
        send_kwargs: Dict,
        retry_codes: Set[int] = set(),
        retry_exceptions: Tuple[Exception, ...] = tuple(),
    ):
        """
        Send a request and retry it if it fails.

        Sends the provided request and retries it up to PREFECT_CLIENT_MAX_RETRIES times
        if the request either raises an exception listed in `retry_exceptions` or
        receives a response with a status code listed in `retry_codes`.

        Retries will be delayed based on either the retry header (preferred) or
        exponential backoff if a retry header is not provided.
        """
        try_count = 0
        response = None

        is_change_request = request.method.lower() in {"post", "put", "patch", "delete"}

        if self.enable_csrf_support and is_change_request:
            self._add_csrf_headers(request=request)

        while try_count <= PREFECT_CLIENT_MAX_RETRIES.value():
            try_count += 1
            retry_seconds = None
            exc_info = None

            try:
                response = send(request, *send_args, **send_kwargs)
            except retry_exceptions:  # type: ignore
                if try_count > PREFECT_CLIENT_MAX_RETRIES.value():
                    raise
                # Otherwise, we will ignore this error but capture the info for logging
                exc_info = sys.exc_info()
            else:
                # We got a response; check if it's a CSRF error, otherwise
                # return immediately if it is not retryable
                if (
                    response.status_code == status.HTTP_403_FORBIDDEN
                    and "Invalid CSRF token" in response.text
                ):
                    # We got a CSRF error, clear the token and try again
                    self.csrf_token = None
                    self._add_csrf_headers(request)
                elif response.status_code not in retry_codes:
                    return response

                if "Retry-After" in response.headers:
                    retry_seconds = float(response.headers["Retry-After"])

            # Use an exponential back-off if not set in a header
            if retry_seconds is None:
                retry_seconds = 2**try_count

            # Add jitter
            jitter_factor = PREFECT_CLIENT_RETRY_JITTER_FACTOR.value()
            if retry_seconds > 0 and jitter_factor > 0:
                if response is not None and "Retry-After" in response.headers:
                    # Always wait for _at least_ retry seconds if requested by the API
                    retry_seconds = bounded_poisson_interval(
                        retry_seconds, retry_seconds * (1 + jitter_factor)
                    )
                else:
                    # Otherwise, use a symmetrical jitter
                    retry_seconds = clamped_poisson_interval(
                        retry_seconds, jitter_factor
                    )

            logger.debug(
                (
                    "Encountered retryable exception during request. "
                    if exc_info
                    else (
                        "Received response with retryable status code"
                        f" {response.status_code}. "
                    )
                )
                + f"Another attempt will be made in {retry_seconds}s. "
                "This is attempt"
                f" {try_count}/{PREFECT_CLIENT_MAX_RETRIES.value() + 1}.",
                exc_info=exc_info,
            )
            time.sleep(retry_seconds)

        assert (
            response is not None
        ), "Retry handling ended without response or exception"

        # We ran out of retries, return the failed response
        return response

    def send(self, request: Request, *args, **kwargs) -> Response:
        """
        Send a request with automatic retry behavior for the following status codes:

        - 403 Forbidden, if the request failed due to CSRF protection
        - 408 Request Timeout
        - 429 CloudFlare-style rate limiting
        - 502 Bad Gateway
        - 503 Service unavailable
        - Any additional status codes provided in `PREFECT_CLIENT_RETRY_EXTRA_CODES`
        """

        super_send = super().send
        response = self._send_with_retry(
            request=request,
            send=super_send,
            send_args=args,
            send_kwargs=kwargs,
            retry_codes={
                status.HTTP_429_TOO_MANY_REQUESTS,
                status.HTTP_503_SERVICE_UNAVAILABLE,
                status.HTTP_502_BAD_GATEWAY,
                status.HTTP_408_REQUEST_TIMEOUT,
                *PREFECT_CLIENT_RETRY_EXTRA_CODES.value(),
            },
            retry_exceptions=(
                httpx.ReadTimeout,
                httpx.PoolTimeout,
                httpx.ConnectTimeout,
                # `ConnectionResetError` when reading socket raises as a `ReadError`
                httpx.ReadError,
                # Sockets can be closed during writes resulting in a `WriteError`
                httpx.WriteError,
                # Uvicorn bug, see https://github.com/PrefectHQ/prefect/issues/7512
                httpx.RemoteProtocolError,
                # HTTP2 bug, see https://github.com/PrefectHQ/prefect/issues/7442
                httpx.LocalProtocolError,
            ),
        )

        # Convert to a Prefect response to add nicer errors messages
        response = PrefectResponse.from_httpx_response(response)

        if self.raise_on_all_errors:
            response.raise_for_status()

        return response

    def _add_csrf_headers(self, request: Request):
        now = datetime.now(timezone.utc)

        if not self.enable_csrf_support:
            return

        if not self.csrf_token or (
            self.csrf_token_expiration and now > self.csrf_token_expiration
        ):
            token_request = self.build_request(
                "GET", f"/csrf-token?client={self.csrf_client_id}"
            )

            try:
                token_response = self.send(token_request)
            except PrefectHTTPStatusError as exc:
                old_server = exc.response.status_code == status.HTTP_404_NOT_FOUND
                unconfigured_server = (
                    exc.response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
                    and "CSRF protection is disabled." in exc.response.text
                )

                if old_server or unconfigured_server:
                    # The token endpoint is either unavailable, suggesting an
                    # older server, or CSRF protection is disabled. In either
                    # case we should disable CSRF support.
                    self.enable_csrf_support = False
                    return

                raise

            token: CsrfToken = CsrfToken.parse_obj(token_response.json())
            self.csrf_token = token.token
            self.csrf_token_expiration = token.expiration

        request.headers["Prefect-Csrf-Token"] = self.csrf_token
        request.headers["Prefect-Csrf-Client"] = str(self.csrf_client_id)


class PrefectHttpxSyncEphemeralClient(TestClient, PrefectHttpxSyncClient):
    """
    This client is a synchronous httpx client that can be used to talk directly
    to an ASGI app, such as an ephemeral Prefect API.

    It is a subclass of both Starlette's `TestClient` and Prefect's
    `PrefectHttpxSyncClient`, so it combines the synchronous testing
    capabilities of `TestClient` with the Prefect-specific behaviors of
    `PrefectHttpxSyncClient`.
    """

    def __init__(
        self,
        *args,
        # override TestClient default
        raise_server_exceptions=False,
        **kwargs,
    ):
        super().__init__(
            *args,
            raise_server_exceptions=raise_server_exceptions,
            **kwargs,
        )

    pass
