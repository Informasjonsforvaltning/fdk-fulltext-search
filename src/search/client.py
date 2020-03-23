from .queries import *
from ..ingest import client


def search_all(query_string: str):
    s = None
    if query_string == "":
        s = client.search(body=all_indices)
    return s


def count():
    return client.count()
