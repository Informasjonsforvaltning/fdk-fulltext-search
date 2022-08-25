import json

import pytest

from fdk_fulltext_search.ingest.utils import IndicesKey
from fdk_fulltext_search.search.field_utils import fulltext_fields, title_fields
from fdk_fulltext_search.search.query_aggregation_utils import (
    default_all_indices_aggs,
    get_aggregation_term_for_key,
)
from fdk_fulltext_search.search.query_filter_utils import (
    collection_filter,
    get_field_by_filter_key,
    get_index_filter_for_key,
    last_x_days_filter,
    term_filter,
)
from fdk_fulltext_search.search.query_utils import (
    default_query,
    description_query,
    get_catch_all_query_string,
    query_string,
    query_template,
    simple_query_string,
    title_exact_match_query,
    title_query,
    words_only_string,
)


@pytest.mark.unit
def test_should_return_filter_array_with_modified_key():
    expected = [{"term": {"publisher.orgPath": "KOMMUNE/678687"}}]
    result = term_filter({"orgPath": "KOMMUNE/678687"})
    assert result == expected


@pytest.mark.unit
def test_should_return_filter_array_with_unmodified_key():
    request_filter = {"openLicence": "true"}
    expected = [{"term": {"openLicence": "true"}}]
    result = term_filter(request_filter)
    assert result == expected


@pytest.mark.unit
def test_should_return_filter_array_with_two_entiries():
    request_filter = {"los": "kjoretøy,trafikk-og-transport"}
    expected = [
        {"term": {"losTheme.losPaths.keyword": "kjoretøy"}},
        {"term": {"losTheme.losPaths.keyword": "trafikk-og-transport"}},
    ]
    result = term_filter(request_filter)
    assert result == expected


@pytest.mark.unit
def test_exact_match_title():
    expected = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": "åpne data",
                    "fields": ["prefLabel.*.raw", "title.*.raw", "title.raw"],
                }
            },
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
            "boost": 20,
        }
    }
    result = title_exact_match_query(["prefLabel.*", "title.*", "title"], "åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_title_query():
    expected = {
        "bool": {
            "must": {
                "dis_max": {
                    "queries": [
                        {
                            "multi_match": {
                                "query": "åpne data",
                                "type": "bool_prefix",
                                "fields": [
                                    "title.*.ngrams",
                                    "title.*.ngrams.2_gram",
                                    "title.*.ngrams.3_gram",
                                ],
                            }
                        },
                        {
                            "multi_match": {
                                "query": "åpne data",
                                "type": "bool_prefix",
                                "fields": [
                                    "title.ngrams",
                                    "title.ngrams.2_gram",
                                    "title.ngrams.3_gram",
                                ],
                            }
                        },
                        {
                            "multi_match": {
                                "query": "åpne data",
                                "type": "bool_prefix",
                                "fields": [
                                    "prefLabel.*.ngrams",
                                    "prefLabel.*.ngrams.2_gram",
                                    "prefLabel.*.ngrams.3_gram",
                                ],
                            }
                        },
                        {
                            "query_string": {
                                "query": "*åpne* *data*",
                                "fields": [
                                    "title.*.raw",
                                    "title.raw",
                                    "prefLabel.*.raw",
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
                            {"term": {"accessRights.code.keyword": "PUBLIC"}},
                            {"term": {"isOpenData": "true"}},
                        ]
                    }
                },
            ],
            "boost": 10,
        }
    }

    result = title_query(
        fields=["title.*", "title", "prefLabel.*"], search_string="åpne data"
    )
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_match_in_description_one_word():
    expected = {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "heimevernet heimevernet*",
                    "fields": ["description", "definition.text.*", "schema^0.5"],
                }
            },
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
    }
    result = description_query(
        fields=["description", "definition.text.*", "schema^0.5"],
        search_string="heimevernet",
    )
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_word_in_description_several_words():
    expected = {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "åpne+data åpne+data*",
                    "fields": ["description", "definition.text.*", "schema^0.5"],
                }
            },
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
    }
    result = description_query(
        fields=["description", "definition.text.*", "schema^0.5"],
        search_string="åpne data",
    )
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_word_in_description_several_words_without_aut_clause():
    expected = {
        "bool": {
            "must": {
                "simple_query_string": {
                    "query": "åpne+data åpne+data*",
                    "fields": ["schema^0.5"],
                }
            },
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
    }

    result = description_query(fields=["schema^0.5"], search_string="åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_simple_query_string_query():
    expected = {
        "bool": {
            "must": {"simple_query_string": {"query": "åpne+data åpne+data*"}},
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
            "boost": 0.02,
        }
    }
    result = simple_query_string(search_string="åpne data")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_simple_query_string_query_special_chars():
    expected = {
        "bool": {
            "must": {"simple_query_string": {"query": "åpne+data åpne+data*"}},
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
            "boost": 0.02,
        }
    }
    result = simple_query_string(search_string="åpne - !! (data)")
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_query_string():
    expected = {
        "bool": {
            "must": {"query_string": {"query": "*mange* *bekker*"}},
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
            "boost": 0.001,
        }
    }

    result = query_string(
        search_string="mange bekker",
    )

    assert json.dumps(result) == json.dumps(expected)


def test_query_string_with_fields():
    expected = {
        "bool": {
            "must": {
                "query_string": {
                    "query": "*mange* *bekker*",
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
                            {"term": {"accessRights.code.keyword": "PUBLIC"}},
                            {"term": {"isOpenData": "true"}},
                        ]
                    }
                },
            ],
            "boost": 0.001,
        }
    }

    result = query_string(
        search_string="mange bekker",
        fields=fulltext_fields([IndicesKey.DATA_SETS]),
    )
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_query_template_should_return_empty_query():
    expected = {"query": {}, "aggs": {}}
    result = query_template()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_query_template_should_return_empty_query_with_boost():
    expected = {"query": {}, "aggs": {}}
    result = query_template()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_default_query():
    expected = {
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
    }

    result = default_query()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_default_aggs():
    expected = {
        "los": {"terms": {"field": "losTheme.losPaths.keyword", "size": 1000000000}},
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
                        {"term": {"isOpenData": "true"}},
                    ]
                }
            }
        },
        "theme": {"terms": {"field": "euTheme"}},
    }
    result = default_all_indices_aggs()
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_get_filter_key():
    result_org_path = get_field_by_filter_key("orgPath")
    assert result_org_path == "publisher.orgPath"
    result_access = get_field_by_filter_key("accessRights")
    assert result_access == "accessRights.code.keyword"
    result_los = get_field_by_filter_key("los")
    assert result_los == "losTheme.losPaths.keyword"
    result_theme = get_field_by_filter_key("theme")
    assert result_theme == "euTheme"
    result_random_key = get_field_by_filter_key("random")
    assert result_random_key == "random"
    result_spatial = get_field_by_filter_key("spatial")
    assert result_spatial == "spatial.prefLabel.no.keyword"
    result_provenance = get_field_by_filter_key("provenance")
    assert result_provenance == "provenance.code.keyword"


@pytest.mark.unit
def test_get_filter_index():
    result_access = get_index_filter_for_key("accessRights")
    result_theme = get_index_filter_for_key("theme")
    result_org_path = get_index_filter_for_key("orgPath")
    assert result_access == "datasets"
    assert result_theme == "datasets"
    assert not result_org_path


@pytest.mark.unit
def test_words_only_string():
    string_with_special_char = "]some - thing ["
    string_with_special_char1 = "some 9 - ( thing"
    string_with_special_char2 = "some - thing()"
    string_with_special_char3 = "+some +9 + thing !    "
    string_with_special_char4 = "+some +9 + -thing !    "
    string_with_special_char_only = "("
    string_with_four_words = "some thing must happen"
    string_with_one_word = "nothing"
    string_with_one_word_and_special_char = "nothing-"

    assert words_only_string(string_with_special_char) == "some thing"
    assert words_only_string(string_with_special_char1) == "some 9 thing"
    assert words_only_string(string_with_special_char2) == "some thing"
    assert words_only_string(string_with_special_char3) == "some 9 thing"
    assert words_only_string(string_with_special_char4) == "some 9 thing"
    assert words_only_string(string_with_special_char_only) is None
    assert words_only_string(string_with_four_words) == string_with_four_words
    assert words_only_string(string_with_one_word) == "nothing"
    assert (
        words_only_string(string_with_one_word_and_special_char) == string_with_one_word
    )


@pytest.mark.unit
def test_words_only_string_in_title_query():
    expected = {
        "query_string": {
            "query": "*some* *query* *to* *be* *queried*",
            "fields": ["title.raw"],
        }
    }

    expected_one_word = {
        "query_string": {
            "query": "*nothing*",
            "fields": ["title.raw"],
        }
    }

    title_fields = ["title"]

    string_with_special_char = title_query(
        fields=title_fields, search_string="]some query to be queried ["
    )
    string_with_special_char2 = title_query(
        fields=title_fields, search_string="some - query to be ()queried"
    )
    string_with_special_char3 = title_query(
        fields=title_fields,
        search_string="+some + + query to be ! queried?   ",
    )
    string_with_special_char4 = title_query(
        fields=title_fields,
        search_string="+some + + -query to be queried !    ",
    )
    string_with_four_words = title_query(
        fields=title_fields, search_string="some query to be queried"
    )
    string_with_one_word = title_query(fields=title_fields, search_string="nothing")
    string_with_one_word_and_special_char = title_query(
        fields=title_fields, search_string="nothing-"
    )
    assert json.dumps(
        string_with_special_char["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected)
    assert json.dumps(
        string_with_special_char2["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected)
    assert json.dumps(
        string_with_special_char3["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected)
    assert json.dumps(
        string_with_special_char4["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected)
    assert json.dumps(
        string_with_four_words["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected)
    assert json.dumps(
        string_with_one_word["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected_one_word)
    assert json.dumps(
        string_with_one_word_and_special_char["bool"]["must"]["dis_max"]["queries"][1]
    ) == json.dumps(expected_one_word)


@pytest.mark.unit
def test_get_catch_all_query_string():
    result = get_catch_all_query_string("oneword")
    result2 = get_catch_all_query_string("two words")
    assert result == "*oneword*"
    assert result2 == "*two* *words*"


@pytest.mark.unit
def test_match_in_title_info_model():
    expected = {
        "bool": {
            "must": {
                "dis_max": {
                    "queries": [
                        {
                            "multi_match": {
                                "query": "RA-05 string",
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
                                "query": "RA-05 string",
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
                                "query": "RA-05 string",
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
                                "query": "RA-05 string",
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
                                "query": "*RA* *05* *string*",
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
                            {"term": {"accessRights.code.keyword": "PUBLIC"}},
                            {"term": {"isOpenData": "true"}},
                        ]
                    }
                },
            ],
            "boost": 10,
        }
    }
    result = title_query(
        fields=title_fields([IndicesKey.INFO_MODEL]), search_string="RA-05 string"
    )
    assert json.dumps(result) == json.dumps(expected)


@pytest.mark.unit
def test_get_aggregation_term_for_key():
    expected_spatial = {"terms": {"field": "spatial.prefLabel.no.keyword"}}

    expected_access = {
        "terms": {"field": "accessRights.code.keyword", "missing": "Ukjent", "size": 10}
    }

    assert get_aggregation_term_for_key("spatial") == expected_spatial
    assert (
        get_aggregation_term_for_key(
            aggregation_key="accessRights", missing="Ukjent", size=10
        )
        == expected_access
    )


def test_last_x_days_filter():
    expected_1 = {
        "range": {"harvest.firstHarvested": {"gte": "now-3d/d", "lt": "now+1d/d"}}
    }
    result_1 = last_x_days_filter({"last_x_days": 3})
    assert result_1 == expected_1

    expected_2 = {
        "range": {"harvest.firstHarvested": {"gte": "now-672d/d", "lt": "now+1d/d"}}
    }
    result_2 = last_x_days_filter({"last_x_days": "672"})
    assert result_2 == expected_2


def test_collection_filter():
    expected = {
        "bool": {
            "should": [
                {
                    "term": {
                        "uri.keyword": "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc"
                    }
                },
                {
                    "term": {
                        "uri.keyword": "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2"
                    }
                },
            ]
        }
    }

    filter_obj = {
        "field": "uri",
        "values": [
            "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc",
            "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2",
        ],
    }

    result = collection_filter(filter_obj)
    assert result == expected


def test_collection_filter_with_and_operator():
    expected = {
        "bool": {
            "must": [
                {
                    "term": {
                        "uri.keyword": "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc"
                    }
                },
                {
                    "term": {
                        "uri.keyword": "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2"
                    }
                },
            ]
        }
    }

    filter_obj = {
        "field": "uri",
        "values": [
            "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc",
            "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2",
        ],
        "operator": "AND",
    }

    result = collection_filter(filter_obj)
    assert result == expected


def test_collection_filter_with_or_operator():
    expected = {
        "bool": {
            "should": [
                {
                    "term": {
                        "uri.keyword": "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc"
                    }
                },
                {
                    "term": {
                        "uri.keyword": "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2"
                    }
                },
            ]
        }
    }

    filter_obj = {
        "field": "uri",
        "values": [
            "https://fellesdatakatalog.brreg.no/api/concepts/a8ea479a-9b61-4cc2-86e8-650a03a322cc",
            "http://brreg.no/catalogs/910244132/datasets/c32b7a4f-655f-45f6-88f6-d01f05d0f7c2",
        ],
        "operator": "OR",
    }

    result = collection_filter(filter_obj)
    assert result == expected
