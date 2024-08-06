class QueryBuilder:
    def get_items(self, **kwargs):
        seller_status = kwargs.pop("seller_status", "online")
        item_name = kwargs.pop("item_name", "")
        item_type = kwargs.pop("item_type", "")
        sort_price = kwargs.pop("sort_price", "asc")

        query_dict = {
            "status": {"option": seller_status},
        }
        if item_name:
            query_dict["name"] = item_name
        if item_type:
            query_dict["type"] = item_type

        sort_dict = {
            "price": sort_price
        }

        data = {
            "query": query_dict,
            "sort": sort_dict
        }

        return data
    
    def get_exchange(self, buy, sell, **kwargs):
        seller_status = kwargs.pop("seller_status", "online")

        data = {
            "exchange": {
                "status": seller_status,
                "want": [buy],
                "have": [sell]
            }
        }

        return data