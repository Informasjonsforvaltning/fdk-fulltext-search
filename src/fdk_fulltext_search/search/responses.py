from math import ceil
from typing import Any, Dict, List, Optional

from fdk_fulltext_search.search.client import count


class SearchResponse:
    response: dict = {"hits": {}, "page": {}, "aggregations": {}}

    def map_response(self: Any, es_result: Dict, requested_page: int = 0) -> Dict:
        self.map_page(es_result["hits"], requested_page)
        if "aggregations" in es_result.keys():
            self.map_aggregations(es_result["aggregations"])
        self.map_hits(es_result["hits"]["hits"])
        return self.response

    def map_page(self: Any, es_hits: Dict, requested_page: int) -> None:
        size = len(es_hits["hits"])
        total = es_hits["total"]["value"]
        hits_per_page = max(size, 10)
        total_pages = ceil(float(total) / float(hits_per_page))

        self.response["page"] = {
            "size": size,
            "totalElements": total,
            "totalPages": total_pages,
            "currentPage": requested_page,
        }

    def map_aggregations(self: Any, aggregations_result: Dict) -> None:
        response_aggregations = {}
        for agg_key in aggregations_result.keys():
            if agg_key == "dataset_access":
                response_aggregations["accessRights"] = aggregations_result[
                    "dataset_access"
                ]["accessRights"]
            else:
                response_aggregations[agg_key] = aggregations_result[agg_key]
        self.response["aggregations"] = response_aggregations

    def map_hits(self: Any, hits_result: List) -> None:
        hits = []
        for item in hits_result:
            hits.append(self.map_hit_item(item))

        self.response["hits"] = hits

    def map_hit_item(self: Any, item: Dict) -> Dict:
        mapped_item = item["_source"]
        mapped_item["type"] = item["_index"].split("-")[0].rstrip("s")
        return mapped_item


class IndicesInfoResponse:
    def __init__(self: Any, es_result: Dict) -> None:
        self.es_result = es_result["hits"]["hits"]

    def map_response(self: Any) -> List:
        response = []
        for hit in self.es_result:
            source = hit["_source"]
            doc_count = count(index=hit["_source"]["name"])
            source["count"] = doc_count["count"]
            response.append(source)
        return response


class SuggestionResponse:
    def __init__(self: Any, es_result: Dict) -> None:
        self.es_result = es_result["hits"]["hits"]

    def map_response(self: Any, language: Optional[Any] = None) -> Dict:
        if language:
            return {}
        else:
            suggestion_objects = []
            for hits in self.es_result:
                suggestion_objects.append(hits["_source"])
            return {"suggestions": suggestion_objects}

    @classmethod
    def empty_response(cls: Any) -> Dict[str, Dict]:
        return {"suggestion": {}}
