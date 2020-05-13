import json

import pytest

from src.search.query_utils_dataset import data_sets_default_query


@pytest.mark.unit
def test_data_sett_default_query():
    expected_query = {
        "bool": {
            "must": [
                {
                    "match_all": {}
                }
            ],
            "should": [
                {
                    "match": {
                        "provenance.code": "NASJONAL"
                    }
                },
                {
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
            ]
        }
    }
    assert json.dumps(data_sets_default_query()) == json.dumps(expected_query)

