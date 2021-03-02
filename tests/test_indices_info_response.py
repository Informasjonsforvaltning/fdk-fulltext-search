import pytest

from fdk_fulltext_search.ingest.utils import IndicesKey
from fdk_fulltext_search.search.responses import IndicesInfoResponse


@pytest.mark.unit
def test_map_all_indices_info_response(mock_count_elastic):
    elastic_info = {
        "took": 2,
        "timed_out": "false",
        "_shards": {
            "total": 1,
            "successful": 1,
            "skipped": 0,
            "failed": 0
        },
        "hits": {
            "total": {
                "value": 4,
                "relation": "eq"
            },
            "max_score": 1.0,
            "hits": [
                {
                    "_index": "info",
                    "_type": "_doc",
                    "_id": "BOM-7nEBW5iUXflFsP-n",
                    "_score": 1.0,
                    "_source": {
                        "lastUpdate": "2020-05-07T08:27:14.839804",
                        "name": "informationmodels"
                    }
                },
                {
                    "_index": "info",
                    "_type": "_doc",
                    "_id": "BeM-7nEBW5iUXflFx_8O",
                    "_score": 1.0,
                    "_source": {
                        "lastUpdate": "2020-05-07T08:27:18.742168",
                        "name": "concepts"
                    }
                },
                {
                    "_index": "info",
                    "_type": "_doc",
                    "_id": "BuM-7nEBW5iUXflF0f_z",
                    "_score": 1.0,
                    "_source": {
                        "lastUpdate": "2020-05-07T08:27:20.729579",
                        "name": "dataservices"
                    }
                },
                {
                    "_index": "info",
                    "_type": "_doc",
                    "_id": "B-M-7nEBW5iUXflF3P_D",
                    "_score": 1.0,
                    "_source": {
                        "lastUpdate": "2020-05-07T08:27:26.131969",
                        "name": "datasets"
                    }
                }
            ]
        }
    }
    expected = [
        {
            "lastUpdate": "2020-05-07T08:27:14.839804",
            "name": "informationmodels",
            "count": 1090
        },
        {
            "lastUpdate": "2020-05-07T08:27:18.742168",
            "name": "concepts",
            "count": 1090
        },
        {
            "lastUpdate": "2020-05-07T08:27:20.729579",
            "name": "dataservices",
            "count": 1090
        },
        {
            "lastUpdate": "2020-05-07T08:27:26.131969",
            "name": "datasets",
            "count": 1090
        }
    ]

    assert IndicesInfoResponse(elastic_info).map_response() == expected


def test_map_one_indices_info_response(mock_count_elastic):
    elastic_info = {
        "took": 2,
        "timed_out": "false",
        "_shards": {
            "total": 1,
            "successful": 1,
            "skipped": 0,
            "failed": 0
        },
        "hits": {
            "total": {
                "value": 1,
                "relation": "eq"
            },
            "max_score": 1.0,
            "hits": [
                {
                    "_index": "info",
                    "_type": "_doc",
                    "_id": "B-M-7nEBW5iUXflF3P_D",
                    "_score": 1.0,
                    "_source": {
                        "lastUpdate": "2020-05-07T08:27:26.131969",
                        "name": "datasets"
                    }
                }
            ]
        }
    }

    expected = [
        {
            "lastUpdate": "2020-05-07T08:27:26.131969",
            "name": "datasets",
            "count": 1090
        }
    ]

    assert IndicesInfoResponse(elastic_info).map_response() == expected
