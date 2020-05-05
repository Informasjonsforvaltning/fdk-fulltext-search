from enum import Enum

from src.search.query_utils import *


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AllIndicesQuery:

    def __init__(self, search_string=None, aggs=None, filters=None):
        if search_string:
            self.body = query_template()
            self.query = {"dis_max": {
                "queries": []
            }}
            self.add_search_string(search_string.strip())
        else:
            self.body = query_template(dataset_boost=1.2)
            self.query = all_indices_default_query()
        if aggs is None:
            self.add_aggs()
        if filters:
            self.body["query"] = {
                "bool":
                    {
                        "must": [
                            self.query
                        ]
                    }
            }
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_page(self, size=10, page=None) -> dict:
        if size is None:
            size = 10
        self.body['size'] = size
        if page is not None:
            self.body['from'] = page * size

    def add_aggs(self, fields=None):
        if fields is None:
            self.body["aggs"] = default_aggs()

    def add_search_string(self, param: str):
        self.query["dis_max"]["queries"].append(exact_match_in_title_query(
            title_field_names=["prefLabel.*", "title.*", "title"],
            search_string=param))
        self.query["dis_max"]["queries"].append(
            word_in_title_query(title_field_names=["title.*", "title", "prefLabel.*"],
                                search_string=param))
        self.query["dis_max"]["queries"].append(
            word_in_description_query(
                description_field_names_with_boost=["description", "definition.text.*", "schema^0.5"],
                search_string=param))
        some_words_in_title = some_words_in_title_query(title_fields_list=["title.*", "title", "prefLabel.*"],
                                                        search_string=param)
        if some_words_in_title:
            self.query["dis_max"]["queries"].append(some_words_in_title)

        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param, boost=0.0015))
        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param, boost=0.001, lenient=True))

    def add_filters(self, filters):
        self.body["query"]["bool"]["filter"] = []
        for f in filters:
            key = list(f.keys())[0]
            if (f[key]) == 'MISSING' or (f[key]) == 'Ukjent':
                self.body["query"]["bool"]["filter"].append(must_not_filter(key))
            elif key == 'opendata':
                self.body["query"]["bool"]["filter"].append(open_data_filter())
            else:
                self.body["query"]["bool"]["filter"].extend(get_term_filter(f))

    def add_sorting(self, param):
        self.body["sort"] = {
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
