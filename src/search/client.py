from .queries import *
from elasticsearch import Elasticsearch

client = Elasticsearch()


def search_all(query_string: str):
    s = None
    if query_string == "":
        s = client.search(body=match_all)
    return s


def count():
    return client.count()
