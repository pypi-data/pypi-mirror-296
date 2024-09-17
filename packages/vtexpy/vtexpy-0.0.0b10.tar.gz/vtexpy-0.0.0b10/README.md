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

```python
from vtex import VTEX

vtex_client = VTEX(
    account_name="<ACCOUNT_NAME>", 
    app_key="<APP_KEY>", 
    app_token="<APP_TOKEN>",
)
```
