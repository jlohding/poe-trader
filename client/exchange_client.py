import requests
from client.client import Client
from settings import EXCHANGE_ENDPOINT


class ExchangeClient(Client):    
    def __init__(self):
       super().__init__()
       self.search_endpoint = EXCHANGE_ENDPOINT

    def query(self, **kwargs):
        base_currency = kwargs.pop("base_currency")
        quote_currency = kwargs.pop("quote_currency")

        bq_result = self.__search(buy=base_currency, sell=quote_currency)
        parsed_bq_result = self.parser.parse(bq_result, how="exchange")

        qb_result = self.__search(buy=quote_currency, sell=base_currency)
        parsed_qb_result = self.parser.parse(qb_result, how="exchange")
        
        return parsed_bq_result, parsed_qb_result

    def __search(self, buy, sell):
        try:
            resp = requests.post(
                url = self.search_endpoint,
                headers=self.headers,
                json = self.queries.get_exchange(buy, sell)
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)

        results = list(resp.json()["result"].values())
        return results
    

if __name__ == "__main__":
    client = ExchangeClient()

    results = client.query(
        base_currency="chaos",
        quote_currency="exalted",
    )
    
    print(results)