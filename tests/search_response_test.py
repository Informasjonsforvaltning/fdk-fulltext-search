import pytest
from .mock_data.test_data import test_hits
from src.search.responses import SearchResponse

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
