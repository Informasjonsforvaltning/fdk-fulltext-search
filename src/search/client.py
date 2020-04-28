import json

from .queries import *
from ..ingest import client
from elasticsearch.exceptions import ConnectionError


def search_all(request: dict = None):
    try:
        aggs = None
        search_str = None
        f = None
        size = None
        page = None
        sorting = None
        if request:
            if "aggregations" in request:
                aggs = request.get("aggregations")
            if "q" in request:
                search_str = request.get("q")
            if "filters" in request:
                f = request.get("filters")
            if "page" in request:
                page = request.get("page")
            if "size" in request:
                size = request.get("size")
            if "sorting" in request:
                sorting = request.get("sorting")
        q = AllIndicesQuery(search_string=search_str, aggs=aggs, filters=f)
        if size or page:
            q.add_page(size=size, page=page)
        if sorting:
            q.add_sorting(sorting)
        print(json.dumps(q.body))
        return client.search(body=q.body, search_type='dfs_query_then_fetch')
    except ConnectionError:
        return {
            "count": -1,
            "operation": "search",
            "error": "could not connect to elasticsearch"
        }


def count():
    try:
        return client.count()

    except ConnectionError:
        return {
            "count": -1,
            "operation": "count",
            "error": "could not connect to elasticsearch"
        }


def get_recent(size=None):
    q = RecentQuery(size).query
    print(json.dumps(q))
    return client.search(body=q)
