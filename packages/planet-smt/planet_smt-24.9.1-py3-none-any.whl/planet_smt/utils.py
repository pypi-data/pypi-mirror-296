"""Utilities for handling HTTP requests and responses."""

import json
import logging
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import backoff
import httpx

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)

P = ParamSpec("P")
R = TypeVar("R")


def _get_content(bytes_content: bytes) -> str | None:
    """Get content from bytes of a response. If the content is JSON, it is pretty printed,
    otherwise it is returned as is. If the content is empty, None is returned.

    :param bytes_content: The content of the response.
    """

    try:
        content = json.dumps(json.loads(bytes_content.decode()), indent=4)
    except json.decoder.JSONDecodeError:
        content = bytes_content.decode()

    if len(content) == 0:
        return None

    return content


def handle_http_status_errors(
    raise_error_type: type[httpx.HTTPStatusError] = httpx.HTTPStatusError, max_time: int = 0
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator that handles HTTP status errors and raises a custom error type. Also includes a
    backoff decorator to retry the request if an HTTP error is encountered. The chosen backoff
    strategy is exponential backoff with full jitter with a maximum wait time of 180 seconds.
    The backoff strategy imidiatelly gives up if the status code is between 400 and 500.

    :param raise_error_type: The error type to raise when an HTTP status error is encountered.
        Must be a subclass of 'httpx.HTTPStatusError'.
    """

    def handle_http_status_errors_decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def handle_http_status_errors_implementation(*args: P.args, **kwargs: P.kwargs) -> R:
            """Handle HTTP status errors and raise a custom error type with a pretty-printed error
            message with all the necessary information.
            """

            backoff_decorator = backoff.on_exception(
                wait_gen=backoff.expo,  # exponential increase in wait time between retries
                exception=httpx.HTTPError,  # retry all httpx HTTP error
                max_time=max_time,  # maximum time to retry
                # give up if status code is between 400 and 500 since those are usually
                # not worth retrying because it is a user-error or a server-error
                giveup=lambda e: isinstance(e, httpx.HTTPStatusError) and 400 <= e.response.status_code <= 500,
                logger=logger,  # logger to log backoff information
            )
            decorated_func = backoff_decorator(func)

            try:
                return decorated_func(*args, **kwargs)
            except httpx.HTTPStatusError as err:
                request = err.request
                response = err.response
                message = f"Received status code '{response.status_code}' from '{request.url}' with error: {err!s}\n\n"

                request_content = _get_content(request.content)
                if request_content:
                    message += f"Request content:\n{request_content}\n\n"

                response_content = _get_content(response.content)
                if response_content:
                    message += f"Response content:\n{response_content}\n\n"

                raise raise_error_type(message=message, response=response, request=request) from err

        return handle_http_status_errors_implementation

    return handle_http_status_errors_decorator
