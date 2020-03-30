import json

import pytest

from src.search.query_utils import constant_simple_query


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

