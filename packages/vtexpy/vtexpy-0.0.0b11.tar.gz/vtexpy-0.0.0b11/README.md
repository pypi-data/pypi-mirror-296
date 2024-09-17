# VTEXPY
[![PyPI Version](https://img.shields.io/pypi/v/vtexpy.svg)](https://pypi.python.org/pypi/vtexpy)

## Unofficial Python SDK for VTEX API

VTEXPY is an unofficial Python SDK designed to facilitate integration with the VTEX API.

Even though it is still tagged as beta, vtexpy has been in use by a _SaaS_ company in a
production environment for over a year, making millions of requests a day to the VTEX
API.

### Features

- Easy to use Python interface for calling endpoints on the VTEX API.
- Custom exception handling
- Automatic retries
- Request logging

### Getting Started

#### Requirements

- Python >= 3.9, < 3.14
- httpx >= 0.26, < 1.0
- python-dateutil >= 2.9, < 3.0
- tenacity >= 8.3, < 10.0

#### Installation

```bash
pip install vtexpy
```

#### Usage

If the API you want to call is not yet implemented, feel free to create an issue on the 
VTEXPY Github repository and request it to be added.

```python
from vtex import VTEX

# 1 - Instantiate the VTEX client for the account you want to access:
vtex_client = VTEX(
    account_name="<ACCOUNT_NAME>", 
    app_key="<APP_KEY>", 
    app_token="<APP_TOKEN>",
)

# 2 - Call one of the available APIs, e.g.:
vtex_client.license_manager.get_account()
vtex_client.catalog.list_sku_ids(page=1, page_size=1000)
vtex_client.orders.list_orders(page=1, page_size=100)

# 3 - If the API you want to call is not yet implemented you can use the `custom` API.
vtex_client.custom.request(
    method="GET",
    environment="vtexcommercestable",
    endpoint="/api/catalog_system/pvt/commercialcondition/list",
)
```
