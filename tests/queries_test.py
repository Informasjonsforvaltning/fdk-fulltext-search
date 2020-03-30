import json

import pytest

from src.search.queries import RecentQuery, AllIndicesQuery


@pytest.mark.unit
def test_recent_query_should_have_size_5():
    expected = {
        "size": 5,
        "sort":
            {"harvest.firstHarvested": {"order": "desc"}}
    }
    result = RecentQuery().query
    assert result.keys() == expected.keys()
    assert result["size"] == expected["size"]
    assert result["sort"] == result["sort"]


@pytest.mark.unit
def test_recent_query_should_have_size_18():
    expected = {
        "size": 18,
        "sort":
            {"harvest.firstHarvested": {"order": "desc"}}
    }
    result = RecentQuery(18).query
    assert result.keys() == expected.keys()
    assert result["size"] == expected["size"]
    assert result["sort"] == result["sort"]


@pytest.mark.unit
def test_all_indices_query_should_return_query_with_constant_score():
    expected = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "bool": {
                            "must": [
                                {
                                    "constant_score": {
                                        "filter": {
                                            "simple_query_string": {
                                                "query": "stønad stønad*",
                                                "boost": 1,
                                                "default_operator": "or"
                                            }
                                        },
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
                    },
                    {
                        "simple_query_string": {
                            "query": "stønad stønad*",
                            "boost": 0.1,
                            "default_operator": "or"
                        }
                    }
                ]
            }
        },
        "aggs": {
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
            "isOpenAccess": {
                "terms": {
                    "field": "isOpenAccess",
                    "size": 3
                }
            },
            "accessRights": {
                "terms": {
                    "field": "accessRights.code.keyword",
                    "size": 10
                }
            }
        }

    }
    result = AllIndicesQuery(searchString="stønad")
    assert json.dumps(result.query) == json.dumps(expected)
