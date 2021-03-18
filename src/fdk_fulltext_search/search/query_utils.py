import re


def autorativ_data_service_query() -> dict:
    return {"term": {"nationalComponent": "true"}}


def autorativ_dataset_query() -> dict:
    return {"match": {"provenance.code": "NASJONAL"}}


def open_data_query():
    return {
        "bool": {
            "must": [
                {"term": {"accessRights.code.keyword": "PUBLIC"}},
                {"term": {"distribution.openLicense": "true"}},
            ]
        }
    }


def default_query():
    return {
        "bool": {
            "must": {"match_all": {}},
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
        }
    }


def title_exact_match_query(fields: list, search_string: str):
    return {
        "bool": {
            "must": {
                "multi_match": {
                    "query": search_string,
                    "fields": list(map(lambda field: f"{field}.raw", fields)),
                }
            },
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
            "boost": 20,
        }
    }


def title_query(fields: list, search_string: str):
    dismax_queries = []
    for field in fields:
        title_match_query = {
            "multi_match": {
                "query": search_string,
                "type": "bool_prefix",
                "fields": [
                    f"{field}.ngrams",
                    f"{field}.ngrams.2_gram",
                    f"{field}.ngrams.3_gram",
                ],
            }
        }
        dismax_queries.append(title_match_query)

    words_only = words_only_string(search_string)
    if words_only:
        dismax_queries.append(
            {
                "query_string": {
                    "query": get_catch_all_query_string(words_only),
                    "fields": list(map(lambda field: f"{field}.raw", fields)),
                }
            }
        )

    return {
        "bool": {
            "must": {"dis_max": {"queries": dismax_queries}},
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
            "boost": 10,
        }
    }


def title_suggestion_query(fields: list, search_string: str) -> dict:
    query_list = []
    for field in fields:
        fields_list = [
            field + ".ngrams",
            field + ".ngrams.2_gram",
            field + ".ngrams.3_gram",
        ]
        query_list.append(
            {
                "multi_match": {
                    "query": search_string,
                    "type": "bool_prefix",
                    "fields": fields_list,
                }
            }
        )
    return {"dis_max": {"queries": query_list}}


def description_query(fields: list, search_string: str) -> dict:
    query_string = search_string.replace(" ", "+")
    return {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "{0} {0}*".format(query_string),
                    "fields": fields,
                }
            },
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
        }
    }


def organization_query(search_str: str) -> dict:
    return {
        "bool": {
            "must": {
                "multi_match": {
                    "query": search_str,
                    "fields": [
                        "publisher.prefLabel.*",
                        "publisher.title.*",
                        "hasCompetentAuthority.prefLabel.*",
                        "hasCompetentAuthority.name.*",
                    ],
                }
            },
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
            "boost": 10,
        }
    }


def simple_query_string(
    search_string: str,
    fields=None,
) -> dict:
    words_only = words_only_string(search_string)
    final_search_string = words_only or search_string

    simple_query = {
        "simple_query_string": {
            "query": "{0} {0}*".format(final_search_string.replace(" ", "+"))
        }
    }

    if fields:
        simple_query["simple_query_string"]["fields"] = fields

    return {
        "bool": {
            "must": simple_query,
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
            "boost": 0.02,
        }
    }


def query_string(
    search_string: str,
    fields=None,
) -> dict:
    words_only = words_only_string(search_string)
    final_search_string = words_only or search_string

    query = {"query_string": {"query": get_catch_all_query_string(final_search_string)}}
    if fields:
        query["query_string"]["fields"] = fields

    return {
        "bool": {
            "must": query,
            "should": [
                autorativ_dataset_query(),
                autorativ_data_service_query(),
                open_data_query(),
            ],
            "boost": 0.001,
        }
    }


def get_catch_all_query_string(original_string) -> str:
    new_string_list = []
    for word in original_string.split():
        new_string_list.append("*{0}* ".format(word))
    return "".join(new_string_list).strip()


def query_with_filter_template(must_clause: list) -> dict:
    return {"bool": {"must": must_clause, "filter": []}}


def query_template():
    template = {"query": {}, "aggs": {}}
    return template


def dismax_template():
    return {"dis_max": {"queries": []}}


def words_only_string(query_string: str):
    """ Returns a string with words only, where words are defined as any sequence of digits or letters """
    words = re.findall(r"\w+", query_string)
    if words.__len__() > 0:
        return " ".join(words)

    return None
