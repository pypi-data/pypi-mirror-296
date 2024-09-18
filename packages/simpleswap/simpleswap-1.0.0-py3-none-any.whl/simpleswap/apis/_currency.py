from simpleswap.apis._base import BaseAPIRequest


class CurrencyAPI(BaseAPIRequest):
    def __init__(self, api_key):
        super().__init__(api_key)

    def get_currency(self, symbol: str):
        """Get information about a specific currency.
        Return info about currency by provided symbol

        Args:
            symbol (str): The currency symbol to get information for (e.g. BTC, ETH, LTC)
        """
        params = {"api_key": self.api_key, "symbol": symbol}
        url = f"{self.BASE_URL}/get_currency"
        return self._request("GET", url, params=params)

    def get_all_currencies(self):
        """Get information about all currencies"""
        params = {"api_key": self.api_key}
        url = f"{self.BASE_URL}/get_all_currencies"
        return self._request("GET", url, params=params)
