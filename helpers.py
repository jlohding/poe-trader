class Queries:
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

class ResultParser:
    def parse(self, results, how="simple"):
        if how == "simple":
            return self.__simple_parse(results)
        elif how == "basic":
            return self.__basic_parse(results)
        elif how == "exchange":
            return self.__exchange_parse(results)
        else:
            raise Exception("Error: Invalid parse type specified")

    def __simple_parse(self, results):
        # give high-level overiew of item desc
        parsed_results = []
        for res in results:
            parsed = {
                "id": res["id"],
                "indexed": res["listing"]["indexed"],
                "price": {
                    "amount": res["listing"]["price"]["amount"],
                    "currency": res["listing"]["price"]["currency"]
                },
                "item": {
                    "name": res["item"].get("name"),
                    "type": res["item"].get("typeLine"),
                    "rarity": res["item"].get("rarity"),
                    "ilvl": res["item"].get("ilvl")
                }
            }
            parsed_results.append(parsed)
        
        return parsed_results

    def __basic_parse(self, results):
        # give basic info for any item type
        parsed_results = []
        for res in results:
            parsed = {
                "id": res["id"],
                "indexed": res["listing"]["indexed"],
                "whisper": res["listing"]["whisper"],
                "price": {
                    "amount": res["listing"]["price"]["amount"],
                    "currency": res["listing"]["price"]["currency"]
                },
                "item": res["item"]
            }       
            parsed_results.append(parsed)

        return parsed_results 
    
    def __exchange_parse(self, results):
        # for exchange pairs
        parsed_results = []
        for result in results:
            parsed = {
                "id": result["id"],
                "indexed": result["listing"]["indexed"],
                "whisper": result["listing"]["whisper"],
                "pay": {
                    "amount": result["listing"]["offers"][0]["exchange"]["amount"],
                    "currency": result["listing"]["offers"][0]["exchange"]["currency"],
                },
                "get": {
                    "amount": result["listing"]["offers"][0]["item"]["amount"],
                    "currency": result["listing"]["offers"][0]["item"]["currency"],
                    "stock": result["listing"]["offers"][0]["item"]["stock"],
                },
                "exch_rate": float(result["listing"]["offers"][0]["exchange"]["amount"]) / float(result["listing"]["offers"][0]["item"]["amount"])
            }
            parsed_results.append(parsed)

        return parsed_results