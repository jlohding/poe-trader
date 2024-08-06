import os 
import requests 
from client.client import Client
from settings import ITEMS_ENDPOINT, FETCH_ENDPOINT


class ItemsClient(Client):    
    def __init__(self):
       super().__init__()
       self.search_endpoint = ITEMS_ENDPOINT
       self.fetch_endpoint = FETCH_ENDPOINT

    def query(self, **kwargs):
        search_results = self.__search(**kwargs)
        fetch_results = self.__fetch(search_results, n_limit=10)
        parsed_results = self.parser.parse(fetch_results, "simple")

        return parsed_results

    def __search(self, **kwargs):
        json_data = self.queries.get_items(**kwargs)

        try:
            resp = requests.post(
                url=self.search_endpoint,
                headers=self.headers,
                json=json_data
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
        
        search_json = resp.json()
        search_results = search_json["result"]
        return search_results

    def __fetch(self, search_results, n_limit=10):
        search_results = search_results[:n_limit]
        results_str = ",".join(search_results)

        try:
            resp = requests.get(
                url=os.path.join(self.fetch_endpoint, results_str),
                headers=self.headers,
            )
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)
    
        fetch_json = resp.json()
        fetch_results = fetch_json["result"]

        return fetch_results
    

if __name__ == "__main__":
    client = ItemsClient()

    results = client.query(
        item_name="Voidforge",
        item_type="Infernal Sword",
    )
    
    print(results)