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
    fields_list = []
    for field in fields:
        fields_list.append(field + ".raw")
    return {
        "bool": {
            "must": {"multi_match": {"query": search_string, "fields": fields_list}},
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

    sanitized_string = words_only_string(search_string)
    if sanitized_string:
        dismax_queries.append(
            {
                "simple_query_string": {
                    "query": sanitized_string,
                    "fields": fields,
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
    boost=0.001,
    lenient=False,
    fields=None,
) -> dict:
    replace_special_chars = words_only_string(search_string)
    final_string = replace_special_chars or search_string

    query_string = (
        get_catch_all_query_string(final_string)
        if lenient
        else "{0} {0}*".format(final_string.replace(" ", "+"))
    )
    simple_query = {"simple_query_string": {"query": query_string}}
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
            "boost": boost,
        }
    }


def get_catch_all_query_string(original_string) -> str:
    new_string_list = []
    for word in original_string.split():
        new_string_list.append("*{0} ".format(word))
        new_string_list.append("{0} ".format(word))
        new_string_list.append("{0}* ".format(word))
    return "".join(new_string_list).strip()


def query_with_filter_template(must_clause: list) -> dict:
    return {"bool": {"must": must_clause, "filter": []}}


def query_template():
    template = {"query": {}, "aggs": {}}
    return template


def dismax_template():
    return {"dis_max": {"queries": []}}


def words_only_string(query_string):
    """ Returns a string with words only, where words are defined as any sequence of digits or letters """
    non_words = re.findall(r"[^a-z@øåA-ZÆØÅ\d]", query_string)
    if non_words.__len__() > 0:
        words = re.findall(r"\w+", query_string)
        if words.__len__() > 0:
            return " ".join(words)

    return None
