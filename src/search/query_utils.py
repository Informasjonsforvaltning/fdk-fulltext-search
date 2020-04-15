def title_term_query(field, search_string):
    return {
        "term": {
            field: search_string
        }
    }


def autorativ_boost_clause():
    return {
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
    }


def simple_query_string(search_string: str, boost=0.001):
    query_string = search_string.replace(" ", "+")
    return {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "{0} {0}*".format(query_string),
                }
            },
            "should": [autorativ_boost_clause()],
            "boost": boost
        }
    }


def exact_match_in_title_query(title_field_names: list, search_string: str):
    fields_list = []
    for field in title_field_names:
        fields_list.append(field + ".raw")
    return {
        "bool": {
            "must": {
                "multi_match": {
                    "query": search_string,
                    "fields": fields_list
                }
            },
            "should": [autorativ_boost_clause()],
            "boost": 5

        }
    }


def word_in_title_query(title_field_names: list, search_string: str):
    fields_list = []
    for field in title_field_names:
        fields_list.append(field + ".ngrams")
        fields_list.append(field + ".ngrams.2_gram")
        fields_list.append(field + ".ngrams.3_gram")
    return {
        "bool": {
            "must": {
                "multi_match": {
                    "query": search_string,
                    "type": "phrase_prefix",
                    "fields": fields_list
                }
            },
            "should": [autorativ_boost_clause()],
            "boost": 2
        }
    }


def word_in_description_query(description_field_names: list, search_string: str):
    query_string = search_string.replace(" ", "+")
    return {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "{0} {0}*".format(query_string),
                    "fields": description_field_names
                }
            },
            "should": [autorativ_boost_clause()],
            "boost": 1.5
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
        "availability": {
            "filters": {
                "filters": {
                    "isOpenAccess": {
                        "term": {
                            "isOpenAccess": "true"
                        }
                    },
                    "isOpenLicense": {
                        "term": {
                            "isOpenLicense": "true"
                        }
                    },
                    "isFree": {
                        "term": {
                            "isFree": "true"
                        }
                    }
                }
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
        "query": {
        }
    }
