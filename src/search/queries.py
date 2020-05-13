import abc
from enum import Enum

from src.search.query_utils import *


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AbstractSearchQuery(metaclass=abc.ABCMeta):

    def __init__(self, search_string: str = None):
        self.body = query_template()
        if search_string:
            self.query = dismax_template()

    def add_page(self, size: int = 10, page: int = None) -> dict:
        if size is None:
            size = 10
        self.body['size'] = size
        if page is not None:
            self.body['from'] = page * size

    def add_filters(self, filters: list):
        self.body["query"]["bool"]["filter"] = []
        for f in filters:
            key = list(f.keys())[0]
            if (f[key]) == 'MISSING' or (f[key]) == 'Ukjent':
                self.body["query"]["bool"]["filter"].append(must_not_filter(key))
            elif key == 'opendata':
                self.body["query"]["bool"]["filter"].append(open_data_query())
            else:
                self.body["query"]["bool"]["filter"].extend(get_term_filter(f))
        # TODO implement user defined filters?

    def add_sorting(self, param: dict):
        self.body["sort"] = {
            param.get("field"): {
                "order": param.get("direction")
            }
        }

    @abc.abstractmethod
    def add_aggs(self, fields: list):
        pass

    @abc.abstractmethod
    def add_search_string(self, search_string: str):
        pass


class AllIndicesQuery(AbstractSearchQuery):

    def __init__(self, search_string=None, aggs=None, filters=None):
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string.strip())
        else:
            self.body["indices_boost"] = [{"datasets": 1.2}]
            self.query = all_indices_default_query()
        if aggs is None:
            self.add_aggs()
        if filters:
            self.body["query"] = query_with_filter_template(must_clause=[self.query])
            self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_aggs(self, fields=None):
        # TODO user defined aggs
        if fields is None:
            self.body["aggs"] = default_all_indices_aggs()

    def add_search_string(self, param: str):
        self.query["dis_max"]["queries"].append(exact_match_in_title_query(
            title_field_names=["prefLabel.*", "title.*", "title"],
            search_string=param))
        self.query["dis_max"]["queries"].append(
            word_in_title_query(title_field_names=["title.*", "title", "prefLabel.*"],
                                search_string=param))
        self.query["dis_max"]["queries"].append(
            word_in_description_query(
                index_key=IndicesKey.ALL,
                search_string=param))
        some_words_in_title = some_words_in_title_query(title_fields_list=["title.*", "title", "prefLabel.*"],
                                                        search_string=param)
        if some_words_in_title:
            self.query["dis_max"]["queries"].append(some_words_in_title)

        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param, boost=0.0015))
        self.query["dis_max"]["queries"].append(simple_query_string(search_string=param, boost=0.001, lenient=True))

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
                "order": Direction.DESC.value}
            }
        }

        if size is not None:
            self.query["size"] = size


class InformationModelQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = information_model_default_query()
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_filter_template(must_clause=[self.query])
                self.add_filters(filters)
        else:
            self.body["query"] = self.query

    def add_search_string(self, search_string: str):
        dismax_queries = [index_match_in_title_query(index_key=IndicesKey.INFO_MODEL,
                                                     search_string=search_string),
                          word_in_description_query(index_key=IndicesKey.INFO_MODEL,
                                                    search_string=search_string,
                                                    autorativ_boost=False),
                          simple_query_string(search_string=search_string,
                                              autorativ_boost=False,
                                              boost=0.02),
                          simple_query_string(search_string=search_string,
                                              autorativ_boost=False,
                                              lenient=True)]
        self.query["dis_max"]["queries"] = dismax_queries

    def add_aggs(self, fields: list):
        if fields is None:
            self.body["aggs"]["los"] = los_aggregation()
            self.body["aggs"]["orgPath"] = org_path_aggregation()
        # TODO implement user defined aggregations?


class DataSettQuery(AbstractSearchQuery):

    def __init__(self, search_string: str = None, aggs: list = None, filters: list = None):
        super().__init__(search_string)
        if search_string:
            self.add_search_string(search_string)
        else:
            self.query = information_model_default_query()
        self.add_aggs(aggs)
        if filters:
            if filters:
                self.body["query"] = query_with_filter_template(must_clause=[self.query])
                self.add_filters(filters)
        else:
            self.body["query"] = self.query

        def add_aggs(self, fields: list):
            pass

        def add_search_string(self, search_string: str):
            pass
