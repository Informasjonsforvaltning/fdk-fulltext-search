import json

import pytest

from fdk_fulltext_search.ingest.utils import IndicesKey
from fdk_fulltext_search.search.queries import (
    AllIndicesQuery,
    RecentQuery,
    SuggestionQuery,
)
from fdk_fulltext_search.search.query_utils import open_data_query


@pytest.mark.unit
def test_recent_query_should_have_size_5():
    expected = {"size": 5, "sort": {"harvest.firstHarvested": {"order": "desc"}}}
    result = RecentQuery().query
    assert result.keys() == expected.keys()
    assert result["size"] == expected["size"]
    assert result["sort"] == result["sort"]


@pytest.mark.unit
def test_recent_query_should_have_size_18():
    expected = {"size": 18, "sort": {"harvest.firstHarvested": {"order": "desc"}}}
    result = RecentQuery(18).query
    assert result.keys() == expected.keys()
    assert result["size"] == expected["size"]
    assert result["sort"] == result["sort"]


@pytest.mark.unit
def test_all_indices_query_should_return_query_with_dis_max():
    expected = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": "stønad",
                                    "fields": [
                                        "prefLabel.en.raw",
                                        "prefLabel.nb.raw",
                                        "prefLabel.nn.raw",
                                        "prefLabel.no.raw",
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
                                                    "distribution.openLicense": "true"
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
                                                "query": "stønad",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.en.ngrams",
                                                    "prefLabel.en.ngrams.2_gram",
                                                    "prefLabel.en.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "stønad",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.nb.ngrams",
                                                    "prefLabel.nb.ngrams.2_gram",
                                                    "prefLabel.nb.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "stønad",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.nn.ngrams",
                                                    "prefLabel.nn.ngrams.2_gram",
                                                    "prefLabel.nn.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "stønad",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.no.ngrams",
                                                    "prefLabel.no.ngrams.2_gram",
                                                    "prefLabel.no.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "stønad",
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
                                                "query": "stønad",
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
                                                "query": "stønad",
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
                                                "query": "stønad",
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
                                                "query": "*stønad*",
                                                "fields": [
                                                    "prefLabel.en.raw",
                                                    "prefLabel.nb.raw",
                                                    "prefLabel.nn.raw",
                                                    "prefLabel.no.raw",
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
                                                    "distribution.openLicense": "true"
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
                                    "query": "stønad",
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
                                                    "distribution.openLicense": "true"
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
                                    "query": "stønad stønad*",
                                    "fields": [
                                        "definition.text.en",
                                        "definition.text.nb",
                                        "definition.text.nn",
                                        "definition.text.no",
                                        "description.en",
                                        "description.nb",
                                        "description.nn",
                                        "description.no",
                                        "schema^0.5",
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
                                                    "distribution.openLicense": "true"
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
                                    "query": "stønad stønad*",
                                    "fields": [
                                        "accessRights.code",
                                        "accessRights.prefLabel.*^3",
                                        "definition.source.prefLabel.*^3",
                                        "definition.sourceRelationship",
                                        "definition.sources.text.*",
                                        "definition.text.*",
                                        "description.*",
                                        "distribution.format",
                                        "distribution.title.*",
                                        "expandedLosTema.*",
                                        "hasCompetentAuthority.name^3",
                                        "hasCompetentAuthority.prefLabel^3",
                                        "keyword.*^2",
                                        "losTheme.name.^3",
                                        "mediaType.code",
                                        "objective.*",
                                        "prefLabel.*^3",
                                        "publisher.name^3",
                                        "publisher.prefLabel^3",
                                        "subject.*",
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
                                            {
                                                "term": {
                                                    "distribution.openLicense": "true"
                                                }
                                            },
                                        ]
                                    }
                                },
                            ],
                            "boost": 0.02,
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "query_string": {
                                    "query": "*stønad*",
                                    "fields": [
                                        "accessRights.code",
                                        "accessRights.prefLabel.*^3",
                                        "definition.source.prefLabel.*^3",
                                        "definition.sourceRelationship",
                                        "definition.sources.text.*",
                                        "definition.text.*",
                                        "description.*",
                                        "distribution.format",
                                        "distribution.title.*",
                                        "expandedLosTema.*",
                                        "hasCompetentAuthority.name^3",
                                        "hasCompetentAuthority.prefLabel^3",
                                        "keyword.*^2",
                                        "losTheme.name.^3",
                                        "mediaType.code",
                                        "objective.*",
                                        "prefLabel.*^3",
                                        "publisher.name^3",
                                        "publisher.prefLabel^3",
                                        "subject.*",
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
                                            {
                                                "term": {
                                                    "distribution.openLicense": "true"
                                                }
                                            },
                                        ]
                                    }
                                },
                            ],
                            "boost": 0.001,
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
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {"term": {"isOpenAccess": "true"}},
                        "isOpenLicense": {"term": {"isOpenLicense": "true"}},
                        "isFree": {"term": {"isFree": "true"}},
                    }
                }
            },
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
                            {"term": {"distribution.openLicense": "true"}},
                        ]
                    }
                }
            },
            "theme": {"terms": {"field": "euTheme"}},
        },
    }
    result = AllIndicesQuery(search_string="stønad")
    assert json.dumps(result.body) == json.dumps(expected)


@pytest.mark.unit
def test_empty_all_indices_query():
    """Should return query with high boost on authority and datasets and lower boost for authority and dataservices"""
    expected_query = {
        "bool": {
            "must": {"match_all": {}},
            "should": [
                {"match": {"provenance.code": "NASJONAL"}},
                {"term": {"nationalComponent": "true"}},
                {
                    "bool": {
                        "must": [
                            {"term": {"accessRights.code.keyword": "PUBLIC"}},
                            {"term": {"distribution.openLicense": "true"}},
                        ]
                    }
                },
            ],
        }
    }
    expected_indices_boost = [{"datasets": 1.2}]
    result = AllIndicesQuery().body
    assert json.dumps(result["indices_boost"]) == json.dumps(expected_indices_boost)
    assert json.dumps(result["query"]) == json.dumps(expected_query)


@pytest.mark.unit
def test_all_indices_should_return_query_with_filter():
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
                                                "query": "barnehage",
                                                "fields": [
                                                    "prefLabel.en.raw",
                                                    "prefLabel.nb.raw",
                                                    "prefLabel.nn.raw",
                                                    "prefLabel.no.raw",
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
                                                                "distribution.openLicense": "true"
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
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.en.ngrams",
                                                                "prefLabel.en.ngrams.2_gram",
                                                                "prefLabel.en.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.nb.ngrams",
                                                                "prefLabel.nb.ngrams.2_gram",
                                                                "prefLabel.nb.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.nn.ngrams",
                                                                "prefLabel.nn.ngrams.2_gram",
                                                                "prefLabel.nn.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.no.ngrams",
                                                                "prefLabel.no.ngrams.2_gram",
                                                                "prefLabel.no.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
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
                                                            "query": "barnehage",
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
                                                            "query": "barnehage",
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
                                                            "query": "barnehage",
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
                                                            "query": "*barnehage*",
                                                            "fields": [
                                                                "prefLabel.en.raw",
                                                                "prefLabel.nb.raw",
                                                                "prefLabel.nn.raw",
                                                                "prefLabel.no.raw",
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
                                                        {
                                                            "term": {
                                                                "distribution.openLicense": "true"
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
                                                "query": "barnehage",
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
                                                                "distribution.openLicense": "true"
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
                                                "query": "barnehage barnehage*",
                                                "fields": [
                                                    "definition.text.en",
                                                    "definition.text.nb",
                                                    "definition.text.nn",
                                                    "definition.text.no",
                                                    "description.en",
                                                    "description.nb",
                                                    "description.nn",
                                                    "description.no",
                                                    "schema^0.5",
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
                                                                "distribution.openLicense": "true"
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
                                                "query": "barnehage barnehage*",
                                                "fields": [
                                                    "accessRights.code",
                                                    "accessRights.prefLabel.*^3",
                                                    "definition.source.prefLabel.*^3",
                                                    "definition.sourceRelationship",
                                                    "definition.sources.text.*",
                                                    "definition.text.*",
                                                    "description.*",
                                                    "distribution.format",
                                                    "distribution.title.*",
                                                    "expandedLosTema.*",
                                                    "hasCompetentAuthority.name^3",
                                                    "hasCompetentAuthority.prefLabel^3",
                                                    "keyword.*^2",
                                                    "losTheme.name.^3",
                                                    "mediaType.code",
                                                    "objective.*",
                                                    "prefLabel.*^3",
                                                    "publisher.name^3",
                                                    "publisher.prefLabel^3",
                                                    "subject.*",
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
                                                        {
                                                            "term": {
                                                                "distribution.openLicense": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 0.02,
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "query_string": {
                                                "query": "*barnehage*",
                                                "fields": [
                                                    "accessRights.code",
                                                    "accessRights.prefLabel.*^3",
                                                    "definition.source.prefLabel.*^3",
                                                    "definition.sourceRelationship",
                                                    "definition.sources.text.*",
                                                    "definition.text.*",
                                                    "description.*",
                                                    "distribution.format",
                                                    "distribution.title.*",
                                                    "expandedLosTema.*",
                                                    "hasCompetentAuthority.name^3",
                                                    "hasCompetentAuthority.prefLabel^3",
                                                    "keyword.*^2",
                                                    "losTheme.name.^3",
                                                    "mediaType.code",
                                                    "objective.*",
                                                    "prefLabel.*^3",
                                                    "publisher.name^3",
                                                    "publisher.prefLabel^3",
                                                    "subject.*",
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
                                                        {
                                                            "term": {
                                                                "distribution.openLicense": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 0.001,
                                    }
                                },
                            ]
                        }
                    }
                ],
                "filter": [{"term": {"publisher.orgPath": "/KOMMUNE/840029212"}}],
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
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {"term": {"isOpenAccess": "true"}},
                        "isOpenLicense": {"term": {"isOpenLicense": "true"}},
                        "isFree": {"term": {"isFree": "true"}},
                    }
                }
            },
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
                            {"term": {"distribution.openLicense": "true"}},
                        ]
                    }
                }
            },
            "theme": {"terms": {"field": "euTheme"}},
        },
    }
    result = AllIndicesQuery(
        search_string="barnehage", filters=[{"orgPath": "/KOMMUNE/840029212"}]
    )
    assert json.dumps(result.body) == json.dumps(expected)


@pytest.mark.unit
def test_all_indices_with_several_words():
    """ should return query with simple query string query for title"""
    search_string = "some string"
    expected = {
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "bool": {
                            "must": {
                                "multi_match": {
                                    "query": "some string",
                                    "fields": [
                                        "prefLabel.en.raw",
                                        "prefLabel.nb.raw",
                                        "prefLabel.nn.raw",
                                        "prefLabel.no.raw",
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
                                                    "distribution.openLicense": "true"
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
                                                "query": "some string",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.en.ngrams",
                                                    "prefLabel.en.ngrams.2_gram",
                                                    "prefLabel.en.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "some string",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.nb.ngrams",
                                                    "prefLabel.nb.ngrams.2_gram",
                                                    "prefLabel.nb.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "some string",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.nn.ngrams",
                                                    "prefLabel.nn.ngrams.2_gram",
                                                    "prefLabel.nn.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "some string",
                                                "type": "bool_prefix",
                                                "fields": [
                                                    "prefLabel.no.ngrams",
                                                    "prefLabel.no.ngrams.2_gram",
                                                    "prefLabel.no.ngrams.3_gram",
                                                ],
                                            }
                                        },
                                        {
                                            "multi_match": {
                                                "query": "some string",
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
                                                "query": "some string",
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
                                                "query": "some string",
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
                                                "query": "some string",
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
                                                "query": "*some* *string*",
                                                "fields": [
                                                    "prefLabel.en.raw",
                                                    "prefLabel.nb.raw",
                                                    "prefLabel.nn.raw",
                                                    "prefLabel.no.raw",
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
                                            {
                                                "term": {
                                                    "distribution.openLicense": "true"
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
                                    "query": "some string",
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
                                                    "distribution.openLicense": "true"
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
                                    "query": "some+string some+string*",
                                    "fields": [
                                        "definition.text.en",
                                        "definition.text.nb",
                                        "definition.text.nn",
                                        "definition.text.no",
                                        "description.en",
                                        "description.nb",
                                        "description.nn",
                                        "description.no",
                                        "schema^0.5",
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
                                                    "distribution.openLicense": "true"
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
                                    "query": "some+string some+string*",
                                    "fields": [
                                        "accessRights.code",
                                        "accessRights.prefLabel.*^3",
                                        "definition.source.prefLabel.*^3",
                                        "definition.sourceRelationship",
                                        "definition.sources.text.*",
                                        "definition.text.*",
                                        "description.*",
                                        "distribution.format",
                                        "distribution.title.*",
                                        "expandedLosTema.*",
                                        "hasCompetentAuthority.name^3",
                                        "hasCompetentAuthority.prefLabel^3",
                                        "keyword.*^2",
                                        "losTheme.name.^3",
                                        "mediaType.code",
                                        "objective.*",
                                        "prefLabel.*^3",
                                        "publisher.name^3",
                                        "publisher.prefLabel^3",
                                        "subject.*",
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
                                            {
                                                "term": {
                                                    "distribution.openLicense": "true"
                                                }
                                            },
                                        ]
                                    }
                                },
                            ],
                            "boost": 0.02,
                        }
                    },
                    {
                        "bool": {
                            "must": {
                                "query_string": {
                                    "query": "*some* *string*",
                                    "fields": [
                                        "accessRights.code",
                                        "accessRights.prefLabel.*^3",
                                        "definition.source.prefLabel.*^3",
                                        "definition.sourceRelationship",
                                        "definition.sources.text.*",
                                        "definition.text.*",
                                        "description.*",
                                        "distribution.format",
                                        "distribution.title.*",
                                        "expandedLosTema.*",
                                        "hasCompetentAuthority.name^3",
                                        "hasCompetentAuthority.prefLabel^3",
                                        "keyword.*^2",
                                        "losTheme.name.^3",
                                        "mediaType.code",
                                        "objective.*",
                                        "prefLabel.*^3",
                                        "publisher.name^3",
                                        "publisher.prefLabel^3",
                                        "subject.*",
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
                                            {
                                                "term": {
                                                    "distribution.openLicense": "true"
                                                }
                                            },
                                        ]
                                    }
                                },
                            ],
                            "boost": 0.001,
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
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {"term": {"isOpenAccess": "true"}},
                        "isOpenLicense": {"term": {"isOpenLicense": "true"}},
                        "isFree": {"term": {"isFree": "true"}},
                    }
                }
            },
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
                            {"term": {"distribution.openLicense": "true"}},
                        ]
                    }
                }
            },
            "theme": {"terms": {"field": "euTheme"}},
        },
    }
    result = AllIndicesQuery(search_string=search_string)
    assert json.dumps(result.body) == json.dumps(expected)


@pytest.mark.unit
def test_add_filter_should_add_opendata_filter():
    builder = AllIndicesQuery(
        filters=[{"opendata": "true"}, {"other": "filter"}], search_string="something"
    )
    has_open_data = False
    for f in builder.body["query"]["bool"]["filter"]:
        if f == open_data_query():
            has_open_data = True
            break
    assert has_open_data is True


@pytest.mark.unit
def test_add_filter_should_add_multiple_los_filters():
    builder = AllIndicesQuery(
        filters=[{"los": "helse-og-omsorg,naring"}, {"other": "filter"}],
        search_string="something",
    )
    los_count = 0
    for f in builder.body["query"]["bool"]["filter"]:
        if "term" in f.keys() and "losTheme.losPaths.keyword" in f["term"].keys():
            los_count += 1
    assert los_count == 2


@pytest.mark.unit
def test_add_filter_should_add_must_not_filter_for_ukjent():
    must_no_access_rights = {"exists": {"field": "accessRights.code.keyword"}}
    index_filter = {"term": {"_index": "datasets"}}
    builder = AllIndicesQuery(
        filters=[{"accessRights": "Ukjent"}, {"other": "filter"}],
        search_string="something",
    )
    has_must_not = False
    has_index_filter = False
    for f in builder.body["query"]["bool"]["filter"]:
        if "bool" in f.keys():
            if (
                "must_not" in f["bool"].keys()
                and f["bool"]["must_not"] == must_no_access_rights
            ):
                has_must_not = True
            if "must" in f["bool"].keys() and f["bool"]["must"] == index_filter:
                has_index_filter = True
        if has_must_not and has_index_filter:
            break

    assert has_must_not is True
    assert has_index_filter is True


@pytest.mark.unit
def test_all_indices_should_return_query_with_must_not():
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
                                                "query": "barnehage",
                                                "fields": [
                                                    "prefLabel.en.raw",
                                                    "prefLabel.nb.raw",
                                                    "prefLabel.nn.raw",
                                                    "prefLabel.no.raw",
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
                                                                "distribution.openLicense": "true"
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
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.en.ngrams",
                                                                "prefLabel.en.ngrams.2_gram",
                                                                "prefLabel.en.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.nb.ngrams",
                                                                "prefLabel.nb.ngrams.2_gram",
                                                                "prefLabel.nb.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.nn.ngrams",
                                                                "prefLabel.nn.ngrams.2_gram",
                                                                "prefLabel.nn.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
                                                            "type": "bool_prefix",
                                                            "fields": [
                                                                "prefLabel.no.ngrams",
                                                                "prefLabel.no.ngrams.2_gram",
                                                                "prefLabel.no.ngrams.3_gram",
                                                            ],
                                                        }
                                                    },
                                                    {
                                                        "multi_match": {
                                                            "query": "barnehage",
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
                                                            "query": "barnehage",
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
                                                            "query": "barnehage",
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
                                                            "query": "barnehage",
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
                                                            "query": "*barnehage*",
                                                            "fields": [
                                                                "prefLabel.en.raw",
                                                                "prefLabel.nb.raw",
                                                                "prefLabel.nn.raw",
                                                                "prefLabel.no.raw",
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
                                                                "distribution.openLicense": "true"
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
                                                "query": "barnehage",
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
                                                                "distribution.openLicense": "true"
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
                                                "query": "barnehage barnehage*",
                                                "fields": [
                                                    "definition.text.en",
                                                    "definition.text.nb",
                                                    "definition.text.nn",
                                                    "definition.text.no",
                                                    "description.en",
                                                    "description.nb",
                                                    "description.nn",
                                                    "description.no",
                                                    "schema^0.5",
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
                                                                "distribution.openLicense": "true"
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
                                                "query": "barnehage barnehage*",
                                                "fields": [
                                                    "accessRights.code",
                                                    "accessRights.prefLabel.*^3",
                                                    "definition.source.prefLabel.*^3",
                                                    "definition.sourceRelationship",
                                                    "definition.sources.text.*",
                                                    "definition.text.*",
                                                    "description.*",
                                                    "distribution.format",
                                                    "distribution.title.*",
                                                    "expandedLosTema.*",
                                                    "hasCompetentAuthority.name^3",
                                                    "hasCompetentAuthority.prefLabel^3",
                                                    "keyword.*^2",
                                                    "losTheme.name.^3",
                                                    "mediaType.code",
                                                    "objective.*",
                                                    "prefLabel.*^3",
                                                    "publisher.name^3",
                                                    "publisher.prefLabel^3",
                                                    "subject.*",
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
                                                        {
                                                            "term": {
                                                                "distribution.openLicense": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 0.02,
                                    }
                                },
                                {
                                    "bool": {
                                        "must": {
                                            "query_string": {
                                                "query": "*barnehage*",
                                                "fields": [
                                                    "accessRights.code",
                                                    "accessRights.prefLabel.*^3",
                                                    "definition.source.prefLabel.*^3",
                                                    "definition.sourceRelationship",
                                                    "definition.sources.text.*",
                                                    "definition.text.*",
                                                    "description.*",
                                                    "distribution.format",
                                                    "distribution.title.*",
                                                    "expandedLosTema.*",
                                                    "hasCompetentAuthority.name^3",
                                                    "hasCompetentAuthority.prefLabel^3",
                                                    "keyword.*^2",
                                                    "losTheme.name.^3",
                                                    "mediaType.code",
                                                    "objective.*",
                                                    "prefLabel.*^3",
                                                    "publisher.name^3",
                                                    "publisher.prefLabel^3",
                                                    "subject.*",
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
                                                        {
                                                            "term": {
                                                                "distribution.openLicense": "true"
                                                            }
                                                        },
                                                    ]
                                                }
                                            },
                                        ],
                                        "boost": 0.001,
                                    }
                                },
                            ]
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
            "availability": {
                "filters": {
                    "filters": {
                        "isOpenAccess": {"term": {"isOpenAccess": "true"}},
                        "isOpenLicense": {"term": {"isOpenLicense": "true"}},
                        "isFree": {"term": {"isFree": "true"}},
                    }
                }
            },
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
                            {"term": {"distribution.openLicense": "true"}},
                        ]
                    }
                }
            },
            "theme": {"terms": {"field": "euTheme"}},
        },
    }
    result = AllIndicesQuery(
        search_string="barnehage", filters=[{"orgPath": "MISSING"}]
    )
    assert json.dumps(result.body) == json.dumps(expected)


@pytest.mark.unit
def test_add_filter_should_add_x_last_days_filter():
    builder = AllIndicesQuery(filters=[{"last_x_days": 6}])
    has_x_last_days = False
    for f in builder.body["query"]["bool"]["filter"]:
        if f == {
            "range": {"harvest.firstHarvested": {"gte": "now-6d/d", "lt": "now+1d/d"}}
        }:
            has_x_last_days = True
            break
    assert has_x_last_days is True


@pytest.mark.unit
def test_suggestion_query_data_sett():
    expected_body = {
        "_source": ["title", "uri"],
        "query": {
            "dis_max": {
                "queries": [
                    {
                        "multi_match": {
                            "query": "Giv",
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
                            "query": "Giv",
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
                            "query": "Giv",
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
                            "query": "Giv",
                            "type": "bool_prefix",
                            "fields": [
                                "title.no.ngrams",
                                "title.no.ngrams.2_gram",
                                "title.no.ngrams.3_gram",
                            ],
                        }
                    },
                ]
            }
        },
    }
    result = SuggestionQuery(search_string="Giv", index_key=IndicesKey.DATA_SETS).body
    assert json.dumps(result) == json.dumps(expected_body)
