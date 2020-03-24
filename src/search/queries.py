all_indices_aggs = {
    "los": {
        "terms": {
            "field": "expandedLosTema.keyword"
        }
    },
    "orgPath": {
        "terms": {
            "field": "publisher.orgPath.keyword"
        }
    },
    "isOpenAccess": {
        "terms": {
            "field": "isOpenAccess"
        }
    },
    "accessRights": {
        "terms": {
            "field": "accessRights.code.keyword"
        }
    }
}

all_indices = {
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


def add_page(query: dict, size=None, start=None) -> dict:
    if size is not None:
        query['size'] = size
    if start is not None:
        query['from'] = start
    return query


def add_aggregation(query: dict, fields=None):
    if fields is None:
        query["aggs"] = all_indices_aggs
    else:
        # TODO
        query["aggs"] = {}
    return query
