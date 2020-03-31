import json

from .queries import *
from ..ingest import client


def search_all(request: dict = None):
    aggs = None
    search_str = None
    f = None
    if request:
        if "aggregations" in request:
            aggs = request.get("aggregations")
        if "q" in request:
            search_str = request.get("q")
        if "filters" in request:
            f = request.get("filters")
    q = AllIndicesQuery(search_string=search_str, aggs=aggs, filters=f)
    return client.search(body=q.query, search_type='dfs_query_then_fetch')


def count():
    return client.count()


def get_recent(size=None):
    q = RecentQuery(size).query
    return client.search(body=q)
