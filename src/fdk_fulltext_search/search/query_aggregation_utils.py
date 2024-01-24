from typing import Dict, Optional, Union

from fdk_fulltext_search.search.query_filter_utils import (
    get_field_by_filter_key,
)


def default_all_indices_aggs() -> Dict:
    """Return a dict with default aggregation for all indices search"""
    return {
        "los": los_aggregation(),
        "orgPath": org_path_aggregation(),
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
                        {"term": {"isOpenData": "true"}},
                    ]
                }
            }
        },
        "theme": {"terms": {"field": "euTheme"}},
    }


def los_aggregation() -> Dict[str, Dict]:
    return {"terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}}


def org_path_aggregation() -> Dict[str, Dict]:
    return {
        "terms": {
            "field": "publisher.orgPath",
            "missing": "MISSING",
            "size": 1000000000,
        }
    }


def has_competent_authority_aggregation() -> Dict[str, Dict]:
    return {
        "terms": {
            "field": "hasCompetentAuthority.orgPath",
            "missing": "MISSING",
            "size": 1000000000,
        }
    }


def is_grouped_by_aggregation() -> Dict[str, Dict]:
    return {"terms": {"field": "isGroupedBy.keyword", "size": 1000000000}}


def fdk_format_aggregation() -> Dict[str, Dict]:
    return {"terms": {"field": "fdkFormatPrefixed.keyword", "size": 1000000000}}


def get_aggregation_term_for_key(
    aggregation_key: str, missing: Optional[str] = None, size: Optional[int] = None
) -> Dict[str, Dict[str, Union[str, int]]]:
    query: Dict[str, Dict[str, Union[str, int]]] = {
        "terms": {"field": get_field_by_filter_key(aggregation_key)}
    }
    if missing:
        query["terms"]["missing"] = missing
    if size:
        query["terms"]["size"] = size
    return query
