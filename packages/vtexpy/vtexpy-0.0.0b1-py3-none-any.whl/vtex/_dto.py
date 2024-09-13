from dataclasses import dataclass
from json import JSONDecodeError
from math import ceil
from typing import Dict, TypeVar, Union

from httpx import Request, Response

from ._types import IterableType, JSONType
from ._utils import to_snake_case_deep

VTEXResponseType = TypeVar("VTEXResponseType", bound="VTEXResponse", covariant=True)


@dataclass
class VTEXRequest:
    request: Request
    method: str
    url: str
    headers: Dict[str, str]

    @classmethod
    def factory(cls, request: Request) -> "VTEXRequest":
        return cls(
            request=request,
            method=str(request.method).upper(),
            url=str(request.url),
            headers=dict(request.headers),
        )


@dataclass
class VTEXResponse:
    request: VTEXRequest
    response: Response
    data: JSONType
    status: int
    headers: Dict[str, str]

    @classmethod
    def factory(cls, response: Response) -> "VTEXResponse":
        try:
            data = to_snake_case_deep(response.json(strict=False))
        except JSONDecodeError:
            data = response.text

        return cls(
            request=VTEXRequest.factory(response.request),
            response=response,
            data=data,
            status=int(response.status_code),
            headers=dict(response.headers),
        )


@dataclass
class VTEXListResponse(VTEXResponse):
    items: IterableType[JSONType]

    @classmethod
    def factory(cls, response: Response) -> "VTEXListResponse":
        vtex_response = VTEXResponse.factory(response)
        data = vtex_response.data

        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and isinstance(data.get("list"), list):
            items = data["list"]
        elif isinstance(data, dict) and isinstance(data.get("items"), list):
            items = data["items"]
        elif isinstance(data, dict) and isinstance(data.get("data"), list):
            items = data["data"]
        else:
            raise ValueError(f"Not a valid list response: {data}")

        return cls(
            request=vtex_response.request,
            response=vtex_response.response,
            data=vtex_response.data,
            status=vtex_response.status,
            headers=vtex_response.headers,
            items=items,
        )


@dataclass
class VTEXPagination:
    total: int
    pages: int
    page_size: int
    page: int
    previous_page: Union[int, None]
    next_page: Union[int, None]

    @classmethod
    def factory(cls, vtex_list_response: VTEXListResponse) -> "VTEXPagination":
        data = vtex_list_response.data
        request_headers = vtex_list_response.request.headers
        response_headers = vtex_list_response.headers

        total, pages, page_size, page = -1, -1, -1, -1
        if isinstance(data, dict) and data.get("paging"):
            pagination = data["paging"]
            total = pagination["total"]
            page_size = pagination["per_page"]
            pages = pagination["pages"]
            page = int(pagination.get("page") or pagination.get("current_page"))
        elif isinstance(data, dict) and data.get("total_page"):
            total = data["total_rows"]
            page_size = data["size"]
            pages = data["total_page"]
            page = data["page"]
        elif "rest-content-range" in response_headers:
            request_pagination = request_headers["rest-range"].split("=")[-1].split("-")
            response_pagination = response_headers["rest-content-range"].split(" ")[-1]
            total = int(response_pagination.split("/")[1])
            page_size = int(request_pagination[1]) - int(request_pagination[0])
            pages = ceil(total / page_size)
            page = ceil(
                int(response_pagination.split("/")[0].split("-")[1]) / page_size
            )

        if all(
            isinstance(field, int) and field != -1
            for field in {total, pages, page_size, page}
        ):
            return cls(
                total=total,
                pages=pages,
                page_size=page_size,
                page=page,
                previous_page=page - 1 if page > 1 else None,
                next_page=page + 1 if page < pages else None,
            )

        raise ValueError(f"Not a valid paginated list response: {vtex_list_response}")


@dataclass
class VTEXPaginatedListResponse(VTEXListResponse):
    pagination: VTEXPagination

    @classmethod
    def factory(cls, response: Response) -> "VTEXPaginatedListResponse":
        vtex_list_response = VTEXListResponse.factory(response)

        return cls(
            request=vtex_list_response.request,
            response=vtex_list_response.response,
            data=vtex_list_response.data,
            status=vtex_list_response.status,
            headers=vtex_list_response.headers,
            items=vtex_list_response.items,
            pagination=VTEXPagination.factory(vtex_list_response),
        )


@dataclass
class VTEXScroll:
    token: Union[str, None]

    @classmethod
    def factory(cls, vtex_list_response: VTEXListResponse) -> "VTEXScroll":
        return cls(token=None)


@dataclass
class VTEXScrollListResponse(VTEXListResponse):
    scroll: VTEXScroll

    @classmethod
    def factory(cls, response: Response) -> "VTEXScrollListResponse":
        vtex_list_response = VTEXListResponse.factory(response)

        return cls(
            request=vtex_list_response.request,
            response=vtex_list_response.response,
            data=vtex_list_response.data,
            status=vtex_list_response.status,
            headers=vtex_list_response.headers,
            items=vtex_list_response.items,
            scroll=VTEXScroll.factory(vtex_list_response),
        )


@dataclass
class VTEXCartItem:
    sku_id: str
    quantity: int
    seller_id: str

    def to_vtex_cart_item(self) -> Dict[str, Union[str, int]]:
        return {
            "id": self.sku_id,
            "quantity": self.quantity,
            "seller": self.seller_id,
        }
