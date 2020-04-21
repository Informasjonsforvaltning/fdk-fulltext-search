import json

import pytest

from src.search.queries import RecentQuery, AllIndicesQuery
from src.search.query_utils import open_data_filter


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
def test_all_indices_query_should_return_query_with_dis_max():
    search_str = "stønad"
    expected = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": search_str,
                                    "fields": [
                                        "prefLabel.*.raw",
                                        "title.*.raw",
                                        "title.raw"
                                    ]
                                }
                            },
                            "should": [
                                {
                                    "bool": {
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
                            ],
                            "boost": 5
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": search_str,
                                    "type": "phrase_prefix",
                                    "fields": [
                                        "title.*.ngrams",
                                        "title.*.ngrams.2_gram",
                                        "title.*.ngrams.3_gram",
                                        "title.ngrams",
                                        "title.ngrams.2_gram",
                                        "title.ngrams.3_gram",
                                        "prefLabel.*.ngrams",
                                        "prefLabel.*.ngrams.2_gram",
                                        "prefLabel.*.ngrams.3_gram"
                                    ]
                                }
                            },
                            "should": [
                                {
                                    "bool": {
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
                            ],
                            "boost": 2
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "simple_query_string": {
                                    "query": "{0} {0}*".format(search_str.replace(" ", "+")),
                                    "fields": [
                                        "description",
                                        "definition.text.*",
                                        "schema^0.5"
                                    ]
                                }
                            },
                            "should": [
                                {
                                    "bool": {
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
                            ]
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "simple_query_string": {
                                    "query": "{0} {0}*".format(search_str.replace(" ", "+"))
                                }
                            },
                            "should": [
                                {
                                    "bool": {
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
                            ],
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
            },
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {
                            "term": {
                                "isOpenAccess": "true"
                            }
                        },
                        "isOpenLicense": {
                            "term": {
                                "isOpenLicense": "true"
                            }
                        },
                        "isFree": {
                            "term": {
                                "isFree": "true"
                            }
                        }
                    }
                }
            },
            "dataset_access": {
                "filter": {
                    "term": {
                        "_index": "datasets"
                    }
                },
                "aggs": {
                    "accessRights": {
                        "terms": {
                            "field": "accessRights.code.keyword",
                            "missing": "Ukjent",
                            "size": 10
                        }
                    }
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
            }
        }

    }
    result = AllIndicesQuery(search_string="stønad")
    assert json.dumps(result.query) == json.dumps(expected)


@pytest.mark.unit
def test_all_indices_should_return_query_with_filter():
    search_str = "barnehage"
    expected = {
        "query": {
            "bool": {
                "must": [{
                    "dis_max": {
                        "queries": [
                            {
                                "bool": {
                                    "must": {
                                        "multi_match": {
                                            "query": search_str,
                                            "fields": [
                                                "prefLabel.*.raw",
                                                "title.*.raw",
                                                "title.raw"
                                            ]
                                        }
                                    },
                                    "should": [
                                        {
                                            "bool": {
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
                                    ],
                                    "boost": 5
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "multi_match": {
                                            "query": search_str,
                                            "type": "phrase_prefix",
                                            "fields": [
                                                "title.*.ngrams",
                                                "title.*.ngrams.2_gram",
                                                "title.*.ngrams.3_gram",
                                                "title.ngrams",
                                                "title.ngrams.2_gram",
                                                "title.ngrams.3_gram",
                                                "prefLabel.*.ngrams",
                                                "prefLabel.*.ngrams.2_gram",
                                                "prefLabel.*.ngrams.3_gram"
                                            ]
                                        }
                                    },
                                    "should": [
                                        {
                                            "bool": {
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
                                    ],
                                    "boost": 2
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "simple_query_string": {
                                            "query": "{0} {0}*".format(search_str.replace(" ", "+")),
                                            "fields": [
                                                "description",
                                                "definition.text.*",
                                                "schema^0.5"
                                            ]
                                        }
                                    },
                                    "should": [
                                        {
                                            "bool": {
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
                                    ]
                                }
                            },
                            {
                                "bool": {
                                    "must": {
                                        "simple_query_string": {
                                            "query": "{0} {0}*".format(search_str.replace(" ", "+"))
                                        }
                                    },
                                    "should": [
                                        {
                                            "bool": {
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
                                    ],
                                    "boost": 0.001
                                }
                            }
                        ]
                    }
                }],
                "filter": [
                    {
                        "term": {
                            "publisher.orgPath": "/KOMMUNE/840029212"
                        }
                    }
                ],
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
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {
                            "term": {
                                "isOpenAccess": "true"
                            }
                        },
                        "isOpenLicense": {
                            "term": {
                                "isOpenLicense": "true"
                            }
                        },
                        "isFree": {
                            "term": {
                                "isFree": "true"
                            }
                        }
                    }
                }
            },
            "dataset_access": {
                "filter": {
                    "term": {
                        "_index": "datasets"
                    }
                },
                "aggs": {
                    "accessRights": {
                        "terms": {
                            "field": "accessRights.code.keyword",
                            "missing": "Ukjent",
                            "size": 10
                        }
                    }
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
            }
        }
    }
    result = AllIndicesQuery(search_string="barnehage", filters=[{'orgPath': '/KOMMUNE/840029212'}])
    assert json.dumps(result.query) == json.dumps(expected)


@pytest.mark.unit
def test_all_indices_should_return_query_with_must_not():
    search_str = "barnehage"
    expected = {
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
                                                "query": search_str,
                                                "fields": [
                                                    "prefLabel.*.raw",
                                                    "title.*.raw",
                                                    "title.raw"
                                                ]
                                            }
                                        },
                                        "should": [
                                            {
                                                "bool": {
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
                                        ],
                                        "boost": 5
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "multi_match": {
                                                "query": search_str,
                                                "type": "phrase_prefix",
                                                "fields": [
                                                    "title.*.ngrams",
                                                    "title.*.ngrams.2_gram",
                                                    "title.*.ngrams.3_gram",
                                                    "title.ngrams",
                                                    "title.ngrams.2_gram",
                                                    "title.ngrams.3_gram",
                                                    "prefLabel.*.ngrams",
                                                    "prefLabel.*.ngrams.2_gram",
                                                    "prefLabel.*.ngrams.3_gram"
                                                ]
                                            }
                                        },
                                        "should": [
                                            {
                                                "bool": {
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
                                        ],
                                        "boost": 2
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "simple_query_string": {
                                                "query": "{0} {0}*".format(search_str.replace(" ", "+")),
                                                "fields": [
                                                    "description",
                                                    "definition.text.*",
                                                    "schema^0.5"
                                                ]
                                            }
                                        },
                                        "should": [
                                            {
                                                "bool": {
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
                                        ]
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "simple_query_string": {
                                                "query": "{0} {0}*".format(search_str.replace(" ", "+"))
                                            }
                                        },
                                        "should": [
                                            {
                                                "bool": {
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
                                        ],
                                        "boost": 0.001
                                    }
                                }
                            ]
                        }
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
            },
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {
                            "term": {
                                "isOpenAccess": "true"
                            }
                        },
                        "isOpenLicense": {
                            "term": {
                                "isOpenLicense": "true"
                            }
                        },
                        "isFree": {
                            "term": {
                                "isFree": "true"
                            }
                        }
                    }
                }
            },
            "dataset_access": {
                "filter": {
                    "term": {
                        "_index": "datasets"
                    }
                },
                "aggs": {
                    "accessRights": {
                        "terms": {
                            "field": "accessRights.code.keyword",
                            "missing": "Ukjent",
                            "size": 10
                        }
                    }
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
            }
        }
    }
    result = AllIndicesQuery(search_string="barnehage", filters=[{'orgPath': 'MISSING'}])
    assert json.dumps(result.query) == json.dumps(expected)


@pytest.mark.unit
def test_add_filter_should_add_opendata_filter():
    builder = AllIndicesQuery(filters=[{"opendata": "true"}, {"other": "filter"}], search_string="something")
    has_open_data = False
    for f in builder.query["query"]["bool"]["filter"]:
        if f == open_data_filter():
            has_open_data = True
            break
    assert has_open_data is True


@pytest.mark.unit
def test_add_filter_should_add_must_not_filter_for_Ukjent():
    must_no_access_rights = {'exists': {'field': 'accessRights.code.keyword'}}
    index_filter = {
            "term": {
                "_index": "datasets"
            }
    }
    builder = AllIndicesQuery(filters=[{"accessRights": "Ukjent"}, {"other": "filter"}], search_string="something")
    has_must_not = False
    has_index_filter = False
    for f in builder.query['query']['bool']['filter']:
        if 'bool' in f.keys():
            if 'must_not' in f['bool'].keys() and f['bool']['must_not'] == must_no_access_rights:
                has_must_not = True
            if 'must' in f['bool'].keys() and f['bool']['must'] == index_filter:
                has_index_filter = True
        if has_must_not and has_index_filter:
            break

    assert has_must_not is True
    assert has_index_filter is True


correct_query_clause = {
    "dis_max": {
        "queries": [
            {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": "åpne data",
                            "fields": [
                                "prefLabel.*.raw",
                                "title.*.raw",
                                "title.raw"
                            ]
                        }
                    },
                    "should": [
                        {
                            "bool": {
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
                    ],
                    "boost": 5
                }
            },
            {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": "åpne data",
                            "type": "phrase_prefix",
                            "fields": [
                                "title.*.ngrams",
                                "title.*.ngrams.2_gram",
                                "title.*.ngrams.3_gram",
                                "title.ngrams",
                                "title.ngrams.2_gram",
                                "title.ngrams.3_gram",
                                "prefLabel.*.ngrams",
                                "prefLabel.*.ngrams.2_gram",
                                "prefLabel.*.ngrams.3_gram"
                            ]
                        }
                    },
                    "should": [
                        {
                            "bool": {
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
                    ],
                    "boost": 2
                }
            },
            {
                "bool": {
                    "must": {
                        "simple_query_string": {
                            "query": "åpne+data åpne+data*",
                            "fields": [
                                "description",
                                "definition.text.*",
                                "schema"
                            ]
                        }
                    },
                    "should": [
                        {
                            "bool": {
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
                    ],
                    "boost": 1.5
                }
            },
            {
                "bool": {
                    "must": {
                        "simple_query_string": {
                            "query": "åpne+data åpne+data*"
                        }
                    },
                    "should": [
                        {
                            "bool": {
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
                    ],
                    "boost": 0.001
                }
            }
        ]
    }
}
