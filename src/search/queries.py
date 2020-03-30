# noinspection PyTypeChecker
import os
from enum import Enum


def simple_query_string(search_string: str):
    return {
        "simple_query_string": {
            "query": "{0} {0}*".format(search_string),
            "boost": 0.5,
            "default_operator": "or"
        }
    }


class Direction(Enum):
    ASC = "asc"
    DESC = "desc"


class AllIndicesQuery:
    default_aggs = {
        "los": {
            "terms": {
                "field": "expandedLosTema.keyword"
            }
        },
        "orgPath": {
            "terms": {
                "field": "publisher.orgPath",
                "missing": "MISSING",
                "size": 100000000
            }
        },
        "isOpenAccess": {
            "terms": {
                "field": "isOpenAccess",
                "size": 100000000
            }
        },
        "accessRights": {
            "terms": {
                "field": "accessRights.code.keyword",
                "size": 100000000
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

    def __init__(self):
        self.query = self.query_template

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
        self.query["query"]["dis_max"]["queries"][1] = simple_query_string(param)


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
