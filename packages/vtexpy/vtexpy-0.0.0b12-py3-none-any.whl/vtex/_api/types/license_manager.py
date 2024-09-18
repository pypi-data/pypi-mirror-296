from typing import TypedDict, Union


class GetAccountData(TypedDict, total=False):
    account_name: str
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
