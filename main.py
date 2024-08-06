from client.exchange_client import ExchangeClient
from client.items_client import ItemsClient

if __name__ == "__main__":
    items = ItemsClient()

    search_1 = items.query(
        item_name = "Voidforge",
        item_type="Infernal Sword"
    )

    print(search_1[0])

    exch = ExchangeClient()
    search_2, _ = exch.query(
        base_currency="chaos",
        quote_currency="exalted"
    )

    print(search_2[0])