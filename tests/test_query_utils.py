import json
import pytest

from src.search.query_utils import get_term_filter, exact_match_in_title_query, word_in_title_query, \
    word_in_description_query, autorativ_boost_clause, simple_query_string, query_template, all_indices_default_query, \
    default_aggs, get_filter_key, get_index_filter_for_key


@pytest.mark.unit
def test_should_return_filter_array_with_modified_key():
    expected = [{"term": {"publisher.orgPath": "KOMMUNE/678687"}}]
    result = get_term_filter({"orgPath": "KOMMUNE/678687"})
    assert result == expected


@pytest.mark.unit
def test_should_return_filter_array_with_unmodified_key():
    request_filter = {"openLicence": "true"}
    expected = [{"term": {"openLicence": "true"}}]
    result = get_term_filter(request_filter)
    assert result == expected


@pytest.mark.unit
def test_should_return_filter_array_with_two_entiries():
    request_filter = {"los": "kjoretøy,trafikk-og-transport"}
    expected = [{"term": {"losTheme.losPaths.keyword": "kjoretøy"}},
                {"term": {"losTheme.losPaths.keyword": "trafikk-og-transport"}}]
    result = get_term_filter(request_filter)
    assert result == expected


@pytest.mark.unit
def test_exact_match_title():
    expected = {"bool": {
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
    }}
    result = exact_match_in_title_query(["prefLabel.*", "title.*", "title"], "åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_word_in_title():
    expected = {
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
    }

    result = word_in_title_query(title_field_names=["title.*", "title", "prefLabel.*"], search_string="åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_word_in_description_one_word():
    expected = {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "heimevernet heimevernet*",
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
    }
    result = word_in_description_query(
        description_field_names_with_boost=["description", "definition.text.*", "schema^0.5"],
        search_string="heimevernet")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_word_in_description_several_words():
    expected = {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "åpne+data åpne+data*",
                    "fields": [
                        "description",
                        "defintion.text.*",
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
    }
    result = word_in_description_query(
        description_field_names_with_boost=["description", "defintion.text.*", "schema^0.5"],
        search_string="åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_boost_autorativ_clause():
    expected = {
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

    result = autorativ_boost_clause()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_simple_query_string_query():
    expected = {
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
    result = simple_query_string(search_string="åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_simple_query_string_query_boost_1():
    expected = {
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
            "boost": 1
        }
    }

    result = simple_query_string(search_string="åpne data", boost=1)

    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_query_template_should_return_empty_query():
    expected = {
        "query": {}
    }
    result = query_template()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_query_template_should_return_empty_query_with_boost():
    expected = {
        "query": {},
        "indices_boost": [{"datasets": 1.2}]
    }
    result = query_template(dataset_boost=1.2)
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_all_indices_default_query():
    expected = {
        "bool": {
            "must": {
                "match_all": {}
            },
            "should": [
                {
                    "term": {
                        "provenance.code.keyword": {
                            "value": "NASJONAL",
                            "boost": 2
                        }
                    }
                },
                {
                    "term": {
                        "nationalComponent": {
                            "value": "true",
                            "boost": 1
                        }
                    }
                }
            ]
        }
    }

    result = all_indices_default_query()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_default_aggs():
    expected = {
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
        },
        "theme": {
            "terms": {
                "field": "euTheme"
            }
        }
    }
    result = default_aggs()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_get_filter_key():
    result_orgPath = get_filter_key("orgPath")
    assert result_orgPath == "publisher.orgPath"
    result_access = get_filter_key("accessRights")
    assert result_access == "accessRights.code.keyword"
    result_los = get_filter_key("los")
    assert result_los == "losTheme.losPaths.keyword"
    result_theme = get_filter_key("theme")
    assert result_theme == "euTheme"
    result_random_key = get_filter_key("random")
    assert result_random_key == "random"


def test_get_filter_index():
    result_access = get_index_filter_for_key("accessRights")
    result_theme = get_index_filter_for_key("theme")
    result_orgPath = get_index_filter_for_key("orgPath")
    assert result_access == 'datasets'
    assert result_theme == 'datasets'
    assert not result_orgPath
