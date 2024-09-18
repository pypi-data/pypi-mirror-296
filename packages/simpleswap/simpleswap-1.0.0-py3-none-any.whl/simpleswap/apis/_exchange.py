from datetime import datetime
from simpleswap.apis._base import BaseAPIRequest


class ExchangeAPI(BaseAPIRequest):
    def __init__(self, api_key):
        super().__init__(api_key)

    def create_exchange(self, currency_from: str, currency_to: str, amount: float, address_to: str, fixed=False, user_refund_address=None):
        """Create an exchange request

        Args:
            currency_from (str): The currency to exchange from
            currency_to (str): The currency to exchange to
            amount (float): The amount to exchange
            address_to (str): The address to send the exchanged currency
            fixed (bool, optional): Whether the amount is fixed or not. Defaults to False.
            user_refund_address (str, optional): The address to refund the user. Defaults to None.
        """
        url = f"{self.BASE_URL}/create_exchange"
        data = {"currency_from": currency_from, "currency_to": currency_to, "amount": amount, "address_to": address_to, "fixed": fixed}
        if user_refund_address:
            data["user_refund_address"] = user_refund_address
        params = {"api_key": self.api_key}
        return self._request("POST", url, data=data, params=params)

    def get_exchange(self, id: str):
        # Generate documentation
        """Get a specific exchange by its id

        Args:
            id (str): The id of the exchange
        """

        url = f"{self.BASE_URL}/get_exchange"
        params = {"api_key": self.api_key, "id": id}
        return self._request("GET", url, params=params)

    def get_exchanges(self, limit=100, offset=0, after_date: datetime = None, before_date: datetime = None):
        """Get a list of exchanges made by the user

        Args:
            limit (int, optional): limit of th results. Defaults to 100.
            offset (int, optional): offset to skip. Defaults to 0.
            after_date (datetime, optional): Get results after this date. Defaults to None.
            before_date (datetime, optional): Get results before this date. Defaults to None.
        """
        if limit < 0 or limit > 1000:
            raise ValueError("Limit must be between 0 and 1000")
        if offset < 0:
            raise ValueError("Offset must be greater than or equal to 0")

        url = f"{self.BASE_URL}/get_exchanges"
        params = {"api_key": self.api_key, "limit": limit, "offset": offset}
        if after_date:
            params["gte"] = after_date.isoformat()
        if before_date:
            params["lte"] = before_date.isoformat()
        return self._request("GET", url, params=params)

    def get_ranges(self, currency_from: str, currency_to: str, fixed=False):
        """Return minimal and maximal (if exists) amount for exchange between selected currencies

        Args:
            currency_from (str): The currency to exchange from
            currency_to (str): The currency to exchange to
            fixed (bool, optional): Whether the amount is fixed or not. Defaults to False.
        """
        url = f"{self.BASE_URL}/get_ranges"
        params = {"api_key": self.api_key, "currency_from": currency_from, "currency_to": currency_to, "fixed": fixed}
        return self._request("GET", url, params=params)

    def get_estimated(self, currency_from: str, currency_to: str, amount: float, fixed=False):
        """Return estimated exchange amount

        Args:
            currency_from (str): The currency to exchange from
            currency_to (str): The currency to exchange to
            amount (float): The amount to exchange
            fixed (bool, optional): Whether the amount is fixed or not. Defaults to False.
        """
        url = f"{self.BASE_URL}/get_estimated"
        params = {"api_key": self.api_key, "currency_from": currency_from, "currency_to": currency_to, "amount": amount, "fixed": fixed}
        return self._request("GET", url, params=params)

    def check_exchange(self, currency_from: str, currency_to: str, amount: float, fixed=False):
        """Returns "true" if it is possible to create an exchange with the given parameters

        Args:
            currency_from (str): The currency to exchange from
            currency_to (str): The currency to exchange to
            amount (float): The amount to exchange
            fixed (bool, optional): Whether the amount is fixed or not. Defaults to False.
        """
        url = f"{self.BASE_URL}/check_exchanges"
        params = {"api_key": self.api_key, "currency_from": currency_from, "currency_to": currency_to, "amount": amount, "fixed": fixed}
        return self._request("GET", url, params=params)
