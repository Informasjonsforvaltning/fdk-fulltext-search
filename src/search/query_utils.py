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


def word_in_description_query(description_field_names_with_boost: list, search_string: str):
    query_string = search_string.replace(" ", "+")
    return {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "{0} {0}*".format(query_string),
                    "fields": description_field_names_with_boost
                }
            },
            "should": [autorativ_boost_clause()],
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


def get_term_filter(request_item):
    """ map request filter for one key to ES term queries"""
    filters = []
    key = list(request_item.keys())[0]
    # get all values in request filter
    terms = request_item[key].split(',')
    for term in terms:
        q = {"term": {get_filter_key(key): term}}
        filters.append(q)
    return filters


def open_data_filter():
    return {
        "bool": {
            "must": [
                {
                    "term": {
                        "accessRights.code.keyword": "PUBLIC"
                    }
                },
                {
                    "term": {
                        "distribution.openLicense": "true"
                    }
                }
            ]
        }
    }


def get_filter_key(filter_key: str):
    """ Map the request filter key to keys in the elasticsearch mapping"""
    if filter_key == "orgPath":
        return "publisher.orgPath"
    elif filter_key == "accessRights":
        return "accessRights.code.keyword"
    elif filter_key == "los":
        return "losTheme.losPaths.keyword"
    else:
        return filter_key


def get_filter_index(filter_key):
    """get indexes containing filter_key """
    if filter_key == "accessRights":
        return "datasets"
    else:
        return False


def must_not_filter(filter_key: str):
    missing_filter = {
        "bool": {
            "must_not":
                {
                    "exists": {
                        "field": get_filter_key(filter_key)
                    }
                }
        }
    }
    index = get_filter_index(filter_key)
    if index:
        missing_filter["bool"]["must"] = {"term": {"_index": get_filter_index(filter_key)}}
    return missing_filter


def default_aggs():
    """ Return a dict with default aggregation for all indices search"""
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
        "dataset_access": {
            "filter": {
                "term": {
                    "_index": "datasets"
                }
            },
            "aggs": {
                "accessRights": {
                    "terms": {
                        "field": "accessRights.code.keyword",
                        "missing": "Ukjent",
                        "size": 10
                    }
                }
            }
        },
        "opendata": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "term": {
                                "accessRights.code.keyword": "PUBLIC"
                            }
                        },
                        {
                            "term": {
                                "distribution.openLicense": "true"
                            }
                        }
                    ]
                }
            }
        },
        "theme": {
            "terms": {
                "field": "theme.code.keyword"
            }
        }
    }


def all_indices_default_query():
    return {
        "bool": {
            "must": {
                "match_all": {}
            },
            "should": [
                {
                    "term": {
                        "provenance.code.keyword": {
                            "value": "NASJONAL",
                            "boost": 2
                        }
                    }
                },
                {
                    "term": {
                        "nationalComponent": {
                            "value": "true",
                            "boost": 1
                        }
                    }
                }
            ]
        }
    }


def query_template(dataset_boost=0):
    template = {
        "query": {
        }
    }
    if dataset_boost > 0:
        template["indices_boost"] = [{"datasets": dataset_boost}]
    return template
