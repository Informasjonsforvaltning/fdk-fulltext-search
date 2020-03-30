from enum import Enum

from src.search.query_utils import simple_query_string, constant_simple_query


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AllIndicesQuery:
    default_aggs = {
        "los": {
            "terms": {
                "field": "losTheme.losPaths.keyword",
                "size": 1000000000
            }
        },
        "orgPath": {
            "terms": {
                "field": "publisher.orgPath",
                "missing": "MISSING",
                "size": 1000000000
            }
        },
        "isOpenAccess": {
            "terms": {
                "field": "isOpenAccess",
                "size": 3
            }
        },
        "accessRights": {
            "terms": {
                "field": "accessRights.code.keyword",
                "size": 10
            }
        }
    }
    query_template = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "constant_score": {
                            "filter": {
                                "bool": {
                                    "should": [
                                        {
                                            "match": {
                                                "provenance.code": "NASJONAL"
                                            }
                                        },
                                        {
                                            "term": {
                                                "nationalComponent": "true"
                                            }
                                        }
                                    ]
                                }
                            },
                            "boost": 1.2
                        }
                    },
                    {
                        "match_all": {}
                    }

                ]
            }
        }
    }

    def __init__(self, searchString=None, aggs=None):
        self.query = self.query_template
        if searchString:
            self.add_search_string(searchString)
        if aggs is None:
            self.add_aggs()

    def add_page(self, size=None, start=None) -> dict:
        if size is not None:
            self.query['size'] = size
        if start is not None:
            self.query['from'] = start

    def add_aggs(self, fields=None):
        if fields is None:
            self.query["aggs"] = self.default_aggs
        # TODO: self defined aggs

    def add_search_string(self, param):
        self.query["query"]["dis_max"]["queries"][0] = constant_simple_query(param)
        self.query["query"]["dis_max"]["queries"][1] = simple_query_string(search_string=param, boost=0.1)


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
