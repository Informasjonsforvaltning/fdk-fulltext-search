from typing import Any, Dict, Optional, Union

from elasticsearch.exceptions import ConnectionError

from .queries import (
    AllIndicesQuery,
    ConceptQuery,
    DataServiceQuery,
    DataSetQuery,
    EventQuery,
    InformationModelQuery,
    PublicServiceQuery,
    PublicServicesAndEventsQuery,
    RecentQuery,
    SuggestionQuery,
)
from ..ingest import es_client, IndicesKey

query_builder = {
    IndicesKey.INFO_MODEL: InformationModelQuery,
    IndicesKey.DATA_SETS: DataSetQuery,
    IndicesKey.DATA_SERVICES: DataServiceQuery,
    IndicesKey.CONCEPTS: ConceptQuery,
    IndicesKey.PUBLIC_SERVICES: PublicServiceQuery,
    IndicesKey.EVENTS: EventQuery,
}


def search_all(request: Optional[Dict] = None) -> Dict[str, Union[int, str]]:
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
        return es_client.search(
            index=IndicesKey.SEARCHABLE_ALIAS,
            body=q.body,
        )

    except ConnectionError:
        return {
            "count": -1,
            "operation": "search",
            "error": "could not connect to elasticsearch",
        }


def search_in_index(index: str, request: Optional[Dict] = None) -> Dict:
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
        q = query_builder[index](search_string=search_str, aggs=aggs, filters=f)  # type: ignore
        if size or page:
            q.add_page(size=size, page=page)
        if sorting:
            q.add_sorting(sorting)
        return es_client.search(index=index, body=q.body)
    except ConnectionError:
        return {
            "count": -1,
            "operation": "search",
            "index": index,
            "error": "could not connect to elasticsearch",
        }


def search_public_services_and_events(
    request: Optional[Dict] = None,
) -> Dict[str, Union[int, str]]:
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
        q = PublicServicesAndEventsQuery(search_string=search_str, aggs=aggs, filters=f)
        if size or page:
            q.add_page(size=size, page=page)
        if sorting:
            q.add_sorting(sorting)
        return es_client.search(
            index=IndicesKey.PUBLIC_SERVICES_AND_EVENTS_ALIAS,
            body=q.body,
        )

    except ConnectionError:
        return {
            "count": -1,
            "operation": "search",
            "error": "could not connect to elasticsearch",
        }


def count(index: Optional[str] = None) -> Dict[str, Union[int, str]]:
    try:
        if index:
            return es_client.count(index=index)
        else:
            return es_client.count()

    except ConnectionError:
        return {
            "count": -1,
            "operation": "count",
            "error": "could not connect to elasticsearch",
        }


def get_recent(size: Optional[int] = None) -> Any:
    q = RecentQuery(size).query
    return es_client.search(index=IndicesKey.SEARCHABLE_ALIAS, body=q)


def get_indices(index_name: Optional[str] = None) -> Any:
    req_body: Dict[str, Dict] = {"query": {}}
    if index_name:
        req_body["query"]["term"] = {"name": index_name}
    else:
        req_body["query"] = {"match_all": {}}
    if es_client.indices.exists(index=IndicesKey.INDICES_INFO):
        return es_client.search(index=IndicesKey.INDICES_INFO, body=req_body)
    else:
        return None


def get_suggestions(
    search_string: str,
    index_key: str = IndicesKey.DATA_SETS,
    is_transport: bool = False,
    publisher_id: Optional[str] = None,
) -> Any:
    query = SuggestionQuery(
        indices=[index_key],
        search_string=search_string,
        is_transport=is_transport,
        publisher_id=publisher_id,
    )
    return es_client.search(index=index_key, body=query.body)


def get_suggestions_all_indices(search_string: str, is_transport: bool = False) -> Any:
    query = SuggestionQuery(
        indices=[
            IndicesKey.DATA_SETS,
            IndicesKey.CONCEPTS,
            IndicesKey.DATA_SERVICES,
            IndicesKey.INFO_MODEL,
        ],
        search_string=search_string,
        is_transport=is_transport,
    )
    return es_client.search(index=IndicesKey.SEARCHABLE_ALIAS, body=query.body)
