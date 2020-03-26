from .queries import *
from ..ingest import client


def search_all(request: dict = None):
    q = AllIndicesQuery()
    if request is None:
        q.add_aggs()
    else:
        #TODO
        if "aggs" not in request:
            q.add_aggs()
        if "searchString" in request:
            q.add_search_string(request.get("searchString"))
    return client.search(body=q.query)


def count():
    return client.count()


