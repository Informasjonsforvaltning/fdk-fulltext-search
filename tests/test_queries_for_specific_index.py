import json

import pytest

from fdk_fulltext_search.search.queries import DataSetQuery, InformationModelQuery


@pytest.mark.unit
def test_information_model_empty_query():
    expected_body = {
        "query": {
            "bool": {
                "must": {"match_all": {}},
                "should": [
                    {"match": {"provenance.code": "NASJONAL"}},
                    {"term": {"nationalComponent": "true"}},
                    {
                        "bool": {
                            "must": [
                                {"term": {"accessRights.code.keyword": "PUBLIC"}},
                                {"term": {"isOpenData": "true"}},
                            ]
                        }
                    },
                ],
            }
        },
        "aggs": {
            "los": {
                "terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}
            },
            "orgPath": {
                "terms": {
                    "field": "publisher.orgPath",
                    "missing": "MISSING",
                    "size": 1000000000,
                }
            },
        },
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
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": "RA-0554 Pris",
                                    "fields": [
                                        "title.en.raw",
                                        "title.nb.raw",
                                        "title.nn.raw",
                                        "title.no.raw",
                                    ],
                                }
                            },
                            "should": [
                                {"match": {"provenance.code": "NASJONAL"}},
                                {"term": {"nationalComponent": "true"}},
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "accessRights.code.keyword": "PUBLIC"
                                                }
                                            },
                                            {"term": {"isOpenData": "true"}},
                                        ]
                                    }
                                },
                            ],
                            "boost": 20,
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "dis_max": {
                                    "queries": [
                                        {
                                            "multi_match": {
                                                "query": "RA-0554 Pris",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.en.ngrams",
                                                    "title.en.ngrams.2_gram",
                                                    "title.en.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "RA-0554 Pris",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.nb.ngrams",
                                                    "title.nb.ngrams.2_gram",
                                                    "title.nb.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "RA-0554 Pris",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.nn.ngrams",
                                                    "title.nn.ngrams.2_gram",
                                                    "title.nn.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "RA-0554 Pris",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "title.no.ngrams",
                                                    "title.no.ngrams.2_gram",
                                                    "title.no.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "query_string": {
                                                "query": "*RA* *0554* *Pris*",
                                                "fields": [
                                                    "title.en.raw",
                                                    "title.nb.raw",
                                                    "title.nn.raw",
                                                    "title.no.raw",
                                                ],
                                            }
                                        },
                                    ],
                                }
                            },
                            "should": [
                                {"match": {"provenance.code": "NASJONAL"}},
                                {"term": {"nationalComponent": "true"}},
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "accessRights.code.keyword": "PUBLIC"
                                                }
                                            },
                                            {"term": {"isOpenData": "true"}},
                                        ]
                                    }
                                },
                            ],
                            "boost": 10,
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": "RA-0554 Pris",
                                    "fields": [
                                        "publisher.prefLabel.*",
                                        "publisher.title.*",
                                        "hasCompetentAuthority.prefLabel.*",
                                        "hasCompetentAuthority.name.*",
                                        "keyword.*",
                                    ],
                                }
                            },
                            "should": [
                                {"match": {"provenance.code": "NASJONAL"}},
                                {"term": {"nationalComponent": "true"}},
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "accessRights.code.keyword": "PUBLIC"
                                                }
                                            },
                                            {"term": {"isOpenData": "true"}},
                                        ]
                                    }
                                },
                            ],
                            "boost": 10,
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "simple_query_string": {
                                    "query": "RA-0554+Pris RA-0554+Pris*",
                                    "fields": ["schema^0.5"],
                                }
                            },
                            "should": [
                                {"match": {"provenance.code": "NASJONAL"}},
                                {"term": {"nationalComponent": "true"}},
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "accessRights.code.keyword": "PUBLIC"
                                                }
                                            },
                                            {"term": {"isOpenData": "true"}},
                                        ]
                                    }
                                },
                            ],
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "simple_query_string": {
                                    "query": "RA+0554+Pris RA+0554+Pris*",
                                    "fields": [
                                        "description.*",
                                        "keyword.*^2",
                                        "losTheme.name.*^3",
                                        "publisher.name^3",
                                        "publisher.prefLabel^3",
                                        "theme.title.*",
                                        "title.*^3",
                                    ],
                                }
                            },
                            "should": [
                                {"match": {"provenance.code": "NASJONAL"}},
                                {"term": {"nationalComponent": "true"}},
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "accessRights.code.keyword": "PUBLIC"
                                                }
                                            },
                                            {"term": {"isOpenData": "true"}},
                                        ]
                                    }
                                },
                            ],
                            "boost": 0.02,
                        }
                    },
                ]
            }
        },
        "aggs": {
            "los": {
                "terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}
            },
            "orgPath": {
                "terms": {
                    "field": "publisher.orgPath",
                    "missing": "MISSING",
                    "size": 1000000000,
                }
            },
        },
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
                                    "bool": {
                                        "must": {
                                            "multi_match": {
                                                "query": "RA-0554 Pris",
                                                "fields": [
                                                    "title.en.raw",
                                                    "title.nb.raw",
                                                    "title.nn.raw",
                                                    "title.no.raw",
                                                ],
                                            }
                                        },
                                        "should": [
                                            {"match": {"provenance.code": "NASJONAL"}},
                                            {"term": {"nationalComponent": "true"}},
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
                                                                "isOpenData": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 20,
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "dis_max": {
                                                "queries": [
                                                    {
                                                        "multi_match": {
                                                            "query": "RA-0554 Pris",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "title.en.ngrams",
                                                                "title.en.ngrams.2_gram",
                                                                "title.en.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "RA-0554 Pris",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "title.nb.ngrams",
                                                                "title.nb.ngrams.2_gram",
                                                                "title.nb.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "RA-0554 Pris",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "title.nn.ngrams",
                                                                "title.nn.ngrams.2_gram",
                                                                "title.nn.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "RA-0554 Pris",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "title.no.ngrams",
                                                                "title.no.ngrams.2_gram",
                                                                "title.no.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "query_string": {
                                                            "query": "*RA* *0554* *Pris*",
                                                            "fields": [
                                                                "title.en.raw",
                                                                "title.nb.raw",
                                                                "title.nn.raw",
                                                                "title.no.raw",
                                                            ],
                                                        }
                                                    },
                                                ],
                                            }
                                        },
                                        "should": [
                                            {"match": {"provenance.code": "NASJONAL"}},
                                            {"term": {"nationalComponent": "true"}},
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
                                                                "isOpenData": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 10,
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "multi_match": {
                                                "query": "RA-0554 Pris",
                                                "fields": [
                                                    "publisher.prefLabel.*",
                                                    "publisher.title.*",
                                                    "hasCompetentAuthority.prefLabel.*",
                                                    "hasCompetentAuthority.name.*",
                                                    "keyword.*",
                                                ],
                                            }
                                        },
                                        "should": [
                                            {"match": {"provenance.code": "NASJONAL"}},
                                            {"term": {"nationalComponent": "true"}},
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
                                                                "isOpenData": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 10,
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "simple_query_string": {
                                                "query": "RA-0554+Pris RA-0554+Pris*",
                                                "fields": ["schema^0.5"],
                                            }
                                        },
                                        "should": [
                                            {"match": {"provenance.code": "NASJONAL"}},
                                            {"term": {"nationalComponent": "true"}},
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
                                                                "isOpenData": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "simple_query_string": {
                                                "query": "RA+0554+Pris RA+0554+Pris*",
                                                "fields": [
                                                    "description.*",
                                                    "keyword.*^2",
                                                    "losTheme.name.*^3",
                                                    "publisher.name^3",
                                                    "publisher.prefLabel^3",
                                                    "theme.title.*",
                                                    "title.*^3",
                                                ],
                                            }
                                        },
                                        "should": [
                                            {"match": {"provenance.code": "NASJONAL"}},
                                            {"term": {"nationalComponent": "true"}},
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
                                                                "isOpenData": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 0.02,
                                    }
                                },
                            ]
                        }
                    }
                ],
                "filter": [{"term": {"losTheme.losPaths.keyword": "naring"}}],
            }
        },
        "aggs": {
            "los": {
                "terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}
            },
            "orgPath": {
                "terms": {
                    "field": "publisher.orgPath",
                    "missing": "MISSING",
                    "size": 1000000000,
                }
            },
        },
    }
    result = InformationModelQuery(
        search_string="RA-0554 Pris", filters=[{"los": "naring"}]
    ).body
    assert json.dumps(result) == json.dumps(expected_body)


@pytest.mark.unit
def test_information_model_should_return_query_with_must_not_for_missing():
    expected_body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "must": {"match_all": {}},
                            "should": [
                                {"match": {"provenance.code": "NASJONAL"}},
                                {"term": {"nationalComponent": "true"}},
                                {
                                    "bool": {
                                        "must": [
                                            {
                                                "term": {
                                                    "accessRights.code.keyword": "PUBLIC"
                                                }
                                            },
                                            {"term": {"isOpenData": "true"}},
                                        ]
                                    }
                                },
                            ],
                        }
                    }
                ],
                "filter": [
                    {"bool": {"must_not": {"exists": {"field": "publisher.orgPath"}}}}
                ],
            }
        },
        "aggs": {
            "los": {
                "terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}
            },
            "orgPath": {
                "terms": {
                    "field": "publisher.orgPath",
                    "missing": "MISSING",
                    "size": 1000000000,
                }
            },
        },
    }
    result = InformationModelQuery(filters=[{"orgPath": "MISSING"}]).body
    assert json.dumps(result) == json.dumps(expected_body)


@pytest.mark.unit
def test_dataset_default_aggregations():
    expected_aggs = {
        "format": {"terms": {"field": "fdkFormatPrefixed.keyword", "size": 1000000000}},
        "los": {"terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}},
        "provenance": {"terms": {"field": "provenance.code.keyword"}},
        "orgPath": {
            "terms": {
                "field": "publisher.orgPath",
                "missing": "MISSING",
                "size": 1000000000,
            }
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
        "accessRights": {
            "terms": {
                "field": "accessRights.code.keyword",
                "missing": "Ukjent",
                "size": 10,
            }
        },
        "spatial": {"terms": {"field": "spatial.prefLabel.no.keyword"}},
    }
    result = DataSetQuery().body["aggs"]
    agg_keys = result.keys()
    assert "format" in agg_keys
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
                "must": {"match_all": {}},
                "should": [
                    {"match": {"provenance.code": "NASJONAL"}},
                    {"term": {"nationalComponent": "true"}},
                    {
                        "bool": {
                            "must": [
                                {"term": {"accessRights.code.keyword": "PUBLIC"}},
                                {"term": {"isOpenData": "true"}},
                            ]
                        }
                    },
                ],
            }
        },
        "aggs": {
            "format": {
                "terms": {"field": "fdkFormatPrefixed.keyword", "size": 1000000000}
            },
            "los": {
                "terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}
            },
            "provenance": {"terms": {"field": "provenance.code.keyword"}},
            "orgPath": {
                "terms": {
                    "field": "publisher.orgPath",
                    "missing": "MISSING",
                    "size": 1000000000,
                }
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
            "accessRights": {
                "terms": {
                    "field": "accessRights.code.keyword",
                    "missing": "Ukjent",
                    "size": 10,
                }
            },
            "spatial": {"terms": {"field": "spatial.prefLabel.no.keyword"}},
        },
    }
    assert json.dumps(DataSetQuery().body) == json.dumps(expected_body)


@pytest.mark.unit
def test_dataset_with_query_string_query():
    expected = {
        "dis_max": {
            "queries": [
                {
                    "bool": {
                        "must": {
                            "multi_match": {
                                "query": "Elbiloversikt i",
                                "fields": [
                                    "title.en.raw",
                                    "title.nb.raw",
                                    "title.nn.raw",
                                    "title.no.raw",
                                ],
                            }
                        },
                        "should": [
                            {"match": {"provenance.code": "NASJONAL"}},
                            {"term": {"nationalComponent": "true"}},
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "accessRights.code.keyword": "PUBLIC"
                                            }
                                        },
                                        {"term": {"isOpenData": "true"}},
                                    ]
                                }
                            },
                        ],
                        "boost": 20,
                    }
                },
                {
                    "bool": {
                        "must": {
                            "dis_max": {
                                "queries": [
                                    {
                                        "multi_match": {
                                            "query": "Elbiloversikt i",
                                            "type": "bool_prefix",
                                            "fields": [
                                                "title.en.ngrams",
                                                "title.en.ngrams.2_gram",
                                                "title.en.ngrams.3_gram",
                                            ],
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Elbiloversikt i",
                                            "type": "bool_prefix",
                                            "fields": [
                                                "title.nb.ngrams",
                                                "title.nb.ngrams.2_gram",
                                                "title.nb.ngrams.3_gram",
                                            ],
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Elbiloversikt i",
                                            "type": "bool_prefix",
                                            "fields": [
                                                "title.nn.ngrams",
                                                "title.nn.ngrams.2_gram",
                                                "title.nn.ngrams.3_gram",
                                            ],
                                        }
                                    },
                                    {
                                        "multi_match": {
                                            "query": "Elbiloversikt i",
                                            "type": "bool_prefix",
                                            "fields": [
                                                "title.no.ngrams",
                                                "title.no.ngrams.2_gram",
                                                "title.no.ngrams.3_gram",
                                            ],
                                        }
                                    },
                                    {
                                        "query_string": {
                                            "query": "*Elbiloversikt* *i*",
                                            "fields": [
                                                "title.en.raw",
                                                "title.nb.raw",
                                                "title.nn.raw",
                                                "title.no.raw",
                                            ],
                                        }
                                    },
                                ],
                            }
                        },
                        "should": [
                            {"match": {"provenance.code": "NASJONAL"}},
                            {"term": {"nationalComponent": "true"}},
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "accessRights.code.keyword": "PUBLIC"
                                            }
                                        },
                                        {"term": {"isOpenData": "true"}},
                                    ]
                                }
                            },
                        ],
                        "boost": 10,
                    }
                },
                {
                    "bool": {
                        "must": {
                            "multi_match": {
                                "query": "Elbiloversikt i",
                                "fields": [
                                    "publisher.prefLabel.*",
                                    "publisher.title.*",
                                    "hasCompetentAuthority.prefLabel.*",
                                    "hasCompetentAuthority.name.*",
                                    "keyword.*",
                                ],
                            }
                        },
                        "should": [
                            {"match": {"provenance.code": "NASJONAL"}},
                            {"term": {"nationalComponent": "true"}},
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "accessRights.code.keyword": "PUBLIC"
                                            }
                                        },
                                        {"term": {"isOpenData": "true"}},
                                    ]
                                }
                            },
                        ],
                        "boost": 10,
                    }
                },
                {
                    "bool": {
                        "must": {
                            "simple_query_string": {
                                "query": "Elbiloversikt+i Elbiloversikt+i*",
                                "fields": [
                                    "description.en",
                                    "description.nb",
                                    "description.nn",
                                    "description.no",
                                ],
                            }
                        },
                        "should": [
                            {"match": {"provenance.code": "NASJONAL"}},
                            {"term": {"nationalComponent": "true"}},
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "accessRights.code.keyword": "PUBLIC"
                                            }
                                        },
                                        {"term": {"isOpenData": "true"}},
                                    ]
                                }
                            },
                        ],
                    }
                },
                {
                    "bool": {
                        "must": {
                            "simple_query_string": {
                                "query": "Elbiloversikt+i Elbiloversikt+i*",
                                "fields": [
                                    "accessRights.code",
                                    "accessRights.prefLabel.*^3",
                                    "description.*",
                                    "distribution.format",
                                    "distribution.title.*",
                                    "keyword.*^2",
                                    "losTheme.name.*^3",
                                    "objective.*",
                                    "publisher.name^3",
                                    "publisher.prefLabel^3",
                                    "subject.altLabel.*",
                                    "subject.definition.*",
                                    "subject.prefLabel.*",
                                    "theme.title.*",
                                    "title.*^3",
                                ],
                            }
                        },
                        "should": [
                            {"match": {"provenance.code": "NASJONAL"}},
                            {"term": {"nationalComponent": "true"}},
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "term": {
                                                "accessRights.code.keyword": "PUBLIC"
                                            }
                                        },
                                        {"term": {"isOpenData": "true"}},
                                    ]
                                }
                            },
                        ],
                        "boost": 0.02,
                    }
                },
            ]
        }
    }
    result = DataSetQuery("Elbiloversikt i").body["query"]
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
                                "bool": {
                                    "must": {
                                        "multi_match": {
                                            "query": "Ad",
                                            "fields": [
                                                "title.en.raw",
                                                "title.nb.raw",
                                                "title.nn.raw",
                                                "title.no.raw",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 20,
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "dis_max": {
                                            "queries": [
                                                {
                                                    "multi_match": {
                                                        "query": "Ad",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.en.ngrams",
                                                            "title.en.ngrams.2_gram",
                                                            "title.en.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "multi_match": {
                                                        "query": "Ad",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.nb.ngrams",
                                                            "title.nb.ngrams.2_gram",
                                                            "title.nb.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "multi_match": {
                                                        "query": "Ad",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.nn.ngrams",
                                                            "title.nn.ngrams.2_gram",
                                                            "title.nn.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "multi_match": {
                                                        "query": "Ad",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.no.ngrams",
                                                            "title.no.ngrams.2_gram",
                                                            "title.no.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "query_string": {
                                                        "query": "*Ad*",
                                                        "fields": [
                                                            "title.en.raw",
                                                            "title.nb.raw",
                                                            "title.nn.raw",
                                                            "title.no.raw",
                                                        ],
                                                    }
                                                },
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 10,
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "multi_match": {
                                            "query": "Ad",
                                            "fields": [
                                                "publisher.prefLabel.*",
                                                "publisher.title.*",
                                                "hasCompetentAuthority.prefLabel.*",
                                                "hasCompetentAuthority.name.*",
                                                "keyword.*",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 10,
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "simple_query_string": {
                                            "query": "Ad Ad*",
                                            "fields": [
                                                "description.en",
                                                "description.nb",
                                                "description.nn",
                                                "description.no",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "simple_query_string": {
                                            "query": "Ad Ad*",
                                            "fields": [
                                                "accessRights.code",
                                                "accessRights.prefLabel.*^3",
                                                "description.*",
                                                "distribution.format",
                                                "distribution.title.*",
                                                "keyword.*^2",
                                                "losTheme.name.*^3",
                                                "objective.*",
                                                "publisher.name^3",
                                                "publisher.prefLabel^3",
                                                "subject.altLabel.*",
                                                "subject.definition.*",
                                                "subject.prefLabel.*",
                                                "theme.title.*",
                                                "title.*^3",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 0.02,
                                }
                            },
                        ]
                    }
                }
            ],
            "filter": [{"term": {"spatial.prefLabel.no.keyword": "Norge"}}],
        }
    }
    result = DataSetQuery(search_string="Ad", filters=[{"spatial": "Norge"}]).body[
        "query"
    ]

    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_dataset_with_media_type_filter():
    expected = {
        "bool": {
            "must": [
                {
                    "dis_max": {
                        "queries": [
                            {
                                "bool": {
                                    "must": {
                                        "multi_match": {
                                            "query": "Fotball",
                                            "fields": [
                                                "title.en.raw",
                                                "title.nb.raw",
                                                "title.nn.raw",
                                                "title.no.raw",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 20,
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "dis_max": {
                                            "queries": [
                                                {
                                                    "multi_match": {
                                                        "query": "Fotball",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.en.ngrams",
                                                            "title.en.ngrams.2_gram",
                                                            "title.en.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "multi_match": {
                                                        "query": "Fotball",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.nb.ngrams",
                                                            "title.nb.ngrams.2_gram",
                                                            "title.nb.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "multi_match": {
                                                        "query": "Fotball",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.nn.ngrams",
                                                            "title.nn.ngrams.2_gram",
                                                            "title.nn.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "multi_match": {
                                                        "query": "Fotball",
                                                        "type": "bool_prefix",
                                                        "fields": [
                                                            "title.no.ngrams",
                                                            "title.no.ngrams.2_gram",
                                                            "title.no.ngrams.3_gram",
                                                        ],
                                                    }
                                                },
                                                {
                                                    "query_string": {
                                                        "query": "*Fotball*",
                                                        "fields": [
                                                            "title.en.raw",
                                                            "title.nb.raw",
                                                            "title.nn.raw",
                                                            "title.no.raw",
                                                        ],
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 10,
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "multi_match": {
                                            "query": "Fotball",
                                            "fields": [
                                                "publisher.prefLabel.*",
                                                "publisher.title.*",
                                                "hasCompetentAuthority.prefLabel.*",
                                                "hasCompetentAuthority.name.*",
                                                "keyword.*",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 10,
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "simple_query_string": {
                                            "query": "Fotball Fotball*",
                                            "fields": [
                                                "description.en",
                                                "description.nb",
                                                "description.nn",
                                                "description.no",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "simple_query_string": {
                                            "query": "Fotball Fotball*",
                                            "fields": [
                                                "accessRights.code",
                                                "accessRights.prefLabel.*^3",
                                                "description.*",
                                                "distribution.format",
                                                "distribution.title.*",
                                                "keyword.*^2",
                                                "losTheme.name.*^3",
                                                "objective.*",
                                                "publisher.name^3",
                                                "publisher.prefLabel^3",
                                                "subject.altLabel.*",
                                                "subject.definition.*",
                                                "subject.prefLabel.*",
                                                "theme.title.*",
                                                "title.*^3",
                                            ],
                                        }
                                    },
                                    "should": [
                                        {"match": {"provenance.code": "NASJONAL"}},
                                        {"term": {"nationalComponent": "true"}},
                                        {
                                            "bool": {
                                                "must": [
                                                    {
                                                        "term": {
                                                            "accessRights.code.keyword": "PUBLIC"
                                                        }
                                                    },
                                                    {"term": {"isOpenData": "true"}},
                                                ]
                                            }
                                        },
                                    ],
                                    "boost": 0.02,
                                }
                            },
                        ]
                    }
                }
            ],
            "filter": [
                {"term": {"distribution.mediaType.code.keyword": "application/json"}}
            ],
        }
    }
    result = DataSetQuery(
        search_string="Fotball",
        filters=[{"distribution.mediaType.code.keyword": "application/json"}],
    ).body["query"]

    assert json.dumps(result) == json.dumps(expected)
