from typing import Any, List, Union

from .._dto import VTEXCartItem, VTEXResponse
from .._sentinels import UNDEFINED, UndefinedSentinel
from .._utils import exclude_undefined_values
from .base import BaseAPI


class CheckoutAPI(BaseAPI):
    """
    Client for the Catalog API.
    https://developers.vtex.com/docs/api-reference/checkout-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def cart_simulation(
        self,
        cart: List[VTEXCartItem],
        country: Union[str, UndefinedSentinel] = UNDEFINED,
        postal_code: Union[str, UndefinedSentinel] = UNDEFINED,
        geo_coordinates: Union[List[float], UndefinedSentinel] = UNDEFINED,
        rnb_behavior: Union[int, UndefinedSentinel] = UNDEFINED,
        sales_channel: Union[int, UndefinedSentinel] = UNDEFINED,
        individual_shipping_estimates: Union[bool, UndefinedSentinel] = UNDEFINED,
        **kwargs: Any,
    ) -> VTEXResponse:
        return self._request(
            method="POST",
            environment=self.ENVIRONMENT,
            endpoint="/api/checkout/pub/orderForms/simulation",
            params=exclude_undefined_values({
                "RnbBehavior": rnb_behavior,
                "sc": sales_channel,
                "individualShippingEstimates": individual_shipping_estimates,
            }),
            json=exclude_undefined_values({
                "items": [item.to_vtex_cart_item() for item in cart],
                "country": country,
                "postalCode": postal_code,
                "geoCoordinates": geo_coordinates,
            }),
            config=self._config.with_overrides(**kwargs),
            response_class=VTEXResponse,
        )
