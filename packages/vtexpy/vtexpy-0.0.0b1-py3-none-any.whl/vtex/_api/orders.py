from datetime import datetime, timezone
from typing import Any, Dict, Union

from .._constants import (
    LIST_FEED_ORDERS_MAX_PAGE_SIZE,
    LIST_ORDERS_MAX_PAGE,
    LIST_ORDERS_MAX_PAGE_SIZE,
    LIST_ORDERS_START_PAGE,
    MIN_PAGE_SIZE,
)
from .._dto import VTEXListResponse, VTEXPaginatedListResponse, VTEXResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._types import IterableType, OrderingDirectionType
from .._utils import now, three_years_ago
from .base import BaseAPI


class OrdersAPI(BaseAPI):
    """
    Client for the Orders API.
    https://developers.vtex.com/docs/api-reference/orders-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_orders(
        self,
        query: Union[str, UndefinedSentinel] = UNDEFINED,
        search: Union[str, UndefinedSentinel] = UNDEFINED,
        creation_date_from: Union[datetime, UndefinedSentinel] = UNDEFINED,
        creation_date_to: Union[datetime, UndefinedSentinel] = UNDEFINED,
        incomplete: bool = False,
        order_by_field: str = "creationDate",
        order_by_direction: OrderingDirectionType = "desc",
        page: int = LIST_ORDERS_START_PAGE,
        page_size: int = LIST_ORDERS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedListResponse:
        if page > LIST_ORDERS_MAX_PAGE:
            raise ValueError("List Orders endpoint can only return up to page 30")

        params: Dict[str, Union[str, int]] = {
            "incompleteOrders": incomplete,
            "orderBy": f"{order_by_field},{order_by_direction.lower()}",
            "page": max(
                min(page, LIST_ORDERS_MAX_PAGE),
                LIST_ORDERS_START_PAGE,
            ),
            "per_page": max(
                min(page_size, LIST_ORDERS_MAX_PAGE_SIZE),
                MIN_PAGE_SIZE,
            ),
        }

        if query is not UNDEFINED:
            params["q"] = str(query)

        if search is not UNDEFINED:
            params["searchField"] = str(search)

        if creation_date_from is not UNDEFINED or creation_date_to is not UNDEFINED:
            if not isinstance(creation_date_from, datetime):
                creation_date_from = three_years_ago()

            if not isinstance(creation_date_to, datetime):
                creation_date_to = now()

            start = (
                creation_date_from.astimezone(timezone.utc)
                .isoformat(timespec="milliseconds")
                .split("+")[0]
            )
            end = (
                creation_date_to.astimezone(timezone.utc)
                .isoformat(timespec="milliseconds")
                .split("+")[0]
            )

            params["f_creationDate"] = f"creationDate:[{start}Z TO {end}Z]"

        response = self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="/api/oms/pvt/orders/",
            params=params,
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXPaginatedListResponse,
        )

        pagination = response.pagination
        if isinstance(pagination.next_page, int) and pagination.next_page > 30:
            pagination.next_page = None

        return response

    def get_order(self, order_id: str, **kwargs: Any) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/oms/pvt/orders/{order_id}",
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def list_feed_orders(
        self,
        page_size: int = LIST_FEED_ORDERS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXListResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="/api/orders/feed/",
            params={
                "maxlot": max(
                    min(page_size, LIST_FEED_ORDERS_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXListResponse,
        )

    def commit_feed_orders(
        self,
        handles: IterableType[str],
        **kwargs: Any,
    ) -> VTEXResponse:
        if not handles:
            raise ValueError(
                "At least one handle must be provided to commit to the feed"
            )
        elif len(handles) > LIST_FEED_ORDERS_MAX_PAGE_SIZE:
            raise ValueError(
                f"At most {LIST_FEED_ORDERS_MAX_PAGE_SIZE} feed orders can be commited"
                f"at once"
            )

        return self._request(
            method="POST",
            environment=self.ENVIRONMENT,
            endpoint="/api/orders/feed/",
            json={"handles": handles},
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )
