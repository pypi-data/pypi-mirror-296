from . import _constants as VTEXConstants  # noqa: N812
from ._dto import (
    VTEXCartItem,
    VTEXListResponse,
    VTEXPaginatedListResponse,
    VTEXResponse,
    VTEXScrollListResponse,
)
from ._exceptions import VTEXError, VTEXRequestError, VTEXResponseError
from ._vtex import VTEX

__all__ = [
    "VTEX",
    "VTEXCartItem",
    "VTEXConstants",
    "VTEXError",
    "VTEXListResponse",
    "VTEXPaginatedListResponse",
    "VTEXRequestError",
    "VTEXResponse",
    "VTEXResponseError",
    "VTEXScrollListResponse",
]


for name in __all__:
    locals()[name].__module__ = "vtex"
