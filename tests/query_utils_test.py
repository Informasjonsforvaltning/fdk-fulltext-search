import json

import pytest

from src.search.query_utils import constant_simple_query, get_filter


@pytest.mark.unit
def test_constant_simple_query_should_return_correct_query():
    expected = {
        "bool": {
            "must": [
                {
                    "constant_score": {
                        "filter": {
                            "simple_query_string": {
                                "query": "barnehage barnehage*",
                                'boost': 1,
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
    }

    result = constant_simple_query("barnehage")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_should_return_filter_with_modified_key():
    expected = {"publisher.orgPath": "KOMMUNE/678687"}
    result = get_filter({"orgPath": "KOMMUNE/678687"})
    assert result == expected

@pytest.mark.unit
def test_should_return_filter_with_unmodified_key():
    expected = {"openLicence": "KOMMUNE/678687"}
    result = get_filter(expected)
    assert result == expected