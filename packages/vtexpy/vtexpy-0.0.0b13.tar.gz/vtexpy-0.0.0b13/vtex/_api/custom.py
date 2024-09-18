from datetime import datetime
from typing import Any, List, Type, Union

from httpx._types import (
    CookieTypes,
    HeaderTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
)

from .._dto import VTEXResponseType
from .._types import HTTPMethodType
from .._utils import to_datetime
from .base import BaseAPI


class CustomAPI(BaseAPI):
    """
    Client for calling endpoints that have not yet been implemented by the SDK.
    You can directly call the `request` method to call any VTEX API.
    """

    def request(
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
        response_class: Union[Type[VTEXResponseType], None] = None,
        **kwargs: Any,
    ) -> VTEXResponseType:
        return self._request(
            method=method,
            environment=environment,
            endpoint=endpoint,
            headers=headers,
            cookies=cookies,
            params=params,
            json=json,
            data=data,
            content=content,
            files=files,
            config=self.client.config.with_overrides(**kwargs),
            response_class=response_class,
        )

    def get_account_name(self) -> str:
        return self.client.license_manager.get_account().data["account_name"]

    def get_account_creation_date(self) -> datetime:
        return to_datetime(
            self.client.license_manager.get_account().data["creation_date"],
        )

    def get_account_site_names(self) -> datetime:
        return to_datetime(
            self.client.license_manager.get_account().data["creation_date"],
        )

    def get_main_seller(self) -> str:
        return "1"

    def get_market_place_sellers(self, include_inactive: bool = False) -> List[str]:
        return [
            seller["seller_id"]
            for seller in self.client.catalog.list_sellers().items
            if seller["seller_type"] == 1
            and seller["seller_id"] != "1"
            and (seller["is_active"] or include_inactive)
        ]

    def get_franchise_sellers(self, include_inactive: bool = False) -> List[str]:
        return [
            seller["seller_id"]
            for seller in self.client.catalog.list_sellers().items
            if seller["seller_type"] == 2 and (seller["is_active"] or include_inactive)
        ]
