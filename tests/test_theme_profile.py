import json

import pytest
from jsonpath_ng import parse

from fdk_fulltext_search.search.queries import DataSetQuery
from fdk_fulltext_search.search.themeprofiles import (
    theme_profile_filter,
    ThemeProfileKeys,
    theme_profile_los_paths,
)


@pytest.mark.unit
def test_should_get_transport_filter():
    expected_terms = theme_profile_los_paths[ThemeProfileKeys.TRANSPORT]
    result = theme_profile_filter(key=ThemeProfileKeys.TRANSPORT)
    assert "bool" in result.keys()
    assert "should" in result["bool"].keys()
    should_clauses = result["bool"]["should"]
    assert should_clauses.__len__() == 4
    los_key_path = parse('$.[*].term."losTheme.losPaths.keyword"')
    result_terms = [match.value for match in los_key_path.find(should_clauses)]
    for term in expected_terms:
        assert term in result_terms


@pytest.mark.unit
def test_theme_profile_filter_in_query():
    expected = {
        "bool": {
            "should": [
                {
                    "term": {
                        "losTheme.losPaths.keyword": "trafikk-og-transport/mobilitetstilbud"
                    }
                },
                {
                    "term": {
                        "losTheme.losPaths.keyword": "trafikk-og-transport/trafikkinformasjon"
                    }
                },
                {
                    "term": {
                        "losTheme.losPaths.keyword": "trafikk-og-transport/veg-og-vegregulering"
                    }
                },
                {
                    "term": {
                        "losTheme.losPaths.keyword": "trafikk-og-transport/yrkestransport"
                    }
                },
            ]
        }
    }

    query = DataSetQuery(filters=[{"themeprofile": "transport"}]).body["query"]

    assert "bool" in query.keys()
    assert "filter" in query["bool"].keys()
    assert "should" in query["bool"]["filter"][0]["bool"]
    should_clauses = query["bool"]["filter"][0]["bool"]["should"]
    assert should_clauses.__len__() == 4
    assert json.dumps(query["bool"]["filter"][0]) == json.dumps(expected)
