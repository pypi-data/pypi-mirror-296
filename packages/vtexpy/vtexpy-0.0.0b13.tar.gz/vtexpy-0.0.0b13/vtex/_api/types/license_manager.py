from typing import List, TypedDict, Union

from .generic import PagePagination


class AccountAppKey(TypedDict, total=False):
    app_key: str
    id: str
    is_active: bool
    is_blocked: bool
    label: str


class GetAccountData(TypedDict, total=False):
    account_name: str
    app_keys: List[AccountAppKey]
    company_name: str
    creation_date: str
    have_parent_account: bool
    id: str
    inactivation_date: Union[str, None]
    is_active: bool
    is_operating: bool
    name: str
    operation_date: Union[str, None]
    parent_account_id: Union[str, None]
    parent_account_name: Union[str, None]
    trading_name: str


class UserRole(TypedDict, total=False):
    id: int
    name: str


class RoleProduct(TypedDict, total=False):
    name: str


class Role(TypedDict, total=False):
    id: int
    is_admin: bool
    name: str
    products: List[RoleProduct]
    role_type: int


class ListRolesData(TypedDict, total=False):
    items: List[Role]
    paging: PagePagination
