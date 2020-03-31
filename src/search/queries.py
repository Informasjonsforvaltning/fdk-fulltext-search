from enum import Enum

from src.search.query_utils import simple_query_string, constant_simple_query, get_filter, get_filter_key, \
    must_not_query, query_template, default_dismax, default_aggs


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AllIndicesQuery:

    def __init__(self, search_string=None, aggs=None, filters=None):
        self.query = query_template()
        self.dismax = default_dismax()
        if search_string:
            self.add_search_string(search_string)
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
        print(size)
        print(page)
        if size is not None:
            self.query['size'] = size
        if page is not None:
            self.query['from'] = page

    def add_aggs(self, fields=None):
        if fields is None:
            self.query["aggs"] = default_aggs()
        # TODO: self defined aggs

    def add_search_string(self, param):
        self.dismax["dis_max"]["queries"][0] = constant_simple_query(param)
        self.dismax["dis_max"]["queries"][1] = simple_query_string(search_string=param, boost=0.01)

    def add_filters(self, filters):
        self.query["query"]["bool"]["filter"] = []
        for f in filters:
            key = list(f.keys())[0]
            if (f[key]) == 'MISSING':
                self.query["query"]["bool"]["filter"].append(must_not_query(key))
            else:
                self.query["query"]["bool"]["filter"].append({"term": get_filter(f)})


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
