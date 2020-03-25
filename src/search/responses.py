from math import ceil


class SearchResponse:
    response: dict = {
        "hits": {},
        "page": {},
        "aggregations": {}
    }

    def map_response(self, es_result, size=10, requested_page=0):
        self.map_page(es_result["hits"], size, requested_page)
        self.map_aggregations(es_result["aggregations"])
        self.map_hits(es_result["hits"]["hits"])
        return self.response

    def map_page(self, es_hits, size, requested_page):
        total = es_hits["total"]["value"]
        total_pages = ceil(float(total) / float(size))
        page = {
            "size": size,
            "totalElements": total,
            "totalPages": total_pages,
            "currentPage": requested_page
        }
        self.response["page"] = page

    def map_aggregations(self, aggregations_result):
        self.response["aggregations"] = aggregations_result

    def map_hits(self, hits_result):
        hits = []
        for item in hits_result:
            hits.append(self.map_hit_item(item))

        self.response["hits"] = hits

    def map_hit_item(self, item):
        mapped_item = item["_source"]
        mapped_item["type"] = item["_index"].rstrip('s')
        return mapped_item
