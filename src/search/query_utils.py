def simple_query_string(search_string: str, boost=0.5):
    return {
        "simple_query_string": {
            "query": "{0} {0}*".format(search_string),
            "boost": boost,
            "default_operator": "or"
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
