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

def add_size(query: dict, size: int) -> dict:
    if size is not None:
        query['size'] = size
    return query
