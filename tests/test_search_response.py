import pytest

from fdk_fulltext_search.search.responses import SearchResponse
from tests.mock_data.test_data import empty_result, test_hits

data_types = ["dataservice", "dataset", "concept", "informationmodel"]


@pytest.mark.unit
def test_all_hits_should_have_type():
    result = SearchResponse().map_response(test_hits["hits"])
    for hit in result["hits"]:
        assert "type" in hit.keys()
        assert hit["type"] in data_types


@pytest.mark.unit
def test_hits_should_have_object_without_es_data():
    result = SearchResponse().map_response(test_hits["hits"])
    for hit in result["hits"]:
        assert "_type" not in hit.keys()
        assert "_source" not in hit.keys()


@pytest.mark.unit
def test_should_map_data_access_to_accessRights():
    result = SearchResponse().map_response(test_hits["hits"])
    aggregation_keys = result["aggregations"].keys()
    assert "accessRights" in aggregation_keys
    assert "los" in aggregation_keys
    assert "orgPath" in aggregation_keys
    assert "isOpenAccess" in aggregation_keys


@pytest.mark.unit
def test_should_empty_response_for_empty_search():
    result = SearchResponse().map_response(empty_result)
    assert "page" in result
    assert "hits" in result
    assert "aggregations" in result
