from typing import (
    List,
    Literal,
    Mapping,
    Set,
    Tuple,
    TypeVar,
    Union,
)

IterableValueType = TypeVar("IterableValueType")
IterableType = Union[
    Tuple[IterableValueType, ...],
    Set[IterableValueType],
    List[IterableValueType],
]

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

PrimitiveTypes = Union[None, bool, int, float, str]
JSONType = Union[PrimitiveTypes, IterableType["JSONType"], Mapping[str, "JSONType"]]
