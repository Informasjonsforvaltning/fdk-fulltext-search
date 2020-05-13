import json

from .queries import *
from ..ingest import es_client, IndicesKey
from elasticsearch.exceptions import ConnectionError

query_builder = {
    'informationmodels': InformationModelQuery
}


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
        return es_client.search(body=q.body, search_type='dfs_query_then_fetch')

    except ConnectionError:
        return {
            "count": -1,
            "operation": "search",
            "error": "could not connect to elasticsearch"
        }


def search_in_index(index: str, request: dict = None):
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
        q = query_builder[index](search_string=search_str, aggs=aggs, filters=f)
        if size or page:
            q.add_page(size=size, page=page)
        if sorting:
            q.add_sorting(sorting)
        print(json.dumps(q.body))
        return es_client.search(index=index, body=q.body)
    except ConnectionError:
        return {
            "count": -1,
            "operation": "search",
            "index": index,
            "error": "could not connect to elasticsearch"
        }


def count(index=None):
    try:
        if index:
            return es_client.count(index=index)
        else:
            return es_client.count()

    except ConnectionError:
        return {
            "count": -1,
            "operation": "count",
            "error": "could not connect to elasticsearch"
        }


def get_recent(size=None):
    q = RecentQuery(size).query
    print(json.dumps(q))
    return es_client.search(body=q)


def get_indices(index_name=None):
    req_body = {"query": {}}
    if index_name:
        req_body["query"]["term"] = {
            "name": index_name
        }
    else:
        req_body["query"] = {
            "match_all": {}
        }
    if es_client.indices.exists(index=IndicesKey.INDICES_INFO):
        return es_client.search(index=IndicesKey.INDICES_INFO, body=req_body)
    else:
        return None


def get_suggestions(query, indices=None):
    return None
