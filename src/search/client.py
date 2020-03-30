from .queries import *
from ..ingest import client



def search_all(request: dict = None):
    q = AllIndicesQuery()
    if request is None:
        q.add_aggs()
    else:
        # TODO
        if "aggs" not in request:
            q.add_aggs()
        if "q" in request:
            q.add_search_string(request.get("q"))
    return client.search(body=q.query, search_type='dfs_query_then_fetch')


def count():
    return client.count()


def get_recent(size=None):
    q = RecentQuery(size).query
    return client.search(body=q)
