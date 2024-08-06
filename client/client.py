from utils.parsers import Parser
from utils.queries import QueryBuilder
from settings import USER_AGENT


class Client:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT
        }
        self.queries = QueryBuilder()
        self.parser = Parser()
    
    def query(self, **kwargs):
        raise NotImplementedError()