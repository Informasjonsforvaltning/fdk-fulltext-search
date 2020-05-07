from math import ceil

from src.search.client import count


class SearchResponse:
    response: dict = {
        "hits": {},
        "page": {},
        "aggregations": {}
    }

    def map_response(self, es_result, requested_page=0):
        size = len(es_result["hits"]["hits"])
        self.map_page(es_result["hits"], size, requested_page)
        if "aggregations" in es_result.keys():
            self.map_aggregations(es_result["aggregations"])
        self.map_hits(es_result["hits"]["hits"])
        return self.response

    def map_page(self, es_hits, size, requested_page):
        total = es_hits["total"]["value"]
        if total > 0:
            total_pages = ceil(float(total) / float(size))
        else:
            total_pages = 0
        page = {
            "size": size,
            "totalElements": total,
            "totalPages": total_pages,
            "currentPage": requested_page
        }
        self.response["page"] = page

    def map_aggregations(self, aggregations_result):
        response_aggregations = {}
        for agg_key in aggregations_result.keys():
            if agg_key == "dataset_access":
                response_aggregations["accessRights"] = aggregations_result["dataset_access"]["accessRights"]
            else:
                response_aggregations[agg_key] = aggregations_result[agg_key]
        self.response["aggregations"] = response_aggregations

    def map_hits(self, hits_result):
        hits = []
        for item in hits_result:
            hits.append(self.map_hit_item(item))

        self.response["hits"] = hits

    def map_hit_item(self, item):
        mapped_item = item["_source"]
        mapped_item["type"] = item["_index"].rstrip('s')
        return mapped_item


class IndicesInfoResponse:
    def __init__(self, es_result):
        self.es_result = es_result["hits"]["hits"]

    def map_response(self):
        response = []
        for hit in self.es_result:
            source = hit["_source"]
            doc_count = count(index=hit["_source"]["name"])
            source["count"] = doc_count["count"]
            response.append(source)
        return response
