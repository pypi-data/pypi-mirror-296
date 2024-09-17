from typing import Any

from .. import VTEXListResponse
from .._dto import VTEXResponse
from .base import BaseAPI


class PromotionsAndTaxesAPI(BaseAPI):
    """
    Client for the Promotions and Taxes API.
    https://developers.vtex.com/docs/api-reference/promotions-and-taxes-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def list_archived_promotions(self, **kwargs: Any) -> VTEXListResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="api/rnb/pvt/archive/benefits/calculatorconfiguration",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXListResponse,
        )

    def list_promotions(self, **kwargs: Any) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="api/rnb/pvt/benefits/calculatorconfiguration",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def list_taxes(self, **kwargs: Any) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="api/rnb/pvt/taxes/calculatorconfiguration",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )

    def get_promotion_or_tax(
        self,
        promotion_or_tax_id: str,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint=f"/api/rnb/pvt/calculatorconfiguration/{promotion_or_tax_id}",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )
