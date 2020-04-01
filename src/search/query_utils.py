def simple_query_string(search_string: str, boost=0.5):
    return {
        "simple_query_string": {
            "query": "{0} {0}*".format(search_string),
            "boost": boost,
            "default_operator": "or"
        }
    }

def title_term_query(field, search_string):
    return {
        "term": {
            field: search_string
        }
    }


def constant_simple_query(search_string: str):
    return {
        "bool": {
            "must": [
                {
                    "constant_score": {
                        "filter": simple_query_string(search_string=search_string, boost=1),
                        "boost": 1.2
                    }
                }
            ],
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
    }


def get_filter(filter_object):
    key = list(filter_object.keys())[0]
    return {get_filter_key(key): filter_object[key]}


def get_filter_key(filter_key):
    if filter_key == "orgPath":
        return "publisher.orgPath"
    elif filter_key == "accessRights":
        return "accessRights.code.keyword"
    elif filter_key == "los":
        return "losTheme.losPaths.keyword"
    else:
        return filter_key


def must_not_query(filter_key):
    return {
        "bool": {
            "must_not":
                {
                    "exists": {
                        "field": get_filter_key(filter_key)
                    }
                }
        }
    }


def default_aggs():
    return {
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


def default_dismax():
    return {"dis_max": {
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
    }}


def query_template():
    return {
        "indices_boost": {
            "datasets": 1.2
        },
        "query": {
        }
    }
