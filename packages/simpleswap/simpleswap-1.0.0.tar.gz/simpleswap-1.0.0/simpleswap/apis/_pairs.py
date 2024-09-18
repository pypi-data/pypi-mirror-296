from simpleswap.apis._base import BaseAPIRequest


class PairsAPI(BaseAPIRequest):
    def __init__(self, api_key=None):
        super().__init__(api_key)

    def get_pairs(self, symbol: str, fixed=False) -> list:
        """Return all active pairs with specified currency

        Args:
            symbol (str): The currency to get pairs for
            fixed (bool, optional): Whether the amount is fixed or not. Defaults to False.
        """
        url = f"{self.BASE_URL}/get_pairs"
        params = {"api_key": self.api_key, "symbol": symbol, "fixed": fixed}
        return self._request("GET", url, params=params)

    def get_all_pairs(self, fixed=False) -> list:
        """Return list with all active exchange pairs
        List of pairs is updated every 5 minutes

                Args:
                    fixed (bool, optional): Whether the amount is fixed or not. Defaults to False.
        """
        url = f"{self.BASE_URL}/get_all_pairs"
        params = {"api_key": self.api_key, "fixed": fixed}
        return self._request("GET", url, params=params)
