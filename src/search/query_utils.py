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
                        "filter": simple_query_string(search_string = search_string, boost=1),
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
