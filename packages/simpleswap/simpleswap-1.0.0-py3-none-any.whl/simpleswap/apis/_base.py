from types import SimpleNamespace

import requests

from simpleswap.errors import BaseSimpleSwapException


class BaseAPIRequest:
    BASE_URL = "https://api.simpleswap.io"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _request(self, method: str, url: str, **kwargs):
        response = requests.request(method, url, **kwargs)
        if response.status_code == 401:
            raise BaseSimpleSwapException("Invalid API key")
        return response.json(object_hook=lambda d: SimpleNamespace(**d))
