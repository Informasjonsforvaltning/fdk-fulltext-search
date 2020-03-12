from .queries import *
from elasticsearch import Elasticsearch

client = Elasticsearch()


def search_all(queryString):
    s = None
    if queryString == "":
        s = client.search(body=match_all)
        return s


def count():
    return client.count()
