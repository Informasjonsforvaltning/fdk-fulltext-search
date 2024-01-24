from typing import Dict, List, Union

from fdk_fulltext_search.ingest.utils import IndicesKey


def get_field_by_filter_key(filter_key: str) -> str:
    """Map the request filter key to keys in the elasticsearch mapping"""
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
        return "spatial.prefLabel.nb.keyword"
    elif filter_key == "uri":
        return "uri.keyword"
    else:
        return filter_key


def get_index_filter_for_key(filter_key: str) -> Union[str, bool]:
    """get indexes containing filter_key"""
    if filter_key == "accessRights" or filter_key == "theme":
        return IndicesKey.DATA_SETS
    else:
        return False


def term_filter(request_item: Dict) -> List[Dict[str, Dict]]:
    """map request filter for one key to ES term queries"""
    filters = []
    key = list(request_item.keys())[0]
    # get all values in request filter
    terms = request_item[key].split(",")
    for term in terms:
        q = {"term": {get_field_by_filter_key(key): term}}
        filters.append(q)
    return filters


def term_filter_from_collection(key: str, collection: List) -> List[Dict[str, Dict]]:
    """map request filter for one key to ES term queries"""
    filters = []
    for term in collection:
        q = {"term": {get_field_by_filter_key(key): term}}
        filters.append(q)
    return filters


def exists_filter(request_item: Dict) -> List[Dict[str, Dict]]:
    """map request filter for fields to ES exists queries"""
    filters = []
    key = list(request_item.keys())[0]
    # get all values in request filter
    fields = request_item[key].split(",")
    for field in fields:
        q = {"exists": {"field": field}}
        filters.append(q)
    return filters


def last_x_days_filter(request_item: Dict) -> Dict[str, Dict[str, Dict[str, str]]]:
    range_str = f"now-{request_item['last_x_days']}d/d"
    return {"range": {"harvest.firstHarvested": {"gte": range_str, "lt": "now+1d/d"}}}


def catalogs_by_name_filter(cat_name: str) -> Dict[str, Dict]:
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


def information_model_by_relation_filter(model_uri: str) -> Dict[str, Dict]:
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


def requires_or_relates_filter(model_uri: str) -> Dict[str, Dict]:
    return {
        "bool": {
            "should": [
                {"match": {"requires.uri.keyword": model_uri}},
                {"match": {"relation.uri.keyword": model_uri}},
            ],
            "minimum_should_match": 1,
        }
    }


def must_not_filter(filter_key: str) -> Dict[str, Dict]:
    missing_filter: Dict = {
        "bool": {"must_not": {"exists": {"field": get_field_by_filter_key(filter_key)}}}
    }
    index = get_index_filter_for_key(filter_key)
    if index:
        missing_filter["bool"]["must"] = {
            "term": {"_index": get_index_filter_for_key(filter_key)}
        }
    return missing_filter


def collection_filter(filter_obj: Dict) -> Dict[str, Dict]:
    collection = term_filter_from_collection(
        key=filter_obj["field"], collection=filter_obj["values"]
    )

    clause = "should"
    if get_field_by_filter_key("formats") == filter_obj["field"]:
        clause = "must"

    if "operator" in filter_obj:
        clause = "must" if filter_obj["operator"] == "AND" else "should"

    return {"bool": {clause: collection}}


def keyword_filter(keyword: str) -> Dict[str, Dict]:
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


def info_model_filter(uri: str) -> Dict[str, Dict]:
    return {"bool": {"filter": [{"term": {"informationModel.uri.keyword": uri}}]}}


def required_by_service_filter(uri: str) -> Dict[str, Dict]:
    return {
        "bool": {
            "should": [{"match": {"requires.uri.keyword": uri}}],
            "minimum_should_match": 1,
        }
    }


def related_by_service_filter(uri: str) -> Dict[str, Dict]:
    return {
        "bool": {
            "should": [{"match": {"relation.uri.keyword": uri}}],
            "minimum_should_match": 1,
        }
    }


def event_filter(filter_values: List[str]) -> Dict[str, Dict]:
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


def event_type_filter(filter_values: List[str]) -> Dict[str, Dict]:
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


def dataset_info_model_relations_filter(uri: str) -> Dict[str, Dict]:
    return {
        "bool": {
            "should": [
                {"match": {"informationModel.uri.keyword": uri}},
                {"match": {"conformsTo.uri.keyword": uri}},
            ],
            "minimum_should_match": 1,
        }
    }
