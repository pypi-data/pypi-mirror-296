from functools import cached_property
from typing import TYPE_CHECKING, List, Union

from ._config import Config  # type: ignore[attr-defined]
from ._logging import CLIENT_LOGGER
from ._sentinels import UNDEFINED, UndefinedSentinel

if TYPE_CHECKING:
    from ._api import (
        CatalogAPI,
        CheckoutAPI,
        CustomAPI,
        LicenseManagerAPI,
        LogisticsAPI,
        MasterDataAPI,
        OrdersAPI,
        PaymentsGatewayAPI,
        PromotionsAndTaxesAPI,
    )


class VTEX:
    """
    Entrypoint for the VTEX SDK.
    From this class you can access all the APIs on VTEX
    """

    def __init__(
        self,
        account_name: Union[str, UndefinedSentinel] = UNDEFINED,
        app_key: Union[str, UndefinedSentinel] = UNDEFINED,
        app_token: Union[str, UndefinedSentinel] = UNDEFINED,
        timeout: Union[float, None, UndefinedSentinel] = UNDEFINED,
        retry_attempts: Union[int, UndefinedSentinel] = UNDEFINED,
        retry_backoff_min: Union[float, UndefinedSentinel] = UNDEFINED,
        retry_backoff_max: Union[float, UndefinedSentinel] = UNDEFINED,
        retry_backoff_exponential: Union[bool, float, UndefinedSentinel] = UNDEFINED,
        retry_statuses: Union[List[int], UndefinedSentinel] = UNDEFINED,
        retry_logs: Union[bool, UndefinedSentinel] = UNDEFINED,
        raise_for_status: Union[bool, UndefinedSentinel] = UNDEFINED,
    ) -> None:
        self.logger = CLIENT_LOGGER
        self.config = Config(
            account_name=account_name,
            app_key=app_key,
            app_token=app_token,
            timeout=timeout,
            retry_attempts=retry_attempts,
            retry_backoff_min=retry_backoff_min,
            retry_backoff_max=retry_backoff_max,
            retry_backoff_exponential=retry_backoff_exponential,
            retry_statuses=retry_statuses,
            retry_logs=retry_logs,
            raise_for_status=raise_for_status,
        )

    @cached_property
    def custom(self) -> "CustomAPI":
        from ._api import CustomAPI

        return CustomAPI(client=self)

    @cached_property
    def catalog(self) -> "CatalogAPI":
        from ._api import CatalogAPI

        return CatalogAPI(client=self)

    @cached_property
    def checkout(self) -> "CheckoutAPI":
        from ._api import CheckoutAPI

        return CheckoutAPI(client=self)

    @cached_property
    def license_manager(self) -> "LicenseManagerAPI":
        from ._api import LicenseManagerAPI

        return LicenseManagerAPI(client=self)

    @cached_property
    def logistics(self) -> "LogisticsAPI":
        from ._api import LogisticsAPI

        return LogisticsAPI(client=self)

    @cached_property
    def master_data(self) -> "MasterDataAPI":
        from ._api import MasterDataAPI

        return MasterDataAPI(client=self)

    @cached_property
    def orders(self) -> "OrdersAPI":
        from ._api import OrdersAPI

        return OrdersAPI(client=self)

    @cached_property
    def payments_gateway(self) -> "PaymentsGatewayAPI":
        from ._api import PaymentsGatewayAPI

        return PaymentsGatewayAPI(client=self)

    @cached_property
    def promotions_and_taxes(self) -> "PromotionsAndTaxesAPI":
        from ._api import PromotionsAndTaxesAPI

        return PromotionsAndTaxesAPI(client=self)
