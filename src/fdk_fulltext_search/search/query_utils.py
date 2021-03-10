import re

from fdk_fulltext_search.ingest.utils import IndicesKey
from fdk_fulltext_search.search.fields import (
    index_description_fields,
    index_fulltext_fields,
    index_title_fields,
)
from fdk_fulltext_search.search.query_utils_dataset import (
    autorativ_dataset_query,
    open_data_query,
)


def title_term_query(field, search_string):
    return {"term": {field: search_string}}


def index_match_in_title_query(
    index_key: IndicesKey, search_string: str, boost: int = 2
):
    title_fields = index_title_fields[index_key]
    ngram_queries = []

    for field in title_fields:
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
        ngram_queries.append(title_match_query)

    return {"dis_max": {"queries": ngram_queries, "boost": boost}}


def autorativ_boost_clause() -> dict:
    return {
        "bool": {
            "should": [
                autorativ_dataset_query(),
                {"term": {"nationalComponent": "true"}},
            ]
        }
    }


def simple_query_string(
    search_string: str,
    boost=0.001,
    lenient=False,
    all_indices_autorativ_boost=False,
    fields_for_index=None,
) -> dict:
    replace_special_chars = words_only_string(search_string)
    final_string = replace_special_chars or search_string

    query_string = (
        get_catch_all_query_string(final_string)
        if lenient
        else "{0} {0}*".format(final_string.replace(" ", "+"))
    )
    simple_query = {"simple_query_string": {"query": query_string}}
    if fields_for_index:
        simple_query["simple_query_string"]["fields"] = index_fulltext_fields[
            fields_for_index
        ]

    if all_indices_autorativ_boost:
        return {
            "bool": {
                "must": simple_query,
                "should": [autorativ_boost_clause()],
                "boost": boost,
            }
        }
    else:
        simple_query["simple_query_string"]["boost"] = boost
        return simple_query


def get_catch_all_query_string(original_string) -> str:
    new_string_list = []
    for word in original_string.split():
        new_string_list.append("*{0} ".format(word))
        new_string_list.append("{0} ".format(word))
        new_string_list.append("{0}* ".format(word))
    return "".join(new_string_list).strip()


def exact_match_in_title_query(title_field_names: list, search_string: str):
    fields_list = []
    for field in title_field_names:
        fields_list.append(field + ".raw")
    return {
        "bool": {
            "must": {"multi_match": {"query": search_string, "fields": fields_list}},
            "should": [autorativ_boost_clause()],
            "boost": 20,
        }
    }


def word_in_title_query(title_field_names: list, search_string: str):
    fields_list = []
    for field in title_field_names:
        is_single_field_part = len(field.split(".")) == 1
        if is_single_field_part:
            fields_list.append(field + ".nb")
            fields_list.append(field + ".no")
            fields_list.append(field + ".nn")
            fields_list.append(field + ".en")
        fields_list.append(field + ".ngrams")
        fields_list.append(field + ".ngrams.2_gram")
        fields_list.append(field + ".ngrams.3_gram")
    return {
        "bool": {
            "must": {
                "multi_match": {
                    "query": search_string,
                    "type": "phrase_prefix",
                    "fields": fields_list,
                }
            },
            "should": [autorativ_boost_clause()],
            "boost": 2,
        }
    }


def suggestion_title_query(index_key: IndicesKey, search_string: str) -> dict:
    query_list = []
    for field in index_title_fields[index_key]:
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


def match_on_publisher_name_query(search_str: str) -> dict:
    return {
        "bool": {
            "must": {
                "multi_match": {
                    "query": search_str,
                    "fields": ["publisher.prefLabel.*", "publisher.title.*"],
                }
            },
            "should": [
                {
                    "bool": {
                        "should": [
                            {"match": {"provenance.code": "NASJONAL"}},
                            {"term": {"nationalComponent": "true"}},
                        ]
                    }
                }
            ],
            "boost": 10,
        }
    }


def word_in_description_query(
    index_key: IndicesKey, search_string: str, autorativ_boost=True
) -> dict:
    query_string = search_string.replace(" ", "+")
    if autorativ_boost:
        return {
            "bool": {
                "must": simple_query_string_for_description(index_key, query_string),
                "should": [autorativ_boost_clause()],
            }
        }
    else:
        return simple_query_string_for_description(index_key, query_string)


def simple_query_string_for_description(index_key: IndicesKey, search_string) -> dict:
    return {
        "simple_query_string": {
            "query": "{0} {0}*".format(search_string),
            "fields": index_description_fields[index_key],
        }
    }


def some_words_in_title_query(title_fields_list, search_string):
    """Get words excluding special chars in title query if search string has more than one word"""
    sanitized_string = words_only_string(search_string)
    if sanitized_string is None:
        return None
    if sanitized_string:
        return {
            "bool": {
                "must": {
                    "simple_query_string": {
                        "query": sanitized_string,
                        "fields": title_fields_list,
                    }
                },
                "should": [autorativ_boost_clause()],
            }
        }
    else:
        return None


def constant_simple_query(search_string: str):
    return {
        "bool": {
            "must": [
                {
                    "constant_score": {
                        "filter": simple_query_string(
                            search_string=search_string, boost=1
                        ),
                        "boost": 1.2,
                    }
                }
            ],
            "should": [
                {"match": {"provenance.code": "NASJONAL"}},
                {"term": {"nationalComponent": "true"}},
            ],
        }
    }


def get_term_filter(request_item):
    """ map request filter for one key to ES term queries"""
    filters = []
    key = list(request_item.keys())[0]
    # get all values in request filter
    terms = request_item[key].split(",")
    for term in terms:
        q = {"term": {get_field_key(key): term}}
        filters.append(q)
    return filters


def get_term_filter_from_collection(key: str, collection: list):
    """ map request filter for one key to ES term queries"""
    filters = []
    for term in collection:
        q = {"term": {get_field_key(key): term}}
        filters.append(q)
    return filters


def get_exists_filter(request_item):
    """ map request filter for fields to ES exists queries"""
    filters = []
    key = list(request_item.keys())[0]
    # get all values in request filter
    fields = request_item[key].split(",")
    for field in fields:
        q = {"exists": {"field": field}}
        filters.append(q)
    return filters


def get_last_x_days_filter(request_item):
    range_str = f"now-{request_item['last_x_days']}d/d"
    return {"range": {"harvest.firstHarvested": {"gte": range_str, "lt": "now/d"}}}


def get_catalogs_by_name(cat_name):
    return {
        "bool": {
            "should": [
                {"match": {"catalog.title.no.raw": cat_name}},
                {"match": {"catalog.title.nb.raw": cat_name}},
                {"match": {"catalog.title.nn.raw": cat_name}},
                {"match": {"catalog.title.en.raw": cat_name}},
            ],
            "minimum_should_match": 1,
        }
    }


def get_information_model_by_relation(model_uri):
    return {
        "bool": {
            "should": [
                {"match": {"isPartOf.keyword": model_uri}},
                {"match": {"hasPart.keyword": model_uri}},
                {"match": {"isReplacedBy.keyword": model_uri}},
                {"match": {"replaces.keyword": model_uri}},
                {"match": {"containsSubjects.keyword": model_uri}},
            ],
            "minimum_should_match": 1,
        }
    }


def requires_or_relates(model_uri):
    return {
        "bool": {
            "should": [
                {"match": {"requires.uri.keyword": model_uri}},
                {"match": {"relation.uri.keyword": model_uri}},
            ],
            "minimum_should_match": 1,
        }
    }


def get_field_key(filter_key: str):
    """ Map the request filter key to keys in the elasticsearch mapping"""
    if filter_key == "orgPath":
        return "publisher.orgPath"
    elif filter_key == "accessRights":
        return "accessRights.code.keyword"
    elif filter_key == "los":
        return "losTheme.losPaths.keyword"
    elif filter_key == "theme":
        return "euTheme"
    elif filter_key == "provenance":
        return "provenance.code.keyword"
    elif filter_key == "spatial":
        return "spatial.prefLabel.no.keyword"
    elif filter_key == "uri":
        return "uri.keyword"
    elif filter_key == "formats":
        return "mediaType.keyword"
    elif filter_key == "datasetMediaType":
        return "distribution.mediaType.code.keyword"
    else:
        return filter_key


def get_index_filter_for_key(filter_key):
    """get indexes containing filter_key """
    if filter_key == "accessRights" or filter_key == "theme":
        return "datasets"
    else:
        return False


def must_not_filter(filter_key: str):
    missing_filter = {
        "bool": {"must_not": {"exists": {"field": get_field_key(filter_key)}}}
    }
    index = get_index_filter_for_key(filter_key)
    if index:
        missing_filter["bool"]["must"] = {
            "term": {"_index": get_index_filter_for_key(filter_key)}
        }
    return missing_filter


def collection_filter(filter_obj: dict):
    collection = get_term_filter_from_collection(
        key=filter_obj["field"], collection=filter_obj["values"]
    )

    if get_field_key("datasetMediaType") == filter_obj["field"]:
        return {"bool": {"must": collection}}
    if get_field_key("formats") == filter_obj["field"]:
        return {"bool": {"must": collection}}

    return {"bool": {"should": collection}}


def keyword_filter(keyword):
    return {
        "bool": {
            "should": [
                {"match": {"keyword.no": keyword}},
                {"match": {"keyword.nb": keyword}},
                {"match": {"keyword.nn": keyword}},
                {"match": {"keyword.en": keyword}},
            ],
            "minimum_should_match": 1,
        }
    }


def info_model_filter(uri):
    return {"bool": {"filter": [{"term": {"informationModel.uri.keyword": uri}}]}}


def dataset_info_model_relations(uri):
    return {
        "bool": {
            "should": [
                {"match": {"informationModel.uri.keyword": uri}},
                {"match": {"conformsTo.uri.keyword": uri}},
            ],
            "minimum_should_match": 1,
        }
    }


def required_by_service_filter(uri):
    return {
        "bool": {
            "should": [{"match": {"requires.uri.keyword": uri}}],
            "minimum_should_match": 1,
        }
    }


def related_by_service_filter(uri):
    return {
        "bool": {
            "should": [{"match": {"relation.uri.keyword": uri}}],
            "minimum_should_match": 1,
        }
    }


def event_filter(filter_values):
    is_grouped_by_list = []
    uri_list = []
    for uri in filter_values:
        is_grouped_by_list.append({"match": {"isGroupedBy.keyword": uri}})
    for uri in filter_values:
        uri_list.append({"match": {"uri.keyword": uri}})
    return {
        "bool": {
            "should": [
                {"bool": {"should": uri_list}},
                {"bool": {"must": is_grouped_by_list}},
            ],
            "minimum_should_match": 1,
        }
    }


def event_type_filter(filter_values):
    associated_broader_types_by_events_list = []
    associated_broader_types_list = []
    for uri in filter_values:
        associated_broader_types_by_events_list.append(
            {"match": {"associatedBroaderTypesByEvents.keyword": uri}}
        )
    for uri in filter_values:
        associated_broader_types_list.append(
            {"match": {"associatedBroaderTypes.keyword": uri}}
        )
    return {
        "bool": {
            "should": [
                {"bool": {"should": associated_broader_types_list}},
                {"bool": {"must": associated_broader_types_by_events_list}},
            ]
        }
    }


def get_aggregation_term_for_key(
    aggregation_key: str, missing: str = None, size: int = None
) -> dict:
    query = {"terms": {"field": get_field_key(aggregation_key)}}
    if missing:
        query["terms"]["missing"] = missing
    if size:
        query["terms"]["size"] = size
    return query


def los_aggregation():
    return {"terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}}


def org_path_aggregation():
    return {
        "terms": {
            "field": "publisher.orgPath",
            "missing": "MISSING",
            "size": 1000000000,
        }
    }


def has_competent_authority_aggregation():
    return {
        "terms": {
            "field": "hasCompetentAuthority.orgPath",
            "missing": "MISSING",
            "size": 1000000000,
        }
    }


def is_grouped_by_aggregation():
    return {"terms": {"field": "isGroupedBy.keyword", "size": 1000000000}}


def reference_source_filter(uri):
    return {"bool": {"filter": [{"term": {"references.source.uri.keyword": uri}}]}}


def associated_broader_types_by_events_aggregation():
    return {
        "terms": {"field": "associatedBroaderTypesByEvents.keyword", "size": 1000000000}
    }


def default_all_indices_aggs():
    """ Return a dict with default aggregation for all indices search"""
    return {
        "los": los_aggregation(),
        "orgPath": org_path_aggregation(),
        "availability": {
            "filters": {
                "filters": {
                    "isOpenAccess": {"term": {"isOpenAccess": "true"}},
                    "isOpenLicense": {"term": {"isOpenLicense": "true"}},
                    "isFree": {"term": {"isFree": "true"}},
                }
            }
        },
        "dataset_access": {
            "filter": {"term": {"_index": "datasets"}},
            "aggs": {
                "accessRights": {
                    "terms": {
                        "field": "accessRights.code.keyword",
                        "missing": "Ukjent",
                        "size": 10,
                    }
                }
            },
        },
        "opendata": {
            "filter": {
                "bool": {
                    "must": [
                        {"term": {"accessRights.code.keyword": "PUBLIC"}},
                        {"term": {"distribution.openLicense": "true"}},
                    ]
                }
            }
        },
        "theme": {"terms": {"field": "euTheme"}},
    }


def all_indices_default_query():
    return {
        "bool": {
            "must": {"match_all": {}},
            "should": [
                {
                    "term": {
                        "provenance.code.keyword": {"value": "NASJONAL", "boost": 3}
                    }
                },
                {"term": {"nationalComponent": {"value": "true", "boost": 1}}},
                open_data_query(),
            ],
        }
    }


def query_with_filter_template(must_clause: list) -> dict:
    return {"bool": {"must": must_clause, "filter": []}}


def query_with_final_boost_template(
    must_clause: list, should_clause, filter_clause: bool = False
) -> dict:
    template = {"bool": {"must": must_clause, "should": should_clause}}
    if filter_clause:
        template["bool"]["filter"] = []
    return template


def query_template(dataset_boost=0):
    template = {"query": {}, "aggs": {}}
    if dataset_boost > 0:
        template["indices_boost"] = [{"datasets": dataset_boost}]
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
