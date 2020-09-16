import json

import pytest
from jsonpath_ng import parse

from src.search.queries import InformationModelQuery, DataSetQuery, index_fulltext_fields, IndicesKey


@pytest.mark.unit
def test_information_model_empty_query():
    expected_body = {
        "query": {
            "match_all": {}
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
            }
        }
    }

    result_body = InformationModelQuery().body
    assert result_body == expected_body


@pytest.mark.unit
def test_information_model_with_search_string_query():
    expected_body = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "dis_max": {
                            "queries": [
                                {
                                    "multi_match": {
                                        "query": "RA-0554 Pris",
                                        "type": "bool_prefix",
                                        "fields": [
                                            "title.nb.ngrams",
                                            "title.nb.ngrams.2_gram",
                                            "title.nb.ngrams.3_gram"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "RA-0554 Pris",
                                        "type": "bool_prefix",
                                        "fields": [
                                            "title.nn.ngrams",
                                            "title.nn.ngrams.2_gram",
                                            "title.nn.ngrams.3_gram"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "RA-0554 Pris",
                                        "type": "bool_prefix",
                                        "fields": [
                                            "title.no.ngrams",
                                            "title.no.ngrams.2_gram",
                                            "title.no.ngrams.3_gram"
                                        ]
                                    }
                                },
                                {
                                    "multi_match": {
                                        "query": "RA-0554 Pris",
                                        "type": "bool_prefix",
                                        "fields": [
                                            "title.en.ngrams",
                                            "title.en.ngrams.2_gram",
                                            "title.en.ngrams.3_gram"
                                        ]
                                    }
                                }
                            ],
                            "boost": 2
                        }
                    },
                    {
                        "simple_query_string": {
                            "query": "RA-0554+Pris RA-0554+Pris*",
                            "fields": ["schema^0.5"],
                        }
                    },
                    {
                        "simple_query_string": {
                            "query": "RA+0554+Pris RA+0554+Pris*",
                            "boost": 0.02
                        }
                    },
                    {
                        "simple_query_string": {
                            "query": "*RA RA RA* *0554 0554 0554* *Pris Pris Pris*",
                            "boost": 0.001
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
            }
        }
    }
    result_body = InformationModelQuery(search_string="RA-0554 Pris").body
    assert result_body == expected_body


@pytest.mark.unit
def test_information_model_add_filter():
    expected_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "dis_max": {
                            "queries": [
                                {
                                    "dis_max": {
                                        "queries": [
                                            {
                                                "multi_match": {
                                                    "query": "RA-0554 Pris",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.nb.ngrams",
                                                        "title.nb.ngrams.2_gram",
                                                        "title.nb.ngrams.3_gram"
                                                    ]
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": "RA-0554 Pris",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.nn.ngrams",
                                                        "title.nn.ngrams.2_gram",
                                                        "title.nn.ngrams.3_gram"
                                                    ]
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": "RA-0554 Pris",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.no.ngrams",
                                                        "title.no.ngrams.2_gram",
                                                        "title.no.ngrams.3_gram"
                                                    ]
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": "RA-0554 Pris",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.en.ngrams",
                                                        "title.en.ngrams.2_gram",
                                                        "title.en.ngrams.3_gram"
                                                    ]
                                                }
                                            }
                                        ],
                                        "boost": 2
                                    }
                                },
                                {
                                    "simple_query_string": {
                                        "query": "RA-0554+Pris RA-0554+Pris*",
                                        "fields": [
                                            "schema^0.5"
                                        ]
                                    }
                                },
                                {
                                    "simple_query_string": {
                                        "query": "RA+0554+Pris RA+0554+Pris*",
                                        "boost": 0.02
                                    }
                                },
                                {
                                    "simple_query_string": {
                                        "query": "*RA RA RA* *0554 0554 0554* *Pris Pris Pris*",
                                        "boost": 0.001
                                    }
                                }
                            ]
                        }
                    }
                ],
                "filter": [
                    {
                        "term": {
                            "losTheme.losPaths.keyword": "naring"
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
            }
        }
    }
    result = InformationModelQuery(search_string="RA-0554 Pris", filters=[{"los": "naring"}]).body
    assert json.dumps(result) == json.dumps(expected_body)


@pytest.mark.unit
def test_information_model_should_return_query_with_must_not_for_MISSING():
    expected_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match_all": {}
                    }
                ],
                "filter": [
                    {
                        "bool": {
                            "must_not": {
                                "exists": {
                                    "field": "publisher.orgPath"
                                }
                            }
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
            }
        }
    }
    result = InformationModelQuery(filters=[{"orgPath": "MISSING"}]).body
    assert json.dumps(result) == json.dumps(expected_body)


@pytest.mark.unit
def test_dataset_default_aggregations():
    expected_aggs = {
        "los": {
            "terms": {
                "field": "losTheme.losPaths.keyword",
                "size": 1000000000
            }
        },
        "provenance": {
            "terms": {
                "field": "provenance.code.keyword"
            }
        },
        "orgPath": {
            "terms": {
                "field": "publisher.orgPath",
                "missing": "MISSING",
                "size": 1000000000
            }
        },
        "opendata": {
            "filter": {
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
        },
        "theme": {
            "terms": {
                "field": "euTheme"
            }
        },
        "accessRights": {
            "terms": {
                "field": "accessRights.code.keyword",
                "missing": "Ukjent",
                "size": 10
            }
        },
        "spatial": {
            "terms": {
                "field": "spatial.prefLabel.no.keyword"
            }
        }
    }
    result = DataSetQuery().body["aggs"]
    agg_keys = result.keys()
    assert "los" in agg_keys
    assert "provenance" in agg_keys
    assert "orgPath" in agg_keys
    assert "opendata" in agg_keys
    assert "theme" in agg_keys
    assert "accessRights" in agg_keys
    assert "spatial" in agg_keys

    assert json.dumps(result) == json.dumps(expected_aggs)


@pytest.mark.unit
def test_dataset_empty_query():
    expected_body = {
        "query": {
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
        },
        "aggs": {
            "los": {
                "terms": {
                    "field": "losTheme.losPaths.keyword",
                    "size": 1000000000
                }
            },
            "provenance": {
                "terms": {
                    "field": "provenance.code.keyword"
                }
            },
            "orgPath": {
                "terms": {
                    "field": "publisher.orgPath",
                    "missing": "MISSING",
                    "size": 1000000000
                }
            },
            "opendata": {
                "filter": {
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
            },
            "theme": {
                "terms": {
                    "field": "euTheme"
                }
            },
            "accessRights": {
                "terms": {
                    "field": "accessRights.code.keyword",
                    "missing": "Ukjent",
                    "size": 10
                }
            },
            "spatial": {
                "terms": {
                    "field": "spatial.prefLabel.no.keyword"
                }
            }
        }
    }
    assert json.dumps(DataSetQuery().body) == json.dumps(expected_body)


@pytest.mark.unit
def test_dataset_with_query_string_query():
    expected = {
        "bool": {
            "must": [
                {
                    "dis_max": {
                        "queries": [
                            {
                                "dis_max": {
                                    "queries": [
                                        {
                                            "multi_match": {
                                                "query": "Elbiloversikt i",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.nb.ngrams",
                                                    "title.nb.ngrams.2_gram",
                                                    "title.nb.ngrams.3_gram"
                                                ]
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "Elbiloversikt i",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.nn.ngrams",
                                                    "title.nn.ngrams.2_gram",
                                                    "title.nn.ngrams.3_gram"
                                                ]
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "Elbiloversikt i",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.no.ngrams",
                                                    "title.no.ngrams.2_gram",
                                                    "title.no.ngrams.3_gram"
                                                ]
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "Elbiloversikt i",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.en.ngrams",
                                                    "title.en.ngrams.2_gram",
                                                    "title.en.ngrams.3_gram"
                                                ]
                                            }
                                        }
                                    ],
                                    "boost": 5
                                }
                            },
                            {
                                "simple_query_string": {
                                    "query": "Elbiloversikt+i Elbiloversikt+i*",
                                    "fields": [
                                        "description.nb",
                                        "description.nn",
                                        "description.no",
                                        "description.en"
                                    ]
                                }
                            },
                            {
                                "simple_query_string": {
                                    "query": "Elbiloversikt+i Elbiloversikt+i*",
                                    "fields": index_fulltext_fields[IndicesKey.DATA_SETS],
                                    "boost": 0.5
                                }
                            },
                            {
                                "simple_query_string": {
                                    "query": "*Elbiloversikt Elbiloversikt Elbiloversikt* *i i i*",
                                    "fields": index_fulltext_fields[IndicesKey.DATA_SETS],
                                    "boost": 0.001,
                                }
                            }
                        ]
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
    result = DataSetQuery("Elbiloversikt i").body["query"]
    # has boolean root clause
    assert parse('bool.must').find(result).__len__() > 0 and parse('bool.should').find(result).__len__() > 0, \
        "No boolean root clause "
    assert parse('bool.must[*].dis_max').find(result).__len__() == 1, "No dismax query in boolean must root clause"
    # has title clause
    assert parse('bool.must[*].dis_max.queries[*].dis_max').find(result).__len__() == 1, "No root query for " \
                                                                                         "dismax_title "
    assert parse('bool.must[*].dis_max.queries[*].dis_max.queries[*].multi_match').find(result).__len__() == 4, \
        "clauses missing from dis_max title queries "
    # has fulltext clauses
    assert parse('bool.must[*].dis_max.queries[*].simple_query_string').find(
        result).__len__() == 3, "missing fulltext_queries"
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_dataset_with_spatial_filter():
    expected = {
            "bool": {
                "must": [
                    {
                        "dis_max": {
                            "queries": [
                                {
                                    "dis_max": {
                                        "queries": [
                                            {
                                                "multi_match": {
                                                    "query": "Ad",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.nb.ngrams",
                                                        "title.nb.ngrams.2_gram",
                                                        "title.nb.ngrams.3_gram"
                                                    ]
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": "Ad",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.nn.ngrams",
                                                        "title.nn.ngrams.2_gram",
                                                        "title.nn.ngrams.3_gram"
                                                    ]
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": "Ad",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.no.ngrams",
                                                        "title.no.ngrams.2_gram",
                                                        "title.no.ngrams.3_gram"
                                                    ]
                                                }
                                            },
                                            {
                                                "multi_match": {
                                                    "query": "Ad",
                                                    "type": "bool_prefix",
                                                    "fields": [
                                                        "title.en.ngrams",
                                                        "title.en.ngrams.2_gram",
                                                        "title.en.ngrams.3_gram"
                                                    ]
                                                }
                                            }
                                        ],
                                        "boost": 5
                                    }
                                },
                                {
                                    "simple_query_string": {
                                        "query": "Ad Ad*",
                                        "fields": [
                                            "description.nb",
                                            "description.nn",
                                            "description.no",
                                            "description.en"
                                        ]
                                    }
                                },
                                {
                                    "simple_query_string": {
                                        "query": "Ad Ad*",
                                        "fields": [
                                            "title.*^3",
                                            "objective.*",
                                            "keyword.*^2",
                                            "theme.title.*",
                                            "expandedLosTema.*",
                                            "description.*",
                                            "publisher.name^3",
                                            "publisher.prefLabel^3",
                                            "accessRights.prefLabel.*^3",
                                            "accessRights.code",
                                            "subject.prefLabel.*",
                                            "subject.altLabel.*",
                                            "subject.definition.*",
                                            "distribution.title.*"
                                        ],
                                        "boost": 0.5
                                    }
                                },
                                {
                                    "simple_query_string": {
                                        "query": "*Ad Ad Ad*",
                                        "fields": [
                                            "title.*^3",
                                            "objective.*",
                                            "keyword.*^2",
                                            "theme.title.*",
                                            "expandedLosTema.*",
                                            "description.*",
                                            "publisher.name^3",
                                            "publisher.prefLabel^3",
                                            "accessRights.prefLabel.*^3",
                                            "accessRights.code",
                                            "subject.prefLabel.*",
                                            "subject.altLabel.*",
                                            "subject.definition.*",
                                            "distribution.title.*"
                                        ],
                                        "boost": 0.001
                                    }
                                }
                            ]
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
                ],
                "filter": [
                    {
                        "term": {
                            "spatial.prefLabel.no.keyword": "Norge"
                        }
                    }
                ]
            }
    }
    result = DataSetQuery(search_string="Ad", filters=[{"spatial": "Norge"}]).body["query"]

    assert json.dumps(result) == json.dumps(expected)
