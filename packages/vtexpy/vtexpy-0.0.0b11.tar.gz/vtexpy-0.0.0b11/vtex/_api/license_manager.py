from typing import Any

from .._dto import VTEXDataResponse
from .base import BaseAPI
from .types.license_manager import GetAccountData


class LicenseManagerAPI(BaseAPI):
    """
    Client for the License Manager API.
    https://developers.vtex.com/docs/api-reference/license-manager-api
    """

    ENVIRONMENT = "vtexcommercestable"

    def get_account(self, **kwargs: Any) -> VTEXDataResponse[GetAccountData]:
        return self._request(
            method="GET",
            environment=self.ENVIRONMENT,
            endpoint="/api/vlm/account",
            config=self.client.config.with_overrides(**kwargs),
            response_class=VTEXDataResponse[GetAccountData],
        )
