from enum import Enum

from src.search.query_utils import get_filter, must_not_query, query_template, default_dismax, default_aggs, \
    exact_match_in_title_query, word_in_title_query, word_in_description_query, simple_query_string


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AllIndicesQuery:

    def __init__(self, search_string=None, aggs=None, filters=None):
        self.query = query_template()
        if search_string:
            self.dismax = {"dis_max": {
                "queries": []
            }}
            self.add_search_string(search_string)
        else:
            self.dismax = default_dismax()
        if aggs is None:
            self.add_aggs()
        if filters:
            self.query["query"] = {
                "bool":
                    {
                        "must": [
                            self.dismax
                        ]
                    }
            }
            self.add_filters(filters)
        else:
            self.query["query"] = self.dismax

    def add_page(self, size=10, page=None) -> dict:
        if size is None:
            size = 10
            self.query['size'] = size
        if page is not None:
            self.query['from'] = page * size

    def add_aggs(self, fields=None):
        if fields is None:
            self.query["aggs"] = default_aggs()
        # TODO: self defined aggs

    def add_search_string(self, param: str):
        self.dismax["dis_max"]["queries"].append(exact_match_in_title_query(
            title_field_names=["prefLabel.*", "title.*", "title"],
            search_string=param))
        self.dismax["dis_max"]["queries"].append(
            word_in_title_query(title_field_names=["title.*", "title", "prefLabel.*"],
                                search_string=param))
        self.dismax["dis_max"]["queries"].append(
            word_in_description_query(description_field_names=["description", "definition.text.*", "schema"],
                                      search_string=param))
        self.dismax["dis_max"]["queries"].append(simple_query_string(search_string=param))

    def add_filters(self, filters):
        self.query["query"]["bool"]["filter"] = []
        for f in filters:
            key = list(f.keys())[0]
            if (f[key]) == 'MISSING':
                self.query["query"]["bool"]["filter"].append(must_not_query(key))
            else:
                self.query["query"]["bool"]["filter"].append({"term": get_filter(f)})

    def add_sorting(self, param):
        self.query["sort"] = {
            param.get("field"): {
                "order": param.get("direction")
            }
        }


class RecentQuery:
    def __init__(self, size=None):
        self.query = {
            "size": 5,
            "sort": {"harvest.firstHarvested": {
                "order": Direction.DESC.value
            }
            }
        }

        if size is not None:
            self.query["size"] = size
