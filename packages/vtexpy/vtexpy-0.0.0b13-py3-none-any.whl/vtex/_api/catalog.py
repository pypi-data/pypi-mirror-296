from typing import Any, List, Union

from .._constants import (
    GET_CATEGORY_TREE_MAX_LEVELS,
    LIST_CATEGORIES_MAX_PAGE_SIZE,
    LIST_CATEGORIES_START_PAGE,
    LIST_SKU_IDS_MAX_PAGE_SIZE,
    LIST_SKU_IDS_START_PAGE,
    MIN_PAGE_SIZE,
)
from .._dto import VTEXDataResponse, VTEXItemsResponse, VTEXPaginatedItemsResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._types import DictType
from .._utils import exclude_undefined_values
from .base import BaseAPI


class CatalogAPI(BaseAPI):
    """
    Client for the Catalog API.
    https://developers.vtex.com/docs/api-reference/catalog-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_sellers(
        self,
        sales_channel: Union[int, UndefinedSentinel] = UNDEFINED,
        seller_type: Union[int, UndefinedSentinel] = UNDEFINED,
        is_better_scope: Union[bool, UndefinedSentinel] = UNDEFINED,
        **kwargs: Any,
    ) -> VTEXItemsResponse[DictType, DictType]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="/api/catalog_system/pvt/seller/list",
            params=exclude_undefined_values({
                "sc": sales_channel,
                "sellerType": seller_type,
                "isBetterScope": is_better_scope,
            }),
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[DictType, DictType],
        )

    def list_sku_ids(
        self,
        page: int = LIST_SKU_IDS_START_PAGE,
        page_size: int = LIST_SKU_IDS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXItemsResponse[List[str], str]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="/api/catalog_system/pvt/sku/stockkeepingunitids",
            params={
                "page": max(page, LIST_SKU_IDS_START_PAGE),
                "pagesize": max(
                    min(page_size, LIST_SKU_IDS_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXItemsResponse[List[str], str],
        )

    def get_sku_with_context(
        self,
        sku_id: int,
        **kwargs: Any,
    ) -> VTEXDataResponse[DictType]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/catalog_system/pvt/sku/stockkeepingunitbyid/{sku_id}",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[DictType],
        )

    def list_categories(
        self,
        page: int = LIST_SKU_IDS_START_PAGE,
        page_size: int = LIST_SKU_IDS_MAX_PAGE_SIZE,
        **kwargs: Any,
    ) -> VTEXPaginatedItemsResponse[DictType, DictType]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="/api/catalog/pvt/category",
            params={
                "page": max(page, LIST_CATEGORIES_START_PAGE),
                "pagesize": max(
                    min(page_size, LIST_CATEGORIES_MAX_PAGE_SIZE),
                    MIN_PAGE_SIZE,
                ),
            },
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXPaginatedItemsResponse[DictType, DictType],
        )

    def get_category_tree(
        self,
        levels: int = GET_CATEGORY_TREE_MAX_LEVELS,
        **kwargs: Any,
    ) -> VTEXDataResponse[DictType]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/catalog_system/pub/category/tree/{levels}",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[DictType],
        )

    def get_category(
        self,
        category_id: str,
        **kwargs: Any,
    ) -> VTEXDataResponse[DictType]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/catalog/pvt/category/{category_id}",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[DictType],
        )
