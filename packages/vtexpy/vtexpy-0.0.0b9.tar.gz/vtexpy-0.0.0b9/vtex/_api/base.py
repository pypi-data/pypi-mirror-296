from http import HTTPStatus
from json import JSONDecodeError
from logging import WARNING, Logger
from typing import Any, Type, Union, cast
from urllib.parse import urljoin

from httpx import (
    Client,
    Headers,
    HTTPError,
    HTTPStatusError,
    Response,
)
from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
)
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from .._config import Config  # type: ignore[attr-defined]
from .._constants import APP_KEY_HEADER, APP_TOKEN_HEADER
from .._dto import VTEXResponse, VTEXResponseType
from .._exceptions import VTEXRequestError, VTEXResponseError
from .._logging import get_logger, log_before_retry
from .._types import HTTPMethodType
from .._utils import redact_headers, to_snake_case, to_snake_case_deep


class BaseAPI:
    """
    Base client for VTEX API.
    """

    def __init__(
        self,
        config: Union[Config, None] = None,
        logger: Union[Logger, None] = None,
    ) -> None:
        self._config = config or Config()
        self._logger = get_logger(
            name=to_snake_case(type(self).__name__),
            parent=logger,
        )

    def _request(
        self,
        method: HTTPMethodType,
        environment: str,
        endpoint: str,
        headers: Union[HeaderTypes, None] = None,
        cookies: Union[CookieTypes, None] = None,
        params: Union[QueryParamTypes, None] = None,
        json: Union[Any, None] = None,
        data: Union[RequestData, None] = None,
        content: Union[RequestContent, None] = None,
        files: Union[RequestFiles, None] = None,
        config: Union[Config, None] = None,
        response_class: Union[Type[VTEXResponseType], None] = None,
    ) -> VTEXResponseType:
        request_config = self._get_config(config=config)
        url = self._get_url(
            config=request_config,
            environment=environment,
            endpoint=endpoint,
        )
        headers = self._get_headers(config=request_config, headers=headers)
        retry_statuses = set(request_config.get_retry_statuses())

        @retry(
            stop=stop_after_attempt(
                max_attempt_number=request_config.get_retry_attempts() + 1,
            ),
            wait=wait_exponential(
                min=request_config.get_retry_backoff_min(),
                max=request_config.get_retry_backoff_max(),
                exp_base=request_config.get_retry_backoff_exponential(),
            ),
            retry=retry_if_exception_type(exception_types=HTTPError),
            before_sleep=(
                log_before_retry(logger=self._logger, log_level=WARNING)
                if request_config.get_retry_logs()
                else None
            ),
            reraise=True,
        )
        def send_vtex_request() -> Response:
            with Client(timeout=request_config.get_timeout()) as client:
                response = client.request(
                    method.upper(),
                    url,
                    headers=headers,
                    cookies=cookies,
                    params=params,
                    json=json,
                    data=data,
                    content=content,
                    files=files,
                )

                response.request.headers = Headers(
                    redact_headers(dict(response.request.headers)),
                )
                response.headers = Headers(redact_headers(dict(response.headers)))
                if response.status_code in retry_statuses:
                    response.raise_for_status()

                return response

        try:
            response = send_vtex_request()
        except HTTPStatusError as exception:
            response = exception.response
        except HTTPError as exception:
            headers = redact_headers(dict(headers))

            details = {
                "exception": exception,
                "method": str(method).upper(),
                "url": str(url),
                "headers": headers,
            }

            self._logger.error(str(exception), extra=details, exc_info=True)

            raise VTEXRequestError(**details) from None  # type: ignore[arg-type]

        self._raise_from_response(response=response, config=request_config)

        return cast(
            VTEXResponseType,
            (response_class or VTEXResponse).factory(response),
        )

    def _get_config(self, config: Union[Config, None]) -> Config:
        return config or self._config

    def _get_url(self, config: Config, environment: str, endpoint: str) -> str:
        return urljoin(
            f"https://{config.get_account_name()}.{environment}.com.br",
            endpoint,
        )

    def _get_headers(
        self,
        config: Config,
        headers: Union[HeaderTypes, None] = None,
    ) -> Headers:
        request_headers = Headers(headers=headers)

        request_headers[APP_KEY_HEADER] = config.get_app_key()
        request_headers[APP_TOKEN_HEADER] = config.get_app_token()

        request_headers["Content-Type"] = "application/json; charset=utf-8"
        request_headers["Accept"] = "application/json"

        return request_headers

    def _raise_from_response(self, response: Response, config: Config) -> None:
        if response.is_error and config.get_raise_for_status():
            try:
                data = to_snake_case_deep(response.json(strict=False))
            except JSONDecodeError:
                data = response.text or HTTPStatus(response.status_code).phrase

            error = VTEXResponseError(
                data,
                method=str(response.request.method).upper(),
                url=str(response.request.url),
                request_headers=response.request.headers,
                status=response.status_code,
                data=data,
                response_headers=response.headers,
            )

            if response.is_server_error:
                self._logger.error(data, extra=error.to_dict())
            else:
                self._logger.warning(data, extra=error.to_dict())

            raise error from None
