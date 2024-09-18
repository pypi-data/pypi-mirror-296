from simpleswap.apis._base import BaseAPIRequest


class MarketAPI(BaseAPIRequest):
    def __init__(self, api_key=None):
        super().__init__(api_key)

    def get_market_info(self):
        """Get full market information (only for fixed rate)"""
        url = f"{self.BASE_URL}/get_market_info"
        params = {"api_key": self.api_key}
        return self._request("GET", url, params=params)
