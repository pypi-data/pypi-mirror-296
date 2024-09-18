from typing import Any, Dict, Literal

OrderingDirectionType = Literal["ASC", "DESC", "asc", "desc"]

HTTPMethodType = Literal[
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "delete",
    "get",
    "head",
    "options",
    "patch",
    "post",
    "put",
]

DictType = Dict[str, Any]
