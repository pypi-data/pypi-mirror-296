from logging import Logger, getLogger
from typing import Callable, Union

from httpx import HTTPStatusError
from tenacity import RetryCallState


def get_logger(name: str, parent: Union[Logger, None] = None) -> Logger:
    if parent:
        return parent.getChild(name)

    return getLogger(f"vtex.{name}")


def log_before_retry(
    logger: Logger,
    log_level: int,
) -> Callable[[RetryCallState], None]:
    def retry_log(retry_state: RetryCallState) -> None:
        if not retry_state.outcome or not retry_state.next_action:
            raise RuntimeError("Retry log called before request was finished")

        exception = retry_state.outcome.exception()
        if not isinstance(exception, HTTPStatusError):
            raise RuntimeError("Retry log called without an http status error outcome")

        method = str(exception.request.method)
        url = str(exception.request.url)
        status = str(exception.response.status_code)
        reason = str(exception.response.reason_phrase)

        logger.log(
            log_level,
            f"Retrying {method} {url} in {retry_state.next_action.sleep}s as "
            f"attempt {retry_state.attempt_number} failed with: {status} - {reason}",
            extra={
                "exception": exception,
                "request": exception.request.__dict__,
                "response": exception.response.__dict__,
                "retry_state": retry_state.__dict__,
            },
        )

    return retry_log


CLIENT_LOGGER = get_logger(name="client")
EXCEPTIONS_LOGGER = get_logger(name="exceptions")
UTILS_LOGGER = get_logger(name="utils")
