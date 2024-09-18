from simpleswap.apis import CurrencyAPI, ExchangeAPI, MarketAPI, PairsAPI


class SimpleSwap:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    @property
    def currency(self):
        return CurrencyAPI(self.api_key)

    @property
    def exchange(self):
        return ExchangeAPI(self.api_key)

    @property
    def market(self):
        return MarketAPI(self.api_key)

    @property
    def pairs(self):
        return PairsAPI(self.api_key)
