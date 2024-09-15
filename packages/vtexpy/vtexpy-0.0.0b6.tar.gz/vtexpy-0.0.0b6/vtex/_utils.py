from datetime import datetime, timezone, tzinfo
from re import compile
from typing import Any, Dict, Mapping, Union
from uuid import UUID

from distutils.util import strtobool

from ._constants import APP_KEY_HEADER, APP_TOKEN_HEADER
from ._logging import get_logger
from ._sentinels import UNDEFINED
from ._types import JSONType

TO_SNAKE_CASE_STEP_1_PATTERN = compile(r"(.)([A-Z][a-z]+)")
TO_SNAKE_CASE_STEP_2_PATTERN = compile(r"([a-z0-9])([A-Z])")


def is_nullish_str(value: str) -> bool:
    return value.lower() in {"", "null", "none", "nil"}


def exclude_undefined_values(obj: Dict[Any, Any]) -> Dict[Any, Any]:
    return {key: value for key, value in obj.items() if value is not UNDEFINED}


def str_to_bool(value: str) -> bool:
    return bool(strtobool(value))


def remove_null_bytes(value: str) -> str:
    return value.replace("\x00", "")


def to_snake_case(string: str) -> str:
    try:
        UUID(string)
    except (AttributeError, ValueError, TypeError):
        return TO_SNAKE_CASE_STEP_2_PATTERN.sub(
            r"\1_\2",
            TO_SNAKE_CASE_STEP_1_PATTERN.sub(r"\1_\2", string),
        ).lower()

    return string


def to_snake_case_deep(obj: JSONType) -> JSONType:
    logger = get_logger("utils")

    if isinstance(obj, dict):
        snake_cased_obj = {}

        for key, value in sorted(
            obj.items(),
            key=lambda item: [(int(c.isupper()), c.lower()) for c in item[0]],
        ):
            if isinstance(key, str):
                key = to_snake_case(remove_null_bytes(key))

                while key in snake_cased_obj:
                    logger.warning(
                        f"Snake cased key {key} appears multiple times in object",
                        extra=obj,
                    )
                    key = f"_{key}"

            snake_cased_obj[key] = to_snake_case_deep(value)

        return snake_cased_obj

    if isinstance(obj, (list, set, tuple)):
        return type(obj)([to_snake_case_deep(element) for element in obj])

    if isinstance(obj, str):
        return remove_null_bytes(obj)

    return obj


def redact_headers(headers: Mapping[str, str]) -> Dict[str, str]:
    redacted_headers = {}

    for key, value in list(headers.items()):
        if key.lower() in {APP_KEY_HEADER.lower(), APP_TOKEN_HEADER.lower()}:
            redacted_headers[key] = "*" * 32
        else:
            redacted_headers[key] = value

    return redacted_headers


def now(use_tz: bool = True, tz: Union[tzinfo, None] = None) -> datetime:
    return datetime.now((tz or timezone.utc) if use_tz else None)


def three_years_ago(use_tz: bool = True, tz: Union[tzinfo, None] = None) -> datetime:
    current_datetime = now(use_tz=use_tz, tz=tz)

    return current_datetime.replace(
        year=current_datetime.year - 3,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
