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
        "indices_boost": {
            "datasets": 1.2
        },
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
                            "boost": 0.01,
                            "default_operator": "or"
                        }
                    },
                    {
                        "term": {
                            "title.nb.raw": "stønad"
                        }
                    },
                    {
                        "term": {
                            "title.raw": "stønad"
                        }
                    },
                    {
                        "term": {
                            "prefLabel.nb.raw": "stønad"
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
    result = AllIndicesQuery(search_string="stønad")
    assert json.dumps(result.query) == json.dumps(expected)


@pytest.mark.unit
def test_all_indices_should_return_query_with_filter():
    expected = {
        "indices_boost": {
            "datasets": 1.2
        },
        "query": {
            "bool": {
                "must": [{
                    "dis_max": {
                        "queries": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "constant_score": {
                                                "filter": {
                                                    "simple_query_string": {
                                                        "query": "barnehage barnehage*",
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
                                    "query": "barnehage barnehage*",
                                    "boost": 0.01,
                                    "default_operator": "or"
                                }
                            },
                            {
                                "term": {
                                    "title.nb.raw": "barnehage"
                                }
                            },
                            {
                                "term": {
                                    "title.raw": "barnehage"
                                }
                            },
                            {
                                "term": {
                                    "prefLabel.nb.raw": "barnehage"
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
    result = AllIndicesQuery(search_string="barnehage", filters=[{'orgPath': '/KOMMUNE/840029212'}])
    assert json.dumps(result.query) == json.dumps(expected)


@pytest.mark.unit
def test_all_indices_should_return_query_with_must_not():
    expected = {
        "indices_boost": {
            "datasets": 1.2
        },
        "query": {
        "bool": {
            "must": [
                {
                    "dis_max": {
                        "queries": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "constant_score": {
                                                "filter": {
                                                    "simple_query_string": {
                                                        "query": "barnehage barnehage*",
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
                                    "query": "barnehage barnehage*",
                                    "boost": 0.01,
                                    "default_operator": "or"
                                }
                            },
                            {
                                "term": {
                                    "title.nb.raw": "barnehage"
                                }
                            },
                            {
                                "term": {
                                    "title.raw": "barnehage"
                                }
                            },
                            {
                                "term": {
                                    "prefLabel.nb.raw": "barnehage"
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
                        		"field":"publisher.orgPath"
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
    result = AllIndicesQuery(search_string="barnehage", filters=[{'orgPath': 'MISSING'}])
    assert json.dumps(result.query) == json.dumps(expected)
